from flask import Flask, jsonify, send_file, request, send_from_directory
import os
import time

app = Flask(__name__, static_url_path='/static')

# -------------------- CONFIG --------------------
DEFAULT_DIR = os.path.expanduser("./Downloads")
DOWNLOADS_DIR = DEFAULT_DIR  # dossier actif
CACHE_TTL = 5  # secondes

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
AUDIO_EXT = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}
PDF_EXT   = {".pdf"}

FILE_CACHE = {"data": None, "mtime": 0}

# -------------------- UTILITAIRES --------------------
def detect_type(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in PDF_EXT:
        return "pdf"
    return "other"


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
                "size": 0,
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
    """Support MULTI-FICHIERS (files[])."""
    if "files[]" not in request.files:
        return "No files[] field", 400

    files = request.files.getlist("files[]")
    count = 0

    for f in files:
        if f.filename == "":
            continue
        if f.filename.startswith(".") or f.filename.startswith("._"):
            continue
        dest = os.path.join(DOWNLOADS_DIR, f.filename)
        f.save(dest)
        count += 1

    FILE_CACHE["data"] = None
    return jsonify({"uploaded": count})


@app.route("/setdir", methods=["POST"])
def set_directory():
    """Changer le dossier actif."""
    global DOWNLOADS_DIR
    data = request.get_json()
    path = data.get("path", DEFAULT_DIR)

    if not os.path.isdir(path):
        return jsonify({"error": "Chemin invalide"}), 400

    DOWNLOADS_DIR = os.path.abspath(path)
    FILE_CACHE["data"] = None
    return jsonify({"success": True, "path": DOWNLOADS_DIR})


# ---------------- STATIC FOR PDF.js ----------------
@app.route("/static/pdfjs/<path:filename>")
def serve_pdfjs(filename):
    """Permet à pdf.js et pdf.worker.js d’être chargés correctement."""
    return send_from_directory("static/pdfjs", filename)


# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
