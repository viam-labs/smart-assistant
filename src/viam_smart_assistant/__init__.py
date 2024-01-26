# from viam.components.generic import Generic
# from viam.resource.registry import Registry, ResourceCreatorRegistration
from .assistant import Assistant
from .config import AssistantConfig

# Registry.register_resource_creator(Generic.SUBTYPE, Assistant.MODEL, ResourceCreatorRegistration(Assistant.new, Assistant.validate_config))

__all__ = ["Assistant", "AssistantConfig"]
