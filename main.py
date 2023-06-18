import requests
import logging

logging.basicConfig(level=logging.DEBUG)

def download_mp3(url: str, file_path: str) -> None:
    """
    Downloads an MP3 file from the given URL and saves it to the specified file path.

    Args:
        url (str): The URL of the MP3 file to download.
        file_path (str): The file path to save the downloaded MP3 file to.

    Raises:
        requests.exceptions.RequestException: If there was an error downloading the MP3 file.
    """
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        logging.info(f"Downloaded MP3 from {url} to {file_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading MP3 from {url}: {e}")

if __name__ == "__main__":
    url = "https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/high/stream.mp3"
    file_path = "stream.mp3"
    download_mp3(url, file_path)