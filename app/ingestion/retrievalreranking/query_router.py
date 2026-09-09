import re


class QueryRouter:

    SYMBOL_PATTERNS = [
        r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\bfunction\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\bmethod\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s+class\b",
    ]

    def extract_symbol(
        self,
        query: str,
    ) -> str | None:

        for pattern in self.SYMBOL_PATTERNS:

            match = re.search(
                pattern,
                query,
                re.IGNORECASE,
            )

            if match:
                return match.group(1)

        return None

    def is_class_query(
        self,
        query: str,
    ) -> bool:

        return bool(
            re.search(
                r"\bclass\b",
                query,
                re.IGNORECASE,
            )
        )

    def is_file_query(
        self,
        query: str,
    ) -> bool:

        return bool(
            re.search(
                r"\bfile\b",
                query,
                re.IGNORECASE,
            )
        )
