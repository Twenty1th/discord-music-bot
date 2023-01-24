from src.downloader.downloader import DownloaderInterface
from pytube import YouTube as YouTubeLib


class Youtube(DownloaderInterface):

    async def _download(self, link: str) -> str:
        yt = YouTubeLib(link)
        for __ in range(3):
            try:
                streams = yt.streams.filter(only_audio=True, file_extension=self._file_extension)
                return streams.last().download(output_path=self._output_path)

            except Exception as e:
                print(e)  # TODO
