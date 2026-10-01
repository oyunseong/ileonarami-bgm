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
        "id": "maple",
        "title": {"en": "MapleStory", "ko": "메이플스토리"},
        "description": {
            "en": "MapleStory BGM. Provided with permission from NEXON.",
            "ko": "메이플스토리 BGM. 넥슨 허락 하에 제공.",
        },
        "tracks": [
            ("above_the_treetops", "Above the Treetops", "나무 위에서", "NEXON-permission", "NEXON"),
            ("bad_guys", "Bad Guys", "악당들", "NEXON-permission", "NEXON"),
            ("cash_shop", "Cash Shop", "캐시샵", "NEXON-permission", "NEXON"),
            ("floral_life", "Floral Life", "꽃 피는 나날", "NEXON-permission", "NEXON"),
            ("go_picnic", "Go Picnic", "소풍 가자", "NEXON-permission", "NEXON"),
            ("gold_beach", "Gold Beach", "황금 해변", "NEXON-permission", "NEXON"),
            ("little_maple_planet", "Little Maple Planet", "작은 메이플 행성", "NEXON-permission", "NEXON"),
            ("maple_leaf", "Maple Leaf", "단풍잎", "NEXON-permission", "NEXON"),
            ("nightmare", "Nightmare", "악몽", "NEXON-permission", "NEXON"),
            ("rest_n_peace", "Rest N' Peace", "고요한 안식", "NEXON-permission", "NEXON"),
            ("shop_bgm", "Shop", "상점", "NEXON-permission", "NEXON"),
            ("subway", "Subway", "지하철", "NEXON-permission", "NEXON"),
            ("the_beginning_of_the_adventure", "The Beginning of the Adventure", "모험의 시작", "NEXON-permission", "NEXON"),
            ("wc_select", "Character Select", "캐릭터 선택", "NEXON-permission", "NEXON"),
            ("when_the_morning_comes", "When the Morning Comes", "아침이 오면", "NEXON-permission", "NEXON"),
            ("old_title", "Classic Title", "클래식 타이틀", "NEXON-permission", "NEXON"),
            ("secret_flower", "Secret Flower", "비밀의 꽃", "NEXON-permission", "NEXON"),
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
