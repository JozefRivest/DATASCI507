import base64
import json
import os
from pathlib import Path

import pymupdf
from anthropic import Anthropic
from dotenv import load_dotenv
from PIL import Image

load_dotenv(os.path.expanduser("~/.env"))

api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(
    api_key=api_key,
)

input_dir = Path("data/raw_bulletins/aichi")
output_root = Path("data/test/crops")

prompt = """
This image is one page of a Japanese electoral bulletin (選挙公報).
Identify each candidate's block: the area containing one candidate's photo,
name, and campaign text. Ignore headers, footers, voting-day notices, and maps.

Give each box as normalized coordinates (0 to 1, as fractions of the image
width and height), with (0, 0) at the TOP-LEFT corner.
If the page has no candidates, return [].

Respond with JSON only, no other text, in this format:
[{"name": "大西雅人", "party": "社民党", "x0": 0.02, "y0": 0.29, "x1": 0.98, "y1": 0.52}]
"""


def split_pdf(pdf_path):
    district = pdf_path.stem.split("_")[-1]  # e.g. 愛知10区, taken from the filename

    out_dir = output_root / district
    out_dir.mkdir(parents=True, exist_ok=True)  # creates folder if missing

    # --- Step 1: PDF -> PNGs (the only PyMuPDF part) ---
    doc = pymupdf.open(pdf_path)
    page_images = []
    for i, page in enumerate(doc, start=1):
        png_path = out_dir / f"page{i}.png"
        page.get_pixmap(dpi=150).save(png_path)
        page_images.append(png_path)

    # --- Steps 2 and 3, once per page ---
    count = 0
    for png_path in page_images:

        # Step 2: send the PNG to Claude, get boxes back
        png_b64 = base64.standard_b64encode(png_path.read_bytes()).decode("utf-8")
        message = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": png_b64,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        boxes = json.loads(message.content[0].text)

        # Step 3: crop each box with Pillow
        img = Image.open(png_path)
        width, height = img.size

        for candidate in boxes:
            count += 1
            left = candidate["x0"] * width
            top = candidate["y0"] * height
            right = candidate["x1"] * width
            bottom = candidate["y1"] * height

            crop = img.crop((left, top, right, bottom))
            filename = (
                f"{count:02d}_{district}_{candidate['name']}_{candidate['party']}.png"
            )
            crop.save(out_dir / filename)
            print("saved", filename)


if __name__ == "__main__":
    failed = []

    for pdf_path in sorted(input_dir.glob("*.pdf")):
        district = pdf_path.stem.split("_")[-1]

        # Skip districts that already have crops, so reruns don't pay for API calls twice
        if any((output_root / district).glob("0*.png")):
            print("skip", district)
            continue

        print("---", district)
        try:
            split_pdf(pdf_path)
        except Exception as e:  # one bad file shouldn't stop the whole run
            print("FAILED", district, e)
            failed.append(district)

    print("failed:", failed)
