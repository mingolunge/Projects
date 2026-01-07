from time import sleep
import json
from subprocess import run, check_output
from threading import Thread

####AIRTABLE
from pyairtable import Api
api = Api("secret")
table = api.table('appid', 'tableid')
table.all()
##################


duration: int

def duration_to_seconds(duration_str):
    """Convert 'ss', 'mm:ss', or 'hh:mm:ss' to total seconds."""
    parts = [int(p) for p in duration_str.split(":")]

    if len(parts) == 1:  # just seconds
        return parts[0]
    elif len(parts) == 2:  # mm:ss
        minutes, seconds = parts
        return minutes * 60 + seconds
    elif len(parts) == 3:  # hh:mm:ss
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid duration format: {duration_str}")
        

def parsecmd(cmd: str):
    return cmd.split()

def exec(cmd):
    run(parsecmd(cmd))

def closetab():
    exec("hyprctl dispatch sendshortcut CTRL,W,")

def play(query):
    global duration
    search = f"ytsearch1:{query} Karaoke"
    
    video_id = check_output([
        "yt-dlp",
        search,
        "--get-id"
    ], text=True).strip()
    link =  f"https://www.youtube.com/watch?v={video_id}"
    duration = check_output(parsecmd(f"yt-dlp --get-duration {link}"), text=True)
    duration = duration_to_seconds(duration) - 10
    closetab()
    exec(f'firefox -p Karaoke --new-tab {link}')
    sleep(10)
    exec("hyprctl dispatch sendshortcut ,F,")

Thread(target=exec, args=("firefox -p Karaoke",)).start()

played = set()

while True:
    songs = table.all()
    print("got table")
    # songs_sorted = sorted(records, key=lambda r: r["createdTime"])

    for record in songs:
        fields = record["fields"]
        title = fields.get("Song - Artist")

        if not title or title in played:
            continue

        print(title)
        try:
            play(title)
            sleep(duration)
            played.add(title)
        except:
            pass

    sleep(5)

