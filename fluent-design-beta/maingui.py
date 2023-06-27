import tkinter as tk
import ctypes
from win32mica import MICAMODE, ApplyMica
import customtkinter
import requests
from datetime import datetime
import os
import threading
import logging


class BlankGUI(customtkinter.CTkFrame):
    """A GUI for downloading audio streams from ByteFM."""

    def __init__(self, parent=None):
        super().__init__(parent, fg_color="#000000")
        self._make_widgets()

    def _make_widgets(self):
        """Create the GUI widgets."""
        self.quality_var = tk.StringVar()
        self.quality_var.set("192kbps")

        self.quality_button = customtkinter.CTkButton(
            self,
            text=self.quality_var.get(),
            fg_color="#181A1B",
            state="normal",
            width=30,
            height=30,
            command=self.toggle_quality,
        )
        self.quality_button.grid(row=0, column=0, padx=10, pady=10)

        self.button = customtkinter.CTkButton(
            self,
            text="Download",
            fg_color="#181A1B",
            state="normal",
            width=30,
            height=30,
            command=self.start_download,
        )
        self.button.grid(row=0, column=1, padx=10, pady=10)

        self.size_label = customtkinter.CTkLabel(
            self,
            text="Size: 0 MB",
            fg_color="#000000",
        )
        self.size_label.grid(row=1, column=0, padx=10, pady=10)

        self.time_label = customtkinter.CTkLabel(
            self,
            text="Time: 0 seconds",
            fg_color="#000000",
        )
        self.time_label.grid(row=1, column=1, padx=10, pady=10)

        self.timeout_label = customtkinter.CTkLabel(
            self,
            text="Timeout: N/A",
            fg_color="#000000",
        )
        self.timeout_label.grid(row=2, column=0, padx=10, pady=10)

        self.speed_label = customtkinter.CTkLabel(
            self,
            text="Speed: N/A",
            fg_color="#000000",
        )
        self.speed_label.grid(row=2, column=1, padx=10, pady=10)

        # Configure grid column and row weights to center the widgets
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)



    def toggle_quality(self):
        """Toggle the audio stream quality."""
        if self.quality_var.get() == "192kbps":
            self.quality_var.set("128kbps")
        else:
            self.quality_var.set("192kbps")
        self.quality_button.configure(text=self.quality_var.get())

    def start_download(self):
        """Start the download process."""
        self.button.configure(state="disabled")
        self.button.configure(text="Downloading...")
        self.update()

        # Start the download process in a separate thread
        download_thread = threading.Thread(target=self.download)
        download_thread.start()

    def download(self):
        """Download the audio stream."""
        quality = self.quality_var.get()
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
                                # Convert elapsed time to hours and minutes
                                elapsed_time_str = f"{int(elapsed_time // 3600)} h, {int((elapsed_time % 3600) // 60)} m"
                            elif elapsed_time >= 60:
                                # Convert elapsed time to minutes and seconds
                                elapsed_time_str = f"{int(elapsed_time // 60)} m, {int(elapsed_time % 60)} s"
                            else:
                                elapsed_time_str = f"{int(elapsed_time)} seconds"
                            self.size_label.configure(
                                text=f"Size: {downloaded_size / 1024 / 1024:.2f} MB"
                            )
                            self.time_label.configure(text=f"Time: {elapsed_time_str}")

                            # Calculate and update download speed
                            download_speed = downloaded_size / elapsed_time / 1024
                            self.speed_label.configure(
                                text=f"Speed: {download_speed:.2f} KB/s"
                            )
            logging.info("Download complete.")
        except requests.exceptions.RequestException as error:
            logging.error(f"Error: {error}")
            self.timeout_label.configure(text="Timeout: Yes")

        # Enable the button once the download is complete or encounters an error
        self.button.configure(text="Download")
        self.button.configure(state="normal")
        self.size_label.configure(text="Size: 0 MB")
        self.time_label.configure(text="Time: 0 seconds")



def main():
    """Create the GUI and start the main loop."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
    )

    root = customtkinter.CTk()
    root.title("ByteFM Downloader")
    root.geometry("280x130")
    root.configure(bg="#000000")
    root.resizable(False, False)
    root.iconbitmap("ByteFM.ico")
    root.deiconify()
    ApplyMica(HWND=ctypes.windll.user32.GetForegroundWindow(), ColorMode=MICAMODE.DARK)
    root.option_add("*background", "#1E1E1E")
    root.option_add("*foreground", "#D4D4D4")
    root.option_add("*activeBackground", "#3F3F3F")
    root.option_add("*activeForeground", "#D4D4D4")
    root.attributes("-alpha", 0.9)  # Set alpha value to 1.0 (fully opaque)

    gui = BlankGUI(root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    # Constants
    URL_HIGH_QUALITY = "https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/high/stream.mp3"
    URL_MID_QUALITY = "https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/mid/stream.mp3"
    FILE_PATH = "stream.mp3"

    main()