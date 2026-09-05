from pathlib import Path
import subprocess
import tempfile
import zipfile


class RepositoryLoader:
    def load_from_github(self, repo_url: str) -> Path:
        destination = Path(tempfile.mkdtemp(prefix="repomind_"))

        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                repo_url,
                str(destination),
            ],
            check=True,
        )

        return destination

    def load_from_zip(self, zip_path: str | Path) -> Path:
        destination = Path(tempfile.mkdtemp(prefix="repomind_"))

        with zipfile.ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(destination)

        return destination