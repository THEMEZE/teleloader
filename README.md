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

Si tu veux, je peux aussi ajouter une **question interactive** pour chaque fichier existant : demander `O/N` avant de retélécharger, même si `--overwrite` n’est pas utilisé. Cela rendrait le script plus interactif pour des téléchargements ponctuels.

Veux‑tu que je fasse ça ?


---

## 👤 You

le fichier eest downloader.py

comment l'utiliser

---

## 🤖 ChatGPT

Parfait, si ton fichier s’appelle maintenant `downloader.py`, voici comment l’utiliser.

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

Si tu veux, je peux te préparer **une version encore plus pratique** :

* qui crée automatiquement `Downloads` s’il n’existe pas,
* et qui te demande **interactivement** si tu veux retélécharger un fichier existant (O/N) au lieu de toujours utiliser `--overwrite`.

Veux‑tu que je fasse ça ?

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



Crée un fichier : `server.py``

```python
from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

DOWNLOADS_DIR = os.path.expanduser("./Downloads")

@app.route("/list")
def list_files():
    files = []
    for f in os.listdir(DOWNLOADS_DIR):
        path = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(path):
            files.append(f)
    return jsonify(files)

@app.route("/file/<name>")
def serve_file(name):
    path = os.path.join(DOWNLOADS_DIR, name)
    return send_file(path)

app.run(host="0.0.0.0", port=5000)
```

```python
from flask import Flask, jsonify, send_file, request, send_from_directory
import os
import time

app = Flask(__name__)

# Dossier à exposer (change ici si tu veux autre chose que Downloads)
DOWNLOADS_DIR = os.path.expanduser("./Downloads")

# Cache simple en mémoire
FILE_CACHE = {"data": None, "mtime": 0}
CACHE_TTL = 5  # en secondes


IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
AUDIO_EXT = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}


def detect_type(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"


def scan_files():
    """Scan le dossier et met en cache le résultat."""
    now = time.time()
    if FILE_CACHE["data"] is not None and now - FILE_CACHE["mtime"] < CACHE_TTL:
        return FILE_CACHE["data"]

    files = []
    for f in os.listdir(DOWNLOADS_DIR):
        path = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(path):
            stat = os.stat(path)
            files.append({
                "name": f,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "type": detect_type(f)
            })

    FILE_CACHE["data"] = files
    FILE_CACHE["mtime"] = now
    return files


@app.route("/")
def index():
    # Sert le fichier index.html placé dans le même dossier que server.py
    return send_from_directory(".", "index.html")


@app.route("/list")
def list_files():
    files = scan_files()
    return jsonify(files)


@app.route("/file/<path:name>")
def serve_file(name):
    path = os.path.join(DOWNLOADS_DIR, name)
    if not os.path.isfile(path):
        return "Not found", 404
    return send_file(path)


@app.route("/upload", methods=["POST"])
def upload():
    # drag & drop upload
    if "file" not in request.files:
        return "No file", 400

    f = request.files["file"]
    if f.filename == "":
        return "No filename", 400

    # Simple : on garde le nom tel quel (tu peux sécuriser avec secure_filename si tu veux)
    dest = os.path.join(DOWNLOADS_DIR, f.filename)
    f.save(dest)

    # Invalide le cache
    FILE_CACHE["data"] = None
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

```bash
from flask import Flask, jsonify, send_file, request, send_from_directory
import os
import time

app = Flask(__name__)

# Dossier à exposer (change ici si tu veux autre chose que Downloads)
DOWNLOADS_DIR = os.path.expanduser("./Downloads")

# Cache simple en mémoire
FILE_CACHE = {"data": None, "mtime": 0}
CACHE_TTL = 5  # en secondes

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
AUDIO_EXT = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}


def detect_type(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"


def scan_files():
    """Scan le dossier et met en cache le résultat."""
    now = time.time()
    if FILE_CACHE["data"] is not None and now - FILE_CACHE["mtime"] < CACHE_TTL:
        return FILE_CACHE["data"]

    files = []
    for f in os.listdir(DOWNLOADS_DIR):
        # Ignore les fichiers qui commencent par '.', '..' ou '._'
        if f.startswith(".") or f.startswith("._"):
            continue
        path = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(path):
            stat = os.stat(path)
            files.append({
                "name": f,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "type": detect_type(f)
            })

    FILE_CACHE["data"] = files
    FILE_CACHE["mtime"] = now
    return files


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/list")
def list_files():
    files = scan_files()
    return jsonify(files)


@app.route("/file/<path:name>")
def serve_file(name):
    path = os.path.join(DOWNLOADS_DIR, name)
    if not os.path.isfile(path):
        return "Not found", 404
    return send_file(path)


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file", 400

    f = request.files["file"]
    if f.filename == "":
        return "No filename", 400

    # Ignore si le nom commence par '.' ou '._'
    if f.filename.startswith(".") or f.filename.startswith("._"):
        return "Invalid filename", 400

    dest = os.path.join(DOWNLOADS_DIR, f.filename)
    f.save(dest)

    # Invalide le cache
    FILE_CACHE["data"] = None
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```


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

> ⚠️ Ce code affiche automatiquement ton dossier Downloads comme une galerie moderne + zoom + lecture vidéo + audio\*\*

HTML + CSS + JS COMPLET (copie-colle)

```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <title>📁 Portfolio – Downloads</title>

    <style>
      body {
        background: #f5f5f5;
        font-family: Arial, sans-serif;
        padding: 20px;
      }

      h1 {
        text-align: center;
        margin-bottom: 30px;
      }

      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
      }

      .item {
        position: relative;
        cursor: pointer;
        overflow: hidden;
        border-radius: 15px;
        background: white;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
      }

      .item:hover {
        transform: scale(1.05);
      }

      .item img,
      .item video {
        width: 100%;
        display: block;
        border-radius: 15px;
      }

      /* Fullscreen viewer */
      #viewer {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        display: none;
        align-items: center;
        justify-content: center;
      }

      #viewerContent {
        max-width: 90%;
        max-height: 90%;
      }
    </style>
  </head>
  <body>
    <h1>📁 Portfolio – Downloads</h1>

    <div class="grid" id="grid"></div>

    <div id="viewer" onclick="closeViewer()">
      <div id="viewerContent"></div>
    </div>

    <script>
      async function loadFiles() {
        const response = await fetch("http://localhost:5000/list");
        const files = await response.json();

        const grid = document.getElementById("grid");

        files.forEach((name) => {
          const ext = name.split(".").pop().toLowerCase();
          const url = "http://localhost:5000/file/" + name;

          const div = document.createElement("div");
          div.className = "item";

          // IMAGE
          if (["jpg", "jpeg", "png", "gif", "webp"].includes(ext)) {
            div.innerHTML = `<img src="${url}" alt="">`;
            div.onclick = () => openImage(url);
          }

          // VIDEO
          else if (["mp4", "mov", "webm", "mkv"].includes(ext)) {
            div.innerHTML = `
        <video src="${url}" muted></video>
      `;
            div.onclick = () => openVideo(url);
          }

          // AUDIO
          else if (["mp3", "wav", "ogg", "m4a"].includes(ext)) {
            div.innerHTML = `
        <div style="padding:20px; text-align:center;">
          🎵 ${name}
        </div>`;
            div.onclick = () => openAudio(url);
          }

          grid.appendChild(div);
        });
      }

      function openImage(url) {
        viewer.style.display = "flex";
        viewerContent.innerHTML = `<img src="${url}" style="max-width:100%; max-height:100%;">`;
      }

      function openVideo(url) {
        viewer.style.display = "flex";
        viewerContent.innerHTML = `<video src="${url}" controls autoplay style="max-width:100%; max-height:100%;"></video>`;
      }

      function openAudio(url) {
        viewer.style.display = "flex";
        viewerContent.innerHTML = `<audio src="${url}" controls autoplay></audio>`;
      }

      function closeViewer() {
        viewer.style.display = "none";
        viewerContent.innerHTML = "";
      }

      loadFiles();
    </script>
  </body>
</html>
```





## ✨ Résultat

Tu obtiens un portfolio automatique :

- ✔ Affiche tous les fichiers de `~/Downloads`
- ✔ Zoom au survol
- ✔ Vidéos → miniature automatique + lecture dans le viewer
- ✔ Images → zoom en plein écran au clic
- ✔ Audio → lecteur audio dans la popup
- ✔ Re-clic = ferme + stop media

## 🎁 Bonus possible

Je peux ajouter :

- ✔ tri par date / taille / type
- ✔ panneau latéral
- ✔ mode sombre
- ✔ favicon emoji dynamique
- ✔ drag & drop
- ✔ filtrage (images / videos / audio)
- ✔ lecteur vidéo avec timeline custom
- ✔ mise en cache côté serveur

Si tu veux un design plus pro, dis « oui ».


```bash
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>📁 Portfolio – Downloads</title>

  <!-- Favicon emoji dynamique -->
  <link id="favicon" rel="icon"
        href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">📁</text></svg>'>

  <style>
    :root {
      --bg: #f5f5f5;
      --text: #111;
      --card-bg: #ffffff;
      --shadow: rgba(0, 0, 0, 0.1);
      --accent: #3b82f6;
    }

    body.dark {
      --bg: #111827;
      --text: #f9fafb;
      --card-bg: #1f2937;
      --shadow: rgba(0, 0, 0, 0.6);
      --accent: #60a5fa;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .layout {
      display: grid;
      grid-template-columns: 260px 1fr;
      min-height: 100vh;
    }

    .sidebar {
      padding: 20px;
      border-right: 1px solid rgba(0,0,0,0.1);
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(10px);
    }

    .sidebar h2 {
      margin-top: 0;
      font-size: 1.2rem;
    }

    .main {
      padding: 20px;
    }

    h1 {
      margin-top: 0;
      margin-bottom: 20px;
      font-size: 1.8rem;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 20px;
    }

    .item {
      position: relative;
      cursor: pointer;
      overflow: hidden;
      border-radius: 16px;
      background: var(--card-bg);
      box-shadow: 0 4px 12px var(--shadow);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .item:hover {
      transform: scale(1.05);
      box-shadow: 0 8px 20px var(--shadow);
    }

    .item img,
    .item video {
      width: 100%;
      height: 160px;
      object-fit: cover;
      display: block;
    }

    .item-label {
      padding: 8px 12px;
      font-size: 0.8rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .badge {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(0,0,0,0.6);
      color: white;
      padding: 2px 6px;
      border-radius: 999px;
      font-size: 0.75rem;
    }

    /* Viewer plein écran */
    #viewer {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.8);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }

    #viewerContent {
      max-width: 90vw;
      max-height: 90vh;
      background: #000;
      border-radius: 16px;
      padding: 10px;
      box-sizing: border-box;
    }

    #viewerContent img,
    #viewerContent video {
      max-width: 100%;
      max-height: 70vh;
      display: block;
      margin: 0 auto;
    }

    .viewer-controls {
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
      color: #f9fafb;
      font-size: 0.9rem;
    }

    .viewer-controls button {
      padding: 4px 10px;
      border: none;
      border-radius: 999px;
      background: var(--accent);
      color: white;
      cursor: pointer;
      font-size: 0.85rem;
    }

    .viewer-controls button:hover {
      opacity: 0.9;
    }

    .viewer-progress {
      flex: 1;
    }

    .viewer-progress input[type="range"] {
      width: 100%;
    }

    /* Sidebar controls */
    .control-group {
      margin-bottom: 20px;
    }

    .control-group label {
      display: block;
      margin-bottom: 5px;
      font-size: 0.85rem;
      opacity: 0.8;
    }

    select, button.toggle {
      width: 100%;
      padding: 6px 8px;
      border-radius: 999px;
      border: 1px solid rgba(0,0,0,0.1);
      background: var(--card-bg);
      color: var(--text);
      cursor: pointer;
      font-size: 0.9rem;
    }

    button.toggle {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .filter-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .chip {
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 0.8rem;
      border: 1px solid rgba(0,0,0,0.1);
      background: var(--card-bg);
      cursor: pointer;
      opacity: 0.85;
    }

    .chip.active {
      background: var(--accent);
      color: white;
      opacity: 1;
    }

    /* Dropzone */
    #dropZone {
      border: 2px dashed rgba(0,0,0,0.3);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      font-size: 0.85rem;
      opacity: 0.8;
    }

    #dropZone.dragover {
      border-color: var(--accent);
      background: rgba(59, 130, 246, 0.1);
      opacity: 1;
    }

    .small {
      font-size: 0.75rem;
      opacity: 0.7;
      margin-top: 6px;
    }

    .sort-row {
      display: flex;
      gap: 8px;
      margin-top: 6px;
    }

    .sort-row button {
      flex: 1;
      padding: 4px 6px;
      border-radius: 999px;
      border: 1px solid rgba(0,0,0,0.1);
      background: var(--card-bg);
      cursor: pointer;
      font-size: 0.8rem;
    }

    .sort-row button.active {
      background: var(--accent);
      color: white;
    }
  </style>
</head>
<body>

<div class="layout">
  <aside class="sidebar">
    <h2>⚙️ Options</h2>

    <div class="control-group">
      <label>Mode</label>
      <button id="themeToggle" class="toggle">🌞 / 🌙</button>
    </div>

    <div class="control-group">
      <label>Tri</label>
      <select id="sortSelect">
        <option value="name">Nom</option>
        <option value="date">Date</option>
        <option value="size">Taille</option>
        <option value="type">Type</option>
      </select>
      <div class="sort-row">
        <button id="orderAsc" class="active">⬆️ Asc</button>
        <button id="orderDesc">⬇️ Desc</button>
      </div>
    </div>

    <div class="control-group">
      <label>Filtre</label>
      <div class="filter-row">
        <div class="chip active" data-filter="all">Tout</div>
        <div class="chip" data-filter="image">Images</div>
        <div class="chip" data-filter="video">Vidéos</div>
        <div class="chip" data-filter="audio">Audio</div>
        <div class="chip" data-filter="other">Autres</div>
      </div>
    </div>

    <div class="control-group">
      <label>Drag & drop</label>
      <div id="dropZone">
        Dépose des fichiers ici<br>
        <span class="small">(ils seront copiés dans ton dossier Downloads)</span>
      </div>
    </div>
  </aside>

  <main class="main">
    <h1>📁 Portfolio – Downloads</h1>
    <div class="grid" id="grid"></div>
  </main>
</div>

<!-- Viewer plein écran -->
<div id="viewer">
  <div id="viewerContent"></div>
</div>

<script>
  // ---------- FAVICON EMOJI ----------
  const faviconEl = document.getElementById("favicon");

  function emojiToFavicon(emoji) {
    return `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">${emoji}</text></svg>`;
  }

  function setFaviconForType(type) {
    let emoji = "📁";
    if (!type) emoji = "📁";
    else if (type === "image") emoji = "🖼️";
    else if (type === "video") emoji = "🎬";
    else if (type === "audio") emoji = "🎵";
    else emoji = "📄";
    faviconEl.href = emojiToFavicon(emoji);
  }

  // ---------- THEME ----------
  const body = document.body;
  const themeToggle = document.getElementById("themeToggle");

  function applyStoredTheme() {
    const stored = localStorage.getItem("theme") || "light";
    if (stored === "dark") {
      body.classList.add("dark");
    } else {
      body.classList.remove("dark");
    }
  }

  themeToggle.addEventListener("click", () => {
    body.classList.toggle("dark");
    localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
  });

  applyStoredTheme();

  // ---------- DATA & STATE ----------
  let allFiles = [];
  let filterType = "all";
  let sortKey = "name";
  let sortOrder = "asc";
  let currentOpen = null; // nom du fichier actuellement ouvert dans viewer
  let currentOpenType = null;

  const grid = document.getElementById("grid");
  const viewer = document.getElementById("viewer");
  const viewerContent = document.getElementById("viewerContent");

  // ---------- FETCH FILES ----------
  async function loadFiles() {
    const res = await fetch("/list");
    allFiles = await res.json();
    renderGrid();
  }

  // ---------- TRI & FILTRE ----------
  function getFilteredSortedFiles() {
    let files = [...allFiles];

    if (filterType !== "all") {
      files = files.filter(f => f.type === filterType);
    }

    files.sort((a, b) => {
      let va, vb;
      switch (sortKey) {
        case "date":
          va = a.mtime;
          vb = b.mtime;
          break;
        case "size":
          va = a.size;
          vb = b.size;
          break;
        case "type":
          va = a.type;
          vb = b.type;
          break;
        default:
          va = a.name.toLowerCase();
          vb = b.name.toLowerCase();
      }

      if (va < vb) return sortOrder === "asc" ? -1 : 1;
      if (va > vb) return sortOrder === "asc" ? 1 : -1;
      return 0;
    });

    return files;
  }

  // ---------- RENDER GRID ----------
  function renderGrid() {
    grid.innerHTML = "";
    const files = getFilteredSortedFiles();

    files.forEach(file => {
      const url = "/file/" + encodeURIComponent(file.name);
      const div = document.createElement("div");
      div.className = "item";
      div.dataset.name = file.name;
      div.dataset.type = file.type;

      let content = "";
      let badge = "";

      if (file.type === "image") {
        badge = "IMG";
        content = `<img src="${url}" alt="">`;
      } else if (file.type === "video") {
        badge = "VID";
        // on compte sur preload pour afficher la première image
        content = `<video src="${url}" muted preload="metadata" ></video>`;
      } else if (file.type === "audio") {
        badge = "AUD";
        content = `
          <div style="height:160px;display:flex;align-items:center;justify-content:center;font-size:2rem;">
            🎵
          </div>`;
      } else {
        badge = "FILE";
        content = `
          <div style="height:160px;display:flex;align-items:center;justify-content:center;font-size:2rem;">
            📄
          </div>`;
      }

      div.innerHTML = `
        <span class="badge">${badge}</span>
        ${content}
        <div class="item-label">${file.name}</div>
      `;

      // Hover vidéo -> play / stop
      if (file.type === "video") {
        const vid = div.querySelector("video");
        div.addEventListener("mouseenter", () => {
          vid.currentTime = 0;
          vid.play().catch(() => {});
        });
        div.addEventListener("mouseleave", () => {
          vid.pause();
        });
      }

      // Clic -> toggle viewer
      div.addEventListener("click", () => {
        if (currentOpen === file.name) {
          closeViewer();
        } else {
          openViewer(file);
        }
      });

      grid.appendChild(div);
    });
  }

  // ---------- VIEWER ----------
  function closeViewer() {
    viewer.style.display = "none";
    viewerContent.innerHTML = "";
    currentOpen = null;
    currentOpenType = null;
    setFaviconForType(null);
  }

  viewer.addEventListener("click", (e) => {
    if (e.target === viewer) {
      closeViewer();
    }
  });

  viewerContent.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  function openViewer(file) {
    const url = "/file/" + encodeURIComponent(file.name);
    currentOpen = file.name;
    currentOpenType = file.type;

    setFaviconForType(file.type);

    viewer.style.display = "flex";

    if (file.type === "image") {
      viewerContent.innerHTML = `<img src="${url}" alt="">`;
    } else if (file.type === "video") {
      viewerContent.innerHTML = `
        <video id="viewerVideo" src="${url}" style="max-width:100%;max-height:70vh;" controls hidden ></video>
        <div class="viewer-controls">
          <button id="playPauseBtn">▶️</button>
          <div class="viewer-progress">
            <input id="videoRange" type="range" min="0" max="100" step="0.1" value="0">
          </div>
          <div id="timeLabel">00:00 / 00:00</div>
        </div>
      `;
      setupVideoControls();
    } else if (file.type === "audio") {
      viewerContent.innerHTML = `
        <audio src="${url}" controls autoplay style="width:100%;" controls hidden></audio>
      `;
    } else {
      viewerContent.innerHTML = `
        <div style="padding:20px;color:white;max-width:60vw;">
          <h2>📄 ${file.name}</h2>
          <p>Type non prévisualisé. (taille : ${(file.size/1024).toFixed(1)} Ko)</p>
        </div>
      `;
    }
  }

  function setupVideoControls() {
    const video = document.getElementById("viewerVideo");
    const range = document.getElementById("videoRange");
    const playPauseBtn = document.getElementById("playPauseBtn");
    const timeLabel = document.getElementById("timeLabel");

    function formatTime(t) {
      const m = Math.floor(t / 60).toString().padStart(2, "0");
      const s = Math.floor(t % 60).toString().padStart(2, "0");
      return `${m}:${s}`;
    }

    video.addEventListener("loadedmetadata", () => {
      timeLabel.textContent = `00:00 / ${formatTime(video.duration)}`;
    });

    video.addEventListener("timeupdate", () => {
      if (video.duration) {
        const percent = (video.currentTime / video.duration) * 100;
        range.value = percent;
        timeLabel.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
      }
    });

    range.addEventListener("input", () => {
      if (video.duration) {
        video.currentTime = video.duration * (range.value / 100);
      }
    });

    playPauseBtn.addEventListener("click", () => {
      if (video.paused) {
        video.play();
        playPauseBtn.textContent = "⏸️";
      } else {
        video.pause();
        playPauseBtn.textContent = "▶️";
      }
    });

    video.play().then(() => {
      playPauseBtn.textContent = "⏸️";
    }).catch(() => {
      playPauseBtn.textContent = "▶️";
    });
  }

  // ---------- FILTRES UI ----------
  const chips = document.querySelectorAll(".chip");
  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      filterType = chip.dataset.filter;
      renderGrid();
    });
  });

  const sortSelect = document.getElementById("sortSelect");
  const orderAsc = document.getElementById("orderAsc");
  const orderDesc = document.getElementById("orderDesc");

  sortSelect.addEventListener("change", () => {
    sortKey = sortSelect.value;
    renderGrid();
  });

  orderAsc.addEventListener("click", () => {
    sortOrder = "asc";
    orderAsc.classList.add("active");
    orderDesc.classList.remove("active");
    renderGrid();
  });

  orderDesc.addEventListener("click", () => {
    sortOrder = "desc";
    orderAsc.classList.remove("active");
    orderDesc.classList.add("active");
    renderGrid();
  });

  // ---------- DRAG & DROP UPLOAD ----------
  const dropZone = document.getElementById("dropZone");

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    document.addEventListener(eventName, preventDefaults, false);
  });

  ["dragenter", "dragover"].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add("dragover"), false);
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove("dragover"), false);
  });

  dropZone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (!files || files.length === 0) return;

    [...files].forEach(uploadFile);
  });

  async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    await fetch("/upload", {
      method: "POST",
      body: formData
    });

    // recharge la liste après upload
    await loadFiles();
  }

  // ---------- INIT ----------
  loadFiles();
</script>

</body>
</html>
        

```

#### Résumé de ce que ça fait ✅

- Liste automatique de `./Downloads`

- Tri : nom / date / taille / type (avec asc / desc)

- Filtre : tout / images / vidéos / audio / autres

- Zoom au survol sur chaque vignette

- Vidéo :

    - préview (lecture muette au survol dans la grille)

    - clic → viewer plein écran avec **timeline custom**

- Image : clic → plein écran

- Audio : clic → lecteur audio

- Re-clic sur la même carte → ferme le viewer

- Mode sombre 🌙 / clair 🌞

- Drag & drop → upload dans Downloads

- Cache serveur (scan toutes les 5 s max)

- Favicon emoji qui change selon type (📁 / 🖼️ / 🎬 / 🎵 / 📄)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>🎬 Portfolio Local</title>

<!-- Favicon emoji dynamique -->
<link id="favicon" rel="icon"
      href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"><text y="0.9em" font-size="90">🎬</text></svg>'>

<style>
  body {
    margin: 0;
    font-family: sans-serif;
    background: #111;
    color: white;
  }

  header {
    padding: 15px;
    background: #222;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  #grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 15px;
    padding: 20px;
  }

  .item {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transform: scale(1);
    transition: transform .2s;
    background: #000;
  }

  .item:hover {
    transform: scale(1.05);
    z-index: 10;
  }

  .item img, .item video {
    width: 100%;
    height: 160px;
    object-fit: cover;
  }

  .filename {
    padding: 8px;
    font-size: 14px;
    background: rgba(0,0,0,0.6);
  }

  video.player, img.player, audio.player {
    max-width: 95%;
    max-height: 95%;
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    z-index: 999999;
    background: #000;
    border-radius: 10px;
  }

  #overlay {
    display: none;
    position: fixed;
    top:0; left:0; width:100%; height:100%;
    background: rgba(0,0,0,0.8);
    z-index:999998;
  }
</style>
</head>

<body>

<header>
  <button onclick="pickFolder()">📁 Choisir dossier</button>
  <select id="sort" onchange="sortFiles()">
    <option value="name">Nom</option>
    <option value="date">Date</option>
    <option value="size">Taille</option>
    <option value="type">Type</option>
  </select>
</header>

<div id="grid"></div>
<div id="overlay" onclick="closePlayer()"></div>

<script>
let folderHandle = null;
let files = [];

/* ---------------------- Pick folder ---------------------- */
async function pickFolder() {
  try {
    folderHandle = await window.showDirectoryPicker();
    loadFolder();
  } catch(e) { console.log(e); }
}

/* ---------------------- Load default ./Downloads ---------------------- */
(async function autoLoadDownloads() {
  try {
    folderHandle = await navigator.storage.getDirectory();
  } catch(e) {}
})();

/* ---------------------- Load folder ---------------------- */
async function loadFolder() {
  files = [];

  for await (const [name, handle] of folderHandle.entries()) {
    if (handle.kind !== "file") continue;
    if (name.startsWith(".")) continue;
    if (name.startsWith("._")) continue;

    const fileData = await handle.getFile();

    files.push({
      name,
      size: fileData.size,
      date: fileData.lastModified,
      type: fileData.type,
      file: fileData
    });
  }

  render();
}

/* ---------------------- Sort ---------------------- */
function sortFiles() {
  const mode = document.getElementById("sort").value;

  files.sort((a,b)=>{
    if (mode === "name") return a.name.localeCompare(b.name);
    if (mode === "date") return b.date - a.date;
    if (mode === "size") return b.size - a.size;
    if (mode === "type") return a.type.localeCompare(b.type);
  });

  render();
}

/* ---------------------- Render thumbnails ---------------------- */
async function render() {
  const grid = document.getElementById("grid");
  grid.innerHTML = "";

  for (const f of files) {
    const item = document.createElement("div");
    item.className = "item";

    const url = URL.createObjectURL(f.file);

    if (f.type.startsWith("image")) {
      item.innerHTML = `<img src="${url}"><div class='filename'>${f.name}</div>`;
      item.onclick = () => openImage(url);
    }
    else if (f.type.startsWith("video")) {
      const thumb = await extractFrame(url);
      item.innerHTML = `<img src="${thumb}"><div class='filename'>${f.name}</div>`;
      item.onclick = () => openVideo(url);
    }
    else if (f.type.startsWith("audio")) {
      item.innerHTML = `<img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg'><text y='0.9em' font-size='90'>🎵</text></svg>"><div class='filename'>${f.name}</div>`;
      item.onclick = () => openAudio(url);
    }

    grid.appendChild(item);
  }
}

/* ---------------------- Extract first frame ---------------------- */
function extractFrame(url) {
  return new Promise((resolve) => {
    const video = document.createElement("video");
    video.src = url;
    video.muted = true;
    video.currentTime = 0;

    video.addEventListener("loadeddata", () => {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video,0,0);
      resolve(canvas.toDataURL());
    });
  });
}

/* ---------------------- Player ---------------------- */
function openVideo(url) {
  closePlayer();
  const v = document.createElement("video");
  v.src = url;
  v.className = "player";
  v.controls = true;
  v.autoplay = true;

  v.ondblclick = () => v.requestFullscreen();

  document.body.appendChild(v);
  document.getElementById("overlay").style.display = "block";
}

function openImage(url) {
  closePlayer();
  const img = document.createElement("img");
  img.src = url;
  img.className = "player";
  document.body.appendChild(img);

  document.getElementById("overlay").style.display = "block";
}

function openAudio(url) {
  closePlayer();
  const a = document.createElement("audio");
  a.src = url;
  a.className = "player";
  a.controls = true;
  a.autoplay = true;

  document.body.appendChild(a);
  document.getElementById("overlay").style.display = "block";
}

function closePlayer() {
  document.querySelectorAll(".player").forEach(e => e.remove());
  document.getElementById("overlay").style.display = "none";
}
</script>

</body>
</html>
```

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>📁 Portfolio – Downloads</title>
<style>
body {
  font-family: system-ui; margin:0; background:#f5f5f5; color:#111;
}
.layout {display:grid; grid-template-columns:260px 1fr; min-height:100vh;}
.sidebar {padding:20px; border-right:1px solid rgba(0,0,0,0.1);}
.main {padding:20px;}
.grid {display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:20px;}
.item {position:relative; cursor:pointer; overflow:hidden; border-radius:12px; background:#fff; box-shadow:0 4px 12px rgba(0,0,0,0.1); transition:0.2s;}
.item:hover {transform:scale(1.05); box-shadow:0 8px 20px rgba(0,0,0,0.2);}
.item img, .item video {width:100%; height:160px; object-fit:cover; display:block;}
.item-label {padding:6px 10px; font-size:0.8rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.badge {position:absolute; top:8px; left:8px; background:rgba(0,0,0,0.6); color:white; padding:2px 6px; border-radius:999px; font-size:0.75rem;}
#viewer {position:fixed; inset:0; background:rgba(0,0,0,0.8); display:none; align-items:center; justify-content:center; z-index:1000;}
#viewerContent {max-width:90vw; max-height:90vh; background:#000; border-radius:12px; padding:10px; box-sizing:border-box;}
#viewerContent video, #viewerContent img {max-width:100%; max-height:80vh;}
</style>
</head>
<body>

<div class="layout">
  <aside class="sidebar">
    <h2>⚙️ Options</h2>
    <div>
      <label>Choisir répertoire</label>
      <input type="file" id="dirPicker" webkitdirectory directory multiple>
    </div>
  </aside>
  <main class="main">
    <h1>📁 Portfolio – Downloads</h1>
    <div class="grid" id="grid"></div>
  </main>
</div>

<div id="viewer">
  <div id="viewerContent"></div>
</div>

<script>
const grid = document.getElementById("grid");
const viewer = document.getElementById("viewer");
const viewerContent = document.getElementById("viewerContent");
let allFiles = [];

// ---------- CHOIX REPERTOIRE ----------
const dirPicker = document.getElementById("dirPicker");
dirPicker.addEventListener("change", e=>{
  allFiles = [];
  for(let f of e.target.files){
    if(f.name.startsWith(".") || f.name.startsWith("._")) continue; // ignore
    let type = "other";
    if(f.type.startsWith("image")) type="image";
    else if(f.type.startsWith("video")) type="video";
    else if(f.type.startsWith("audio")) type="audio";
    allFiles.push({name:f.name, url:URL.createObjectURL(f), type:type, file:f});
  }
  renderGrid();
});

// ---------- RENDER GRID ----------
function renderGrid(){
  grid.innerHTML="";
  allFiles.forEach(f=>{
    const div = document.createElement("div");
    div.className="item";
    div.innerHTML = `
      <span class="badge">${f.type.toUpperCase()}</span>
      ${(f.type==="image"?`<img src="${f.url}">`:
        f.type==="video"?`<video src="${f.url}" muted preload="metadata"></video>`:
        `<div style="height:160px;display:flex;align-items:center;justify-content:center;font-size:2rem;">📄</div>`)}
      <div class="item-label">${f.name}</div>
    `;
    if(f.type==="video"){
      const vid = div.querySelector("video");
      div.addEventListener("mouseenter",()=>vid.play().catch(()=>{}));
      div.addEventListener("mouseleave",()=>vid.pause());
    }
    div.addEventListener("click",()=>openViewer(f));
    grid.appendChild(div);
  });
}

// ---------- VIEWER ----------
function openViewer(f){
  viewer.style.display="flex";
  viewerContent.innerHTML="";
  if(f.type==="image"){
    viewerContent.innerHTML = `<img src="${f.url}">`;
  } else if(f.type==="video"){
    viewerContent.innerHTML = `<video src="${f.url}" controls autoplay style="max-width:100%;max-height:80vh;"></video>`;
  } else if(f.type==="audio"){
    viewerContent.innerHTML = `<audio src="${f.url}" controls autoplay style="width:100%;"></audio>`;
  } else {
    viewerContent.innerHTML = `<div style="padding:20px;color:white;">📄 ${f.name}</div>`;
  }
}
viewer.addEventListener("click", e=>{
  if(e.target===viewer) viewer.style.display="none";
});
viewerContent.addEventListener("click", e=>e.stopPropagation());
</script>

</body>
</html>

```



### ✅ Nouvelles fonctionnalités ajoutées

- ✔ Choisir un répertoire (API File System Access)
- ✔ `./Downloads` utilisé **par défaut**
- ✔ Ignorer les fichiers `.`, `..`, `._xxx`, fichiers cachés
- ✔ Chaque miniature :
-  **• image → zoom au survol / clique = afficher**
-  **• vidéo → affiche la première frame, clique = play / pause**
-  **• audio → clique = play / pause**
- ✔ Double-clic = plein écran (pour vidéo)
- ✔ Tri (date / taille / type)
- ✔ Mode sombre
- ✔ Favicon 🤩
- ✔ Drag & drop
- ✔ Aucun serveur nécessaire → 100% local

### ⚠️ Important pour macOS

- Safari ne supporte pas encore l’API File System Access → utiliser **Chrome** (tu l’utilises déjà).
- Pour accéder à un dossier : Chrome va demander l’autorisation (normal et sécurisé).

### 🎁 CODE FINAL — Portfolio Média Local 2025

➡️ COLLE DIRECTEMENT CE FICHIER DANS UN `index.html`
(et ouvre-le simplement dans Chrome)

> ⚠️ comme c’est long, je mets **tout le code propre et complet**.
Tu peux demander une version découpée si tu veux.

### ✔️ Fonctionnalités obtenues
- Choix dossier via bouton 📁
- Dossier par défaut = **Downloads** si autorisé
- **ignore** fichiers :
    - `.`
    - `..`
    - `.hidden`
    - `._AppleDouble`

- Thumbnails :
    - image → affichage direct
    - vidéo → première frame auto
    - audio → icône 🎵
- Survol → **zoom**
- Clic → **ouvrir** (image/vidéo/audio)
- Vidéo → **play / pause, plein écran double-clic**
- Audio → play / pause
- Overlay pour fermer
- Tri complet
- Dark mode natif
- Drag & drop déjà activable si tu veux (je peux l’ajouter)

👉 **Tu veux ajouter quoi maintenant ?**

Je peux te faire :

- ⭐ Drag & Drop complet
- ⭐ Un mode grille + mode liste
- ⭐ Prévisualisation GIF animée
- ⭐ Recherche instantanée
- ⭐ Filtres (images seulement / vidéos seulement / audio seulement)
- ⭐ Un cache local ultra rapide (IndexedDB)
- ⭐ Un mode serveur Node.js si tu veux un accès à n’importe quel dossier sans autorisation

Dis-moi !


---

## Dernier vertion 

```python 
from flask import Flask, jsonify, send_file, request, send_from_directory
import os
import time

app = Flask(__name__)

# -------------------- CONFIG --------------------
DEFAULT_DIR = os.path.expanduser("./Downloads")
DOWNLOADS_DIR = DEFAULT_DIR  # dossier actif
CACHE_TTL = 5  # secondes

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
AUDIO_EXT = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

FILE_CACHE = {"data": None, "mtime": 0}  # cache simple

# -------------------- UTILITAIRES --------------------
def detect_type(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"

def scan_files():
    """Scanne le dossier actif et met en cache le résultat."""
    now = time.time()
    if FILE_CACHE["data"] is not None and now - FILE_CACHE["mtime"] < CACHE_TTL:
        return FILE_CACHE["data"]

    files = []
    for f in os.listdir(DOWNLOADS_DIR):
        if f.startswith(".") or f.startswith("._"):
            continue
        path = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(path):
            stat = os.stat(path)
            files.append({
                "name": f,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "type": detect_type(f)
            })

    FILE_CACHE["data"] = files
    FILE_CACHE["mtime"] = now
    return files

# -------------------- ROUTES --------------------
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/list")
def list_files():
    return jsonify(scan_files())

@app.route("/file/<path:name>")
def serve_file(name):
    path = os.path.join(DOWNLOADS_DIR, name)
    if not os.path.isfile(path):
        return "Not found", 404
    return send_file(path)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file", 400

    f = request.files["file"]
    if f.filename == "":
        return "No filename", 400

    if f.filename.startswith(".") or f.filename.startswith("._"):
        return "Invalid filename", 400

    dest = os.path.join(DOWNLOADS_DIR, f.filename)
    f.save(dest)

    FILE_CACHE["data"] = None  # invalide le cache
    return "OK", 200

@app.route("/setdir", methods=["POST"])
def set_directory():
    """Changer le dossier actif."""
    global DOWNLOADS_DIR
    data = request.get_json()
    path = data.get("path", DEFAULT_DIR)

    if not os.path.isdir(path):
        return jsonify({"error": "Chemin invalide"}), 400

    DOWNLOADS_DIR = os.path.abspath(path)
    FILE_CACHE["data"] = None  # invalide le cache
    return jsonify({"success": True, "path": DOWNLOADS_DIR})

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


```

```bash 
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>📁 Portfolio – Downloads</title>

  <!-- Favicon emoji dynamique -->
  <link id="favicon" rel="icon"
        href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">📁</text></svg>'>

  <style>
    :root {
      --bg: #f5f5f5;
      --text: #111;
      --card-bg: #ffffff;
      --shadow: rgba(0, 0, 0, 0.1);
      --accent: #3b82f6;
    }

    body.dark {
      --bg: #111827;
      --text: #f9fafb;
      --card-bg: #1f2937;
      --shadow: rgba(0, 0, 0, 0.6);
      --accent: #60a5fa;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .layout {
      display: grid;
      grid-template-columns: 260px 1fr;
      min-height: 100vh;
    }

    .sidebar {
      padding: 20px;
      border-right: 1px solid rgba(0,0,0,0.1);
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(10px);
    }

    .sidebar h2 {
      margin-top: 0;
      font-size: 1.2rem;
    }

    .main {
      padding: 20px;
    }

    h1 {
      margin-top: 0;
      margin-bottom: 20px;
      font-size: 1.8rem;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 20px;
    }

    .item {
      position: relative;
      cursor: pointer;
      overflow: hidden;
      border-radius: 16px;
      background: var(--card-bg);
      box-shadow: 0 4px 12px var(--shadow);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .item:hover {
      transform: scale(1.05);
      box-shadow: 0 8px 20px var(--shadow);
    }

    .item img,
    .item video {
      width: 100%;
      height: 160px;
      object-fit: cover;
      display: block;
    }

    .item-label {
      padding: 8px 12px;
      font-size: 0.8rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .badge {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(0,0,0,0.6);
      color: white;
      padding: 2px 6px;
      border-radius: 999px;
      font-size: 0.75rem;
    }

    /* Viewer plein écran */
    #viewer {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.8);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }

    #viewerContent {
      max-width: 90vw;
      max-height: 90vh;
      background: #000;
      border-radius: 16px;
      padding: 10px;
      box-sizing: border-box;
    }

    #viewerContent img,
    #viewerContent video {
      max-width: 100%;
      max-height: 70vh;
      display: block;
      margin: 0 auto;
    }

    .viewer-controls {
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
      color: #f9fafb;
      font-size: 0.9rem;
    }

    .viewer-controls button {
      padding: 4px 10px;
      border: none;
      border-radius: 999px;
      background: var(--accent);
      color: white;
      cursor: pointer;
      font-size: 0.85rem;
    }

    .viewer-controls button:hover {
      opacity: 0.9;
    }

    .viewer-progress {
      flex: 1;
    }

    .viewer-progress input[type="range"] {
      width: 100%;
    }

    /* Sidebar controls */
    .control-group {
      margin-bottom: 20px;
    }

    .control-group label {
      display: block;
      margin-bottom: 5px;
      font-size: 0.85rem;
      opacity: 0.8;
    }

    select, button.toggle {
      width: 100%;
      padding: 6px 8px;
      border-radius: 999px;
      border: 1px solid rgba(0,0,0,0.1);
      background: var(--card-bg);
      color: var(--text);
      cursor: pointer;
      font-size: 0.9rem;
    }

    button.toggle {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .filter-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .chip {
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 0.8rem;
      border: 1px solid rgba(0,0,0,0.1);
      background: var(--card-bg);
      cursor: pointer;
      opacity: 0.85;
    }

    .chip.active {
      background: var(--accent);
      color: white;
      opacity: 1;
    }

    /* Dropzone */
    #dropZone {
      border: 2px dashed rgba(0,0,0,0.3);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      font-size: 0.85rem;
      opacity: 0.8;
    }

    #dropZone.dragover {
      border-color: var(--accent);
      background: rgba(59, 130, 246, 0.1);
      opacity: 1;
    }

    .small {
      font-size: 0.75rem;
      opacity: 0.7;
      margin-top: 6px;
    }

    .sort-row {
      display: flex;
      gap: 8px;
      margin-top: 6px;
    }

    .sort-row button {
      flex: 1;
      padding: 4px 6px;
      border-radius: 999px;
      border: 1px solid rgba(0,0,0,0.1);
      background: var(--card-bg);
      cursor: pointer;
      font-size: 0.8rem;
    }

    .sort-row button.active {
      background: var(--accent);
      color: white;
    }
  </style>
</head>
<body>

<div class="layout">
  <aside class="sidebar">
    <div class="control-group">
  <label>Choisir un dossier</label>
  <input type="file" id="dirPicker" webkitdirectory directory multiple style="width:100%;">
  <div class="small" id="dirStatus"></div>
</div>
    <h2>⚙️ Options</h2>

    <div class="control-group">
      <label>Mode</label>
      <button id="themeToggle" class="toggle">🌞 / 🌙</button>
    </div>

    <div class="control-group">
      <label>Tri</label>
      <select id="sortSelect">
        <option value="name">Nom</option>
        <option value="date">Date</option>
        <option value="size">Taille</option>
        <option value="type">Type</option>
      </select>
      <div class="sort-row">
        <button id="orderAsc" class="active">⬆️ Asc</button>
        <button id="orderDesc">⬇️ Desc</button>
      </div>
    </div>

    <div class="control-group">
      <label>Filtre</label>
      <div class="filter-row">
        <div class="chip active" data-filter="all">Tout</div>
        <div class="chip" data-filter="image">Images</div>
        <div class="chip" data-filter="video">Vidéos</div>
        <div class="chip" data-filter="audio">Audio</div>
        <div class="chip" data-filter="other">Autres</div>
      </div>
    </div>

    <div class="control-group">
      <label>Drag & drop</label>
      <div id="dropZone">
        Dépose des fichiers ici<br>
        <span class="small">(ils seront copiés dans ton dossier Downloads)</span>
      </div>
    </div>
  </aside>

  <main class="main">
    <h1>📁 Portfolio – Downloads</h1>
    <div class="grid" id="grid"></div>
  </main>
</div>

<!-- Viewer plein écran -->
<div id="viewer">
  <div id="viewerContent"></div>
</div>

<script>
  const dirPicker = document.getElementById("dirPicker");
const dirStatus = document.getElementById("dirStatus");

dirPicker.addEventListener("change", async (e) => {
  const files = [...e.target.files];
  if (!files.length) return;

  // On envoie seulement le chemin parent au serveur (pour changer le dossier)
  const path = files[0].webkitRelativePath.split("/")[0];

  const res = await fetch("/setdir", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path })
  });

  const data = await res.json();
  if (res.ok) {
    dirStatus.textContent = `✅ Dossier choisi : ${data.path}`;
    dirStatus.style.color = "green";
    await loadFiles(); // recharge la liste avec le nouveau dossier
  } else {
    dirStatus.textContent = `❌ Erreur : ${data.error}`;
    dirStatus.style.color = "red";
  }
});
</script>

<script>
  // ---------- FAVICON EMOJI ----------
  const faviconEl = document.getElementById("favicon");

  function emojiToFavicon(emoji) {
    return `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">${emoji}</text></svg>`;
  }

  function setFaviconForType(type) {
    let emoji = "📁";
    if (!type) emoji = "📁";
    else if (type === "image") emoji = "🖼️";
    else if (type === "video") emoji = "🎬";
    else if (type === "audio") emoji = "🎵";
    else emoji = "📄";
    faviconEl.href = emojiToFavicon(emoji);
  }

  // ---------- THEME ----------
  const body = document.body;
  const themeToggle = document.getElementById("themeToggle");

  function applyStoredTheme() {
    const stored = localStorage.getItem("theme") || "light";
    if (stored === "dark") {
      body.classList.add("dark");
    } else {
      body.classList.remove("dark");
    }
  }

  themeToggle.addEventListener("click", () => {
    body.classList.toggle("dark");
    localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
  });

  applyStoredTheme();

  // ---------- DATA & STATE ----------
  let allFiles = [];
  let filterType = "all";
  let sortKey = "name";
  let sortOrder = "asc";
  let currentOpen = null; // nom du fichier actuellement ouvert dans viewer
  let currentOpenType = null;

  const grid = document.getElementById("grid");
  const viewer = document.getElementById("viewer");
  const viewerContent = document.getElementById("viewerContent");

  // ---------- FETCH FILES ----------
  async function loadFiles() {
    const res = await fetch("/list");
    allFiles = await res.json();
    renderGrid();
  }

  // ---------- TRI & FILTRE ----------
  function getFilteredSortedFiles() {
    let files = [...allFiles];

    if (filterType !== "all") {
      files = files.filter(f => f.type === filterType);
    }

    files.sort((a, b) => {
      let va, vb;
      switch (sortKey) {
        case "date":
          va = a.mtime;
          vb = b.mtime;
          break;
        case "size":
          va = a.size;
          vb = b.size;
          break;
        case "type":
          va = a.type;
          vb = b.type;
          break;
        default:
          va = a.name.toLowerCase();
          vb = b.name.toLowerCase();
      }

      if (va < vb) return sortOrder === "asc" ? -1 : 1;
      if (va > vb) return sortOrder === "asc" ? 1 : -1;
      return 0;
    });

    return files;
  }

  // ---------- RENDER GRID ----------
  function renderGrid() {
    grid.innerHTML = "";
    const files = getFilteredSortedFiles();

    files.forEach(file => {
      const url = "/file/" + encodeURIComponent(file.name);
      const div = document.createElement("div");
      div.className = "item";
      div.dataset.name = file.name;
      div.dataset.type = file.type;

      let content = "";
      let badge = "";

      if (file.type === "image") {
        badge = "IMG";
        content = `<img src="${url}" alt="">`;
      } else if (file.type === "video") {
        badge = "VID";
        // on compte sur preload pour afficher la première image
        content = `<video src="${url}" muted preload="metadata" ></video>`;
      } else if (file.type === "audio") {
        badge = "AUD";
        content = `
          <div style="height:160px;display:flex;align-items:center;justify-content:center;font-size:2rem;">
            🎵
          </div>`;
      } else {
        badge = "FILE";
        content = `
          <div style="height:160px;display:flex;align-items:center;justify-content:center;font-size:2rem;">
            📄
          </div>`;
      }

      div.innerHTML = `
        <span class="badge">${badge}</span>
        ${content}
        <div class="item-label">${file.name}</div>
      `;

      // Hover vidéo -> play / stop
      if (file.type === "video") {
        const vid = div.querySelector("video");
        div.addEventListener("mouseenter", () => {
          vid.currentTime = 0;
          vid.play().catch(() => {});
        });
        div.addEventListener("mouseleave", () => {
          vid.pause();
        });
      }

      // Clic -> toggle viewer
      div.addEventListener("click", () => {
        if (currentOpen === file.name) {
          closeViewer();
        } else {
          openViewer(file);
        }
      });

      grid.appendChild(div);
    });
  }

  // ---------- VIEWER ----------
  function closeViewer() {
    viewer.style.display = "none";
    viewerContent.innerHTML = "";
    currentOpen = null;
    currentOpenType = null;
    setFaviconForType(null);
  }

  viewer.addEventListener("click", (e) => {
    if (e.target === viewer) {
      closeViewer();
    }
  });

  viewerContent.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  function openViewer(file) {
    const url = "/file/" + encodeURIComponent(file.name);
    currentOpen = file.name;
    currentOpenType = file.type;

    setFaviconForType(file.type);

    viewer.style.display = "flex";

    if (file.type === "image") {
      viewerContent.innerHTML = `<img src="${url}" alt="">`;
    } else if (file.type === "video") {
      viewerContent.innerHTML = `
        <video id="viewerVideo" src="${url}" style="max-width:100%;max-height:70vh;" controls hidden ></video>
        <div class="viewer-controls">
          <button id="playPauseBtn">▶️</button>
          <div class="viewer-progress">
            <input id="videoRange" type="range" min="0" max="100" step="0.1" value="0">
          </div>
          <div id="timeLabel">00:00 / 00:00</div>
        </div>
      `;
      setupVideoControls();
    } else if (file.type === "audio") {
      viewerContent.innerHTML = `
        <audio src="${url}" controls autoplay style="width:100%;" controls hidden></audio>
      `;
    } else {
      viewerContent.innerHTML = `
        <div style="padding:20px;color:white;max-width:60vw;">
          <h2>📄 ${file.name}</h2>
          <p>Type non prévisualisé. (taille : ${(file.size/1024).toFixed(1)} Ko)</p>
        </div>
      `;
    }
  }

  function setupVideoControls() {
    const video = document.getElementById("viewerVideo");
    const range = document.getElementById("videoRange");
    const playPauseBtn = document.getElementById("playPauseBtn");
    const timeLabel = document.getElementById("timeLabel");

    function formatTime(t) {
      const m = Math.floor(t / 60).toString().padStart(2, "0");
      const s = Math.floor(t % 60).toString().padStart(2, "0");
      return `${m}:${s}`;
    }

    video.addEventListener("loadedmetadata", () => {
      timeLabel.textContent = `00:00 / ${formatTime(video.duration)}`;
    });

    video.addEventListener("timeupdate", () => {
      if (video.duration) {
        const percent = (video.currentTime / video.duration) * 100;
        range.value = percent;
        timeLabel.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
      }
    });

    range.addEventListener("input", () => {
      if (video.duration) {
        video.currentTime = video.duration * (range.value / 100);
      }
    });

    playPauseBtn.addEventListener("click", () => {
      if (video.paused) {
        video.play();
        playPauseBtn.textContent = "⏸️";
      } else {
        video.pause();
        playPauseBtn.textContent = "▶️";
      }
    });

    video.play().then(() => {
      playPauseBtn.textContent = "⏸️";
    }).catch(() => {
      playPauseBtn.textContent = "▶️";
    });
  }

  // ---------- FILTRES UI ----------
  const chips = document.querySelectorAll(".chip");
  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      filterType = chip.dataset.filter;
      renderGrid();
    });
  });

  const sortSelect = document.getElementById("sortSelect");
  const orderAsc = document.getElementById("orderAsc");
  const orderDesc = document.getElementById("orderDesc");

  sortSelect.addEventListener("change", () => {
    sortKey = sortSelect.value;
    renderGrid();
  });

  orderAsc.addEventListener("click", () => {
    sortOrder = "asc";
    orderAsc.classList.add("active");
    orderDesc.classList.remove("active");
    renderGrid();
  });

  orderDesc.addEventListener("click", () => {
    sortOrder = "desc";
    orderAsc.classList.remove("active");
    orderDesc.classList.add("active");
    renderGrid();
  });

  // ---------- DRAG & DROP UPLOAD ----------
  const dropZone = document.getElementById("dropZone");

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    document.addEventListener(eventName, preventDefaults, false);
  });

  ["dragenter", "dragover"].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add("dragover"), false);
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove("dragover"), false);
  });

  dropZone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (!files || files.length === 0) return;

    [...files].forEach(uploadFile);
  });

  async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    await fetch("/upload", {
      method: "POST",
      body: formData
    });

    // recharge la liste après upload
    await loadFiles();
  }

  // ---------- INIT ----------
  loadFiles();
</script>

</body>
</html>
        
```



- [] Choix rep input 
- [] Choix rep output 

---

# Save 

```html 
<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <title>📁 Portfolio – Downloads</title>

    <!-- Favicon emoji dynamique -->
    <link id="favicon" rel="icon"
        href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">📁</text></svg>'>

    <style>
        :root {
            --bg: #f5f5f5;
            --text: #111;
            --card-bg: #ffffff;
            --shadow: rgba(0, 0, 0, 0.1);
            --accent: #3b82f6;
        }

        body.dark {
            --bg: #111827;
            --text: #f9fafb;
            --card-bg: #1f2937;
            --shadow: rgba(0, 0, 0, 0.6);
            --accent: #60a5fa;
        }

        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: var(--bg);
            color: var(--text);
        }

        .layout {
            display: grid;
            grid-template-columns: 260px 1fr;
            min-height: 100vh;
        }

        .sidebar {
            padding: 20px;
            border-right: 1px solid rgba(0, 0, 0, 0.1);
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
        }

        .sidebar h2 {
            margin-top: 0;
            font-size: 1.2rem;
        }

        .main {
            padding: 20px;
        }

        h1 {
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }

        .item {
            position: relative;
            cursor: pointer;
            overflow: hidden;
            border-radius: 16px;
            background: var(--card-bg);
            box-shadow: 0 4px 12px var(--shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .item:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px var(--shadow);
        }

        .item img,
        .item video {
            width: 100%;
            height: 160px;
            object-fit: cover;
            display: block;
        }

        .item-label {
            padding: 8px 12px;
            font-size: 0.8rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .badge {
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(0, 0, 0, 0.6);
            color: white;
            padding: 2px 6px;
            border-radius: 999px;
            font-size: 0.75rem;
        }

        /* Viewer plein écran */
        #viewer {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.8);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }

        #viewerContent {
            max-width: 90vw;
            max-height: 90vh;
            background: #000;
            border-radius: 16px;
            padding: 10px;
            box-sizing: border-box;
        }

        #viewerContent img,
        #viewerContent video {
            max-width: 100%;
            max-height: 70vh;
            display: block;
            margin: 0 auto;
        }

        .viewer-controls {
            margin-top: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #f9fafb;
            font-size: 0.9rem;
        }

        .viewer-controls button {
            padding: 4px 10px;
            border: none;
            border-radius: 999px;
            background: var(--accent);
            color: white;
            cursor: pointer;
            font-size: 0.85rem;
        }

        .viewer-controls button:hover {
            opacity: 0.9;
        }

        .viewer-progress {
            flex: 1;
        }

        .viewer-progress input[type="range"] {
            width: 100%;
        }

        /* Sidebar controls */
        .control-group {
            margin-bottom: 20px;
        }

        .control-group label {
            display: block;
            margin-bottom: 5px;
            font-size: 0.85rem;
            opacity: 0.8;
        }

        select,
        button.toggle {
            width: 100%;
            padding: 6px 8px;
            border-radius: 999px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            background: var(--card-bg);
            color: var(--text);
            cursor: pointer;
            font-size: 0.9rem;
        }

        button.toggle {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .filter-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .chip {
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.8rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            background: var(--card-bg);
            cursor: pointer;
            opacity: 0.85;
        }

        .chip.active {
            background: var(--accent);
            color: white;
            opacity: 1;
        }

        /* Dropzone */
        #dropZone {
            border: 2px dashed rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            font-size: 0.85rem;
            opacity: 0.8;
        }

        #dropZone.dragover {
            border-color: var(--accent);
            background: rgba(59, 130, 246, 0.1);
            opacity: 1;
        }

        .small {
            font-size: 0.75rem;
            opacity: 0.7;
            margin-top: 6px;
        }

        .sort-row {
            display: flex;
            gap: 8px;
            margin-top: 6px;
        }

        .sort-row button {
            flex: 1;
            padding: 4px 6px;
            border-radius: 999px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            background: var(--card-bg);
            cursor: pointer;
            font-size: 0.8rem;
        }

        .sort-row button.active {
            background: var(--accent);
            color: white;
        }
    </style>
</head>

<body>

    <div class="layout">
        <aside class="sidebar">

            <div class="control-group">
                <label>Choisir un dossier</label>
                <input type="file" id="dirPicker" webkitdirectory directory multiple style="width:100%;">
                <div class="small" id="dirStatus"></div>
            </div>

            <h2>⚙️ Options</h2>

            <div class="control-group">
                <label>Mode</label>
                <button id="themeToggle" class="toggle">🌞 / 🌙</button>
            </div>

            <div class="control-group">
                <label>Tri</label>
                <select id="sortSelect">
                    <option value="name">Nom</option>
                    <option value="date">Date</option>
                    <option value="size">Taille</option>
                    <option value="type">Type</option>
                </select>
                <div class="sort-row">
                    <button id="orderAsc" class="active">⬆️ Asc</button>
                    <button id="orderDesc">⬇️ Desc</button>
                </div>
            </div>

            <div class="control-group">
                <label>Filtre</label>
                <div class="filter-row">
                    <div class="chip active" data-filter="all">Tout</div>
                    <div class="chip" data-filter="image">Images</div>
                    <div class="chip" data-filter="video">Vidéos</div>
                    <div class="chip" data-filter="audio">Audio</div>
                    <div class="chip" data-filter="other">Autres</div>
                </div>
            </div>

            <div class="control-group">
                <label>Drag & drop</label>
                <div id="dropZone">
                    Dépose des fichiers ici<br>
                    <span class="small">(ils seront copiés dans ton dossier Downloads)</span>
                </div>
            </div>
        </aside>

        <main class="main">
            <h1>📁 Portfolio – Downloads</h1>
            <div class="grid" id="grid"></div>
        </main>
    </div>

    <!-- Viewer plein écran -->
    <div id="viewer">
        <div id="viewerContent"></div>
    </div>

    <script>
        // ---------- FAVICON EMOJI ----------
        const faviconEl = document.getElementById("favicon");

        function emojiToFavicon(emoji) {
            return `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">${emoji}</text></svg>`;
        }

        function setFaviconForType(type) {
            let emoji = "📁";
            if (!type) emoji = "📁";
            else if (type === "image") emoji = "🖼️";
            else if (type === "video") emoji = "🎬";
            else if (type === "audio") emoji = "🎵";
            else emoji = "📄";
            faviconEl.href = emojiToFavicon(emoji);
        }

        // ---------- THEME ----------
        const body = document.body;
        const themeToggle = document.getElementById("themeToggle");

        function applyStoredTheme() {
            const stored = localStorage.getItem("theme") || "light";
            if (stored === "dark") {
                body.classList.add("dark");
            } else {
                body.classList.remove("dark");
            }
        }

        themeToggle.addEventListener("click", () => {
            body.classList.toggle("dark");
            localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
        });

        applyStoredTheme();

        // ---------- DATA & STATE ----------
        let allFiles = [];
        let filterType = "all";
        let sortKey = "name";
        let sortOrder = "asc";
        let currentOpen = null; // nom du fichier actuellement ouvert dans viewer
        let currentOpenType = null;

        const grid = document.getElementById("grid");
        const viewer = document.getElementById("viewer");
        const viewerContent = document.getElementById("viewerContent");

        // ---------- FETCH FILES ----------
        async function loadFiles() {
            const res = await fetch("/list");
            allFiles = await res.json();
            renderGrid();
        }

        // ---------- TRI & FILTRE ----------
        function getFilteredSortedFiles() {
            let files = [...allFiles];

            if (filterType !== "all") {
                files = files.filter(f => f.type === filterType);
            }

            files.sort((a, b) => {
                let va, vb;
                switch (sortKey) {
                    case "date":
                        va = a.mtime;
                        vb = b.mtime;
                        break;
                    case "size":
                        va = a.size;
                        vb = b.size;
                        break;
                    case "type":
                        va = a.type;
                        vb = b.type;
                        break;
                    default:
                        va = a.name.toLowerCase();
                        vb = b.name.toLowerCase();
                }

                if (va < vb) return sortOrder === "asc" ? -1 : 1;
                if (va > vb) return sortOrder === "asc" ? 1 : -1;
                return 0;
            });

            return files;
        }

        // ---------- RENDER GRID ----------
        function renderGrid() {
            grid.innerHTML = "";
            const files = getFilteredSortedFiles();

            files.forEach(file => {
                const url = "/file/" + encodeURIComponent(file.name);
                const div = document.createElement("div");
                div.className = "item";
                div.dataset.name = file.name;
                div.dataset.type = file.type;

                let content = "";
                let badge = "";

                if (file.type === "image") {
                    badge = "IMG";
                    content = `<img src="${url}" alt="">`;
                } else if (file.type === "video") {
                    badge = "VID";
                    // on compte sur preload pour afficher la première image
                    content = `<video src="${url}" muted preload="metadata" ></video>`;
                } else if (file.type === "audio") {
                    badge = "AUD";
                    content = `
          <div style="height:160px;display:flex;align-items:center;justify-content:center;font-size:2rem;">
            🎵
          </div>`;
                } else {
                    badge = "FILE";
                    content = `
          <div style="height:160px;display:flex;align-items:center;justify-content:center;font-size:2rem;">
            📄
          </div>`;
                }

                div.innerHTML = `
        <span class="badge">${badge}</span>
        ${content}
        <div class="item-label">${file.name}</div>
      `;

                // Hover vidéo -> play / stop
                if (file.type === "video") {
                    const vid = div.querySelector("video");
                    div.addEventListener("mouseenter", () => {
                        vid.currentTime = 0;
                        vid.play().catch(() => { });
                    });
                    div.addEventListener("mouseleave", () => {
                        vid.pause();
                    });
                }

                // Clic -> toggle viewer
                div.addEventListener("click", () => {
                    if (currentOpen === file.name) {
                        closeViewer();
                    } else {
                        openViewer(file);
                    }
                });

                grid.appendChild(div);
            });
        }

        // ---------- VIEWER ----------
        function closeViewer() {
            viewer.style.display = "none";
            viewerContent.innerHTML = "";
            currentOpen = null;
            currentOpenType = null;
            setFaviconForType(null);
        }

        viewer.addEventListener("click", (e) => {
            if (e.target === viewer) {
                closeViewer();
            }
        });

        viewerContent.addEventListener("click", (e) => {
            e.stopPropagation();
        });

        function openViewer(file) {
            const url = "/file/" + encodeURIComponent(file.name);
            currentOpen = file.name;
            currentOpenType = file.type;

            setFaviconForType(file.type);

            viewer.style.display = "flex";

            if (file.type === "image") {
                viewerContent.innerHTML = `<img src="${url}" alt="">`;
            } else if (file.type === "video") {
                viewerContent.innerHTML = `
        <video id="viewerVideo" src="${url}" style="max-width:100%;max-height:70vh;" controls hidden ></video>
        <div class="viewer-controls">
          <button id="playPauseBtn">▶️</button>
          <div class="viewer-progress">
            <input id="videoRange" type="range" min="0" max="100" step="0.1" value="0">
          </div>
          <div id="timeLabel">00:00 / 00:00</div>
        </div>
      `;
                setupVideoControls();
            } else if (file.type === "audio") {
                viewerContent.innerHTML = `
        <audio src="${url}" controls autoplay style="width:100%;" controls hidden></audio>
      `;
            } else {
                viewerContent.innerHTML = `
        <div style="padding:20px;color:white;max-width:60vw;">
          <h2>📄 ${file.name}</h2>
          <p>Type non prévisualisé. (taille : ${(file.size / 1024).toFixed(1)} Ko)</p>
        </div>
      `;
            }
        }

        function setupVideoControls() {
            const video = document.getElementById("viewerVideo");
            const range = document.getElementById("videoRange");
            const playPauseBtn = document.getElementById("playPauseBtn");
            const timeLabel = document.getElementById("timeLabel");

            function formatTime(t) {
                const m = Math.floor(t / 60).toString().padStart(2, "0");
                const s = Math.floor(t % 60).toString().padStart(2, "0");
                return `${m}:${s}`;
            }

            video.addEventListener("loadedmetadata", () => {
                timeLabel.textContent = `00:00 / ${formatTime(video.duration)}`;
            });

            video.addEventListener("timeupdate", () => {
                if (video.duration) {
                    const percent = (video.currentTime / video.duration) * 100;
                    range.value = percent;
                    timeLabel.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
                }
            });

            range.addEventListener("input", () => {
                if (video.duration) {
                    video.currentTime = video.duration * (range.value / 100);
                }
            });

            playPauseBtn.addEventListener("click", () => {
                if (video.paused) {
                    video.play();
                    playPauseBtn.textContent = "⏸️";
                } else {
                    video.pause();
                    playPauseBtn.textContent = "▶️";
                }
            });

            video.play().then(() => {
                playPauseBtn.textContent = "⏸️";
            }).catch(() => {
                playPauseBtn.textContent = "▶️";
            });
        }

        // ---------- FILTRES UI ----------
        const chips = document.querySelectorAll(".chip");
        chips.forEach(chip => {
            chip.addEventListener("click", () => {
                chips.forEach(c => c.classList.remove("active"));
                chip.classList.add("active");
                filterType = chip.dataset.filter;
                renderGrid();
            });
        });

        const sortSelect = document.getElementById("sortSelect");
        const orderAsc = document.getElementById("orderAsc");
        const orderDesc = document.getElementById("orderDesc");

        sortSelect.addEventListener("change", () => {
            sortKey = sortSelect.value;
            renderGrid();
        });

        orderAsc.addEventListener("click", () => {
            sortOrder = "asc";
            orderAsc.classList.add("active");
            orderDesc.classList.remove("active");
            renderGrid();
        });

        orderDesc.addEventListener("click", () => {
            sortOrder = "desc";
            orderAsc.classList.remove("active");
            orderDesc.classList.add("active");
            renderGrid();
        });

        // ---------- DRAG & DROP UPLOAD ----------
        const dropZone = document.getElementById("dropZone");

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
            document.addEventListener(eventName, preventDefaults, false);
        });

        ["dragenter", "dragover"].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add("dragover"), false);
        });

        ["dragleave", "drop"].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove("dragover"), false);
        });

        dropZone.addEventListener("drop", (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (!files || files.length === 0) return;

            [...files].forEach(uploadFile);
        });

        async function uploadFile(file) {
            const formData = new FormData();
            formData.append("file", file);

            await fetch("/upload", {
                method: "POST",
                body: formData
            });

            // recharge la liste après upload
            await loadFiles();
        }


        const dirPicker = document.getElementById("dirPicker");
        const dirStatus = document.getElementById("dirStatus");

        dirPicker.addEventListener("change", async (e) => {
            const files = [...e.target.files];
            if (!files.length) return;

            // On envoie seulement le chemin parent au serveur (pour changer le dossier)
            const path = files[0].webkitRelativePath.split("/")[0];

            const res = await fetch("/setdir", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ path })
            });

            const data = await res.json();
            if (res.ok) {
                dirStatus.textContent = `✅ Dossier choisi : ${data.path}`;
                dirStatus.style.color = "green";
                await loadFiles(); // recharge la liste avec le nouveau dossier
            } else {
                dirStatus.textContent = `❌ Erreur : ${data.error}`;
                dirStatus.style.color = "red";
            }
        });


        // ---------- INIT ----------
        loadFiles();
    </script>

</body>

</html>
```

```python
from flask import Flask, jsonify, send_file, request, send_from_directory
import os
import time

app = Flask(__name__)

# -------------------- CONFIG --------------------
DEFAULT_DIR = os.path.expanduser("./Downloads")
# DEFAULT_DIR = os.path.expanduser("../../GOLD/DCIM/DJI_001")
DOWNLOADS_DIR = DEFAULT_DIR  # dossier actif
CACHE_TTL = 5  # secondes

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
AUDIO_EXT = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

FILE_CACHE = {"data": None, "mtime": 0}  # cache simple

# -------------------- UTILITAIRES --------------------
def detect_type(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"

def scan_files():
    """Scanne le dossier actif et met en cache le résultat."""
    now = time.time()
    if FILE_CACHE["data"] is not None and now - FILE_CACHE["mtime"] < CACHE_TTL:
        return FILE_CACHE["data"]

    files = []
    for f in os.listdir(DOWNLOADS_DIR):
        if f.startswith(".") or f.startswith("._"):
            continue
        path = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(path):
            stat = os.stat(path)
            files.append({
                "name": f,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "type": detect_type(f)
            })

    FILE_CACHE["data"] = files
    FILE_CACHE["mtime"] = now
    return files

def scan_files():
    """Scanne le dossier actif et met en cache le résultat."""
    now = time.time()
    if FILE_CACHE["data"] is not None and now - FILE_CACHE["mtime"] < CACHE_TTL:
        return FILE_CACHE["data"]

    items = []
    for f in os.listdir(DOWNLOADS_DIR):
        if f.startswith(".") or f.startswith("._"):
            continue
        path = os.path.join(DOWNLOADS_DIR, f)
        stat = os.stat(path)

        if os.path.isfile(path):
            items.append({
                "name": f,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "type": detect_type(f)
            })
        elif os.path.isdir(path):
            items.append({
                "name": f,
                "size": 0,  # ou None si tu préfères
                "mtime": stat.st_mtime,
                "type": "folder"
            })

    FILE_CACHE["data"] = items
    FILE_CACHE["mtime"] = now
    return items


# -------------------- ROUTES --------------------
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/list")
def list_files():
    return jsonify(scan_files())

@app.route("/file/<path:name>")
def serve_file(name):
    path = os.path.join(DOWNLOADS_DIR, name)
    if not os.path.isfile(path):
        return "Not found", 404
    return send_file(path)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file", 400

    f = request.files["file"]
    if f.filename == "":
        return "No filename", 400

    if f.filename.startswith(".") or f.filename.startswith("._"):
        return "Invalid filename", 400

    dest = os.path.join(DOWNLOADS_DIR, f.filename)
    f.save(dest)

    FILE_CACHE["data"] = None  # invalide le cache
    return "OK", 200

@app.route("/setdir", methods=["POST"])
def set_directory():
    """Changer le dossier actif."""
    global DOWNLOADS_DIR
    data = request.get_json()
    path = data.get("path", DEFAULT_DIR)

    if not os.path.isdir(path):
        return jsonify({"error": "Chemin invalide"}), 400

    DOWNLOADS_DIR = os.path.abspath(path)
    FILE_CACHE["data"] = None  # invalide le cache
    return jsonify({"success": True, "path": DOWNLOADS_DIR})

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


```

---

#Bot 

```bash
source venv/bin/activate
python bot.py
```

# teleloader
