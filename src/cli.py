import argparse
import sys
from pathlib import Path

from .batch_processor import BatchProcessor
from .converter import Converter
from .config_handler import get_config, reset_config, DEFAULT_VOICE, DEFAULT_BITRATE, DEFAULT_SEGMENT_LENGTH, DEFAULT_WORKERS

DEFAULT_CONFIG_PATH = 'config.yaml'


def load_config(args) -> dict:
    config_path = getattr(args, 'config', None)
    if config_path and Path(config_path).exists():
        return get_config(config_path).config
    elif Path(DEFAULT_CONFIG_PATH).exists():
        return get_config(DEFAULT_CONFIG_PATH).config
    return {}


def merge_args_with_config(args, config: dict) -> argparse.Namespace:
    args_dict = vars(args)
    for key, value in config.items():
        if key not in args_dict or args_dict[key] is None:
            setattr(args, key, value)
    return args

def main():
    parser = argparse.ArgumentParser(
        description='电子书转MP3 CLI工具'
    )

    parser.add_argument('--config', default=None, help='配置文件路径 (config.yaml)')

    subparsers = parser.add_subparsers(dest='command', help='命令')

    convert_parser = subparsers.add_parser('convert', help='转换单个文件')
    convert_parser.add_argument('input_file', help='输入文件路径')
    convert_parser.add_argument('--output-dir', default=None, help='输出目录')
    convert_parser.add_argument('--segment-length', type=int, default=None, help='文本分段长度')
    convert_parser.add_argument('--bitrate', choices=['128k', '192k', '256k', '320k'], default=None, help='音频比特率')
    convert_parser.add_argument('--voice', default=None, help='语音名称')
    convert_parser.add_argument('--clean-text', type=bool, default=None, help='是否清理文本')

    batch_parser = subparsers.add_parser('batch', help='批量转换')
    batch_parser.add_argument('input_dir', help='输入目录')
    batch_parser.add_argument('--output-dir', default=None, help='输出目录')
    batch_parser.add_argument('--segment-length', type=int, default=None, help='文本分段长度')
    batch_parser.add_argument('--bitrate', choices=['128k', '192k', '256k', '320k'], default=None, help='音频比特率')
    batch_parser.add_argument('--voice', default=None, help='语音名称')
    batch_parser.add_argument('--workers', type=int, default=None, help='并发工作进程数')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    config = load_config(args)
    args = merge_args_with_config(args, config)

    if args.output_dir is None:
        args.output_dir = 'output' if args.command == 'convert' else 'batch_output'
    if args.segment_length is None:
        args.segment_length = DEFAULT_SEGMENT_LENGTH
    if args.bitrate is None:
        args.bitrate = DEFAULT_BITRATE
    if args.voice is None:
        args.voice = DEFAULT_VOICE
    if args.workers is None:
        args.workers = DEFAULT_WORKERS

    try:
        if args.command == 'convert':
            convert_single_file(args)
        elif args.command == 'batch':
            convert_batch(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def convert_single_file(args):
    converter = Converter(
        voice=args.voice,
        bitrate=args.bitrate,
        segment_length=args.segment_length
    )

    output_path = converter.convert(args.input_file, args.output_dir)
    print(f"✓ Converted: {output_path}")

def convert_batch(args):
    batch_processor = BatchProcessor(workers=args.workers)

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    input_files = []
    for file_path in input_dir.iterdir():
        if file_path.suffix.lower() in ['.epub', '.mobi', '.txt']:
            input_files.append(str(file_path))

    if not input_files:
        print("No supported files found in input directory")
        sys.exit(0)

    print(f"Found {len(input_files)} files to convert...")

    results = batch_processor.batch_convert(input_files, str(output_dir))
    print(f"✓ Converted {len(results)} files to {output_dir}")
