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


def refresh_windows_wallpaper(wallpaper_source_path):
    import ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_source_path, 3)


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
    TARGET_DIRECTORY = sys.argv[4] #.replace(" ", "") # TODO vérifier si c'est essentiel peux ammener a des erreurs
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
        wp_name = os.path.basename(wallpaper_path)
        target_path = os.path.abspath(os.path.join(TARGET_DIRECTORY,
                                                   datetime.datetime.now().strftime("%Y_%d_%m-%H_%M_%S") +
                                                   "-" + MACHINE_NAME + "-" + wp_name))
        # wallpaper target is a file
        # Archive last wallpaper if possible
        if not (ARCHIVE_DIRECTORY is None or ARCHIVE_DIRECTORY == "" or not os.path.exists(TARGET_DIRECTORY)):
            print("Archivage desactive, la nouvelle impementation rendant sa fonction principale innutile.")
            #if not os.path.exists(ARCHIVE_DIRECTORY):
            #    os.mkdir(ARCHIVE_DIRECTORY)
            #print("Archivage de l'ancien fond d'écran.")
            #os.rename(TARGET_DIRECTORY, os.path.join(ARCHIVE_DIRECTORY, "Archive_" + str(random.randint(0, 10 ** 5))))
        # Replace with new wallpaper
        print("Remplacement du fond d ecran.")
        result.save(target_path)
        refresh_windows_wallpaper(target_path)
