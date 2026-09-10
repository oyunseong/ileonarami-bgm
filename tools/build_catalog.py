#!/usr/bin/env python3
"""catalog.json 생성기.

sounds/ 의 실제 파일에서 크기·길이·sha256 을 읽어 catalog.json 을 만든다.
손으로 적으면 반드시 어긋나므로 메타데이터는 항상 이 스크립트로 갱신한다.

사용법: python3 tools/build_catalog.py [TAG]   (기본 TAG=v1)
"""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOUNDS = ROOT / "sounds"
TAG = sys.argv[1] if len(sys.argv) > 1 else "v1"
BASE_URL = f"https://cdn.jsdelivr.net/gh/oyunseong/ileonarami-bgm@{TAG}/sounds"

PACKS = [
    {
        "id": "retro_8bit",
        "title": {"en": "Retro 8-bit", "ko": "레트로 8비트"},
        "description": {
            "en": "Seamlessly looping chiptunes. Public domain (CC0).",
            "ko": "끊김 없이 반복되는 칩튠 모음. 저작권 없음(CC0).",
        },
        "tracks": [
            ("pixel_morning", "Pixel Morning", "픽셀 모닝", "CC0-1.0", "Juhani Junkala"),
            ("pixel_rush", "Pixel Rush", "픽셀 러시", "CC0-1.0", "Juhani Junkala"),
            ("pixel_boss", "Pixel Boss", "픽셀 보스", "CC0-1.0", "Juhani Junkala"),
            ("starlight_city", "Starlight City", "스타라이트 시티", "CC0-1.0", "Zane Little Music"),
            ("nes_mercury", "Mercury", "머큐리", "CC0-1.0", "SketchyLogic"),
            ("nes_venus", "Venus", "비너스", "CC0-1.0", "SketchyLogic"),
        ],
    },
]


def duration_sec(path: pathlib.Path) -> int:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    )
    return round(float(out.decode().strip()))


def build() -> dict:
    packs = []
    for pack in PACKS:
        tracks = []
        for file_id, title_en, title_ko, license_id, credit in pack["tracks"]:
            path = SOUNDS / f"{file_id}.ogg"
            data = path.read_bytes()
            tracks.append(
                {
                    "id": f"{pack['id']}_{file_id}",
                    "title": {"en": title_en, "ko": title_ko},
                    "url": f"{BASE_URL}/{file_id}.ogg",
                    "fileName": f"{file_id}.ogg",
                    "sizeBytes": len(data),
                    "durationSec": duration_sec(path),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "license": license_id,
                    "credit": credit,
                }
            )
        packs.append(
            {
                "id": pack["id"],
                "title": pack["title"],
                "description": pack["description"],
                "tracks": tracks,
            }
        )
    return {"version": 1, "packs": packs}


if __name__ == "__main__":
    catalog = build()
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    total = sum(t["sizeBytes"] for p in catalog["packs"] for t in p["tracks"])
    print(f"catalog.json written — {sum(len(p['tracks']) for p in catalog['packs'])} tracks, {total / 1024 / 1024:.1f}MB")
