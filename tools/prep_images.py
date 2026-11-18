# -*- coding: utf-8 -*-
"""GORNICA: подготовка фотографий для сайта.

Берёт исходники (папка images из присланного архива), убирает водяные знаки
2GIS / бренда по краю кадра, режет детали-кропы и сохраняет WebP в ../images/.
Запуск:  python3 prep_images.py /путь/к/исходникам
Размеры: <имя>-s.webp (до 760 px) для сетки и <имя>-l.webp (до 1500 px) для
полноэкранного просмотра и больших кадров. Увеличение не выполняется.

Чтобы добавить новое фото в галерею: положите файл рядом с исходниками,
добавьте строку в JOBS и затем строку в GALLERY в assets/config.js.
"""
import os, sys, json
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/gornica-src/site-Gornica/images"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "images")
os.makedirs(OUT, exist_ok=True)

G = 0.045   # убрать «2GIS» внизу справа
N = 0.16    # убрать подпись бренда + «2GIS»

# key: (файл, crop_bottom, crop_right, box(x0,y0,x1,y1) в долях или None)
JOBS = {
    # --- ключевые кадры
    "hero":      ("vk03.jpg", 0, 0, None),
    "wedding":   ("vk02.jpg", 0, 0, None),
    "evening":   ("hero-3.jpg", 0.03, 0, None),
    "evening2":  ("g43.jpg", G, 0, None),
    "fitting":   ("g37.jpg", G, 0, None),
    "finale":    ("g12.jpg", G, 0, None),
    # --- галерея: свадебные
    "w01": ("g10.jpg", G, 0, None),
    "w02": ("g13.jpg", G, 0, None),
    "w03": ("g16.jpg", G, 0, None),
    "w04": ("g18.jpg", N, 0, None),
    "w05": ("g20.jpg", N, 0, None),
    "w06": ("g25.jpg", G, 0, None),
    "w07": ("g27.jpg", 0, 0, None),
    "w08": ("g35.jpg", G, 0, None),
    "w09": ("g36.jpg", G, 0, None),
    "w10": ("vk08.jpg", 0, 0, None),
    "w11": ("vk09.jpg", 0, 0, None),
    "w12": ("vk10.jpg", 0, 0, None),
    "w13": ("vk11.jpg", 0, 0, None),
    "w14": ("vk12.jpg", 0, 0, None),
    "w15": ("g05.jpg", G, 0, None),
    "w16": ("g38.jpg", N, 0, None),
    "w17": ("g31.jpg", N, 0, None),
    "w18": ("g02.jpg", G, 0, None),
    "w19": ("g33.jpg", N, 0, None),
    "w20": ("g17.jpg", G, 0, None),
    "w21": ("g22.jpg", G, 0, None),
    # --- галерея: вечерние
    "e01": ("g32.jpg", 0.035, 0.045, None),
    "e02": ("vk15.jpg", 0, 0, None),
    "e03": ("vk14.jpg", 0, 0, None),
    "e04": ("g30.jpg", G, 0, None),
    # --- атмосфера
    "a01": ("hero-1.jpg", 0.07, 0, None),
    "a02": ("g35.jpg", 0, 0, (0.2, 0.12, 0.85, 0.38)),   # кружево корсета
    "a03": ("g25.jpg", 0, 0, (0.05, 0.70, 0.95, 0.95)),  # фатин
    "a04": ("col-06.jpg", 0.04, 0, None),                   # примерка
    "a05": ("g21.jpg", 0, 0, (0.22, 0.28, 0.82, 0.52)),  # бисер
    "a06": ("g49.jpg", 0.22, 0, None),
    "a07": ("g36.jpg", 0, 0, (0.0, 0.5, 1.0, 0.80)),     # шлейф
    "a08": ("vk07.jpg", 0, 0, None),
    "a09": ("g38.jpg", 0, 0, (0.0, 0.58, 1.0, 0.86)),    # атлас
}

meta = {}
for key, (f, cb, cr, box) in JOBS.items():
    p = os.path.join(SRC, f)
    im = Image.open(p).convert("RGB")
    W, H = im.size
    if box:
        im = im.crop((int(box[0]*W), int(box[1]*H), int(box[2]*W), int(box[3]*H)))
    else:
        im = im.crop((0, 0, int(W*(1-cr)), int(H*(1-cb))))
    w, h = im.size
    for suf, mx in (("s", 760), ("l", 1500)):
        k = min(1.0, mx / w)
        t = im.resize((round(w*k), round(h*k)), Image.LANCZOS) if k < 1 else im
        t.save(os.path.join(OUT, f"{key}-{suf}.webp"), "WEBP", quality=80 if suf == "l" else 76, method=6)
    meta[key] = [w, h]

json.dump(meta, open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(json.dumps(meta))
