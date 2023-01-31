from __future__ import annotations
from typing import Callable

import unittest
import pathlib
import tempfile
import filecmp

import rangers.dat

test_files = pathlib.Path() / 'test_data' / 'dat'


class TestDat(unittest.TestCase):
    def test_conversions(self) -> None:
        cls = rangers.dat.DAT
        for folder_name, ext1, ext2 in (
            ('txt2dat', '.txt', '.dat'),
            # ('txt2json', '.txt', '.json'),
            # ('json2txt', '.json', '.txt'),
            # ('json2dat', '.json', '.dat'),
            ('dat2txt', '.dat', '.txt'),
            # ('dat2json', '.dat', '.json'),
        ):
            folder = test_files / folder_name
            for file in [
                file for file in folder.iterdir() if file.is_file() and file.suffix == ext1
            ]:
                with self.subTest(folder=folder_name, file=file):
                    result_file = file.parent / (file.stem + '_result' + ext2)
                    self.assertTrue(
                        result_file.is_file(), f'no result file {result_file} for file {file}'
                    )

                    with tempfile.TemporaryDirectory() as tempdir:
                        temp_file = pathlib.Path(tempdir) / result_file.name
                        cls.from_file(file).to_file(temp_file, fmt='HDMain', sign=False)
                        # self.assertTrue(filecmp.cmp(result_file, temp_file))
                        self.assertEqual(cls.from_file(result_file), cls.from_file(temp_file))
                        self.assertEqual(cls.from_file(result_file), cls.from_file(file))


class TestSign(unittest.TestCase):
    @unittest.skipUnless(rangers.dat.DAT_SIGN_AVAILABLE, 'dat sign not available')
    def test_sign_available(self) -> None:
        sign_data = rangers.dat.sign_data
        unsign_data = rangers.dat.unsign_data
        get_sign = rangers.dat.get_sign
        check_signed = rangers.dat.check_signed

        data = b'0123'

        self.assertEqual(len(get_sign(b'')), 8)
        self.assertEqual(len(sign_data(b'')), 8)
        self.assertEqual(get_sign(b''), sign_data(b''))

        self.assertEqual(len(get_sign(data)), 8)
        self.assertEqual(len(sign_data(data)), 8 + len(data))

        self.assertEqual(get_sign(data), get_sign(data))

        self.assertTrue(check_signed(sign_data(data)))
        self.assertFalse(check_signed(get_sign(data)))

        self.assertEqual(data, unsign_data(data))
        self.assertEqual(sign_data(data), sign_data(sign_data(data)))
        self.assertEqual(data, unsign_data(sign_data(data)))
        self.assertEqual(data, unsign_data(sign_data(sign_data(b'0123'))))

    @unittest.skipIf(rangers.dat.DAT_SIGN_AVAILABLE, 'dat sign available')
    def test_sign_not_available(self) -> None:
        sign_data = rangers.dat.sign_data
        unsign_data = rangers.dat.unsign_data
        get_sign = rangers.dat.get_sign
        check_signed = rangers.dat.check_signed

        data = b'0123'
        self.assertEqual(get_sign(data), b'')
        self.assertEqual(check_signed(data), b'')


if __name__ == '__main__':
    unittest.main()
