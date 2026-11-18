import pymupdf

doc = pymupdf.open("data/raw_bulletins/aichi/23_公報_第51回衆院選_愛知10区.pdf")

pymupdf.Page.rect(doc)

cd = doc.to_chunks()
