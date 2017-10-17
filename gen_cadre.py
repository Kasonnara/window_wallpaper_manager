import os
import random
import sys

from PIL import Image

#TODO get auto nom du pc
DEFAULT_CADRE_DIRECTORY = None
MACHINE_NAME = None
WALLPAPER_TARGET = None
ARCHIVE_DIRECTORY = None

# Check input validity
cadre_path = None
wallpaper_path = None
if len(sys.argv) < 6:
    print("Erreur: veuillez indiquer le chemin d'accès au fond d'écran.")
    sys.exit(1)
elif len(sys.argv) == 6:
    # Normal usage
    DEFAULT_CADRE_DIRECTORY = sys.argv[2]
    MACHINE_NAME = sys.argv[3]
    WALLPAPER_TARGET = sys.argv[4]
    ARCHIVE_DIRECTORY = sys.argv[5]
    cadre_list = os.listdir(DEFAULT_CADRE_DIRECTORY)
    for cadre in cadre_list:
        if MACHINE_NAME in cadre and "." in cadre and not ".py" in cadre:
            print(cadre)
            cadre_path = cadre
    wallpaper_path = sys.argv[1]
    if cadre_path is None:
        print("Erreur: cadre par defaut introuvable pour la machine %s dans le dossier '%s'" %
              (MACHINE_NAME, DEFAULT_CADRE_DIRECTORY))
        sys.exit(3)
else:
    print("Erreur: Trop de paramètres.")
    sys.exit(2)

# Open files
with Image.open(os.path.join(DEFAULT_CADRE_DIRECTORY, cadre_path)) as img_cadre:
    with Image.open(wallpaper_path) as img_wallpaper:
        # Merge images
        result = img_wallpaper.resize(img_cadre.size)
        result.paste(img_cadre, None, img_cadre)

        # Save merged wallpaper
        if os.path.basename(WALLPAPER_TARGET) == "":
            # wallpaper Target is a directory
            # Simply add new wallpaper
            print("Ajout du nouveau fond d'écran.")
            result.save(os.path.join(WALLPAPER_TARGET, os.path.basename(wallpaper_path)))
        else:
            # wallpaper target is a file
            # Archive last wallpaper if possible
            if not (ARCHIVE_DIRECTORY is None or ARCHIVE_DIRECTORY == "" or not os.path.exists(WALLPAPER_TARGET)):
                if not os.path.exists(ARCHIVE_DIRECTORY):
                    os.mkdir(ARCHIVE_DIRECTORY)
                print("Archivage de l'ancien fond d'écran.")
                os.rename(WALLPAPER_TARGET, os.path.join(ARCHIVE_DIRECTORY, "Archive_" + str(random.randint(0, 10 ** 5))))
            # Replace with new wallpaper
            print("Remplacement du fond d'écran.")
            result.save(WALLPAPER_TARGET)


def refresh_windows_wallpaper(wallpaper_filename):
    #TODO tester si ça marche bien
    os.system("reg add \"HKCU\Control Panel\Desktop\" /v Wallpaper /t REG_SZ /d \"C:\%s\" /f;"
      "reg add \"HKCU\Control Panel\Desktop\" /v TileWallpaper /t REG_SZ /d 0 /f;"
      "reg add \"HKCU\Control Panel\Desktop\" /v WallpaperStyle /t REG_SZ /d 2 /f;"
      "RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,true;" % wallpaper_filename)

"""
fig = plt.figure()
ax = fig.add_subplot("111", frame_on=False)

img_cadre = im.imread(cadre_path)
img_wallpaper = im.imread(wallpaper_path)
a, b, c = img_cadre.shape
x, y, z = img_wallpaper.shape

print("cadre", img_cadre.shape)
print("fond", img_wallpaper.shape)

import numpy as np
alpha = np.array([0.5])
result = img_cadre.copy()
for k, line in enumerate(result):
    for l, pixel in enumerate(line):
        if pixel[-1] < 0.5:
            #print((k * a) // x, (l * b)//y)
            #print(img_wallpaper[(k * a) // x, (l * b)//y])
            result[k, l, :3] = img_wallpaper[(k * a) // x, (l * b)//y, :3]
            result[k, l, 4:4] = alpha
            #result[k, l, :3] = np.array([1,0,1])
im.imsave("result.png", result)
"""