import os
import ast

from typing import Set, Tuple, Dict
from collections import Counter


def _get_all_python_files(foldername: str):
    python_files = []
    for root, dirs, files in os.walk(foldername):
        for file in files:
            if file.endswith('.py') and root != "__pycache__" and len(dirs) == 0:
                python_files.append(os.path.join(root, file))
    return python_files


def get_modules_from_python_file(filepath: str) -> Set:
    with open(filepath, 'r') as file:
        tree = ast.parse(file.read(), filename=filepath)

    module_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_names.add(node.module)

    return module_names


def get_modules_from_folder(foldername: str) -> Tuple[Counter, Dict]:
    all_modules, modules_per_file = [list], dict()
    for file_path in sorted(_get_all_python_files(foldername)):
        file_modules = get_modules_from_python_file(file_path)

        if file_modules:
            modules_per_file[file_path] = sorted(file_modules)
            all_modules.extend(file_modules)
    return Counter(all_modules), modules_per_file


if __name__ == "__main__":
    all_modules, modules_per_file = get_modules_from_folder(".")

    print("Modules used:\n", all_modules)
    for filename, modules in modules_per_file.items():
        print(filename, modules)
