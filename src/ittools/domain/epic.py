from __future__ import annotations

import abc

from .issue import Issue
from .issue_counts import IssueCounts


class Epic(Issue, metaclass=abc.ABCMeta):
    """An Epic is an Issue that represents a large unit of work

    An epic can be split up into smaller Issues.
    """

    def __init__(self: Epic, key: str, summary: str):
        super().__init__(key, summary)

    @property
    @abc.abstractmethod
    def issue_counts(self: Epic) -> IssueCounts:
        pass