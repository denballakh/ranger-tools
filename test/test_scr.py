from __future__ import annotations
import unittest
from pathlib import Path
import collections

import rangers.scr

test_data = Path() / 'test_data' / 'scr'


def generate_test_data(game_path: Path) -> None:
    versions = collections.defaultdict[int, list[Path]](list)

    for file in game_path.rglob('*.scr'):
        version = file.read_bytes()[0]
        versions[version].append(file)

        p = test_data / str(version) / file.name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(file.read_bytes())


class TestScr(unittest.TestCase):
    def test_read(self) -> None:
        obj = rangers.scr.SCR
        for version in rangers.scr.SUPPORTED_VERSIONS:
            for file in (test_data / str(version)).glob('*.scr'):
                with self.subTest(file=file, version=version):
                    data = file.read_bytes()
                    self.assertEqual(data[0], version, msg='wrong version')
                    data_2 = obj.write_bytes(obj.read_bytes(data))
                    self.assertEqual(data, data_2)


if __name__ == '__main__':
    unittest.main()
