from abc import ABCMeta, abstractmethod


class IDownloader(metaclass=ABCMeta):
    __name: str = None

    def __init__(self, *, output_path, file_extension):
        self._output_path = output_path
        self._file_extension = file_extension

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    async def download(self, link: str) -> str:
        pass

    @abstractmethod
    async def _download(self, *args, **kwargs) -> str:
        pass
