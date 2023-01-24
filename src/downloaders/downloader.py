from abc import ABCMeta, abstractmethod


class DownloaderInterface(metaclass=ABCMeta):

    def __init__(self, *, output_path='./music/youtube', file_extension='mp4'):
        self._output_path = output_path
        self._file_extension = file_extension

    @abstractmethod
    async def get_path_to_music_file_by_link(self, link: str) -> str:
        pass

    @abstractmethod
    async def _download(self, *args, **kwargs) -> str:
        pass
