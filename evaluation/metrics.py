def retrieval_hit(
    results: list[dict],
    expected_files: list[str],
) -> bool:
    # Negative retrieval case:
    # If no files are expected, retrieval should return no results.
    if not expected_files:
        return len(results) == 0

    expected = set(expected_files)

    for result in results:
        chunk = result["chunk"]
        file_path = chunk.file.path

        if file_path in expected:
            return True

    return False


def citation_hit(
    answer: str,
    expected_files: list[str],
) -> bool:
    # If no file is expected, there is no citation requirement.
    if not expected_files:
        return True

    return any(
        file_path in answer
        for file_path in expected_files
    )


def answer_contains_keywords(
    answer: str,
    expected_keywords: list[str],
) -> bool:
    # Negative-answer case.
    if not expected_keywords:
        negative_indicators = [
            "does not",
            "no file",
            "not found",
            "doesn't",
            "cannot find",
            "not contain",
            "not exist",
            "insufficient",
        ]

        answer_lower = answer.lower()

        return any(
            indicator in answer_lower
            for indicator in negative_indicators
        )

    answer_lower = answer.lower()

    return all(
        keyword.lower() in answer_lower
        for keyword in expected_keywords
    )


def calculate_rate(
    successful: int,
    total: int,
) -> float:
    if total == 0:
        return 0.0

    return successful / total
