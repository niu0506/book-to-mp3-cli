from pathlib import Path
from typing import Optional, Dict, Any
import yaml

# Default configuration constants
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
DEFAULT_BITRATE = "192k"
DEFAULT_SEGMENT_LENGTH = 500
DEFAULT_WORKERS = 4

# Default paths
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
DATA_DIR = Path("data")


class Config:
    DEFAULT_CONFIG = {
        'voice': DEFAULT_VOICE,
        'bitrate': DEFAULT_BITRATE,
        'segment_length': DEFAULT_SEGMENT_LENGTH,
        'workers': DEFAULT_WORKERS,
        'output_dir': 'output',
        'clean_text': True,
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        if config_path and Path(config_path).exists():
            self.load(config_path)

    def load(self, config_path: str) -> None:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)
        if user_config:
            self.config.update(user_config)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.config[key] = value


_config: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def reset_config() -> None:
    global _config
    _config = None