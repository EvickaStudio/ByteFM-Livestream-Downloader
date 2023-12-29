import logging
import os
import time
import warnings

import requests

warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Predefined constants
DEFAULT_AUDIO_URL = "https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/high/stream.mp3"
DEFAULT_TARGET_PATH = "stream.mp3"


def download_audio(
    audio_url: str = DEFAULT_AUDIO_URL,
    target_path: str = DEFAULT_TARGET_PATH,
    retries: int = 3,
) -> None:
    """
    Download audio files from the provided URL and store them at the specific location on disk.

    :param audio_url: A string containing the URL of the audio file.
    :param target_path: A string specifying where the downloaded file should be saved.
    :param retries: An integer defining how many attempts are made before giving up when hitting exceptions during download. Default is set to 3.
    """

    # Ensure directories exist
    directory = os.path.dirname(target_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    logger.info(f"Starting download from '{audio_url}' to '{target_path}'.")
    start_time = time.time()

    for attempt in range(retries + 1):
        try:
            response = requests.get(audio_url, stream=True)
            response.raise_for_status()

            with open(target_path, "wb") as output_file:
                for chunk in response.iter_content(chunk_size=1024):
                    output_file.write(chunk)

            duration = round(time.time() - start_time, 2)
            logger.info(f"Download completed in {duration} seconds.")
            return

        except requests.exceptions.HTTPError as http_error:
            message = f"HTTP error {response.status_code} encountered while downloading audio from '{audio_url}'."
            logg(message, http_error, attempt)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as network_exception:
            message = (
                f"A network error occurred while downloading audio from '{audio_url}'."
            )
            logg(message, network_exception, attempt)


def logg(message, arg1, attempt):
    logger.warning(message)
    logger.warning(arg1)
    logger.warning(f"Retry #{attempt}: Retrying in {attempt*2} seconds.\n")
    time.sleep(attempt * 2)


if __name__ == "__main__":
    download_audio()
