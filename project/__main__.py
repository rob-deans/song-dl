from __future__ import unicode_literals
import youtube_dl
import sys
import argparse
import requests
import json
import ConfigParser


config=ConfigParser.ConfigParser()

def my_hook(d):

	if d['status'] == 'finished':
		print 'Finished downloading'

		song_name=d['filename'][:-17]

		access_token=config.get('pushbullet', 'access_token')

		message_title=config.get('pushbullet', 'message_title')
		message_body=config.get('pushbullet', 'message_body') % song_name

		# Set up the request for the pushbullet notification

		payload={
			'type': 'note',
			'title': message_title,
			'body': message_body,
		}
		
		headers={
			'Access-Token': access_token,
			'Content-Type': 'application/json'
		}

		r = requests.post(
			'https://api.pushbullet.com/v2/pushes',
			data=json.dumps(payload),
			headers=headers
		)


def main(config):

	songlink=config.get('youtube-dl','playlist')

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
		ydl.download([songlink])

if __name__ == '__main__':
	# Get all the options from the config file

	config.read('defaults.cfg')

	main(config)
