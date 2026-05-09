"""Usage-sink hook.

Fan-out for usage rows after a unit of work completes. Each sink decides
which rows it consumes and how to deliver them. Sink failures are isolated by
the caller — they must not break the host's hot path.

The protocol is generic over the row type so each project parametrizes it
with a project-specific row shape (TypedDict, BaseModel, dataclass — the
protocol just sees a `Row`).
"""

import logging
from collections.abc import Sequence
from typing import Protocol, runtime_checkable


@runtime_checkable
class UsageSink[Row](Protocol):
    name: str

    async def emit(self, rows: Sequence[Row], logger: logging.Logger) -> None:
        """Deliver usage rows to a downstream sink."""
        ...
