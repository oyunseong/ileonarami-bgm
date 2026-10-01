# ileonarami-bgm

일어나라미 알람 앱의 **알람음 다운로드 카탈로그**. 음원 파일과 카탈로그 메타데이터만 담는다.
앱 코드는 별도 저장소에 있다.

## 앱이 바라보는 URL

| 용도 | URL | 비고 |
|---|---|---|
| 카탈로그 | `https://raw.githubusercontent.com/oyunseong/ileonarami-bgm/main/catalog.json` | 짧은 캐시. 팩 추가·삭제가 앱 업데이트 없이 즉시 반영된다 |
| 음원 | `https://cdn.jsdelivr.net/gh/oyunseong/ileonarami-bgm@<TAG>/sounds/<file>.ogg` | jsDelivr CDN. 태그 고정이라 영구 캐시된다 |

카탈로그는 `main`(가변), 음원은 태그(불변)를 가리킨다.
음원 URL이 태그에 고정돼 있어야 `sha256` 검증이 항상 성립한다.

## 트랙 추가/교체 순서

1. `sounds/` 에 파일을 넣는다 (아래 인코딩 규격 준수).
2. `tools/build_catalog.py` 의 `PACKS` 에 항목을 추가한다.
3. 새 태그를 정하고 카탈로그를 다시 만든다: `python3 tools/build_catalog.py v2`
4. 커밋 → `git tag v2 && git push --tags` → main 푸시.

크기·길이·sha256은 스크립트가 실제 파일에서 읽는다. 손으로 적지 말 것.

## 인코딩 규격

```
ffmpeg -i input.wav -af "loudnorm=I=-14:TP=-1.0:LRA=11" \
       -c:a libopus -b:a 96k -vbr on -ar 48000 -ac 2 sounds/output.ogg
```

- **Opus/Ogg** — minSdk 26에서 지원되고, mp3와 달리 인코더 패딩이 없어 루프 이음새가 깔끔하다.
- **원본은 seamless loop여야 한다.** 알람은 무한 반복 재생이라 끝과 시작이 안 붙으면 티가 크게 난다.
- **페이드는 넣지 않는다.** 루프마다 소리가 사라진다. 서서히 커지는 기상은 앱의 "부드럽게 깨우기"가 담당한다.

## 라이선스

현재 음원은 `maple` 팩(메이플스토리 BGM)뿐이며, 권리자(NEXON)의 허락을 받아 제공한다.
허락 내역은 [CREDITS.md](CREDITS.md) 참고.
저작권이 있는 음원(게임 BGM 등)은 권리자 서면 허락 없이 절대 추가하지 않는다.
