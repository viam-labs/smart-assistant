import asyncio

# from viam.module.module import Module
# from viam.components.generic import Generic

from . import Assistant
from . import AssistantConfig

async def main():
    assistant = Assistant(config=AssistantConfig())
    try:
        await assistant.start()
    except:
        await assistant.close()

asyncio.run(main())
