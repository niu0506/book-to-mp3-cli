from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List
from pathlib import Path
from .converter import Converter
from .config import logger

class BatchProcessor:
    def __init__(self, workers: int = 4):
        if workers <= 0:
            raise ValueError("Workers must be positive")
        self.workers = workers
        self.converter = Converter()

    def batch_convert(self, input_files: List[str], output_dir: str) -> List[str]:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []

        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = []
            for input_file in input_files:
                future = executor.submit(
                    self._convert_single_file,
                    input_file,
                    str(output_path)
                )
                futures.append(future)

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Completed: {result}")
                except Exception as e:
                    logger.error(f"Failed: {e}")

        return results

    def _convert_single_file(self, input_file: str, output_dir: str) -> str:
        return self.converter.convert(input_file, output_dir)
