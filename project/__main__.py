from __future__ import unicode_literals
import youtube_dl
import sys
import requests
import json
import yaml
import datetime

current_playlist=''
yaml_config=[]

def my_hook(d):

	if d['status'] == 'finished':
		song_name=d['filename'][16:-5]

		access_token=yaml_config['pushbullet']['access_token']

		message_title=yaml_config['pushbullet']['message_title']
		message_body=yaml_config['pushbullet']['message_body'] 
		formatted_message=message_body.format(song=song_name, playlist=current_playlist)

		# Set up the request for the pushbullet notification

		payload={
			'type': 'note',
			'title': message_title,
			'body': formatted_message,
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

	playlists=config['youtube-dl']['playlist']
	dl_location=config['config']['dl_location'] + '%(title)s.%(ext)s'
	archive_location=config['config']['archive_location'] + '.downloaded.txt'

	ydl_opts={
		'format': 'bestaudio/best',
		'ignoreerrors': True,
		'continue': True,
		'nooverwrites': True,
		'download_archive': archive_location,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '256'
		}],
		'outtmpl': dl_location,
		'progress_hooks': [my_hook]
	
	} # Pass in arguments for this
        for playlist in playlists:
            global current_playlist
            current_playlist=playlist['name']

	    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	        ydl.download([playlist['link']])

if __name__ == '__main__':
	# Get all the options from the config file

	stream = file('/home/rob/Documents/song-dl/project/config.yaml')
	yaml_config = yaml.load(stream)

	main(yaml_config)
