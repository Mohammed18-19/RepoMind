from pathlib import Path


class FileDiscovery:
    IGNORED_DIRECTORIES = {
        ".git",
        ".github",
        "node_modules",
        "venv",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        "dist",
        "build",
    }

    IGNORED_EXTENSIONS = {
        ".pyc",
        ".pyo",
        ".so",
        ".dll",
        ".exe",
        ".bin",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".mp3",
        ".mp4",
        ".mov",
        ".zip",
        ".tar",
        ".gz",
    }

    def discover(self, repository_path: Path) -> list[Path]:
        files = []

        for path in repository_path.rglob("*"):
            if not path.is_file():
                continue

            if any(
                directory in self.IGNORED_DIRECTORIES
                for directory in path.parts
            ):
                continue

            if path.suffix.lower() in self.IGNORED_EXTENSIONS:
                continue

            files.append(path)

        return files

    def get_metadata(self, path: Path) -> dict:
        return {
            "path": str(path),
            "filename": path.name,
            "language": path.suffix.lstrip("."),
            "file_size": path.stat().st_size,
        }