"""`UsageSink` example: appends rows to an in-memory ledger.

`UsageSink` is generic over the row type; this example parametrizes it with
`DemoUsageRow` from `state`. Real plugins replace this with a TypedDict
matching their host's emitted row shape.
"""

import logging
from collections.abc import Sequence

from .state import USAGE_LEDGER, DemoUsageRow


class SimpleUsageSink:
    name = "simple_plugin.usage"

    async def emit(self, rows: Sequence[DemoUsageRow], logger: logging.Logger) -> None:
        USAGE_LEDGER.extend(rows)
        logger.info(
            "%s: appended %d row(s); ledger size=%d",
            self.name,
            len(rows),
            len(USAGE_LEDGER),
        )
