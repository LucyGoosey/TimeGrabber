# TimeGrabber

Takes time ranges and gives the time between them. Works with either a provided file, or contents of the clipboard.

## Getting Started

Clone the repo and go!

### Prerequisites

```
pip install pyperclip
```

## Usage
Time must be in the format:
```
00:00-02:34
04:45-15:53
16:17-19:25
22:15-01:19
```

Output will be in the format:
```
00:00-02:34 	// 2 hours and 34 minutes
04:45-15:53 	// 11 hours and 8 minutes
16:17-19:25 	// 3 hours and 8 minutes
22:15-01:19 	// 3 hours and 4 minutes

Total time: 19 hours and 54 minutes
```

Either save the times to a file and drag/drop the file onto TimeGrabber.py, or open TimeGrabber.py and type in the path to the file, or just have the times in your clipboard and open TimeGrabber.py.

If a file is provided the output will be in FILENAME_.EXT, where FILENAME is the original filename and EXT is the original extension.

If the times are on the clipboard the output will replace what is in the clipboard.

## License

This project is licensed under the GNU General Public - see the [LICENSE.md](LICENSE.md) file for details.
