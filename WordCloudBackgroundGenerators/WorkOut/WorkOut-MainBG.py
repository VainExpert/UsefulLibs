#Workout-Helper -> Wordcloud-Mensch als UI-bg, Timer, Workouts-Database

"""
Here:
-> Wordcloud-Mensch als UI-bg
"""
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

#Words to Use
text = "Workout Fitness Body-Improvement! Abs Biceps Sally-Up Jog Run Squats Lads Leg-Day Never-Skip Triceps Calves Calisthenics Fit Back Stable! Exercise Transformation Sport Health Energy Body Active Outdoor Indoor Action Training Focus Train Bodybuild Athletic Muscles Shaoe FullBody Power Healthy Balance Stability Flexibility Endurance Stamina Swim Jump Handball Run Climb Hike Success Wellness Stretch Move Physical Motivation Lifestyle Core Focus SitUps PullUps TABATA Determination Weights Bodyweight Feel Good Trainer Routine Hygiene Reflexes Play Goals Inspiration Accomplishment Toned Cardio Sleep Diet Inspire Vitamins Happiness Clean Vital Vitality Gym Mentality HomeTraining Machines Team Meditation Fitness Fit Strength Abs Body Run Jog Marathon Game Nutrition Healthcare SelfCare Cardio Experience Extreme Fight On Games 5km 10km CrossCountry Ski Breakdance Dance BodyCare Mode Stability Heal NoPainNoGain"

#Get Colors of Image
manColor = np.array(Image.open("human.png"))
manColor = manColor[::3, ::3]

#Mask Image -> Color White is masked
maskedMan = manColor.copy()
maskedMan[maskedMan.sum(axis=2) == 0] = 255

#Makes Wordcloud with the words of the text in the grid of the Mask (uses mask for grid) uses unique colors 
wordCloudWhite = WordCloud(background_color = 'white', mask = maskedMan, width = 2048, height = 1992)
wordCloudWhite.generate(text)
plt.imshow(wordCloudWhite)
wordCloudWhite.to_file("FitMan(1).png")

#Makes Wordcloud with the words of the text in the grid of the Mask (uses mask for grid) recolors with colors of original image
image_colors = ImageColorGenerator(manColor)
wordCloudWhite.recolor(color_func = image_colors)
plt.figure(figsize=(18,10))
plt.imshow(wordCloudWhite, interpolation = 'bilinear')
wordCloudWhite.to_file("FitMan(2).png")

#Changes background from White to Black
img = Image.open('FitMan(2).png')
img = img.convert('RGBA')
data = np.array(img)

rgb = data[:,:,:4]
black = [0, 0, 0, 255]
white = [255, 255, 255, 255]

mask = np.all(rgb == white, axis = -1)
data[mask] = black

newimg = Image.fromarray(data)
newimg.save('FitMan(2)-NewBG.png')

#Changes background from White to Black
img = Image.open('FitMan(1).png')
img = img.convert('RGBA')
data = np.array(img)

rgb = data[:,:,:4]
black = [0, 0, 0, 255]
white = [255, 255, 255, 255]

mask = np.all(rgb == white, axis = -1)
data[mask] = black

newimg = Image.fromarray(data)
newimg.save('FitMan(1)-NewBG.png')

#Shows when everything is done
plt.show()
