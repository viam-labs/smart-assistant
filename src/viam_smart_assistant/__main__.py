import asyncio

from viam.module.module import Module
from viam.components.generic import Generic

from . import Assistant

async def main():
    module = Module.from_args()
    module.add_model_from_registry(Generic.SUBTYPE, Assistant.MODEL)
    await module.start()

asyncio.run(main())
