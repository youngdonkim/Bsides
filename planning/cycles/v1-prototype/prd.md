---
platform: web
cycle: v1-prototype
created_at: 2026-05-11
updated_at: 2026-05-11
---

# 기능 목록

## Must (6) — 없으면 가설 검증 불가

- **F1**: 메인 페이지 (Hero + 타겟 페르소나 단서 + 운영방식 4단계 + 현재 멘토 카드(라이브 상태) + 최근 진행상황 미리보기 + 신청 anchor 섹션)
- **F3**: 진행상황 상세 페이지 `/progress/[slug]` (강의 콘텐츠 본문 + 이전·다음 회차 네비 + 하단 신청 CTA)
- **F4**: 운영 워크플로 (Markdown 파일 추가 → git push → 자동 배포 → 페이지 생성)
- **F5**: 객원 멤버 신청 카톡 link (anchor 섹션 + 신청 후 안내 3줄 + 카톡 외부 link)
- **F7**: 반응형 layout (320px~1920px)
- **F8**: 사이트 chrome (sticky 헤더 + 푸터)

## Should (4)

- **F2**: 진행상황 목록 페이지 `/progress` (회차별 카드 그리드, 최신순) — 메인 미리보기로 폴백 가능
- **F6**: SEO 메타 + OG 이미지 — H2 organic 유입 직결, 3개월 시그널은 약함
- **F10**: 방문자 분석 (zero-config 도구) — H2 검증 시그널, 카톡 "어떻게 알게 됐어요?" 질문으로 폴백
- **F11**: 접근성 baseline (대비·alt text·시맨틱·키보드 4개) — Design 단계에서 baseline으로 자동 적용

## Could (1)

- **F9**: 404 페이지 (brand voice 정합 한 줄 + 메인 link) — 외부 검색 유입 거의 없을 v1엔 default 404로도 OK

## Won't — intent 비목표 반영

- 멤버 로그인·관리자 대시보드
- 결제·유료 멤버쉽
- 자동화된 신청·심사 시스템
- UGC 메이커 로그 피드 (Disquiet 식)
- 모바일 앱
- 매스 마케팅·광고

---

# Must 기능별 명세

## F1: 메인 페이지

- **트리거**: 사용자가 root URL `/` 접속 — 외부 link / 검색 결과 / 지인 소개 URL / 직접 입력
- **동작**: 정적 HTML 렌더. 빌드 시점에 Markdown/data로부터 fetch. 페이지 섹션 구성·stacking·카피·시각 layout은 [sketch.md](sketch.md) 화면 1 + [brand-guide.md](brand-guide.md) §9 카피 패턴 참조
- **결과**: 사용자가 첫 5초~5분 안에 "Bsides가 뭐고 · 내가 맞는 사람인지 · 다음 액션이 뭔지" 파악. 신청·이탈·재방문 중 결정. (시각 표현은 sketch §화면1)
- **엣지 케이스**: sketch §화면별 엣지 케이스 표 참조 (메인 = "현재 멘토 없음" 대체 메시지). 매우 작은 화면(320px+)은 F7 반응형
- **연결**: Sketch §S1, S3 / Intent 가설 H2

## F3: 진행상황 상세 `/progress/[slug]`

- **트리거**: 사용자가 `/progress/[slug]` 접속 — 메인 미리보기 클릭 / 진행상황 목록 클릭 / 외부 공유 link / 검색 결과
- **동작**: 빌드 시점에 `content/progress/[slug].md`를 HTML로 렌더. data 흐름: frontmatter(회차·날짜·멘토·주제·이미지 path) + body(LLM 가공 글). 이전·다음 slug 자동 계산. 시각 layout·컴포넌트 stacking은 [sketch.md](sketch.md) 화면 3 + [brand-guide.md](brand-guide.md) §8 "감성 한 스푼" 시그널 참조
- **결과**: 사용자가 강의 콘텐츠 읽고 멘토·운영 신뢰 형성. 신청 의지 결정. 외부 공유 시 OG preview로 organic 유입 자산. (시각은 sketch §화면3)
- **엣지 케이스**: 잘못된 slug → 404 (F9). 이전·다음 회차 없을 때 → nav 비활성. 이미지 로딩 실패 → alt text. (시각 표현은 sketch §화면별 엣지)
- **연결**: Sketch §S2, S4 / Intent 가설 H2, H3

## F4: 운영 워크플로

- **트리거**: 운영자가 워크샵 회차 완료 → 녹음·메모 raw 보유
- **동작**:
    1. raw를 LLM으로 가공 → 본문 Markdown 작성
    2. AI 이미지 생성 서비스로 대표·보조 이미지 만듦
    3. `content/progress/[slug].md` 경로에 파일 추가 (frontmatter: 회차·날짜·멘토·주제·이미지 path / body: 본문)
    4. `git add . && git commit && git push`
    5. CI/CD가 자동 빌드·배포 (호스팅 webhook)
    6. 새 페이지 `/progress/[slug]` 생성 + 메인 "최근 진행상황 미리보기" 자동 update
- **결과**: 외부 방문자가 새 회차 콘텐츠 즉시 접근 가능. SEO indexing 시작
- **엣지 케이스**:
    - frontmatter schema 오류 → CI 빌드 실패, 운영자에게 알림
    - 이미지 path 오류 → 빌드 시 broken image 경고
    - 빌드 시간 (~30초~몇 분) — 즉시 반영 X, 운영자가 기다림
- **연결**: Sketch §운영자 흐름 / Intent 가설 H2, H3

## F5: 객원 멤버 신청 카톡 link

- **트리거**: 사용자가 객원 멤버 신청 진입점 클릭 (액션 type — UI 위치·라벨은 sketch §화면 1·3 참조):
    1. 헤더 sticky CTA → 메인 `#apply` 스크롤
    2. Hero CTA → 메인 `#apply` 스크롤
    3. 진행상황 상세 페이지 하단 CTA → `#apply` 또는 직접 카톡 link
    4. 신청 섹션 안 카톡 link 버튼 → 카톡 외부 URL
- **동작**:
    1. anchor 진입 시 신청 섹션 표시. 안내문·**신청 후 안내 3줄** 카피는 [brand-guide.md](brand-guide.md) §9 카피 패턴 참조
    2. 카톡 link 클릭 → 카톡 오픈채팅 URL (`open.kakao.com/o/...`) 또는 운영자 카톡 ID URL로 이동
    3. 모바일 = 카톡 앱 deep link 자동 열림 / 데스크톱 = 카톡 웹·QR
- **결과**: 사용자가 운영자에게 카톡으로 자기소개·신청 동기 메시지 전송. (시각 표현은 sketch §화면1 `#apply` + 화면3 하단 CTA)
- **엣지 케이스** (시스템 동작):
    - 카톡 미설치 → 데스크톱 fallback: 카톡 ID 텍스트 노출 + 이메일 link
    - 외부 link 클릭 후 이탈 판정 — F10 분석 도구로 click 카운트
    - 카톡 채널 변경 — 운영자가 config/환경변수 한 곳 update
- **연결**: Sketch §S3 / Intent 가설 H1, H2

## F7: 반응형 layout

- **트리거**: 사용자가 다양한 device·viewport로 접속
- **동작**:
    1. Tailwind / CSS Grid·Flexbox 기반 반응형 break point (sm 640 / md 768 / lg 1024 / xl 1280)
    2. 데스크톱: 3-column card grid, 좌측 정렬 hero (gold-ratio 비대칭, brand 정합)
    3. 모바일: 1-column 세로 stack, sticky 헤더 단순화
    4. 이미지·폰트 size 비율 적용 (clamp() 또는 break point)
    5. max-width 1200px로 큰 데스크톱에서 가운데 정렬
- **결과**: 모든 디바이스에서 콘텐츠 가독·CTA 접근·navigation 가능
- **엣지 케이스**:
    - 320px 폭 (작은 모바일) → 폰트 size 줄어들되 가독 유지 (min 14px 본문)
    - landscape 모바일 → 가로 모드 깨지지 않게
    - 큰 데스크톱 (1920px+) → max-width 적용 + 좌우 여백
- **연결**: Intent 사용 맥락 B-2

## F8: 사이트 chrome (헤더·푸터)

- **트리거**: 모든 페이지 진입 시 자동 렌더
- **동작**:
    1. **헤더 (sticky top)**: 왼쪽 "Bsides" 로고 (메인으로 link) + 오른쪽 "객원 멤버 신청" CTA (메인 `#apply` 스크롤)
    2. 스크롤 시 backdrop blur 또는 opaque 처리 (콘텐츠 가리지 않게)
    3. **푸터**: 모든 페이지 하단. 운영자 이름 · 카톡 ID/오픈채팅 link · 이메일. 단순 텍스트·link. "Made with ❤️" 같은 클리셰 X
    4. 모바일: 헤더 단순화 (로고 작게 + CTA 압축)
- **결과**: 사용자가 어느 페이지에 있든 메인·신청 진입 가능. 푸터의 연락처로 신청 외 contact 가능
- **엣지 케이스**:
    - 헤더 sticky가 본문 가림 → backdrop blur + 적정 height
    - 푸터 link 잘못 → 운영자가 config에서 update
- **연결**: Sketch §S1, S3 / Intent 사용 맥락 B-1·B-2

---

# 비기능 요구사항

## 성능 (web, Google 공식 산업 표준 기준)

- **Core Web Vitals (75th percentile)**: LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1
- **Lighthouse Performance**: prototype 측정만 (참고용 — SKILL.md §5.1 stage 정책)
- **TTFB**: SSG + CDN ≤ 300ms
- **첫 화면 텍스트 노출**: ≤ 1.5s (의미 — 사용자가 "여기가 뭔지" 첫 줄을 1.5s 안에 봄)

## 보안

- HTTPS only (호스팅 기본)
- 외부 link (카톡): `rel="noopener noreferrer"`
- 사용자 데이터 수집 0 (SSG, 로그인·폼·DB 없음)
- 외부 이미지 호스팅 시 referrer policy
- CSP·security headers는 호스팅 기본값 사용

## 호환성

- 반응형: 320px~1920px (F7에서 명세)
- 브라우저: Chrome·Safari·Firefox·Edge 최신 2 메이저 버전
- 모바일: iOS Safari 15+ / Android Chrome 110+

## SEO

- 모든 페이지에 title · meta description · OG image (F6에서 명세)
- sitemap.xml + robots.txt 자동 생성
- 정규 URL · `lang="ko"`
- 페이지마다 unique title

## 접근성 (F11에서 명세, Design baseline)

- 색 대비 WCAG 2.2 AA (≥ 4.5:1 본문, ≥ 3:1 큰 텍스트)
- 모든 이미지 alt text 필수
- 시맨틱 HTML (h1·h2 위계 · `<nav>` · `<main>` · `<section>` · `<footer>`)
- 키보드 navigation (Tab 포커스 visible, Enter activate)

## 다국어

- v1 한국어만. v2 이후 검토.

## 관측성 (F10)

- 방문자 PV / UV (페이지별)
- 외부 link click 카운트 (카톡 신청 click)
- 진입 referer (organic vs 알음알음 분석 시그널)

---

# 외부 의존성 후보 (Architecture에서 확정)

| 카테고리 | 후보 | 용도 | 이유 |
|---|---|---|---|
| 호스팅 | Vercel / Netlify / Cloudflare Pages | SSG 정적 사이트 호스팅 + CI/CD | 무료 tier · git push 자동 배포 · CDN 빌트인 |
| SSG framework | Astro / Next.js / Hugo | Markdown/MDX 처리 + 정적 빌드 | 운영자 익숙도 + Markdown 친화도가 결정 기준 |
| 분석 | Vercel Analytics / Plausible | F10 방문자 분석 | zero-config · 프라이버시 friendly (쿠키 없음) |
| 콘텐츠 source | Markdown / MDX | `content/progress/[slug].md` | frontmatter + body, 운영자 git workflow와 정합 |
| 카톡 신청 채널 | **`open.kakao.com/o/bsides`** (확정) | F5 외부 신청 | 카톡 오픈채팅. v1 무료. |
| 도메인 | **`bsides.kr`** (확정) + 이메일 fallback `hi@bsides.kr` | 외부 노출 URL | Design 단계에서 확정 |

→ 구체 stack 결정은 다음 단계 Architecture.

---

# 제약조건

- **시간**: 3개월 (intent 성공 기준 — 워크샵 6회 · 출시 1건 · 멤버쉽 2명 시점). 이 안에 첫 워크샵 진행 + 첫 콘텐츠 발행 + 객원 멤버 신청 받기까지.
- **예산**: TBD — 호스팅·도메인 월 $0~$20 추정 (prototype 무료 tier 가능). v1엔 비용 0 목표.
- **규제**: 개인정보 수집 X (로그인·결제·폼 없음). 카톡 외부 link로 sensitive 데이터 처리 0. 개인정보처리방침 page는 v1엔 불필요.
- **도구**: TBD — 운영자에게 익숙한 stack 우선. Markdown 친화 SSG framework. 운영자가 Claude Code로 직접 빌드·운영하는 흐름 가정.

---

# 경쟁 / 포지셔닝 (intent 부록 A 흡수)

## 경쟁 / 대체재

- **가장 가까운 경쟁**: Disquiet (한국 메이커 로그 커뮤니티) — 타겟 유저 가장 겹침
- **유저 풀 일부 겹침**: GeekNews (개발 관심자 뉴스 소비)
- **대체재**: 유료 LLM 강의 시장 (LLM 활용법 강의 다수 존재)

## Bsides 차별점

1. 아이템 선정 → 기획 → 개발 → 디자인 → 출시 → 홍보 **전 과정을 강의·코칭으로 통합** 제공
2. **오프라인 만남·연락처 교환·검증된 멤버쉽**으로 출시 의지자들의 실제 네트워크화 (콘텐츠 소비 X, 출시까지 같이 가는 검증된 커뮤니티)

## 포지셔닝 (brand essence·Hero 보조와 정합)

> "혼자가 가능해진 시대, 출시까지 같이 가는 작은 메이커 동아리"

→ Disquiet 같은 "메이커 자기 로그" 피드와 다름. 강의·코칭·실제 출시·오프라인 네트워크가 묶인 검증된 멤버쉽. 콘텐츠 소비가 아닌 **참여형 실습 커뮤니티**.
