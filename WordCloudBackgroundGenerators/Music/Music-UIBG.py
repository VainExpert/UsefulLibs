
"""
Here:
-> Wordcloud-Note als GUI-BG
"""
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

#Words to Use
text = "Music Samba Salsa ChaChaCha Tango Walzer PasoDoble Jive Dance Tanz Musik Paartanz Solotanz HipHop Breakdance Merengue Menuett Polka Rock'n'Roll Rumba Sirtaki SquareDance Stepptanz Swing Latino Klassik Zumba Polonaise Mambo LineDance Limbo LangsamerWalzer WienerWalzer Lambada Hula Foxtrott Discofox Blues BoogieWoogie Charleston Disco Ball Let'sDance Noten Instrumente Band LiveMusik Solotanz Gruppentanz Jury Feier Anlass Tanzschuhe Kleid Anzug"

#Get Colors of Image
notePic = np.array(Image.open("note.jpg"))

#Mask Image -> Color White is masked
maskedMusic = notePic.copy()
maskedMusic[maskedMusic.sum(axis=1) == 0] = 255

#Makes Wordcloud with the words of the text in the grid of the Mask (uses mask for grid) uses unique colors 
wordCloudWhite = WordCloud(background_color = 'white', mask = maskedMusic, width = 2048, height = 1992)
wordCloudWhite.generate(text)
plt.imshow(wordCloudWhite)
wordCloudWhite.to_file("MusicNote.png")

#Shows when everything is done
plt.show()
