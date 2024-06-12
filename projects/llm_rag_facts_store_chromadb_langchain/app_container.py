from dependency_injector import containers, providers

from .lm_container import LMContainer
from .services_container import ServicesContainer
from .vector_store_container import VectorStoreContainer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    lm_container = providers.Container(
        LMContainer,
        # config=config.lm,
        config=config,
    )

    vector_store_container = providers.Container(
        VectorStoreContainer,
        lm_container=lm_container,
        # config=config.vector_store,
        config=config,
    )

    services_container = providers.Container(
        ServicesContainer,
        vector_store_container=vector_store_container,
        # config=config.services,
        config=config,
    )
