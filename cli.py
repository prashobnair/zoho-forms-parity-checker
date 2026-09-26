import argparse
import json
from pathlib import Path
from parity import compare

def main():
    parser = argparse.ArgumentParser(description='Check fictional form output parity')
    parser.add_argument('fixture')
    parser.add_argument('--strict', action='store_true', help='Exit 2 if any case differs')
    args = parser.parse_args()
    try:
        report = compare(json.loads(Path(args.fixture).read_text(encoding='utf-8')))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Input error: {exc}\n')
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.strict and not report['all_pass']:
        parser.exit(2)

if __name__ == '__main__':
    main()
