# This Python script is cross-platform compatible and can be run on any operating system that supports Python and PyQT6/ QT
# Script has been tested on Windows 11 with Python 3.8/ Arch with Python 3.11

import logging
import os
import threading
from datetime import datetime

import requests
from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ByteFMDownloader(QWidget):
    """A GUI for downloading audio streams from ByteFM."""

    def __init__(self, parent=None):
        """
        Initialize the ByteFMDownloader class.

        Args:
            parent: The parent widget of the GUI.
        """
        super().__init__(parent)
        self.setStyleSheet("background-color: #000000; color: #D4D4D4;")
        self._make_widgets()

    def _make_widgets(self):
        """Create the GUI widgets."""
        self.quality_variants = ["192kbps", "128kbps"]
        self.current_quality = 0

        self.quality_button = QPushButton(
            self.quality_variants[self.current_quality], clicked=self.toggle_quality
        )
        self.quality_button.setStyleSheet("background-color: #181A1B; color: #D4D4D4;")
        self.quality_button.setFixedSize(100, 30)

        self.download_button = QPushButton("Download", clicked=self.start_download)
        self.download_button.setStyleSheet("background-color: #181A1B; color: #D4D4D4;")
        self.download_button.setFixedSize(100, 30)

        self.size_label = QLabel("Size: 0 MB")
        self.time_label = QLabel("Time: 0 seconds")
        self.timeout_label = QLabel("Timeout: N/A")
        self.speed_label = QLabel("Speed: N/A")

        grid_layout = QGridLayout(self)
        grid_layout.addWidget(self.quality_button, 0, 0, 1, 1)
        grid_layout.addWidget(self.download_button, 0, 1, 1, 1)
        grid_layout.addWidget(self.size_label, 1, 0)
        grid_layout.addWidget(self.time_label, 1, 1)
        grid_layout.addWidget(self.timeout_label, 2, 0)
        grid_layout.addWidget(self.speed_label, 2, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setRowStretch(2, 1)

    def toggle_quality(self):
        """Toggle the audio stream quality."""
        self.current_quality = 1 - self.current_quality
        self.quality_button.setText(self.quality_variants[self.current_quality])

    def start_download(self):
        """Start the download process."""
        self.download_button.setEnabled(False)
        self.download_button.setText("Downloading...")
        self.download_thread = threading.Thread(target=self.download)
        self.download_thread.start()

    def download(self):
        """Download the audio stream."""
        quality = self.quality_variants[self.current_quality]
        url = ""
        if quality == "192kbps":
            url = URL_HIGH_QUALITY
        elif quality == "128kbps":
            url = URL_MID_QUALITY
        else:
            logging.error("Invalid quality selected.")
            return

        try:
            with requests.get(url, stream=True, timeout=10) as response:
                response.raise_for_status()
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                file_name = f"stream_{quality}.mp3"
                file_path_with_timestamp = os.path.join(
                    os.path.dirname(FILE_PATH), f"{timestamp}_{file_name}"
                )
                with open(file_path_with_timestamp, "wb") as file:
                    downloaded_size = 0
                    start_time = datetime.now()
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        elapsed_time = (datetime.now() - start_time).total_seconds()
                        if elapsed_time > 0:
                            if elapsed_time >= 3600:
                                elapsed_time_str = f"{int(elapsed_time // 3600)} h, {int((elapsed_time % 3600) // 60)} m"
                            elif elapsed_time >= 60:
                                elapsed_time_str = f"{int(elapsed_time // 60)} m, {int(elapsed_time % 60)} s"
                            else:
                                elapsed_time_str = f"{int(elapsed_time)} seconds"
                            self.size_label.setText(
                                f"Size: {downloaded_size / 1024 / 1024:.2f} MB"
                            )
                            self.time_label.setText(f"Time: {elapsed_time_str}")
                            download_speed = downloaded_size / elapsed_time / 1024
                            self.speed_label.setText(
                                f"Speed: {download_speed:.2f} KB/s"
                            )
            logging.info("Download complete.")
        except requests.exceptions.RequestException as error:
            logging.error(f"Error: {error}")
            self.timeout_label.setText("Timeout: Yes")

        self.download_button.setText("Download")
        self.download_button.setEnabled(True)
        self.size_label.setText("Size: 0 MB")
        self.time_label.setText("Time: 0 seconds")


def main():
    """
    Create the GUI and start the main loop.

    This function initializes the logging configuration, sets the application style and palette,
    creates the ByteFMDownloader GUI, sets its window title and geometry, and starts the main event loop.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
    )

    app = QApplication([])
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#181A1B"))
    app.setPalette(palette)
    # app.setWindowIcon(QIcon("ByteFM.ico"))

    gui = ByteFMDownloader()
    gui.setWindowTitle("ByteFM Downloader")
    gui.setGeometry(100, 100, 280, 130)
    gui.show()

    app.exec()


if __name__ == "__main__":
    # Constants
    URL_HIGH_QUALITY = "https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/high/stream.mp3"
    URL_MID_QUALITY = "https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/mid/stream.mp3"
    FILE_PATH = "stream.mp3"

    main()
