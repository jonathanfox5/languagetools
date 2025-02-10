# Language Tools

## NOTE: PARTIALLY SUPERCEEDED
A number of the projects in here have been superceeded by my [gogadget](https://github.com/jonathanfox5/gogadget) project and I intend on transferring the functionality of others across too.

Please check gogadget first!

## Overview

This is my repository of python and bash tools / cheatsheets that I use for manipulating content for language learning. The purpose of this repo is to provide example code that can be manipulated for your own purposes and hopefully save you some time / make sorting out your content easier.

I have placed global variables the top of most scripts to make it easier to change the parameters. Occasionally, a `.env` file is also used so that I don't accidentally upload my account details to Github. Where a `.env` file is required for a script, I have uploaded a `.env.example` file which you can rename to `.env` and enter your own details.

A few disclaimers:

- This is primarily intended to provide examples that you can base your own script on. It is expected that you will have to modify them to make them work for your specific applications.
- This is a git repo of my working directory so links, etc. will all point towards the last resource that I used.
- Since it's just a clone of my personal repo, files will appear to change randomly as I use them.
- Generally, I've kept error handling / comments / etc. to a bare minimum. Again, these are personal utlity scripts, not production code.
- I have only tested the scripts with Italian and English. I have no idea if they will work correctly with non-Latin writing systems!
- I won't be able to provide support for any issues that you may run into.
- I'm not a programmer! I've done things in ways that make sense to me but there are probably much better ways of doing them!

## Included Projects

- [cheatsheets](cheatsheets/) Cheatsheets for using command line tools such as yt-dlp and FFMPEG.
- [transcriber](transcriber/) Uses an optimised version of whisper to automatically transcribe subtitles from a video file.
- [srt_to_epub](srt_to_epub/) Converts a directory of subtitle files into transcripts and automatically compiles these into an `epub` that can be transferred to an eReader.
- [einscraper_ios](einscraper_ios/) Scrapes a clean version of the homepage of [EasyItalianNews.com](https://EasyItalianNews.com) and places the html document in dropbox for syncing with with my eReader. Designed to be run using a python interpretter on iOS.
- [einscraper](einscraper/) Desktop version of the above tool. Creates an epub that can be synced using [calibre](https://calibre-ebook.com). The iOS version of the script will generally be more up to date as I use it more.
- [podcast_italiano_to_ebook](podcast_italiano_to_ebook/) Downloads all transcriptions for Podcast Italiano and puts them into a markdown document. This can then be tidied up manually and manually converted to `epub` using [pandoc](https://pandoc.org) for viewing on an eReader.
- [podcast_downloader](podcast_downloader/) Downloads all episodes of a podcast based upon a set of filters.
- [file_renamer](file_renamer/) Used for the batch renaming of episodic content.
- [launchers](launchers/) Bash scripts to launch my preferred set of language learning tools.
- [link_downloader](link_downloader/) Downloads a list of links using yt-dlp. Used where a playlist file does not exist.

The required python modules for all of the scripts have been combined into [requirements.txt](requirements.txt).

## Workflows

The scripts are specifically written to work with my preferred workflows and tools. I've listed some of the key ones below so that you can understand why the scripts were written in a specific way and make your own adaptions.

Workflows:

- I prefer to read on my eReader. I will generally transfer books in `epub` format using [calibre](https://calibre-ebook.com) and articles in `html` format using Dropbox. I use [KOReader](https://github.com/koreader/koreader) on my eReader for its translation, dictionary lookup, syncing and Anki functionality.
- Making flashcards from subtitles: [asbplayer](https://chromewebstore.google.com/detail/asbplayer-language-learni/hkledmpjpaehamkiehglnbelcpdflcab?pli=1) -> [Vocabsieve](https://github.com/FreeLanguageTools/vocabsieve/) -> [Anki](https://apps.ankiweb.net). See the following video from [Refold](https://www.youtube.com/watch?v=jXO4gmCmcNE).
- Making flashcards from books: [Kobo Libra 2 eReader](https://uk.kobobooks.com/products/kobo-libra-2) -> [KOReader](https://github.com/koreader/koreader) -> [Vocabsieve](https://github.com/FreeLanguageTools/vocabsieve/) -> [Anki](https://apps.ankiweb.net).
- Working with text: I have a preference for editing text in the markdown format and then using [pandoc](https://pandoc.org) to convert it to the required output format.

Other tools:

- Media player (macOS): [IINA](https://iina.io).
- Media player (iOS): Default preview app in the 'Files' app.
- Editing markdown files: [VSCode](https://code.visualstudio.com) with the 'prettier' extension set to format on save.
- Python interpretter (iOS): [Pyto](https://pyto.app)
- Cloud storage: I back up all of my media files to iCloud for easy access on multiple devices.
