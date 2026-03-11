from definitions import *

volume_down = False
stop = False

subprocess.run("aconnect -x", shell = True)

recognizer.dynamic_energy_threshold = False
calibrate_mic()

while stop == False:
    understood = True
    try:
        with mic as source:
            audio = recognizer.listen(source, phrase_time_limit=4)
            text = recognizer.recognize_google(audio, language = "en-US")

            if "alexa" in text.lower():
                play_object = start_sound.play()
                print(colored("listening...", "red"))
                play_object.wait_done()
                start_vol_down()
                volume_down = True
                audio = recognizer.listen(source, phrase_time_limit=7)
                demand_raw = recognizer.recognize_google(audio, language = "en-US")
                demand = demand_raw.lower()
                for char in demand:
                    time.sleep(0.05)
                    sys.stdout.write(char)
                    sys.stdout.flush()
                print("\n")

                if "who" in demand and "you" in demand: #who are you
                    print(colored("Hey Milo, I am Cherry. Your personal assistant.", "cyan"))

                elif "skip" in demand and "song" in demand: #skip song
                    subprocess.call(("playerctl", "next"))

                elif "pause" in demand or "play" in demand: #pause/play song
                    subprocess.call(("playerctl", "play-pause"))

                elif "volume" in demand and "up" in demand: #turn volume up
                    volume_up(demand)

                elif "volume" in demand and "down" in demand: #turn volume down
                    volume_down(demand)

                elif "set timer" in demand:
                    set_timer(demand)

                elif "calibrate" in demand or "recalibrate" in demand:
                    recalibrate_mic()

                elif "search for" in demand and "online" in demand:
                    web_search(demand)

                elif "search" in demand and "on youtube" in demand:
                    youtube_search(demand)

                elif "goodbye" in demand or "stop" in demand: #stop
                    stop = True

                else:
                    print(colored("Sorry, I could't understand you there. Try again", "cyan"))
                    play_object = error_sound.play()
                    understood = False


                end_vol_up()
                volume_down = False
                #end of action sound

                if understood:
                    play_object = stop_sound.play()
                    play_object.wait_done()

                else:
                    pass


    except:
        #print(colored("Error", "red"))
        if volume_down:
            end_vol_up()
            volume_down = False
