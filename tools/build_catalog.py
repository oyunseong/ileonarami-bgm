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
            "en": "MapleStory BGM",
            "ko": "메이플스토리 BGM",
        },
        "tracks": [
            ("above_the_treetops", "Above the Treetops", "리스항구", "NEXON-permission", "MapleStory"),
            ("bad_guys", "Bad Guys", "커닝시티", "NEXON-permission", "MapleStory"),
            ("cash_shop", "Cash Shop", "캐시샵", "NEXON-permission", "MapleStory"),
            ("floral_life", "Floral Life", "헤네시스", "NEXON-permission", "MapleStory"),
            ("go_picnic", "Go Picnic", "암허스트", "NEXON-permission", "MapleStory"),
            ("gold_beach", "Gold Beach", "골드비치", "NEXON-permission", "MapleStory"),
            ("little_maple_planet", "Little Maple Planet", "마지막관문 - 킹슬라임", "NEXON-permission", "MapleStory"),
            ("maple_leaf", "Maple Leaf", "메이플 월드-전직", "NEXON-permission", "MapleStory"),
            ("nightmare", "Nightmare", "페리온", "NEXON-permission", "MapleStory"),
            ("rest_n_peace", "Rest N' Peace", "헤네시스 필드", "NEXON-permission", "MapleStory"),
            ("shop_bgm", "Shop", "(구)캐시샵", "NEXON-permission", "MapleStory"),
            ("subway", "Subway", "커닝시티 지하철", "NEXON-permission", "MapleStory"),
            ("the_beginning_of_the_adventure", "The Beginning of the Adventure", "메이플 아일랜드", "NEXON-permission", "MapleStory"),
            ("wc_select", "Character Select", "(구)서버 선택", "NEXON-permission", "MapleStory"),
            ("when_the_morning_comes", "When the Morning Comes", "엘리니아", "NEXON-permission", "MapleStory"),
            ("old_title", "Classic Title", "(구)로그인", "NEXON-permission", "MapleStory"),
            ("secret_flower", "Secret Flower", "비화원", "NEXON-permission", "MapleStory"),
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
