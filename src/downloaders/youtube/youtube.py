import asyncio
import logging

from src.downloaders.downloader import DownloaderInterface
from pytube import YouTube as YouTubeLib


class Youtube(DownloaderInterface):

    async def _download(self, link: str) -> str:
        yt = YouTubeLib(link)
        loop = asyncio.get_event_loop()
        for __ in range(3):
            try:
                streams = yt.streams.filter(only_audio=True, file_extension=self._file_extension)
                f = loop.run_in_executor(None, streams.last().download(output_path=self._output_path))
                await asyncio.wait([f], timeout=15)
                return f.result()

            except Exception as e:
                logging.error(e)
