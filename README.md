# ByteFM Livestream Downloader

This Python script enables you to download the high-quality ByteFM livestream and save it as an MP3 file. The downloaded file can be played using any media player, such as VLC or Potplayer, even while the program is running.

By default, the script downloads the stream at 192kbps. If you prefer to download the stream at 128kbps, you can use the following URL instead: https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/mid/stream.mp3

## Installation

To use this script, you'll need to have Python 3 installed on your machine. You can download it from the official website: https://www.python.org/downloads/

You'll also need to install the `requests` library. You can do this by running the following command: `pip install requests`

## Usage

To use this script, simply run the `python main.py` file with Python. You can provide an extra URL and file path as arguments when you want to download it from a different source. For example:


`python main.py https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/high/stream.mp3 stream.mp3`

By default, the script downloads the stream at 192kbps. If you want to download the stream at 128kbps, you can use the following URL instead: https://bytefm--di--nacs-ice-01--02--cdn.cast.addradio.de/bytefm/main/mid/stream.mp3

This will download the livestream from the given URL and save it to the specified file path.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Development

A fluent-design style version for Windows 11 has been created, but is still in beta and may not work on Windows 10 or any OS other than Windows 11. 

![Image description](https://i.imgur.com/dLqxiXZ.png)

## Stuff
Here is the original source/ link, that will redirect you to the stream.

https://bytefm.cast.addradio.de/bytefm/main/mid/stream
-> Bit Rate 128 kbps

https://bytefm.cast.addradio.de/bytefm/main/high/stream
-> Bit Rate 192 kbps
