from pathlib import Path


def main() -> None:
    for file in Path('.').rglob('**/*'):
        if not file.is_file():
            continue
        if file.stat().st_size:
            continue
        print(file)
        try:
            file.unlink()
        except Exception as exc:
            print(f'Error while deleting file {file}: {exc}')


if __name__ == '__main__':
    main()
