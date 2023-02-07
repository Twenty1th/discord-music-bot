from abc import ABCMeta, abstractmethod


class DownloaderInterface(metaclass=ABCMeta):

    __name: str = None

    def __init__(self, *, output_path, file_extension):
        self._output_path = output_path
        self._file_extension = file_extension

    @property
    def name(self):
        if self.__name is None:
            raise NotImplemented("Service name is not specified ")
        return self.__name

    @abstractmethod
    async def get_path_to_music_file_by_link(self, link: str) -> str:
        pass

    @abstractmethod
    async def _download(self, *args, **kwargs) -> str:
        pass
