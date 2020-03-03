# -*- coding:utf-8 -*-
import os
import asyncio
import logging
from scheduler import SCHEDULER

logger = logging.getLogger(__name__)

os.path.join(os.path.dirname(os.path.abspath(__file__)))


async def scheduler():
    for schedule in SCHEDULER:
        await schedule().execute()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        scheduler()
    )
