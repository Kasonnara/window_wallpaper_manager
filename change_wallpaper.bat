REM TODO Adapter les 4 paramètres ci dessous ainsi que le chemin d'accès vers gen_cadre.py et python.exe
REM Toujours utiliser des chemins absolus car le code sera executé depuis le dossier
REM courant de l'image drag&drop (c'est à dire, potentiellement n'importe où!)

REM Le chemin d'accès au dossier contenant les cadres.
set DEFAULT_CADRE_DIRECTORY="cadres"

REM Nom de la machine courante, ce nom doit être contenu dans le nom du fichier du cadre.
set MACHINE_NAME="bibi"

REM Chemin vers le fichier où doit être enregistré le resultat
REM   Si WALLPAPER_TARGET est un dossier, le resultat sera enregistré dedans et tous les fonds d'écran seront conservé.
REM   Si c'est un fichier, l'ancien fond sera archivé si possible, puis remplacé par le nouveau
set WALLPAPER_TARGET="./result.png"

REM Chemin d'accès vers le dossier d'archive, mettre "" pour désactiver l'archivage.
set ARCHIVE_DIRECTORY="./archives"

REM "chemin_d_acces_a_python" sccript.py chmin_d_accès_au_nouveau_fond_ecran chemin_d_acces_aux_cadre_sur_buzz com_de_la_machine chemin_où_placer_le_fond dossier_d_archivage
"c:\Python27\python.exe" gen_cadre.py %1 %DEFAULT_CADRE_DIRECTORY% %MACHINE_NAME% %WALLPAPER_TARGET% %ARCHIVE_DIRECTORY%
