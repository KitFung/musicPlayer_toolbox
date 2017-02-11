# Introduction

A tools box for music lover to edit the audio file before import them to the player


# Requirement:

Python library
- bs4
- eyed3
- Pillow

Usage
--
Download music from street voice
`python street_voice_downloader.py target_url SAVE_FOLDER`
Resize the cover image directly
`python resize_coverimg.py folder width height`

Example
--

```bash
python main.py https://tw.streetvoice.com/Serruria/ ../tmusic
python resize_coverimg.py ~/Download 150 150
```
