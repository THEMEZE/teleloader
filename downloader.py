#!/usr/bin/env python3
#python3 downloader.py mp4 \
#    "https://www.youtube.com/watch?v=ZrPpqJpI6sE&t=542s" \
#    "https://www.youtube.com/watch?v=Yo5vRHJ5y0Y&t=1774s" \
#    "https://www.youtube.com/watch?v=s47X4a2OjYA&t=534s"
#python3 downloader.py mp3
#"https://www.youtube.com/watch?v=JfrSpF28TEs" \
#"https://www.youtube.com/watch?v=Gj-wXOcj-l4" \
#"https://www.youtube.com/watch?v=3dIORFHzA_Y&t=28s"

#python3 downloader.py mp3 \
#    "https://youtu.be/JfrSpF28TEs?list=RDJfrSpF28TEs" \
#    "https://www.youtube.com/watch?v=qJBHSyJw6o4&t=189s" \
#    "https://www.youtube.com/watch?v=cKr5Qy-iopw" \
#    "https://youtu.be/qyyG4l0RvWE" \
#    "https://youtu.be/ryl-NvQwYqc"


    
    
# import argparse
# import subprocess
# import sys

# def telecharger(url, mode):
#     """
#     Télécharge une URL avec yt-dlp
#     mode = "mp4" ou "mp3"
#     """

#     if mode == "mp4":
#         cmd = [
#             "yt-dlp",
#             "-f", "bv*+ba",
#             "--merge-output-format", "mp4",
#             "-o", "./Downloads/%(title)s.%(ext)s",
#             url
#         ]
#     else:  # mp3
#         cmd = [
#             "yt-dlp",
#             "-f", "bestaudio/best",
#             "--extract-audio",
#             "--audio-format", "mp3",
#             "-o", "./Downloads/%(title)s.%(ext)s",
#             url
#         ]

#     try:
#         result = subprocess.run(cmd, capture_output=True, text=True)

#         if result.returncode != 0 or "ERROR" in result.stderr:
#             print(f"🔴 Erreur avec {url}")
#             print(result.stderr)
#             return False

#         print(f"🟢 Téléchargement OK : {url}\n")
#         return True

#     except Exception as e:
#         print(f"🔴 Exception pour {url} : {e}")
#         return False


# def main():
#     parser = argparse.ArgumentParser(description="Télécharge des vidéos ou audios Youtube")
#     parser.add_argument("mode", choices=["mp4", "mp3"], help="Format de sortie")
#     parser.add_argument("urls", nargs="+", help="Liste d'URLs Youtube")

#     args = parser.parse_args()

#     urls_fail = []
#     for url in args.urls:
#         print(f"▶️ Tentative : {url}")
#         ok = telecharger(url, args.mode)
#         if not ok:
#             urls_fail.append(url)

#     print("\n=== Résumé ===")
#     if urls_fail:
#         print("🔴 URLs non téléchargées :")
#         for u in urls_fail:
#             print("   -", u)
#     else:
#         print("🟢 Tout téléchargé avec succès !")


# if __name__ == "__main__":
#     main()
    
    
import argparse
import subprocess
import sys
import os

DOWNLOAD_DIR = "./Downloads"

def telecharger(url, mode, overwrite=False):
    """
    Télécharge une URL avec yt-dlp
    mode = "mp4" ou "mp3"
    overwrite = True pour forcer le téléchargement même si le fichier existe
    """

    # Nom du fichier de sortie prévu
    if mode == "mp4":
        out_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    else:
        out_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    # Vérification si le fichier existe déjà
    # On utilise yt-dlp pour connaître le titre prévu
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-filename", "-o", out_template, url],
            capture_output=True, text=True
        )
        fichier_prevu = result.stdout.strip()
    except Exception as e:
        print(f"🔴 Impossible de déterminer le nom du fichier pour {url} : {e}")
        return False

    if os.path.exists(fichier_prevu) and not overwrite:
        print(f"⚠️ Fichier déjà existant : {fichier_prevu}")
        return True  # on considère que c'est OK, pas besoin de retélécharger

    # Construction de la commande yt-dlp
    if mode == "mp4":
        cmd = [
            "yt-dlp",
            "-f", "bv*+ba",
            "--merge-output-format", "mp4",
            "-o", out_template,
            url
        ]
    else:  # mp3
        cmd = [
            "yt-dlp",
            "-f", "bestaudio/best",
            "--extract-audio",
            "--audio-format", "mp3",
            "-o", out_template,
            url
        ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0 or "ERROR" in result.stderr:
            print(f"🔴 Erreur avec {url}")
            print(result.stderr)
            return False

        print(f"🟢 Téléchargement OK : {url}\n")
        return True

    except Exception as e:
        print(f"🔴 Exception pour {url} : {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Télécharge des vidéos ou audios Youtube")
    parser.add_argument("mode", choices=["mp4", "mp3"], help="Format de sortie")
    parser.add_argument("urls", nargs="+", help="Liste d'URLs Youtube")
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Forcer le téléchargement même si le fichier existe"
    )

    args = parser.parse_args()

    urls_fail = []
    for url in args.urls:
        print(f"▶️ Tentative : {url}")
        ok = telecharger(url, args.mode, overwrite=args.overwrite)
        if not ok:
            urls_fail.append(url)

    print("\n=== Résumé ===")
    if urls_fail:
        print("🔴 URLs non téléchargées :")
        for u in urls_fail:
            print("   -", u)
    else:
        print("🟢 Tout téléchargé avec succès !")


if __name__ == "__main__":
    main()


