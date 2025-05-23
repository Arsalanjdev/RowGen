import os
from pathlib import Path

from dotenv import load_dotenv


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


def get_api_key() -> str:
    """
    Returns the API key from environment, loading .env if running locally.
    """
    # Load .env only if not already set (e.g., local dev)
    if "HF_API_KEY" not in os.environ:
        env_path = find_project_root() / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        raise RuntimeError("HF_API_KEY is not set in the environment.")
    return api_key


API_KEY = get_api_key()
