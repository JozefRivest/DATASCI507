import cv2
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_pdf

if __name__ == "__main__":
    PATH_IMGE = "data/cleaned_bulletins/test/01_大西雅人_社民党.pdf"
    analyzer = DocumentAnalyzer(configs={}, visualize=True, device="cpu")
    imgs = load_pdf(PATH_IMGE)

    for i, img in enumerate(imgs):
        results, ocr_vis, layout_vis = analyzer(img)

        results.to_html(f"output/output_{i}.html", img=img)
        results.to_json(f"data/results/output_{i}.json")
        results.to_csv(f"data/results/output_{i}.csv")

        cv2.imwrite(f"output/output_ocr_{i}.jpg", ocr_vis)
        cv2.imwrite(f"output/output_ocr_{i}.jpg", layout_vis)
