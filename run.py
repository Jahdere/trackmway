import httplib
import json
import datetime
import time
import pygame as pg

def getTrams():
    trams = []
    client = httplib.HTTPSConnection('citymapper.com')
    client.request('GET', '/api/1/metrodepartures?headways=1&ids=ParisStation_Marie_de_Miribel&region_id=fr-paris');
    data = json.loads(client.getresponse().read())

    try:
        for departure in data['stations'][0]['sections'][0]['departure_groupings'][1]['departures']:
            trams.append(departure['time_seconds'])
    except Exception, e:
        print 'No tramways found'

    return trams

def playAudio():
    volume = 0.8
    music_file = 'tramway.mp3'
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Hurry up, tramway is here !!")
    except pg.error:
        print("File {} not found! ({})".format(music_file, pg.get_error()))
        return
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(5)

if __name__ == '__main__':
    next_tram = -1

    while True:
        if next_tram <= 0:
            if next_tram == 0:
                playAudio()

            trams = getTrams()

            # If no trams or the last tram is
            if len(trams) == 0:
                print 'End of service'
                break

            # Here tram is coming, switch to the next
            next_tram = int(trams[0])

        m, s = divmod(next_tram, 60)
        print "%02d:%02d" % (m, s)
        time.sleep(1)
        next_tram -= 1
