import os
from PIL import Image, UnidentifiedImageError
import exifread
import datetime
import pathlib

rootdir = "C:/Users/tom02/Pictures/Camera_Roll/Familie-"
VideoEnds = [".mp4", ".3gp", ".mov", ".mpg", ".mpeg", ".swf", ".svd" ,".wmv" , ".flv", ".f4p", ".avi", ".flm", ".flt"]
PicEnds = [".jpeg", ".jpg", ".png"]

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

        except UnidentifiedImageError as e:
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

#Exception Handling
def exception_handling(e):
    date = ""
    return date


def format_date(date):
    date = date.split(" ")
    day = "-".join(date[0].split(":"))
    time = "-".join(date[1].split(":"))
    return f"{day}--{time}"
    
def gnomeSort(array):
    
    n = len(array)
    index = 0
    
    while index < n:
        
        if index == 0:
            index = index + 1
        
        if array[index] >= array[index-1]:
            index = index + 1
        
        else:
            array[index], array[index-1] = array[index-1], array[index]
            index = index - 1
 
    return array

def rename_images(array):
    
    disidx = 1
    for idx in range(len(array)):
        img = array[idx]
        
        ending = img[-4:].lower()
        temp = img.split("--")

        if idx > 0 and temp[0] != array[idx-1].split("--")[0]:
            disidx = 1

        newname = f"{temp[0]}({disidx}){ending}"
        
        if not os.path.exists(newname):
            os.rename(img, newname)

        disidx += 1

def display_results(dir, files, imgs, vids, nodate, unknown):
    
    print(f"\n\nIn the Directory {dir}:")
    print(f"Original Number of Files: {len(files)}")
    print(f"New Number of Files: {len(imgs)}")
    
    for img in imgs:
        print(img)
    
    print("\nThe following Files have no Dates, rename manually:")
    for no in nodate:
        print(no)

    print("\nThe following Files are Videos, rename manually:")
    for vid in vids:
        print(vid)

    print("\nThe following Files are not Media Data, move manually:")
    for un in unknown:
        print(un)

NoDate = []
Videos = []
Unknown = []
Images = []

print("\nAuto Photo Renamer:")
print(f"\nStarting in {rootdir}")
print("Renaming in every directory with \"-\" at the end")

for subdir, dirs, files in os.walk(rootdir):
    if subdir.endswith('-'):
        
        if len(files) == 0:
            continue
        
        dirpath = subdir[:-1]
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        for file in files:

            path = os.path.join(subdir, file)

            ending = file[-4:].lower()
            if ending in VideoEnds:
                Videos.append(path)
                continue
            
            elif ending not in PicEnds:
                Unknown.append(path)
                continue
 
            date = get_date_taken(path)

            if date == "":
                NoDate.append(path)
                continue

            fdate = format_date(date)
            newpath = f"{dirpath}/{fdate}{ending}"
            
            if not os.path.exists(newpath):
                os.rename(path, newpath)
            else:
                eidx = 0
                while os.path.exists(newpath):
                    newpath = f"{dirpath}/{fdate}({eidx}){ending}"
                    eidx += 1
                os.rename(path, newpath)

            Images.append(newpath)

        Images = gnomeSort(Images)
        rename_images(Images)

        display_results(subdir, files, Images, Videos, NoDate, Unknown)

        NoDate = []
        Videos = []
        Images = []

print("\nRemoving empty directories and renaming parents")

import shutil

for subdir, dirs, files in os.walk(rootdir):
    if subdir.endswith('-'):
        check = True
        if len(files) == 0 and len(dirs) == 0:
            shutil.rmtree(subdir)
            
        elif len(files) == 0:
            for dir in dirs:
                if dir.endswith("-"):
                    check = False
            
            if check:
                if not os.path.exists(subdir[:-1]):
                    os.rename(subdir, subdir[:-1])

print("All Done! :)\n\n")