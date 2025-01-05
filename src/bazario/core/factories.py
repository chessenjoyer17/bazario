from bazario.core.builder import DispatcherBuilderImpl
from bazario.protocols.builder import DispatcherBuilder


def get_builder() -> DispatcherBuilder:
    return DispatcherBuilderImpl()
