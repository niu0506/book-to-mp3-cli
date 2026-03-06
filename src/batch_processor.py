from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List
from pathlib import Path
from tqdm import tqdm
from .converter import Converter
from .config import logger
from .config_handler import DEFAULT_WORKERS
from .utils import safe_file_operation

class BatchProcessor:
    def __init__(self, workers: int = DEFAULT_WORKERS):
        if workers <= 0:
            raise ValueError("Workers must be positive")
        self.workers = workers
        self.converter = Converter()

    def batch_convert(self, input_files: List[str], output_dir: str) -> List[str]:
        safe_file_operation(
            lambda: Path(output_dir).mkdir(parents=True, exist_ok=True),
            output_dir,
            "创建输出目录"
        )

        results = []

        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = []
            for input_file in input_files:
                future = executor.submit(
                    self._convert_single_file,
                    input_file,
                    output_dir
                )
                futures.append(future)

            with tqdm(total=len(futures), desc="批量转换", unit="文件") as pbar:
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                        logger.info(f"Completed: {result}")
                    except Exception as e:
                        logger.error(f"Failed: {e}")
                    pbar.update(1)

        return results

    def _convert_single_file(self, input_file: str, output_dir: str) -> str:
        return self.converter.convert(input_file, output_dir)
