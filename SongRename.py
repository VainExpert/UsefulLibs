#Automatisierter Song-Umbenbenner - V1.0



#Imports
import os
import sys

import asyncio
from shazamio import Shazam

from bs4 import BeautifulSoup
import requests

import mutagen
from mutagen.easyid3 import EasyID3


#
def prettyPrinting(dir):

	temp = []
	for file in dir:
		temp.append(os.path.join(path, file))
	
	global col_width
	col_width = max(len(row) for row in temp) + 2  # padding
	
	for row in data:
		print("".join(word.ljust(col_width) for word in row))

#
async def recognize_song(filename):

    shazam = Shazam()
    global out
    out = await shazam.recognize_song(filename)



#
def getInfos():
    
    infos = parseInfos(out)

    if infos == []:
        return {}

    information = {'title': infos[0], 'artist': infos[1], 'albumartist': infos[2], 'album': infos[3], 'label': infos[4], 'genre': infos[5], 'popularity': infos[6], 'year': infos[7], 'lyrics': infos[8], 'writer': infos[9], 'dances': infos[10], 'bpm': infos[11]}
    return information


#
def parseInfos(InfoDict):

    try:
        title = InfoDict['track']['title']
        artist = InfoDict['track']['subtitle']
        albumartist = ""
        album = InfoDict['track']['sections'][0]['metadata'][0]['text']
        recordlabel = InfoDict['track']['sections'][0]['metadata'][1]['text']
        genre = InfoDict['track']['genres']['primary']
        year = InfoDict['track']['sections'][0]['metadata'][2]['text']

        text = ""
        for line in InfoDict['track']['sections'][1]['text']:
            text += line
            text += "\n"

        writer = InfoDict['track']['sections'][1]['footer']
        writer = writer[len("Writer(s):"):-len(" Lyrics powered by www.musixmatch.com")]
        writer = writer.strip().split(", ")

        artist = parseArtist(artist)

        dances, popularity, genres, bpm = parseDances(title, artist)

        if dances == "Error1":
            print("\nTanz-Webseite nicht erreichbar!\nStatus-Code: ",genres,"\n")
            dances = ""
            popularity = ""
            genres = []
            bpm = ""

        elif dances == "Error2":
            dances = ""
            popularity = ""
            genres = []
            bpm = ""

        if genres != []:
            exists = False
            for gen in genres:
                if genre == gen:
                    exists = True

            if not exists:
                genres.append(genre)

        infos = [title, artist, albumartist, album, recordlabel, genres, popularity, year, text, writer, dances, bpm]

        for item in infos:
            if isinstance(item, list):
                item = parseNames(item)

        return infos

    except:
        return []

#
def parseArtist(artist):

    global originalartist
    originalartist = artist
    split = False
    
    if "Feat." in originalartist:
        artist = originalartist.split(" Feat. ")
        split = True
        originalartist = originalartist.replace("Feat.", "feat.")

    if ", " in originalartist:
        
        if split:
            idx = 0
            for art in artist:
                
                if ", " in art:
                    art = art.split(", ")
                    replaced = True
                    
                    for a in art:
                        if replaced:
                            artist[idx] = a
                            replaced = False

                        else:
                            artist.append(a)
                idx += 1

        else:
            artist = originalartist.split(", ")
            split = True


        originalartist = originalartist.replace(", ", " feat. ")

    if "&" in originalartist:
        
        if split:
            idx = 0
            for art in artist:
                
                if "&" in art:
                    art.split(" & ")
                    replaced = True
                    
                    for a in art:
                        if replaced:
                            artist[idx] = a
                            replaced = False

                        else:
                            artist.append(a)
                idx += 1
                    
        else:
            artist = originalartist.split(" & ")
            split = True
        
        originalartist = originalartist.replace("&", "x")        

    if "/" in originalartist:
        
        if split:
            for art in artist:
                if "/" in art:
                    art = art.replace("/", " ")
        
        originalartist = originalartist.replace("/", " ")
        

    return artist    


#
def parseDances(title, artist):
    
    url = "https://www.tanzmusik-online.de/music/{}/title/{}".format(artist, title)

    page = requests.get(url)

    if page.status_code == 200:
        content = page.content

    else:
        return "Error1", "Webseite nicht erreichbar", page.status_code, 0

    WebDocument = BeautifulSoup(content, 'html.parser')

    try:
        title = WebDocument.find("meta", property="og:title").attrs['content'].rsplit('-', 2)[0]
        descr = WebDocument.find("meta", property="og:description").attrs['content']
        
        descr = descr.split(" / ")

        counts = []
        for div in WebDocument.find_all("span", {'class': "danceRating"}):
            count = 0
            for element in div:
                if "star" in str(element):
                    if "red" in str(element):
                        count += 1
        
            counts.append(count)

        maxcount = counts[0]
        for count in counts:
            if count > maxcount:
                maxcount = count
        maxcount = str(maxcount)

        possibleGenres = ['Pop', 'HipHop', 'Rock', 'Ballade', 'Alternative Rock', 'Indie', 'Alternative', 'Pop Rock', 'Rock Ballad', 'House', 'Dance', 'Techno', 'Electronic', 'Klassiker', 'Klassik', 'Classic Rock', 'Sonstige', 'Jazz', 'Soul', 'Rap', 'Dubstep', 'Classical', 'Folk', 'Dancehall', 'Latin', 'Metal', 'Vocal', 'Urban', 'Reggae', 'Country', 'Rock\'n\'Roll', 'Blues']
        genres = []
        bpm = 0
        for div in WebDocument.find_all('div', {'class': 'text'}):
            if "Genre: " in div.contents[0]:
                genres.append(div.contents[0][len("Genre: "):])
        
            if "Schläge pro Minute: " in div.contents[0]:
                bpm = div.contents[0][len("Schläge pro Minute: "):]

        for div in WebDocument.find_all('div', {'class': 'tags clearfix'}):
            for element in div.find_all('a'):
                if element.contents[1].strip().title() in possibleGenres and element.contents[1].strip().title() not in genres:
                    genres.append(element.contents[1].strip().title())

        return descr, maxcount, genres, bpm
        
    except:
        return "Error2", 0, [], 0

#
def parseNames(data):

    words = ""
    for word in data:
        words += word
        words += "; "

    return words


#
def refurbishSong(file, information):

    filepath = os.path.join(path, file)

    EasyID3.RegisterTextKey('comment', 'COMM')
    EasyID3.RegisterTextKey('lyrics', 'USLT')
    EasyID3.RegisterTextKey('popularity', 'POPM')


    try:
        meta = EasyID3(filepath)

    except mutagen.id3.ID3NoHeaderError:
        meta = mutagen.File(filepath, easy=True)
        meta.add_tags()


    if "- Single" in information['album']:
        information['albumartist'] = 'Various Artists'
        information['album'] = 'Single'

    if "feat." in originalartist:
        information['albumartist'] = information['artist'][0]

    elif len(information['artist']) > 1:
        information['albumartist'] = 'Various Artists'
        information['album'] = 'Single'

    meta['title'] = information['title']
    meta['artist'] = information['artist']
    meta['album'] = information['album']
    meta['albumartist'] = information['albumartist']
    meta['organization'] = information['label']
    meta['genre'] = information['genre']
    meta['date'] = information['year']
    meta['lyrics'] = information['lyrics']
    meta['lyricist'] = information['writer']
    meta['comment'] = information['dances']
    meta['popularity'] = information['popularity']
    meta['bpm'] = information['bpm']

    meta.save(filepath, v1=2, v2_version=4)

    newname = "{} - {}.mp3".format(originalartist, information['title'])
    newpath = "C:/Users/Tom/Music/" + newname

    if not os.path.exists(newpath):
        os.rename(filepath, newpath)
        print("{} => {}".format(filepath, newpath))

    else:
        os.remove(newpath)
        os.rename(filepath, newpath)
        print("{} => {}".format(filepath.ljust(col_width), newpath))

    meta.save(newpath, v1=2, v2_version=4)



#"Main"
print("\nSongs umbenennen und taggen - V1.0: \n")

global path
path = "C:/Users/Tom/Videos/4K Video Downloader/"
files = os.listdir(path)

prettyPrinting(files)

nodata = []
loop = asyncio.get_event_loop()

for file in files:

    if file[-4:].lower() != ".mp3":
        continue

    filepath = os.path.join(path, file)
    
    loop.run_until_complete(recognize_song(filepath))
    infos = {}
    infos = getInfos()

    if infos == {}:
        print("Keine Daten => {}".format(file))
        nodata.append(file)
        continue

    refurbishSong(file, infos)

if len(nodata) != 0:
    print("\nFür folgende Dateien gibt es nicht alle notwendigen Informationen: ")
    for data in nodata:
        print(data)

loop.close()
print("\nFertig! :)")
