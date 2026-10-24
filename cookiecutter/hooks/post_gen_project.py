"""Post-generation hook that removes the pygame-only files when pygame is not wanted."""

from pathlib import Path

INCLUDE_PYGAME = {{ cookiecutter.include_pygame }}

PYGAME_ONLY_FILES = [
    "src/{{ cookiecutter.package_name }}/game.py",
    "src/{{ cookiecutter.package_name }}/renderer.py",
    "src/{{ cookiecutter.package_name }}/utils/utils_pygame.py",
    "tests/{{ cookiecutter.package_name }}/test_game.py",
    "tests/{{ cookiecutter.package_name }}/test_renderer.py",
    "tests/{{ cookiecutter.package_name }}/utils/test_utils_pygame.py",
]


def _remove_empty_parent(path: Path) -> None:
    """Remove the parent directory of a file if it is empty.

    Args:
        path (Path): The file whose parent directory may be left empty.
    """
    parent = path.parent

    if not any(parent.iterdir()):
        parent.rmdir()


def _remove_pygame_files(project_root: Path) -> None:
    """Delete the pygame-only files and any directories they leave empty.

    Args:
        project_root (Path): The root folder of the generated project.
    """
    for relative_path in PYGAME_ONLY_FILES:
        path = project_root / relative_path
        path.unlink()
        _remove_empty_parent(path)


if not INCLUDE_PYGAME:
    _remove_pygame_files(Path.cwd())
