# SpotToBee

SpotToQob is a command-line tool for backing up your Spotify playlists using the 'lucky' function in [Vitiko98](https://github.com/vitiko98)'s [qobuz-dl](https://github.com/vitiko98/qobuz-dl). 

Fetching large playlists from Spotify requires Spotify API client credentials from https://developer.spotify.com/dashboard. The tool can be used without credentials to download small playlists, or alongside https://exportify.net/.

## Installation

    pip install SpotToQob

Running SpotToQob will automatically prompt you to create a config file in its run directory if one isn't present.

## Usage
SpotToQob allows you to download either songs or complete albums. Simply specify using either:

	--songs
	--albums

You can specify your config location using:

	--config <path>

You can reconfigure SpotToQob at any time using

	--reconfigure

##Examples:

    SpotToQob path/to/playlist.csv

    SpotToQob --albums https://open.spotify.com/playlist/37i9dQZF1DZ06evO2yQ3x9

	SpotToQob --songs https://open.spotify.com/playlist/37i9dQZF1DZ06evO2yQ3x9 https://open.spotify.com/playlist/37i9dQZF1DZ06evO1ASPuk

    SpotToQob --config path/to/config.ini --<type> <url> or <csv>

    SpotToQob --reconfigure

## Configuration Example

	[SpotifyAPI]
	clientid = <your client id>
	clientsecret = <your client secret>

## Credits
Special thanks to [Vitiko98](https://github.com/vitiko98) for the amazing [qobuz-dl](https://github.com/vitiko98/qobuz-dl), without which this tool could not exist.

## License

Copyright (c) 2024 Brendan Stupik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
