import os
from pathlib import Path
from fnmatch import fnmatch
from typing import List, Optional

class DocumentManager:
    def __init__(self):
        self.file_list: List[Path] = []

    def create_file_list(self, directory: str, whitelist: Optional[List[str]] = None, blacklist: Optional[List[str]] = None) -> List[Path]:
        """
        Creates a list of all files in the given directory recursively, applying optional whitelist and blacklist filters.

        Args:
            directory (str): The root directory to start the search from.
            whitelist (Optional[List[str]]): List of glob patterns to include. If None, all files are included.
            blacklist (Optional[List[str]]): List of glob patterns to exclude.

        Returns:
            List[Path]: A list of Path objects representing the files.
        """
        self.file_list = []
        root_path = Path(directory).resolve()

        for root, _, files in os.walk(root_path):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(root_path)

                if self._match_patterns(relative_path, whitelist, blacklist):
                    self.file_list.append(file_path)

        return self.file_list

    def edit_file_list(self, add_files: Optional[List[str]] = None, remove_files: Optional[List[str]] = None) -> List[Path]:
        """
        Edits the current file list by adding and/or removing files based on the provided lists of files or globs.

        Args:
            add_files (Optional[List[str]]): List of files or glob patterns to add.
            remove_files (Optional[List[str]]): List of files or glob patterns to remove.

        Returns:
            List[Path]: The updated list of Path objects representing the files.
        """
        if add_files:
            for pattern in add_files:
                self._add_files(pattern)

        if remove_files:
            for pattern in remove_files:
                self._remove_files(pattern)

        return self.file_list

    def _match_patterns(self, path: Path, whitelist: Optional[List[str]], blacklist: Optional[List[str]]) -> bool:
        """
        Checks if a given path matches the whitelist and doesn't match the blacklist.

        Args:
            path (Path): The path to check.
            whitelist (Optional[List[str]]): List of glob patterns to include.
            blacklist (Optional[List[str]]): List of glob patterns to exclude.

        Returns:
            bool: True if the path should be included, False otherwise.
        """
        str_path = str(path)

        if whitelist and not any(fnmatch(str_path, pattern) for pattern in whitelist):
            return False

        if blacklist and any(fnmatch(str_path, pattern) for pattern in blacklist):
            return False

        return True

    def _add_files(self, pattern: str):
        """
        Adds files to the file list based on the given pattern.

        Args:
            pattern (str): A file path or glob pattern.
        """
        pattern_path = Path(pattern)
        if pattern_path.is_file():
            if pattern_path not in self.file_list:
                self.file_list.append(pattern_path)
        else:
            search_dir = pattern_path.parent if pattern_path.is_absolute() else Path()
            for file_path in search_dir.glob(pattern_path.name):
                if file_path.is_file() and file_path not in self.file_list:
                    self.file_list.append(file_path)

    def _remove_files(self, pattern: str):
        """
        Removes files from the file list based on the given pattern.

        Args:
            pattern (str): A file path or glob pattern.
        """
        self.file_list = [file for file in self.file_list if not fnmatch(str(file), pattern)]
