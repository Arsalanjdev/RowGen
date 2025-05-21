from pathlib import Path


def find_project_root(start_path: Path = None, marker_files=None) -> Path:
    """
    Find the root directory of the project by looking for marker files/folders.

    Args:
        start_path (Path): Directory to start searching from (defaults to current file's dir).
        marker_files (list[str]): List of filenames or directory names to identify the root.
                                  Common examples: ['.git', 'pyproject.toml', 'setup.py']

    Returns:
        Path: Absolute path to the project root directory.

    Raises:
        FileNotFoundError: If no project root found up to the filesystem root.
    """
    if start_path is None:
        start_path = Path(__file__).resolve().parent

    if marker_files is None:
        marker_files = [".git", "pyproject.toml"]

    current = start_path

    while True:
        if any((current / marker).exists() for marker in marker_files):
            return current
        if current.parent == current:
            # Reached filesystem root
            raise FileNotFoundError(f"Project root not found from {start_path} upward.")
        current = current.parent


def get_env_file_path() -> Path:
    """
    Finds and returns the path of .env file.
    :return: Path object.
    """
    root = find_project_root()
    return f"{root}/.env"


ENV_PATH = get_env_file_path()
