---
cycle: v1-prototype
created_at: 2026-05-11
updated_at: 2026-05-11
scope: AI 디자인·콘텐츠 에이전트(Claude Design 등)가 일관 작동하기 위한 최소 시각·언어 기준. v1 검증 사이클용 한 장. 본격 brand identity는 v2 이후.
---

# 1. Brand essence (한 줄) ✅

> **"AI가 만든 그럴듯한 초고 위에, 감성 한 스푼."**

intent.md 출처 스토리(자기 경험)의 "LLM이 만든 그럴듯한 결과물에 사람 손이 안 가면 실제로 쓸만해지지 않는다"는 인사이트의 카피 표현. **"초고"** = 글쓰기·창작 영역 용어, 첫 원고. **"감성"** = 정량 spec 너머의 정서·맥락·취향 — 사람만 더할 수 있는 한 스푼. 인용 가능 라인이고 차별성 강함. 모든 카피·시각의 출발점.

# 2. Voice & Tone ✅

intent.md + 사용자 cycle 톤(memory 저장됨)에서 직접 추출.

- **친근·반말 OK, 존댓말도 OK** — 상황에 따라. 디폴트는 친근.
- **친구 같은 동료 톤** — 위에서 가르치는 멘토 톤 X. 멘토와 객원이 수평.
- **따뜻함 + 솔직함 한 스푼** — 영감 주되 hype 없음. "혁신적인", "혁명", "10x" 같은 마케팅 클리셰 X.
- **진지함 위에 가벼움** — 기능 설명은 정확하게, 그 위에 부드러운 농담 한 줄 OK.
- **인간 감성 한 스푼** — AI가 한 일과 사람이 한 일을 솔직히 구분. "이건 LLM이 가공했고, 이 한 스푼은 우리가 더했어" 같은 투명함.

# 3. 시각 무드 ✅

키워드 7개. 다음 디자인 산출물에 일관 적용.

- **미니멀 + 따뜻함** — over-designed X, 그러나 차갑지 않음
- **아날로그 한 스푼** — 종이 결·수기 메모·손글씨 accent. AI 슬롭의 매끈함 위에 사람의 결을 얹는 시각화
- **정성** — 작은 디테일 (간격·여백)을 정확히. 화려함 대신 정직한 정렬
- **노트 같음** — 일기·메모·아이디어 노트의 정서. 완성품보다 진행 중인 느낌
- **warm neutral** — 베이지·아이보리·연한 sand 베이스. 흰색보다 살짝 따뜻함
- **일러스트·도식 우선** — AI 이미지가 콘텐츠 자산이지만, UI 자체는 stock 사진 회피. 손그림 같은 일러스트·도식이 더 정합
- **숨 쉬는 여백** — Tailwind 디폴트 spacing보다 한 단계 넓게. 정보 밀도 낮음이 미덕

# 4. 컬러 (Tokens) ✅ — Stage: prototype (방향)

구체 hex·scale은 mvp 사이클에서 lock. v1엔 방향만.

- **Primary (배경·neutral)**: warm neutral — 베이지·아이보리·연한 sand. 흰색 X, cool gray X.
- **Accent (강조·CTA·링크)**: **olive** (따뜻한 saturated, 차분한 자연 톤. neon·vivid 회피). brand essence의 "정성·아날로그 한 스푼" 정서와 정합.
- **Text neutral**: warm gray (검정 대신 따뜻한 회색·dark brown 톤)
- **다크모드**: v1 X. v2 검토.

# 5. 타이포 (Tokens) ✅ — Stage: prototype (폰트 후보 + 톤)

Type scale·weight·line-height는 mvp 사이클에서 lock.

- **본문**: Korean-friendly sans-serif (Pretendard, Spoqa Han Sans, IBM Plex Sans KR 후보)
- **헤딩**: 동일 sans 또는 약간 grotesque 톤. 강세는 size·weight 차이로 (장식 X)
- **Accent (선택)**: 손글씨 폰트 1개. Hero subtitle·section divider 같은 곳에 매우 절제해서 사용. **2회/페이지 max** — 남용하면 cluttered
- **영문 혼용**: Inter·IBM Plex Sans 같이 Korean sans와 시각 호환 되는 것

# 6. Spacing (Tokens) ✅ — Stage: prototype (방향)

Scale 정량(예: 4/8/12/16/24/32/48/64)은 mvp 사이클에서 lock.

- **"숨 쉬는 여백"** — Tailwind 디폴트 spacing보다 한 단계 넓게. 정보 밀도 낮음이 미덕 (§3 시각 무드와 정합)
- **8pt grid 기반** — Apple HIG·Material 표준. Design 단계에서 Claude Design이 자연 적용
- **컴포넌트 spacing**: 카드 padding·section gap·헤딩 below·CTA above 모두 generous하게. 답답함 회피
- **회피**: 12-column grid의 강제 균등 분할 — brand 정합 X (§3 "정직한 정렬"·"숨 쉬는 여백"과 충돌)

# 7. Motion (Tokens) ✅ — Stage: prototype (정성 방향)

Timing·easing 정량은 mvp 사이클에서 lock.

- **즉각성** — 사용자 액션 → 반응은 즉시. delay 없는 transition (성능·정성)
- **subtle** — 과한 entrance·parallax X. 의미 있는 변화만 motion (focus 이동·상태 전환 등)
- **brand 정합 = "정성의 motion"** — bouncy·playful은 아님. 차분하고 정확하게 (note의 종이 한 장 넘기는 느낌)
- **금지**:
    - 자동 carousel·slider (사용자 컨트롤 박탈)
    - 5초+ entrance·loading animation
    - parallax 과도 (스크롤마다 시각 요소 큰 이동)
    - 깜빡임·pulse 강조 (광고 톤)
- **reduced-motion 폴백**: v1엔 명시 X (mvp 이상), 다만 transition 자체가 subtle이라 reduced-motion 환경에서도 큰 문제 X

# 8. 차별 시각 시그널 ✅

intent.md 메커니즘을 시각화하는 패턴. Design 단계에서 화면 구성 시 이 모티프를 일관 사용. **sketch.md 화면 매핑**도 함께 명시.

- **"한 사이클, 한 멤버, 서비스 출시" (운영방식)** → 화살표 chain · 바통 패스 모티프 · 단계 indicator
  → 적용: 메인 화면 "운영방식 — 한 사이클, 한 멤버, 서비스 출시" 4단계 카드 (소개→수업→출시→릴레이) 사이의 화살표 chain
- **"객원 → 정식 멤버 전환"** → 단계·상태 변화 카드 (객원 카드가 다음 단계 카드로 이어지는 시각화). **4단계 명시**: 객원 참여 → 운영자·멤버 심사 → 약관 동의 → 정식 멤버
  → 적용: "운영방식" 다음 섹션에 별도 카드로 4단계 흐름 시각화
- **"학습자료 누적·진행상황"** → 카드 스택 · timeline · 진행 row (수직 누적이 자연스러움)
  → 적용: 메인 "최근 진행상황" 카드 그리드 + `/progress` 회차별 카드 그리드 (최신순). 카드 간격·padding은 §3 "숨 쉬는 여백" 적용
- **"감성 한 스푼"** → 손글씨 accent · 수기 sticky note · 아날로그 텍스처가 LLM 가공 콘텐츠 위에 layered
  → 적용: `/progress/[slug]` 학습자료 상세에서 AI 생성 이미지·LLM 가공 글 위에 운영자 손글씨 메모·테두리 sticky note 1~2개 (사람이 더한 부분 명시)
- **🌟 Mascot 스푼이 (Spooni)** → "감성 한 스푼"을 들고 다니는 작은 반죽 친구. 5포즈 보유
  → 적용:
    - **Primary 포즈** (스푼·노트북 보유): 메인 페이지 hero 보조 영역·about 페이지
    - **고민하는 포즈**: 빈 상태·검색 결과 0건
    - **기뻐하는 포즈**: 출시 완료·회차 종료
    - **기록하는 포즈**: 진행상황·회차 노트
    - **자는 포즈**: 404·모집 종료
  → 색·금지·크기 기준은 design-system.html mascot 섹션 참조. 본문 텍스트는 절대 mascot으로 대체하지 않음.

# 9. 카피 패턴 ✅

`sketch.md`의 화면별 컨텍스트에 매핑된 패턴.

- **Hero (메인 상단)**: 짧고 강렬한 한 줄(essence) + sup-label + 보조 한 줄 + CTA 2개. 좌측 정렬, 우측엔 sticky note 비대칭 layered. 가운데 정렬은 금지(§10).
  → 확정:
    - **sup-label**: "메이커 동아리 · v1 객원 멤버 모집"
    - **제목**: "AI가 만든 그럴듯한 초고 위에, 감성 한 스푼."
    - **보조**: "혼자 개발이 가능해진 시대지만, 각자의 전문성을 더해서 멋진 것을 만드는 작은 프로젝트 팀을 만들어 드려요."
    - **CTA primary**: "객원 멤버 신청하기 →"
    - **CTA secondary**: "진행상황 먼저 둘러보기 →"
- **CTA**: 동사로 시작 + 구체 행동. ✅ "객원 멤버 신청하기" · "카톡으로 신청하기" · "진행상황 먼저 둘러보기" / ❌ "더 알아보기" · "지금 시작"
- **섹션 헤딩**: sup-label (영문, uppercase, olive) + 한국어 heading 패턴. 예: "How it works / 운영방식 — 한 사이클, 한 멤버, 서비스 출시" · "Now running / 이번 사이클 멤버" · "Latest / 최근 진행상황" · "Apply / 객원 멤버 신청"
- **진행상황 제목**: `[N회차] [날짜] · 멤버 [이름]` 패턴 + 본문 제목. 예: `3회차 · 2026-05-04 · 멤버 김도현` + `미미로그 출시 후기와 다음 사이클`
- **이번 사이클 멤버 카드 메타**: `멤버:`·`학습자료:`·`진행 회차:`·`다음 워크샵:` 정직한 label. label 위에 emoji X. live pill로 "다음 워크샵 D-N" 또는 "N/M회차 진행 중"
- **신청 섹션 (`#apply`)**: 안내문 짧고 친근 + 신청 후 안내 3줄 (① 운영자 카톡 응답 / ② 다음 워크샵 일정 안내 / ③ 화상/오프라인 합류) + 카톡 외부 link + 이메일 fallback ("카톡이 어렵다면 hi@bsides.kr로 보내도 OK")
- **푸터**: 한 줄 description ("혼자가 가능해진 시대, 출시까지 같이 가는 프로젝트 팀 빌딩 및 재능 품앗이 서비스.") + 운영자 이름·카톡·이메일. "Made with ❤️" 같은 클리셰 X.

# 10. 금지 사항 ("AI 슬롭" 회피) ✅

- 그라데이션 글로우 (purple-pink, blue-cyan 같은)
- 과한 이모지 — 페이지당 1개 max, 의미 있을 때만
- typical SaaS 패턴 — 3-column features grid · 중앙 정렬 hero stack · "Powered by AI" 식 뱃지
- 영문 hype 카피 — "AI-powered launchpad", "Revolutionize your...", "10x your..."
- 매끈한 stock 이미지 — generic 협업 사진·웃는 팀 사진 X
- 색만으로 강조 — text weight·size 우선. 색은 보조
- 너무 매끈한 일러스트 — flat·corporate 느낌의 일러스트 X. 손그림 결이 있는 것
- typical "AI 텍스트" 톤 — "여러분", "함께 성장하는", "Innovative" 같은 generic 카피

---

# 적용 — Design 단계 결과 반영 ✅

Claude Design 핸드오프 결과(Bsides.html · design-system.html)가 SoT. brand-guide.md는 그 결과의 카피·시그널·운영 모델을 흡수.

**Hero (메인 상단)**:
- sup-label: "메이커 동아리 · v1 객원 멤버 모집"
- 제목: "AI가 만든 그럴듯한 초고 위에, 감성 한 스푼."
- 보조: "혼자 개발이 가능해진 시대지만, 각자의 전문성을 더해서 멋진 것을 만드는 작은 프로젝트 팀을 만들어 드려요."
- CTA: "객원 멤버 신청하기 →" / "진행상황 먼저 둘러보기 →"

**Footer**: "혼자가 가능해진 시대, 출시까지 같이 가는 프로젝트 팀 빌딩 및 재능 품앗이 서비스." + 운영 현지 · 카톡 @bsides · hi@bsides.kr

**핵심 시그널 흡수**:
- Mascot 스푼이 (5포즈) — §8 차별 시각 시그널에 추가됨
- Sticky note 3색 + rotation + hand-drawn underline·arrow — §3 시각 무드·§8 시그널 구체화
- Live pill (warm rust pulse) — "이번 사이클 멤버" 카드의 D-N · "N/M회차 진행 중" 표시
- 객원 → 정식 멤버 4단계 시각화

Token 정량(컬러 hex·type scale·spacing scale·shadow·radii)은 design-system.html에 SoT 보존. v1 brand-guide.md는 방향만(prototype stage). mvp 사이클에 token 흡수.
