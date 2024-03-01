from collections import namedtuple
import unittest
import os


FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_dir', 'parent_dir'])

def get_file_info(path):
    """
    Собирает информацию о файлах и каталогах в указанной директории.

    Аргументы:
        path (str): путь к директории

    Возвращает:
        list[FileInfo]: список объектов FileInfo с информацией о файлах и каталогах
    """
    if not os.path.exists(path):
        raise ValueError(f'Директория "{path}" не существует')
    entries = os.listdir(path)
    file_info = []
    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            name, extension = os.path.splitext(entry)
            file_info.append(FileInfo(name, extension, False, path))
        elif os.path.isdir(full_path):
            file_info.append(FileInfo(entry, None, True, path))
    return file_info


# Запускаем функцию из командной строки
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Использование: python script.py <путь_к_директории>')
        sys.exit(1)
    path = sys.argv[1]
    file_info = get_file_info(path)
    for info in file_info:
        print(f'{info.name} ({info.extension if info.extension else ""}), каталог: {info.is_dir}, родительский каталог: {info.parent_dir}')



# Тест на несуществующую директорию:
class TestGetFileInfo(unittest.TestCase):
    def test_nonexistent_directory(self):
        with self.assertRaises(ValueError):
            get_file_info('nonexistent_directory')


# Тест на пустую директорию:
class TestGetFileInfo(unittest.TestCase):
    def test_empty_directory(self):
        empty_dir = 'empty_dir'
        os.mkdir(empty_dir)
        file_info = get_file_info(empty_dir)
        os.rmdir(empty_dir)
        self.assertEqual(file_info, [])



        
# Тест на директорию с файлами и каталогами:
class TestGetFileInfo(unittest.TestCase):
    def test_directory_with_files_and_directories(self):
        dir_with_files_and_dirs = 'dir_with_files_and_dirs'
        os.mkdir(dir_with_files_and_dirs)
        with open(os.path.join(dir_with_files_and_dirs, 'file1.txt'), 'w'):
            pass
        with open(os.path.join(dir_with_files_and_dirs, 'file2.py'), 'w'):
            pass
        os.mkdir(os.path.join(dir_with_files_and_dirs, 'subdir'))
        file_info = get_file_info(dir_with_files_and_dirs)
        os.rmdir(os.path.join(dir_with_files_and_dirs, 'subdir'))
        os.remove(os.path.join(dir_with_files_and_dirs, 'file1.txt'))
        os.remove(os.path.join(dir_with_files_and_dirs, 'file2.py'))
        os.rmdir(dir_with_files_and_dirs)
        expected_file_info = [
            FileInfo('file1', 'txt', False, dir_with_files_and_dirs),
            FileInfo('file2', 'py', False, dir_with_files_and_dirs),
            FileInfo('subdir', None, True, dir_with_files_and_dirs),
        ]
        self.assertEqual(file_info, expected_file_info)



# Тест на файлы с точками в именах:
class TestGetFileInfo(unittest.TestCase):
    def test_files_with_dots_in_names(self):
        dir_with_files_with_dots = 'dir_with_files_with_dots'
        os.mkdir(dir_with_files_with_dots)
        with open(os.path.join(dir_with_files_with_dots, 'file.with.dots.txt'), 'w'):
            pass
        with open(os.path.join(dir_with_files_with_dots, 'file.with..dots.txt'), 'w'):
            pass
        file_info = get_file_info(dir_with_files_with_dots)
        os.remove(os.path.join(dir_with_files_with_dots, 'file.with.dots.txt'))
        os.remove(os.path.join(dir_with_files_with_dots, 'file.with..dots.txt'))
        os.rmdir(dir_with_files_with_dots)
        expected_file_info = [
            FileInfo('file.with.dots', 'txt', False, dir_with_files_with_dots),
            FileInfo('file.with..dots', 'txt', False, dir_with_files_with_dots),
        ]
        self.assertEqual(file_info, expected_file_info)



# Тест на символьные ссылки:
class TestGetFileInfo(unittest.TestCase):
    def test_symlinks(self):
        dir_with_symlinks = 'dir_with_symlinks'
        os.mkdir(dir_with_symlinks)
        os.symlink('/tmp/file1.txt', os.path.join(dir_with_symlinks, 'file1.txt'))
        os.symlink('/tmp/dir1', os.path.join(dir_with_symlinks, 'dir1'))
        file_info = get_file_info(dir_with_symlinks)
        os.remove(os.path.join(dir_with_symlinks, 'file1.txt'))
        os.remove(os.path.join(dir_with_symlinks, 'dir1'))
        os.rmdir(dir_with_symlinks)
        expected_file_info = [
            FileInfo('file1.txt', None, False, dir_with_symlinks),
            FileInfo('dir1', None, True, dir_with_symlinks),
        ]
        self.assertEqual(file_info, expected_file_info)