from pathlib import Path

import cv2
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image


class Parser:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.analyzer = DocumentAnalyzer(
            configs={}, visualize=False, device="cpu"
        )  # loaded once

    def get_text(self, file):
        img = load_image(file)  # one image, no loop
        results, _, _ = self.analyzer(img)

        stem = Path(file).stem  # e.g. 01_愛知県第10区_若山しんじ_自民党
        district = stem.split("_")[1]  # e.g. 愛知県第10区

        out_dir = self.output / district
        out_dir.mkdir(parents=True, exist_ok=True)  # creates folder if missing
        results.to_json(str(out_dir / f"{stem}.json"))
        return results


if __name__ == "__main__":
    p = Parser(output="data/results")
    failed = []

    for png in sorted(
        Path("data/test/crops").rglob("0*.png")
    ):  # every district subfolder; crops only, skips page*.png
        district = png.stem.split("_")[1]

        # Skip crops already OCR'd, so reruns pick up where they left off
        if (p.output / district / f"{png.stem}.json").exists():
            print("skip", png.name)
            continue

        try:
            p.get_text(png)
            print("done", png.name)
        except Exception as e:  # one bad crop shouldn't stop the whole run
            print("FAILED", png.name, e)
            failed.append(png.name)

    print("failed:", failed)


# if __name__ == "__main__":
#     PATH_IMGE = "data/cleaned_bulletins/test/01_大西雅人_社民党.pdf"
#     analyzer = DocumentAnalyzer(configs={}, visualize=True, device="cpu")
#     imgs = load_pdf(PATH_IMGE)
#
#     for i, img in enumerate(imgs):
#         results, ocr_vis, layout_vis = analyzer(img)
#
#         results.to_html(f"output/output_{i}.html", img=img)
#         results.to_json(f"data/results/output_{i}.json")
#         results.to_csv(f"data/results/output_{i}.csv")
#
#         cv2.imwrite(f"output/output_ocr_{i}.jpg", ocr_vis)
#         cv2.imwrite(f"output/output_ocr_{i}.jpg", layout_vis)
