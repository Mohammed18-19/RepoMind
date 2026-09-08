class ContextBuilder:
    def build(self, ranked_results: list[dict]) -> str:
        context_parts = []

        for index, result in enumerate(ranked_results, start=1):
            chunk = result["chunk"]

            file_path = chunk.file.path
            start_line = chunk.start_line
            end_line = chunk.end_line

            context_parts.append(
                f"""--- Source {index} ---
File: {file_path}
Lines: {start_line}-{end_line}

{chunk.content}
"""
            )

        return "\n".join(context_parts)