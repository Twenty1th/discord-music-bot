from abc import ABCMeta, abstractmethod


class DownloaderInterface(metaclass=ABCMeta):

    def __init__(self, *, output_path='./music/youtube', file_extension='mp4'):
        self._output_path = output_path
        self._file_extension = file_extension

    @abstractmethod
    async def _download(self, link: str) -> str:
        pass

    async def download(self, link: str) -> str:
        return await self._download(link)


