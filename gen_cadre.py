import datetime
import os
import sys

from PIL import Image

#TODO get auto nom du pc
DEFAULT_CADRE_DIRECTORY = None
MACHINE_NAME = None
TARGET_DIRECTORY = None
ARCHIVE_DIRECTORY = None


def usage():
    print("Usage, par le script change_wallpaper.bat:")
    print(" soit drag&drop du nouveau fond sur l icone de change_wallpaper.bat.")
    print(" soit lancer le script avec pour parametre le chemin d acces au fichier image du nouveau fond.")
    print("")
    print("Usage, directement par le script python")
    print("'c:/.../python.exe gen_cadre.py source_wallpaper source_cadres machine destination archive'")
    print(" source_wallpaper = chemin d acces au nouveau fond d ecran.")
    print(" source_cadres    = chemin d acces aux cadres sur buzz.")
    print(" machine          = nom de la machine courante (ce nom doit etre contenu dans le nom de son cadre sur buzz)")
    print(" destination      = chemin vers l endroit ou doit etre enregistre le nouveau cadre.\n"
          "                    si c'est un dossier : simple ajout du nouveau.\n"
          "                    si c'est un fichier : remplacement et archivage si possible de l ancien.")
    print(" archive          = chemin d acces au dossier d archivage.")
    input()


def refresh_windows_wallpaper(wallpaper_path):
    """
    os.system("reg add \"HKCU\Control Panel\Desktop\" /v Wallpaper /t REG_SZ /d \"C:\%s\" /f;"
      "reg add \"HKCU\Control Panel\Desktop\" /v TileWallpaper /t REG_SZ /d 0 /f;"
      "reg add \"HKCU\Control Panel\Desktop\" /v WallpaperStyle /t REG_SZ /d 2 /f;"
      "RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,true;" % wallpaper_filename)
    """
    # TODO tester si ça marche bien
    import ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)


# Check input validity
cadre_path = None
wallpaper_path = None
if len(sys.argv) < 5 or len(sys.argv) > 6:
    print("Erreur: nombre de parametres incorrect.")
    usage()
    sys.exit(1)
else:
    # Normal usage
    DEFAULT_CADRE_DIRECTORY = sys.argv[2]
    MACHINE_NAME = sys.argv[3]
    TARGET_DIRECTORY = sys.argv[4]
    if len(sys.argv) == 6:
        ARCHIVE_DIRECTORY = sys.argv[5]
    cadre_list = os.listdir(DEFAULT_CADRE_DIRECTORY)
    for cadre in cadre_list:
        if MACHINE_NAME in cadre and "." in cadre and not ".py" in cadre:
            print("Cadre trouvé :", cadre)
            cadre_path = cadre
    if cadre_path is None:
        print("Erreur: cadre introuvable pour la machine {} dans le dossier '{}'".format(
            MACHINE_NAME, DEFAULT_CADRE_DIRECTORY))
        input()
        sys.exit(2)
    wallpaper_path = sys.argv[1]


# Open files
with Image.open(os.path.join(DEFAULT_CADRE_DIRECTORY, cadre_path)) as img_cadre:
    with Image.open(wallpaper_path) as img_wallpaper:
        # Merge images
        result = img_wallpaper.resize(img_cadre.size)
        result.paste(img_cadre, None, img_cadre)

        # Compute new unique path
        target_path = os.path.join(TARGET_DIRECTORY, str(datetime.datetime.now())+"-"+MACHINE_NAME+"-"+os.path.basename(wallpaper_path)+".bmp")
        # wallpaper target is a file
        # Archive last wallpaper if possible
        if not (ARCHIVE_DIRECTORY is None or ARCHIVE_DIRECTORY == "" or not os.path.exists(TARGET_DIRECTORY)):
            print("Archivage désactivé, la nouvelle impémentation rendant sa fonction principale innutile.")
            #if not os.path.exists(ARCHIVE_DIRECTORY):
            #    os.mkdir(ARCHIVE_DIRECTORY)
            #print("Archivage de l'ancien fond d'écran.")
            #os.rename(TARGET_DIRECTORY, os.path.join(ARCHIVE_DIRECTORY, "Archive_" + str(random.randint(0, 10 ** 5))))
        # Replace with new wallpaper
        print("Remplacement du fond d'écran.")
        result.save(target_path)
        #refresh_windows_wallpaper(target_path)

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