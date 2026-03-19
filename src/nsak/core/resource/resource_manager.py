from typing import List

from .resource_loader import ResourceLoader


class ResourceManager[T]:
    """
    An abstract base class for manage resources.
    """

    ResourceLoaderClass: type[ResourceLoader[T]]

    @classmethod
    def list(cls) -> List[T]:
        """
        Lists all resources.
        """
        return cls.ResourceLoaderClass.load_all()

    @classmethod
    def get(cls, name: str) -> T:
        """
        Get a resource by name.
        """
        return cls.ResourceLoaderClass.load(name)
