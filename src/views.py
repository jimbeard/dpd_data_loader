from datetime import datetime
from flask import render_template
import logging
import socket
from pathlib import Path
from duckduckgo_search import DDGS
import urllib.request
from urllib.error import URLError, HTTPError
from io import BytesIO
from PIL import Image
import os
import base64
import uuid

from . import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/fetch")
def fetch_image():
    # perform a ddg search to get a list of image URLs
    search_query = os.environ.get("SEARCH_QUERY", "")
    print("search query: " + search_query)
    image_list = DDGS().images(keywords=search_query, max_results=25)

    tmp_folder = Path(r'tmp')
    tmp_search_folder = Path(tmp_folder, search_query.replace(' ', '_'))
    tmp_search_folder.mkdir(parents=True, exist_ok=True)

    tgt_folder = Path(os.environ.get("TARGET_DIR", ""))
    tgt_search_folder = Path(tgt_folder, search_query.replace(' ', '_'))
    tgt_search_folder.mkdir(parents=True, exist_ok=True)

    # iterate image URLs, download, convert and save
    images = []
    for result in image_list:
        link = result['image']
        filename = link.split('/')[-1]
        tmp_filepath = tmp_search_folder / filename
        try:
            urllib.request.urlretrieve(link, tmp_filepath)
            try:
                input = Image.open(tmp_filepath)
                output = BytesIO()
                input.convert('RGBA').resize((600, 600)).save(output, format='PNG')
                output.seek(0)
                images.append(output)

                tgt_filepath = tgt_search_folder / f"{str(uuid.uuid4())}.png"
                with tgt_filepath.open("wb") as f:
                    f.write(output.read())

                os.remove(tmp_filepath)
            except:
                os.remove(tmp_filepath)
                pass
        except URLError as e:
            pass
        except HTTPError as e:
            pass

    return render_template(
        "fetch.html",
        name=f"image count: {len(images)}",
        host=socket.gethostname(),
        date=datetime.now()
    )


@app.route("/api/image")
def show_image():
    search_query = os.environ.get("SEARCH_QUERY", "")
    src_folder = Path(os.environ.get("TARGET_DIR", ""))
    src_search_folder = Path(src_folder, search_query.replace(' ', '_'))

    logger.info("getting next image...")

    in_memory_image = None
    if src_search_folder.exists():
        # check image exists, default None
        next_image = next((x for x in src_search_folder.iterdir() if x.is_file()), None)

        if next_image:
            input = Image.open(next_image)
            output = BytesIO()
            input.save(output, format='png')
            output.seek(0)
            in_memory_image = base64.b64encode(output.getvalue()).decode("utf-8")
            os.remove(next_image)

    return render_template("image.html", image_url=in_memory_image)