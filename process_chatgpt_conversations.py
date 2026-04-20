import json
import sys
from pathlib import Path
from typing import List, Any

# import from old script
from scripts.parse_validate_clean import process_raw_conversations


DEFAULT_FOLDER = 'chatgpt-conversations'


def get_all_files(base: Path) -> List[Path]:
    return sorted(base.rglob('conversations-*.json'))


def merge_files(files: List[Path]) -> List[Any]:
    all_data = []

    for file in files:
        print(f'Loading: {file}')

        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            all_data.extend(data)
        else:
            print(f'Skipping {file} (not list)')

    return all_data


def main():
    # CLI arg handling
    if len(sys.argv) > 1:
        base = Path(sys.argv[1])
    else:
        base = Path(DEFAULT_FOLDER)

    base = base.resolve()

    if not base.exists():
        raise FileNotFoundError(base)

    files = get_all_files(base)

    if not files:
        print('No conversation files found.')
        return

    print(f'Found {len(files)} files')

    merged = merge_files(files)

    print(f'Merged {len(merged)} records')

    # 🔥 Direct function call instead of subprocess
    process_raw_conversations(merged)


if __name__ == '__main__':
    main()
