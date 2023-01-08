#Automatisierter Foto-Sortierer und Umbenenner - V1.5

"""
Funktionen:
Programaufruf mit 2 Unterordnern von Camera_Roll als Programm-Argumente
-> Ausgabe Liste aller Dateien
-> Liste der Dateien sortiert nach Aufnahmezeitpunkt
-> Dateinamen geaendert
"""

#Imports
import os
import sys
import pathlib
import exifread
import PIL
from PIL import Image
import datetime

#Global Variables
VideoEnds = [".mp4", ".3gp", ".mov", ".mpg", ".mpeg", ".swf", ".svd" ,".wmv" , ".flv", ".f4p", ".avi", ".flm", ".flt"]
#PicEnds = []
NoDate = []
DateNums = []

#Get Directories
def get_input():
    if len(sys.argv) == 1:
        print("Keine Ordner angegeben!")
        sys.exit()

    elif len(sys.argv) == 2:
        unter1 = sys.argv[1]
        path = "C:/Users/Tom/Pictures/Camera_Roll/{}".format(unter1)

    elif len(sys.argv) == 3:
        unter1 = sys.argv[1]
        unter2 = sys.argv[2]
        path = "C:/Users/Tom/Pictures/Camera_Roll/{}/{}".format(unter1, unter2)

    elif len(sys.argv) == 4:
        unter1 = sys.argv[1]
        unter2 = sys.argv[2]
        unter3 = sys.argv[3]
        path = "C:/Users/Tom/Pictures/Camera_Roll/{}/{}/{}".format(unter1, unter2, unter3)

    elif len(sys.argv) == 5:
        unter1 = sys.argv[1]
        unter2 = sys.argv[2]
        unter3 = sys.argv[3]
        unter4 = sys.argv[4]
        path = "C:/Users/Tom/Pictures/Camera_Roll/{}/{}/{}/{}".format(unter1, unter2, unter3, unter4)

    elif len(sys.argv) == 6:
        unter1 = sys.argv[1]
        unter2 = sys.argv[2]
        unter3 = sys.argv[3]
        unter4 = sys.argv[4]
        unter5 = sys.argv[5]
        path = "C:/Users/Tom/Pictures/Camera_Roll/{}/{}/{}/{}/{}".format(unter1, unter2, unter3, unter4, unter5)

    return path


#Aufnahmedatum auslesen
def get_date_taken(fpath):

    try:
        with open(fpath, 'rb') as image:
            exif = exifread.process_file(image)
            date = str(exif['EXIF DateTimeOriginal'])
            return date

    except KeyError:
        try:
            img = Image.open(fpath)
            date = img.getexif()[36867]
            img.close()
            return date

        except TypeError as e:
            date = exception_handling(e)
            return date

        except PIL.UnidentifiedImageError as e:
            date = exception_handling(e)
            return date

        except KeyError as e:
            try:
                img = Image.open(fpath)
                date = img.getexif()[306]
                img.close()
                return date

            except TypeError as e:
                date = exception_handling(e)
                return date

            except KeyError as e:
                f = pathlib.Path(fpath)
                date = f.stat().st_mtime
                date = datetime.datetime.fromtimestamp(date)
                date = date.strftime("%Y:%m:%d %H:%M:%S")
                return date


#Format Date
def format_date(path, file):
    tempfullpath = path+"/"+file
    tempdate = get_date_taken(tempfullpath)
    tempdate = tempdate.split(" ")
    return tempdate

#Get Video Date
def video_date(filelist, i, path, f):
    
    if filelist[i-1].endswith(".jpg") or filelist[i-1].endswith(".JPG") and filelist[i+1].endswith(".jpg") or filelist[i+1].endswith(".JPG"):
        prevdate = format_date(path, filelist[i-1])
        nextdate = format_date(path, filelist[i+1])

    elif filelist[i-1].endswith(".jpg") or filelist[i-1].endswith(".JPG") and not (filelist[i+1].endswith(".jpg") or filelist[i+1].endswith(".JPG")):
        t = i + 1
        while not (filelist[t].endswith(".jpg") or filelist[t].endswith(".JPG")) and t < len(filelist)-1:
            t += 1

        nextphoto = filelist[t]
        prevdate = format_date(path, filelist[i-1])
        nextdate = format_date(path, nextphoto)

    elif not (filelist[i-1].endswith(".jpg") or filelist[i-1].endswith(".JPG")) and (filelist[i+1].endswith(".jpg") or filelist[i+1].endswith(".JPG")):
        t = i - 1
        while not (filelist[t].endswith(".jpg") or filelist[t].endswith(".JPG")) and t > 0:
            t -= 1

        prevphoto = filelist[t]
        nextdate = format_date(path, filelist[i+1])
        prevdate = format_date(path, prevphoto)

    else:
        t = i + 1
        d = i - 1
        while not (filelist[t].endswith(".jpg") or filelist[t].endswith(".JPG"))  and t < len(filelist)-1:
            t += 1
        while not (filelist[d].endswith(".jpg") or filelist[d].endswith(".JPG")) and d > 0:
            d -= 1

        prevphoto = filelist[d]
        nextphoto = filelist[t]
        nextdate = format_date(path, nextphoto)
        prevdate = format_date(path, prevphoto)


    if nextdate[0] == "" and prevdate[0] == "":
        print(path, "=> Kein Datum")
        return ""

    elif prevdate[0] == "":
        date = datetime.datetime.strptime(nextdate[0], "%Y:%m:%d")
        date -= datetime.timedelta(days=1)
        print(f, "=> Datum nicht genau!")

    elif nextdate[0] == "":
        date = datetime.datetime.strptime(prevdate[0], "%Y:%m:%d")
        print(f, "=> Datum nicht genau!")
        
    else:
        if prevdate[0] == nextdate[0]:
            date = datetime.datetime.strptime(prevdate[0], "%Y:%m:%d")
        
        else:
            date = datetime.datetime.strptime(prevdate[0], "%Y:%m:%d")
            prevd = datetime.datetime.strptime(prevdate[0], "%Y:%m:%d")
            nextd = datetime.datetime.strptime(nextdate[0], "%Y:%m:%d")

            timediff = nextd - prevd
            ddays = timediff.days
            if ddays == 1:
                date = prevd
            elif ddays == -1:
                date  = nextd
            elif ddays % 2 == 0:
                date += datetime.timedelta(days=(ddays/2))
            else:
                date += datetime.timedelta(days=(ddays%2))

    return date, nextdate

#Exception Handling
def exception_handling(e):
    date = ""
    return date

###Save Copy, Sicherheitskopie der Fotos falls Umbennenung schiefgeht -> Rueckgaengig machen
##def save_copy():
##    
##

#Sort auf Grundlage von Bubble Sort
def sort_photos(filelist):

    tempdates = []
    i = 0
    
    for f in filelist:
        ending = f[-4:].lower()
        if ending == ".jpg":
            
            fpath = path+"/"+f

            tempdate = get_date_taken(fpath)
            if tempdate == "":
                continue

            try:
                cdate = datetime.datetime.strptime(tempdate, "%Y:%m:%d %H:%M:%S")

            except ValueError:
                cdate = datetime.datetime.strptime(tempdate.strip("\x00"), "%Y:%m:%d %H:%M:%S")

            tempdates.append(cdate)

        elif ending in VideoEnds:
            
            cdate, nextdate = video_date(filelist, i, path, f)
            tempdates.append(cdate)

        i += 1
                        
    tempdates, filelist = gnomeSort(tempdates, filelist)

    return filelist

#Gnome Sort fuer Dateien
def gnomeSort(dates, tempfiles):
    n = len(dates)
    index = 0
    while index < n:
        ending = tempfiles[index][-4:].lower()
        if index == 0:
            index = index + 1
            
        elif dates[index] >= dates[index-1]:
            index = index + 1
            
        elif ending in VideoEnds:
            index = index + 1
            
        else:
            prevending = tempfiles[index-1][-4:].lower()
            if prevending not in VideoEnds:
                dates[index], dates[index-1] = dates[index-1], dates[index]
                tempfiles[index], tempfiles[index-1] = tempfiles[index-1], tempfiles[index]
                index = index - 1
                
            else:
                index = index + 1
 
    return dates, tempfiles



def temp_rename(tempfiles):
    
    for i in range(len(tempfiles)):
        
        ending = tempfiles[i][-4:].lower()
        fpath = "{}/{}".format(path, tempfiles[i])
        newpath = "{}/{}{}".format(path, i, ending)
        tempfiles[i] = "{}{}".format(i, ending)
        os.rename(fpath, newpath)

    return tempfiles

#Umbenennung der Dateien
def rename_photos():

    lauf = 1
    tempfiles = os.listdir(path)

    tempfiles = temp_rename(tempfiles)
    
    for i in range(len(tempfiles)):

        f = tempfiles[i]
        ending = f[-4:].lower()
        fpath = path+"/"+f
        
        if ending == ".jpg":

            date = get_date_taken(fpath)
            if date == "":
                print(fpath, "=> Kein Datum")
                NoDate.append(fpath)
                continue

            date = date.split(" ")
            adate = "-".join(date[0].split(":"))
            newname = "{}({}){}".format(adate, lauf, ending)

            tempnewname, nextdate = check_date(date, tempfiles, i, adate, ending)
            if tempnewname != "":
                newname = tempnewname

            pnewname = path+"/"+newname
            tempfiles = true_rename(f, fpath, newname, pnewname, tempfiles, i, lauf)
            
            if i < len(tempfiles)-1:
                if date != ""  and (nextdate != [''] and nextdate != [] and nextdate is not None and nextdate):
                    if date[0] != nextdate[0]:
                        lauf = date_numbs(lauf, date[0])
            lauf += 1
                    

        elif ending in VideoEnds:
            pnewname, newname, lauf, tempfiles = rename_videos(tempfiles, i, f, lauf, ending, fpath)

            if pnewname == "":
                continue

        else:
            print(tempfiles[i], "=> Was machst du hier?")
            continue

#Video Case
def rename_videos(filelist, i, f, lauf, ending, fpath):
    
    date, nextdate = video_date(filelist, i, path, f)
    if date == "":
        NoDate.append(fpath)
        return "", "", lauf, filelist
    
    date = date.strftime("%Y:%m:%d %H:%M:%S")
    date = date.split(" ")
    adate = "-".join(date[0].split(":"))
    newname = "{}({}){}".format(adate, lauf, ending)
    pnewname = path+"/"+newname

    filelist = true_rename(f, fpath, newname, pnewname, filelist, i, lauf)

    if i < len(filelist)-1:
        if date != "" and (nextdate != [''] and nextdate != [] and nextdate is not None and nextdate):
            if date[0] != nextdate[0]:
                lauf = date_numbs(lauf, date[0])
    lauf += 1
    

    return pnewname, newname, lauf, filelist

#Rename with exceptions
def true_rename(f, fpath, newname, pnewname, filelist, i, lauf):
    
    print("{} => {}".format(files[i], newname))
    if not os.path.exists(pnewname):
        os.rename(fpath, pnewname)
        filelist[i] = newname
                
    else:
        z = lauf
        while os.path.exists(pnewname):
            temp = z + 1
            lastname = "{}{}){}".format(newname[:-6], z, newname[-4:])
            tempname = "{}{}){}".format(newname[:-6], temp, newname[-4:])
            lastindex = filelist.index(lastname)
            lastpname = "{}/{}{}){}".format(path, newname[:-6], z, newname[-4:])
            temppname = "{}/{}{}){}".format(path, newname[:-6], temp, newname[-4:])
            os.rename(lastpname, temppname)
            z -= 1
            filelist[lastindex] = tempname
            

        os.rename(fpath, pnewname)
        filelist[i] = newname

    return filelist



#Check Date Numbers
def date_numbs(lauf, date):
    
    if date not in DateNums:
        DateNums.append(date)
        DateNums.append(lauf)
        lauf = 0
        
    else:
        index = DateNums.index(date)
        DateNums[index+1] += 1

    return lauf

#Check Date
def check_date(date, filelist, i, adate, ending):
    
    if i > 0 and i < len(filelist)-1:
        prevdate = format_date(path, filelist[i-1])
        nextdate = format_date(path, filelist[i+1])

        if date[0] != nextdate[0] and date[0] != prevdate[0] and nextdate != "" and prevdate != "":
            return adate+ending, nextdate[0]
        else:
            return "", nextdate

    elif i == 0 and len(filelist) > 1:
        nextdate = format_date(path, filelist[i+1])

        if date[0] != nextdate[0] and nextdate != "":
            return adate+ending, nextdate[0]
        else:
            return "", nextdate

    elif i == len(filelist)-1 and i != 0:
        prevpath = path+"/"+filelist[i-1]
        prevdate = get_date_taken(prevpath)
        prevdate = prevdate.split(" ")

        if date[0] != prevdate[0] and prevdate != "":
            return adate+ending, ""

    elif len(filelist) == 1:
        return adate+ending, ""

    return "", ""



#"Main"
print("\nFotos sortieren und umbenennen - V1.5: \n")

path = get_input()

print()
print(path)
print()

global files
files = os.listdir(path)

##Mehrere Unterordner?: (Umsetzung unklar, os.walk()) -> 2.0
##files = []
##for(dirpath, dirnames, filenames) in os.walk(path):
##    files.extend(filenames)

print("Unsortiert: ")
print(files)
print("\nDateianzahl:", len(files))
print()

files = sort_photos(files)
print("Sortiert: ")
print(files)
print()

rename_photos()

if len(NoDate) != 0:
    print("Folgende Dateien im angegebenen Pfad haben kein Aufnahmedatum, manuelle Umbenennenung noetig: ")
    print(NoDate)


print("\nDateianzahl:", len(files))
print("\nFertig :)")
