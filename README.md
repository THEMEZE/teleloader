# ⚙️ Git Mise à jour
```bash
git add .
git commit -m "Mise à jour"
git push
```

---


1. Vérifier si le fichier existe déjà.
2. Si le fichier existe, proposer une option de **re-téléchargement** contrôlée par un argument de ligne de commande (`--overwrite` ou `--no-overwrite`).
3. Par défaut, ne **pas retélécharger** les fichiers existants.

Voici une version modifiée de ton script :

```python
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
```

### 🔹 Explications des changements :

1. **Détection du fichier existant** :

   * On utilise `yt-dlp --get-filename` pour connaître le nom exact du fichier qui serait généré.
   * Si le fichier existe et que `--overwrite` n’est pas activé, on affiche un message et on considère le téléchargement comme « OK ».

2. **Option `--overwrite`** :

   * Permet de forcer le retéléchargement même si le fichier existe.

3. **Comportement par défaut** :

   * Pas de retéléchargement si le fichier existe, ce qui évite les doublons.





---

### 1️⃣ Structure du fichier

Ton script prend **deux arguments obligatoires** :

```
python downloader.py <mode> <url1> [url2 ...] [--overwrite]
```

* `<mode>` : `mp4` ou `mp3`
* `<url1> [url2 ...]` : une ou plusieurs URLs YouTube
* `--overwrite` (optionnel) : force le téléchargement même si le fichier existe déjà

---

### 2️⃣ Exemples d’utilisation

#### a) Télécharger une vidéo en MP4

```bash
python downloader.py mp4 "https://www.youtube.com/watch?v=m2B5g3ljJH8&list=PLMRkEU6bT3ape5qv7Gfj3lsWTLqtjKAAj&index=21"
```

* Si le fichier existe déjà, il **ne sera pas retéléchargé** par défaut.
* Le fichier sera sauvegardé dans `./Downloads`.

#### b) Télécharger plusieurs vidéos en MP3

```bash
python downloader.py mp3 "https://youtu.be/EX1" "https://youtu.be/EX2"
```

* Convertit automatiquement en audio `.mp3`.
* Ne télécharge pas les fichiers déjà existants.

#### c) Forcer le téléchargement des fichiers existants

```bash
python downloader.py mp4 "https://www.youtube.com/watch?v=EXEMPLE" --overwrite
```

* Même si le fichier existe déjà, le script le télécharge à nouveau.

---

### 3️⃣ Points importants

1. Assure-toi que le dossier `./Downloads` existe :

```bash
mkdir -p Downloads
```

2. Assure-toi que `yt-dlp` est installé et dans le PATH :

```bash
yt-dlp --version
```

3. Les fichiers seront nommés automatiquement selon le titre de la vidéo.



---


1. Un serveur Python (Flask) ultra simple
2. qui liste le contenu du dossier Downloads
3. et ton portfolio web qui affiche :
   - images (avec zoom au survol)
   - vidéos (avec preview image + lecture au clic)
   - fichiers audio
   - clic → ouverture / lecture
   - re-clic → fermeture / stop
   - style moderne

C’est exactement ce que tu veux.

## ✅ 1. Serveur Python pour lister `./Downloads`

### ✅ créer un venv dans ton dossier
Dans un terminal *ngrok.com*

```bash
brew install ngrok
ngrok config add-authtoken 36JlYPCcpzxtQKZmybgiAGIGUxR_xbd8dojHVjojDMnhwbHb
ngrok http 5000
```
*https://unwhining-tribally-robby.ngrok-free.dev*

Sans un autre terminal



Crée un fichier : `server.py`




Lance :

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install python-dotenv
python -c "import flask; print(flask.__version__)"
python3 server.py
```

```bash
python3 server.py

```

Ton site accède maintenant à tes fichiers via :
👉 `http://localhost:5000/list`
👉 `http://localhost:5000/file/NOM`

## ✅ 2. Portfolio HTML moderne

Crée un fichier : `index.html`



---

# Bot 

```bash
source venv/bin/activate
python bot.py
```

