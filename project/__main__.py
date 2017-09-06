from __future__ import unicode_literals
import youtube_dl
import sys
import argparse
import requests
import json

def my_hook(d):

	if d['status'] == 'finished':
		print 'Finished downloading'
		song_name=d['filename'][:-17]
		print song_name
		payload={
			'title': 'Downloaded',
			'body': song_name,
		}
		
		headers={
			'Access-Token': '',
			'Content-Type': 'application/json'
		}

		r = requests.post(
			'https://api.pushbullet.com/v2/pushes',
			data=json.dumps(payload),
			headers=headers
		)

		print r.text


def main(args):
	ydl_opts={
		'format': 'bestaudio/best',
		'ignoreerrors': True,
		'continue': True,
		'nooverwrites': True,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192'
		}],
		'progress_hooks': [my_hook]
	
	} # Pass in arguments for this
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([args])

if __name__ == '__main__':
	# Get all the options from the config file
	parser=argparse.ArgumentParser()
	parser.add_argument(
		'yt_link', help = 'the youtube link to download'
	)
	args=parser.parse_args()
	main(args.yt_link)
