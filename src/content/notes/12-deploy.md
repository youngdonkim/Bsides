---
num: "12"
en: "Deploy"
ko: "배포"
group: build-ship
read_time: "약 7분 읽기"
h1_lead: "배포 — 사이클 안의 한 지점."
lead: "호스팅 올리기 + 도메인 + 환경 변수 + 모니터링. 배포는 끝이 아니라 사이클 안의 한 지점일 뿐."
italic: "\"배포는 끝이 아니라 사이클 안의 한 지점이에요.\" — 운영 노트"
workshop_text: "Deploy는 워크샵에서 운영자와 멤버가 같이 첫 배포 버튼을 누르는 시간이에요. 도메인이 정말 응답하는 그 순간이 한 사이클의 작은 의식."
---
처음 배포는 거창하게 생각하지 말기. 도메인 + HTTPS + 환경 변수 3개만 박으면 충분. 모니터링·CDN·캐시 최적화는 회고 후에.

### 환경 분리

**dev / preview / prod** 셋. preview = prod와 동일 노출 환경 가정 (외부 도달 가능). 위협 모델 일치. NODE_ENV=development는 로컬에서만 true.

### 시크릿 관리

환경 변수·secret은 호스팅 대시보드에서 관리. 코드에 박지 않기. .env 파일은 .gitignore. 시크릿이 commit되면 즉시 회전 + git history 정리.

<div style="margin: 12px 0px; padding: 20px 22px; background: var(--b-note-mint); border-radius: 12px; transform: rotate(-1deg); box-shadow: var(--b-shadow-note);"><div style="font-family: var(--b-font-hand); font-size: 22px; color: var(--b-ink); margin-bottom: 6px;">한 스푼 메모</div><div style="font-family: var(--b-font-sans); font-size: 14.5px; line-height: 1.55; color: var(--b-ink);">처음 배포는 도메인 + HTTPS + 환경 변수 3개만. 모니터링·CDN·캐시는 회고 후 정밀화.</div></div>

### 다음 단계로

배포 후엔 **13 Retrospective**에서 한 사이클을 닫아요. 발견을 3분류로 판정해서 다음 사이클로 흡수.
