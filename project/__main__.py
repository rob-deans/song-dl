from __future__ import unicode_literals
import youtube_dl
import sys
import argparse

def main(args):
	ydl_opts = {
		'format': 'bestaudio/best',
		'ignoreerrors': True,
		'continue': True,
		'nooverwrites': True,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192'
		}],
	
	} # Pass in arguments for this
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([args])

if __name__ == '__main__':
	# Get all the options from the config file
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'yt_link', help = 'the youtube link to download'
	)
	args = parser.parse_args()
	print args.yt_link
	main(args.yt_link)