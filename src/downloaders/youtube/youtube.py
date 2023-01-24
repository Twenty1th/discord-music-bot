import asyncio
import os

from src.downloaders.downloader import DownloaderInterface
from pytube import YouTube as YouTubeLib, StreamQuery


class Youtube(DownloaderInterface):

    @staticmethod
    def __get_uuid_from_link(link: str):
        return link.split("?v=")[-1]

    async def _download(self, link: str, filename: str, *args, **kwargs) -> str:
        yt = YouTubeLib(link)
        loop = asyncio.get_event_loop()
        streams: StreamQuery = yt.streams.filter(only_audio=True, file_extension=self._file_extension)
        f = loop.run_in_executor(None, streams.last().download, self._output_path, filename)
        await asyncio.wait([f], timeout=60)
        return f.result()

    async def get_path_to_music_file_by_link(self, link: str) -> str:
        filename = f"{self.__get_uuid_from_link(link)}.{self._file_extension}"
        if os.path.exists(f"{self._output_path}/{filename}"):
            return f"{self._output_path}/{filename}"
        else:
            return await self._download(link, filename)
