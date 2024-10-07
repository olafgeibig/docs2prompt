import os
import pytest
from pathlib import Path
from docs2prompt.document_manager import DocumentManager

@pytest.fixture
def doc_manager():
    return DocumentManager()

def test_create_file_list(doc_manager, tmp_path):
    # Create a temporary directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.txt").touch()
    (tmp_path / "dir1" / "file2.md").touch()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "file3.py").touch()

    # Test with no filters
    file_list = doc_manager.create_file_list(str(tmp_path))
    assert len(file_list) == 3
    assert set(file.name for file in file_list) == {"file1.txt", "file2.md", "file3.py"}

    # Test with whitelist
    file_list = doc_manager.create_file_list(str(tmp_path), whitelist=["*.txt", "*.md"])
    assert len(file_list) == 2
    assert set(file.name for file in file_list) == {"file1.txt", "file2.md"}

    # Test with blacklist
    file_list = doc_manager.create_file_list(str(tmp_path), blacklist=["*.py"])
    assert len(file_list) == 2
    assert set(file.name for file in file_list) == {"file1.txt", "file2.md"}

def test_edit_file_list(doc_manager, tmp_path):
    # Create initial file list
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.md").touch()
    doc_manager.create_file_list(str(tmp_path))

    # Test adding files
    (tmp_path / "file3.py").touch()
    file_list = doc_manager.edit_file_list(add_files=[str(tmp_path / "*.py")])
    assert len(file_list) == 3
    assert set(file.name for file in file_list) == {"file1.txt", "file2.md", "file3.py"}

    # Test adding files with relative path
    os.chdir(tmp_path)
    (Path("file4.js").touch())
    file_list = doc_manager.edit_file_list(add_files=["*.js"])
    assert len(file_list) == 4
    assert set(file.name for file in file_list) == {"file1.txt", "file2.md", "file3.py", "file4.js"}

    # Test removing files
    file_list = doc_manager.edit_file_list(remove_files=["*.txt"])
    assert len(file_list) == 3
    assert set(file.name for file in file_list) == {"file2.md", "file3.py"}
