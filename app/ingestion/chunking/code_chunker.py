import ast
from pathlib import Path


class CodeChunker:
    def chunk_file(self, file_path: Path) -> list[dict]:
        content = file_path.read_text(encoding="utf-8")

        tree = ast.parse(content)

        lines = content.splitlines()

        chunks = []

        for node in tree.body:
            if isinstance(
                node,
                (
                    ast.Import,
                    ast.ImportFrom,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                start_line = node.lineno
                end_line = node.end_lineno

                chunk_content = "\n".join(
                    lines[start_line - 1:end_line]
                )

                chunks.append(
                    {
                        "content": chunk_content,
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                )

        return chunks