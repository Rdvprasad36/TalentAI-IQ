"""Streaming JSONL loader for Redrob candidate profiles."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import orjson

logger = logging.getLogger(__name__)

CandidateRecord = dict[str, Any]


class LoaderError(Exception):
    """Raised when the candidate loader encounters an unrecoverable error."""


class CandidateLoader:
    """Stream candidates from a JSONL file without loading the full dataset into memory."""

    __slots__ = ("_file_path", "_path")

    def __init__(self, file_path: str) -> None:
        """
        Initialize the loader for a JSONL candidate file.

        Args:
            file_path: Path to the candidates ``.jsonl`` file.
        """
        self._file_path = file_path
        self._path = Path(file_path)

    @property
    def path(self) -> Path:
        """Resolved filesystem path to the candidate file."""
        return self._path

    def validate_path(self) -> Path:
        """
        Validate that the candidate file exists and has a ``.jsonl`` extension.

        Returns:
            Resolved path to the candidate file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file extension is not ``.jsonl``.
        """
        if self._path.suffix.lower() != ".jsonl":
            raise ValueError(
                f"Expected a .jsonl file, got {self._path.suffix!r}: {self._path}"
            )
        if not self._path.is_file():
            raise FileNotFoundError(f"Candidate file not found: {self._path}")
        return self._path.resolve()

    def _iter_nonempty_lines(self) -> Iterator[tuple[int, bytes]]:
        """
        Yield non-empty raw lines with their 1-based line numbers.

        Yields:
            Tuple of ``(line_number, line_bytes)``.
        """
        path = self.validate_path()
        logger.info("Opening candidate file: %s (%.2f MB)", path, get_file_size(path))
        try:
            with path.open("rb") as handle:
                for line_number, line in enumerate(handle, start=1):
                    stripped = line.strip()
                    if stripped:
                        yield line_number, stripped
        except OSError as exc:
            raise LoaderError(f"Failed to read candidate file: {path}") from exc

    def stream_candidates(self) -> Iterator[CandidateRecord]:
        """
        Stream candidate records one at a time from the JSONL file.

        Empty lines are skipped. Malformed JSON lines are logged and skipped;
        processing continues for remaining records.

        Yields:
            Parsed candidate dictionary for each valid JSON line.
        """
        yielded = 0
        skipped = 0

        for line_number, line in self._iter_nonempty_lines():
            try:
                record = orjson.loads(line)
            except orjson.JSONDecodeError as exc:
                skipped += 1
                logger.warning(
                    "Skipping bad JSON at line %d in %s: %s",
                    line_number,
                    self._path,
                    exc,
                )
                continue

            if not isinstance(record, dict):
                skipped += 1
                logger.warning(
                    "Skipping non-object JSON at line %d in %s: expected dict, got %s",
                    line_number,
                    self._path,
                    type(record).__name__,
                )
                continue

            yielded += 1
            yield record

        logger.info(
            "Completed streaming %s: %d candidates yielded, %d lines skipped",
            self._path,
            yielded,
            skipped,
        )

    def count_candidates(self) -> int:
        """
        Count valid candidate records without storing them in memory.

        Returns:
            Number of successfully parsed candidate records.
        """
        count = 0
        skipped = 0

        for line_number, line in self._iter_nonempty_lines():
            try:
                record = orjson.loads(line)
            except orjson.JSONDecodeError as exc:
                skipped += 1
                logger.warning(
                    "Skipping bad JSON at line %d in %s: %s",
                    line_number,
                    self._path,
                    exc,
                )
                continue

            if not isinstance(record, dict):
                skipped += 1
                logger.warning(
                    "Skipping non-object JSON at line %d in %s: expected dict, got %s",
                    line_number,
                    self._path,
                    type(record).__name__,
                )
                continue

            count += 1

        logger.info(
            "Candidate count for %s: %d valid records (%d lines skipped)",
            self._path,
            count,
            skipped,
        )
        return count


def get_file_size(path: str | Path) -> float:
    """
    Return the size of a file in megabytes.

    Args:
        path: File path.

    Returns:
        File size in MB.

    Raises:
        FileNotFoundError: If the file does not exist.
        LoaderError: If the file size cannot be read.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        size_bytes = file_path.stat().st_size
    except OSError as exc:
        raise LoaderError(f"Failed to stat file: {file_path}") from exc
    return size_bytes / (1024 * 1024)


def load_sample(path: str | Path, limit: int = 5) -> list[CandidateRecord]:
    """
    Load the first ``limit`` valid candidates from a JSONL file.

    Useful for debugging and schema inspection without scanning the full dataset.

    Args:
        path: Path to the candidates ``.jsonl`` file.
        limit: Maximum number of candidates to return.

    Returns:
        List of up to ``limit`` candidate dictionaries.

    Raises:
        ValueError: If ``limit`` is less than 1.
    """
    if limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit}")

    loader = CandidateLoader(str(path))
    sample: list[CandidateRecord] = []
    for candidate in loader.stream_candidates():
        sample.append(candidate)
        if len(sample) >= limit:
            break
    return sample
