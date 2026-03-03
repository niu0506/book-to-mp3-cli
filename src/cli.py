import argparse
import sys
from pathlib import Path

from .batch_processor import BatchProcessor
from .converter import Converter
from .web import run_server

def main():
    parser = argparse.ArgumentParser(
        description='电子书转MP3 CLI工具'
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    convert_parser = subparsers.add_parser('convert', help='转换单个文件')
    convert_parser.add_argument('input_file', help='输入文件路径')
    convert_parser.add_argument('--output-dir', default='output', help='输出目录')
    convert_parser.add_argument('--segment-length', type=int, default=500, help='文本分段长度')
    convert_parser.add_argument('--bitrate', choices=['128k', '192k', '256k', '320k'], default='192k', help='音频比特率')
    convert_parser.add_argument('--voice', default='zh-CN-XiaoxiaoNeural', help='语音名称')
    convert_parser.add_argument('--workers', type=int, default=4, help='并发工作进程数')

    batch_parser = subparsers.add_parser('batch', help='批量转换')
    batch_parser.add_argument('input_dir', help='输入目录')
    batch_parser.add_argument('--output-dir', default='batch_output', help='输出目录')
    batch_parser.add_argument('--segment-length', type=int, default=500, help='文本分段长度')
    batch_parser.add_argument('--bitrate', choices=['128k', '192k', '256k', '320k'], default='192k', help='音频比特率')
    batch_parser.add_argument('--voice', default='zh-CN-XiaoxiaoNeural', help='语音名称')
    batch_parser.add_argument('--workers', type=int, default=4, help='并发工作进程数')

    web_parser = subparsers.add_parser('web', help='启动网页界面')
    web_parser.add_argument('--host', default='0.0.0.0', help='服务器地址')
    web_parser.add_argument('--port', type=int, default=5000, help='服务器端口')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'convert':
            convert_single_file(args)
        elif args.command == 'batch':
            convert_batch(args)
        elif args.command == 'web':
            run_server(host=args.host, port=args.port)
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
