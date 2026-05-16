---
name: 2-brand-guide
description: Brand Guide 단계 가이드. AI 디자인·콘텐츠 에이전트가 일관 작동하기 위한 최소 시각·언어 기준을 박는다. v1-prototype은 한 장 깊이로. SKILL.md §3의 2번 단계.
---

Brand Guide는 후속 단계(PRD·Design·콘텐츠 작성·마케팅 카피)에서 AI 에이전트가 **generic하게 뽑지 않도록** baseline을 박는 단계다. 본격 brand identity가 아니라 **AI input 일관성**이 목적 — 사이클이 거듭되며 점점 정교해짐.

**LLM 한계와 직결**: SKILL.md §0.2 "LLM은 시각·UX를 못 본다 → 단계 입력으로 표준 baseline을 박는다"의 가장 직접적 적용. brand guide가 없으면 Claude Design 같은 에이전트가 generic SaaS 톤으로 뽑고, 사용자가 시각으로 검증해야 보이는 어긋남을 LLM은 못 잡는다.

## 1. 단계 목표

- **Brand essence** (한 줄) — 모든 카피·시각의 출발점
- **Voice & Tone** — 텍스트 일관성 baseline
- **시각·언어 기준** — AI 에이전트 input
- **금지 사항** — AI 슬롭 회피

플랫폼 분기:
- **UI 플랫폼**(web/mobile/desktop): 10개 항목 전부 (§1~§10)
- **비 UI 플랫폼**(cli/library/api-server): essence·voice·카피·금지 4개만 (§3~§8 시각·Tokens skip)

**§8·9(차별 시각 시그널·카피 패턴) 보강 시점**: 이 두 항목은 화면 컨텍스트가 있어야 구체화된다 — 따라서 이 단계에선 추상 방향만 박고, **다음 단계인 Sketch가 진행되며 화면이 정해질 때 보강**한다. brand-guide.md는 두 단계에 걸쳐 완성되는 산출물.

**Tokens 그룹(§4~§7) — Stage별 정밀도**: 컬러·타이포·spacing·motion 4 token 영역은 모두 stage별 정밀도 매트릭스를 따른다 (§4.1 형식 부분 참조). prototype은 방향만, mvp부턴 정량 token, prod는 full system. 이 정밀도가 시안 간 일관성·Designer/Engineer 핸드오프 품질을 결정.

## 2. 진행 절차

### 2.1 사이클 종류에 따라 분기

- **첫 사이클(v1-prototype)**: `intent.md`를 input으로 §2.2 흐름 시작. §8·9는 다음 단계 Sketch 진행 중 화면 보고 보강.
- **두 번째 이상 사이클**: 직전 brand-guide + retro 기반 업데이트. **§5 사이클 업데이트 모드** 따름.

### 2.2 인터뷰 흐름: input → 초안 → 확정

#### Step 1. Input 확인

`intent.md` (출처 스토리·문제 정의·타겟·voice 단서)를 읽고 추출 가능한 신호를 분류:

- ✅ **input에서 직접 추출**: 사용자가 채팅·intent에서 명시한 톤·정체성 신호 (예: "반말·친근하게", "그럴듯한 쓰레기 위에 사람 한 스푼")
- 🟡 **AI 추정**: 시각 무드·컬러·타이포·금지 사항 등 input에 명시 안 된 항목

#### Step 2. AI가 10개 항목(또는 비UI 4개) 초안 작성

§4.1 항목을 채워 사용자에게 보여준다. essence는 후보 2~3개 제시.

#### Step 3. 사용자 확정

- ✅는 그대로 굳히거나 다듬음.
- 🟡는 후보 중 선택 또는 다른 방향 제시.
- 빠진 부분은 `TBD: [확인할 것]`으로 표시 후 다음 단계 진입 시 재확인.

## 3. 완료 체크리스트

다음이 모두 충족되어야 다음 단계(Sketch)로 진입. §8·9는 Sketch에서 화면 컨텍스트와 함께 보강되므로 이 단계에선 **추상 방향**만 박혀도 통과.

**모든 플랫폼:**
- [ ] **Brand essence** 한 줄 — generic하지 않고 인용 가능.
- [ ] **Voice & Tone** — 톤 결정 + 예시 카피 1줄 이상.
- [ ] **카피 패턴** 최소 1개 (Hero / CTA / 섹션 등 context별 형식).
- [ ] **금지 사항** 최소 3개 (구체 패턴, 추상 표현 X).

**UI 플랫폼만 추가:**
- [ ] **시각 무드** 키워드 5개 이상.
- [ ] **Tokens — 컬러** stage별 정밀도 (prototype=방향+예시 hex, mvp=scale+대비비, prod=full token system).
- [ ] **Tokens — 타이포** stage별 정밀도 (prototype=폰트 후보+톤, mvp=type scale+weight, prod=full type system).
- [ ] **Tokens — Spacing** stage별 정밀도 (prototype=방향, mvp=scale 정량, prod=full system).
- [ ] **Tokens — Motion** stage별 정밀도 (prototype=정성 방향+금지, mvp=timing+easing, prod=full motion system).
- [ ] **차별 시각 시그널** 제품 메커니즘 → 시각 모티프 매핑 최소 1개.

미충족 시 SKILL.md §5 게이트 정책에 따라 선택지 제시.

## 4. 산출물 스펙

산출물 위치: `planning/cycles/v{N}-{label}/brand-guide.md`

### 4.1 파일 구조

각 섹션은 정해진 **형식**이 있다. 형식이 깨지면 후속 AI 에이전트가 input으로 못 쓴다.

```markdown
---
cycle: v1-prototype
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
scope: AI 디자인·콘텐츠 에이전트가 일관 작동하기 위한 최소 시각·언어 기준.
---

# 1. Brand essence
형식: **한 줄 문장**. 인용 가능·차별성 있음.
*왜*: 모든 카피·시각의 출발점. essence가 generic하면 AI가 generic하게 뽑는다.

# 2. Voice & Tone
형식: **톤 결정(반말/존댓말·친구/멘토·진지/가벼움) + 1줄 설명 + 예시 카피 1줄**.
*왜*: 모든 텍스트의 일관성 baseline. AI 글 가공·UI 마이크로카피의 디폴트.

# 3. 시각 무드 (UI 플랫폼만)
형식: **키워드 5~7개 + 한 줄 정서 설명**.
*왜*: AI 디자인이 어떤 mood로 뽑을지의 baseline. 키워드만으로 instant alignment.

# 4. 컬러 (UI 플랫폼만) — Tokens 그룹

형식: **stage별 정밀도** 강제 (아래 매트릭스).
*왜*: AI 디자인이 컬러 결정 시 input. prototype은 explore, mvp부턴 정합 lock. 시안 간 컬러 해석 차이를 stage 정밀도로 해소.

| Stage | 컬러 정밀도 |
|---|---|
| `v*-prototype` | Primary·Accent·Neutral **방향 + 후보 hex 1~2개** (예시용) + 회피 색상 |
| `v*-mvp` | **Primary·Accent·Neutral 50-900 scale** (10단계 hex) + dark variant + WCAG AA 대비비 검증 (≥4.5:1 본문, ≥3:1 큰 텍스트) |
| `v*-prod` | Full token system + dark mode token set + semantic role tokens (success·warn·error·info) |

# 5. 타이포 (UI 플랫폼만) — Tokens 그룹

형식: **stage별 정밀도** 강제.

| Stage | 타이포 정밀도 |
|---|---|
| `v*-prototype` | 본문·헤딩·Accent **폰트 후보 + 톤** + 사용 규칙 (예: "손글씨 2회/페이지 max") |
| `v*-mvp` | **Type scale 정량** (modular 36/28/22/16/13 등) + weight 위계 (regular/medium/semibold/bold) + line-height + letter-spacing |
| `v*-prod` | Full type system + responsive scale (clamp() 또는 break point) + 다국어 폴백 |

# 6. Spacing (UI 플랫폼만) — Tokens 그룹

형식: **stage별 정밀도** 강제.
*왜*: layout 일관성·시각 위계의 기본. 8pt grid 같은 산업 표준이 일관 적용되어야 시안 간 정합.

| Stage | Spacing 정밀도 |
|---|---|
| `v*-prototype` | "숨 쉬는 여백" 방향 + scale 1~2개 후보 (예: "Tailwind default보다 한 단계 넓게") |
| `v*-mvp` | **Scale 정량** (예: 4/8/12/16/24/32/48/64) + component spacing 가이드 (padding·gap) |
| `v*-prod` | Full spacing system + responsive scale + layout grid system |

# 7. Motion (UI 플랫폼만) — Tokens 그룹

형식: **stage별 정밀도** 강제.
*왜*: motion은 brand의 일부 (Apple HIG·Material 모두 motion을 brand로 명시). AI는 timing 명시 안 하면 generic 200ms ease로 끝남.

| Stage | Motion 정밀도 |
|---|---|
| `v*-prototype` | 정성 방향 (subtle/spring/즉각·느림 등) + 금지 ("과한 parallax·자동 carousel·5초+ entrance 금지" 정도) |
| `v*-mvp` | **Timing 정량** (color/opacity 160ms · transform 120ms · layout 250ms) + easing curve (ease-out · spring) |
| `v*-prod` | Full motion system (entrance · exit · loop · focus · gesture) + reduced-motion 폴백 |

# 8. 차별 시각 시그널 (UI 플랫폼만)
형식: **제품 메커니즘 → 시각 모티프 매핑** 최소 1개.
*왜*: AI는 product mechanic을 시각화하는 발상을 못 한다. 명시 안 하면 generic flat card로 끝남.

# 9. 카피 패턴
형식: **컨텍스트(Hero/CTA/푸터 등)별 패턴 + ✅/❌ 예시 1줄**.
*왜*: 카피 작성 시 AI가 따라야 할 lint.

# 10. 금지 사항 (AI 슬롭 회피)
형식: **구체 패턴 리스트 (최소 3개)**. "AI 같지 않게" 같은 추상 X.
*왜*: AI는 "안 해야 할 것"을 명시 안 하면 디폴트로 뽑는다. negative 명시가 가장 효율적.
```

### 4.2 frontmatter 규칙

- `cycle`: 현재 사이클 라벨.
- `created_at` / `updated_at`: 최초 생성일 / 최근 수정일.
- `scope`: 한 줄로 이 brand guide의 적용 범위·깊이. v1엔 "AI 에이전트 일관 작동 baseline" 정도.

## 5. 사이클 업데이트 모드 (v2 이상)

새 사이클의 brand guide는 직전 사이클 산출물을 base로. 백지 시작 금지.

### 5.1 첫 질문

```
v1-prototype 회고 보니 [brand 관련 발견 한두 줄]였어. v2-mvp brand guide 어떻게 업데이트할까?
- essence: v1 유지 / 다듬기 / 교체
- voice: v1 유지 / 조정
- 시각 무드: 유지 / 키워드 추가·제거
- 컬러: 방향 유지 + hex 확정 / 교체
- 금지 사항: 유지 / 추가 (실제 슬롭 발견 항목)
```

### 5.2 업데이트 원칙

- **덮어쓰기 금지**: 변경 시 이유를 본문 한 줄 메모. 예: "v1엔 따뜻한 orange였지만 v2엔 terracotta로 — 이유: 화면 테스트 결과 orange가 hype 톤이 강함."
- **검증된 항목 보존** + "(v1에서 검증됨)" 마킹.
- **`updated_at` 갱신**, `cycle`을 새 라벨로.

## 6. 좋은 예 vs 나쁜 예

### 6.1 Brand essence

**좋은 예** (차별·인용 가능):
> LLM이 만든 그럴듯한 쓰레기 위에, 사람 한 스푼.

**나쁜 예** (generic·교환 가능):
> 함께 성장하는 메이커 커뮤니티.

### 6.2 Voice & Tone

**좋은 예** (톤 + 예시):
> 친구 같은 동료 톤. 반말 OK. 영감 주되 hype 없음.
> 예시 카피: "혼자가 가능해진 시대, 그래도 같이 가자."

**나쁜 예** ← 톤만, 예시 없음:
> 친근하게.

### 6.3 금지 사항

**좋은 예** (구체 패턴):
> - 그라데이션 글로우 (purple-pink, blue-cyan)
> - typical SaaS 3-column features grid
> - 영문 hype 카피 ("AI-powered", "Revolutionize", "10x")

**나쁜 예** ← 추상:
> AI 같은 디자인 피하기.

## 7. 사용자 응대 톤 + 인터뷰 코칭

톤·코칭은 SKILL.md §1.3·§1.4 따름. 핵심 동작:

- §2.2 3-step 순서: input 확인 → AI 초안(✅/🟡) → 확정. Step 건너뛰기 금지.
- 사용자가 brand 영역을 어색해하면 후보 2~3개 제시 → 선택. essence는 항상 후보 형태로.
- 시각 항목(🟡) 추정은 intent의 metaphor·사용 맥락·금지 사항에서 파생. 임의 추정 금지.
- 정리한 산출물을 보여주고 "이거 맞아? 고칠 데 있어?" 확인.
- 모르는 부분은 `TBD: ...`로 명시.
