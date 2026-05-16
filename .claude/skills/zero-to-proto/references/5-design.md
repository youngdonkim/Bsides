---
name: 5-design
description: Design 단계 가이드. UI 플랫폼(web/mobile/desktop)에서 Claude Design을 활용해 모든 화면 + 엣지까지 hi-fi 디자인 코드로 받고, PRD·Brand Guide·Sketch와의 정합성 점검 후 한쪽으로 정리해 기획 마감. SKILL.md §3의 5번 단계.
---

Design은 **PRD·Brand Guide·Sketch를 받아 hi-fi 디자인 코드로 옮기는 단계**다. Sketch는 핵심 화면 3~7개의 골격만 다뤘고, Claude Design이 이걸 받아 모든 화면 + 엣지(에러·빈·로딩·권한·오프라인) + 인터랙션 상태 + 디자인 시스템까지 자동 확장한다. **`brand-guide.md`는 Claude Design의 가장 직접적 input** — 핸드오프 시 voice·시각 무드·컬러·타이포·차별 시각 시그널·금지 사항을 명시적으로 전달. **이 디자인 코드가 다음 단계 Architecture의 진실의 원천**이 된다 — Architecture에서 디자인 base로 기술 스택·data-model·API 명세·마이그레이션 계획을 결정.

> **Claude Design 공식 docs — 진입 전 필독**: https://support.claude.com/en/articles/14604416-get-started-with-claude-design
>
> Anthropic Labs 연구 미리보기 단계 (Pro/Max/Team/Enterprise 요금제). **실험적 상태로 안정성 한계 있음** — 아래 §3.7 한계점 사전 숙지.

## 1. 단계 적용 범위

- **적용**: `platform` 또는 `platforms`에 UI 플랫폼이 포함된 경우 (`web` / `mobile` / `desktop`).
- **Skip**: `cli` / `library` / `api-server` 단독이면 이 단계 skip하고 PRD에서 바로 Architecture(6단계)로.
- **Cross-platform**: 메인 플랫폼이 UI거나 platforms 안에 UI가 하나라도 있으면 적용. 모든 UI 플랫폼 화면 다 받음.

## 2. 단계 목표

- **모든 화면 + 엣지 화면**(에러·빈 상태·로딩·권한 거부·오프라인)을 hi-fi 디자인 코드로 받기.
- **산출물을 cycle 폴더에 보존** (`planning/cycles/v{N}-{label}/design/`).
- **PRD·Sketch와의 정합성 점검 + 한쪽 정리해 기획 마감**.

## 3. 진행 절차

### 3.1 사이클 분기

- 첫 사이클이고 `design/` 비어있음: Claude Design 신규 호출.
- 첫 사이클인데 이미 있음: 내용 검증 + 빠진 화면·엣지 보완.
- 두 번째 이상 사이클: 직전 디자인 base + retro 기반. 변경된 부분만 재의뢰.

### 3.2 Receiving 방식 결정

Claude Design 공식 export 6가지 (공식 docs 기준):

| # | 방식 | zero-to-proto 사용 |
|---|---|---|
| 1 | Claude Code 핸드오프 (로컬 에이전트 또는 웹) | △ 사용 가능 — 단 핸드오프 결과가 SoT가 안 됨 |
| 2 | Download ZIP | △ 사용 가능 — 풀어서 보존 |
| **3** | **★ HTML 독립형 파일 (`design-system.html` + `screens.html`)** | **✅ 디폴트** — `design/files/`에 두 파일 저장. SoT |
| 4 | PDF 내보내기 | ❌ 코드 아님. 검토·공유용만 |
| 5 | PPTX 내보내기 | ❌ 코드 아님. 프레젠테이션용만 |
| 6 | Canva 전송 | ❌ 코드 아님 |

**디폴트 = 3번 (HTML 두 파일)**. 이유:
- 가장 가벼움 — 두 파일만으로 정합성 점검·디자인 시스템·화면 모두 cover (§3.5 자동 점검 가능)
- 사람·AI 둘 다 빠르게 검토 가능 — 브라우저로 즉시 렌더링 확인
- v1-prototype 검증 단계엔 React 컴포넌트 코드 깊이까지 불필요. Architecture 단계가 디자인 코드를 받아 스택 결정하므로 HTML이면 충분

zip·핸드오프는 인터랙션 코드·React 컴포넌트가 필요한 큰 사이클(v2-mvp 이상)에서 검토 가능.

조직 내 공유 link (보기/댓글/편집 권한) — 운영자와 review 시 사용.

### 3.3 Claude Design 활용 입력 정리

공식 docs는 효과적인 프롬프트의 4요소를 명시: **목표 · 레이아웃 · 콘텐츠 · 대상 사용자**. cycle 산출물에서 이 4요소로 정리해 사용자에게 제시.

| 공식 4요소 | cycle 산출물에서 추출 |
|---|---|
| **목표** (무엇을 만드는가) | `intent.md` 문제 정의 + 핵심 가설 + `prd.md` 기능 목록 Must·Should |
| **레이아웃** (어떻게 배치) | `sketch.md` 화면별 진입 경로·주요 컴포넌트·전환 + 시나리오 ↔ 화면 매핑 표 + `prd.md` Must 명세. **`sketch-wireframes.md`(ASCII)는 핸드오프에 미포함** — layout anchor 회피 |
| **콘텐츠** (어떤 정보 표시) | `sketch.md` 화면별 컴포넌트 + `prd.md` 기능 명세의 결과·메타 |
| **대상 사용자** (누가 사용) | `intent.md` 타겟 사용자 + 사용 맥락 |

추가 입력 (공식 docs 패턴 + zero-to-proto 보강):

- **★ `brand-guide.md` 전체** — 공식 docs "자동 브랜드 적용"이 작동하려면 brand 정보가 input으로 들어가야 함. essence·voice·시각 무드·컬러·타이포·차별 시각 시그널·카피 패턴·금지 사항 모두 명시 전달.
- **플랫폼·platforms** (`prd.md` frontmatter, 4-prd §2.2에서 결정) — 반응형 범위·iOS/Android 일관성 결정
- **비기능 요구사항** (`prd.md`) — 접근성·반응형·성능 임계값
- **★ 횡단 UI/UX 표준** (있으면) — `.claude/rules/ui-ux-baseline.md` 등. 매 cycle 공통 baseline (인터랙션 5상태·다크모드·접근성·반응형·외부 브랜드 island)
- **컨텍스트 첨부** (선택) — 기존 스크린샷·이미지·자산·코드 저장소 link

공식 docs 권장 — **단순함에서 시작 → 복잡성 추가, 2~3가지 대안 요청, 반응형 조기 고려**.

Claude Design 작업 시 다음을 모두 요청 (AI가 사용자에게 보여줄 체크리스트):

- Sketch 핵심 화면 + Sketch에 없던 보조 화면(설정·도움말·계정·약관·온보딩 등).
- **엣지 화면**: 빈 상태·로딩·에러·권한 거부·네트워크 오프라인.
- **디자인 시스템** 별도 (컬러 토큰·타이포 스케일·간격·컴포넌트).
- **인터랙션 상태**: hover·active·disabled·focus·loading. 각 상태별 시각 명세(색 단계·transition timing·transform·focus outline)까지. 단순 "hover 시 어둡게" 수준이 아니라 **디자인 시스템 문서에서 코드(globals.css 등)로 직접 매핑 가능한 정밀도**.
- (cross-platform이면) 모든 UI 플랫폼 — iOS/Android/web 별 화면 분리 또는 공통 인터페이스 명시.

### 3.4 산출물 보존

**디폴트 (3번 HTML 두 파일)**:
- `design/files/design-system.html` — 디자인 시스템 (컬러 토큰·타이포 스케일·간격·컴포넌트)
- `design/files/screens.html` — 모든 화면 + 엣지 화면

기타 방식 (예외):
- **handoff 명령** (1번): AI가 URL fetch → 받은 코드 `design/files/`에 저장. 명령 사본 `design/handoff-command.txt`.
- **zip** (2번): 사용자가 풀어 `design/files/`.

### 3.5 정합성 점검 + 최종 기획 마감

Claude Design은 별도 과정이라 디자인 만드는 중 화면·기능·데이터 형태가 추가/변경되는 게 흔하다. **PRD·Sketch와의 정합성 점검 후 한쪽으로 정리해 기획 마감**한다. **이 단계가 끝나면 기획은 frozen** — 다음 6단계 Architecture는 이 디자인 코드를 진실의 원천으로 받음.

#### 자동 점검 (AI 단독)

PRD·Sketch를 읽고 디자인 코드와 비교. 4 카테고리:

1. **디자인에만 있음** (디자인이 진화한 부분): 새로 추가된 화면·기능·UI 요소.
2. **문서에만 있음** (디자인에서 누락된 부분): PRD Must 기능 중 화면 없음 / Sketch 시나리오 중 cover 안 된 것.
3. **충돌**: 이름·동작이 다름 (예: PRD는 '검토 시작' 버튼, 디자인은 '대조 시작').
4. **암묵적 결정**: 디자인 코드가 가정한 부분 (인증 흐름·에러 처리·로딩 상태 등) 중 PRD 명시 안 된 것.

추가로 **공통 누락 점검** (UI 플랫폼 표준):
- 엣지 화면(빈·에러·로딩·권한 거부·오프라인)
- 인터랙션 상태(hover·active·disabled·focus)
- 접근성 표시(스크린리더·키보드 네비)
- 다국어 레이아웃·다크모드

> data-model·API 명세 등 Architecture 차원 갭은 6단계에서 점검 — Architecture가 이 디자인 코드를 base로 결정되기 때문에 거기서 자연 정리됨.

#### 결과 보고 + 사용자 결정

```
정합성 점검 결과 — 갭 [N]개:

1. 디자인에만 있음 ([n1]): [목록]
   → 추천: PRD에 반영 (디자인이 더 진화한 거)
2. 문서에만 있음 ([n2]): [목록]
   → 추천: 디자인에 추가 또는 PRD에서 제거
3. 충돌 ([n3]): [목록 + 어느 쪽이 맞는지 분석]
   → 사용자 결정 필요
4. 암묵적 결정 ([n4]): [목록]
   → 추천: PRD에 명시화
5. 공통 누락 ([n5]): [목록]

각 항목 결정해줘. 또는 일괄: "다 디자인 우선" / "다 문서 우선".
```

#### 한쪽으로 정리 (AI가 실행)

사용자 결정에 따라:
- **디자인 우선**: PRD·Sketch 업데이트 (디자인 반영).
- **문서 우선**: 디자인 코드 재작업 (Claude Design 재호출 또는 직접 수정) 또는 그 부분 빌드 제외.
- **항목별**: 위 둘 혼합.

변경 내역을 `design/index.md`에 "정합성 정리" 섹션으로 기록.

#### 기획 마감

이 단계 통과 = 디자인·문서 정합성 OK = **기획 frozen**. 6단계 Architecture는 이 디자인 코드를 base로 기술 결정 진행.

### 3.6 Dual-pass 탐색 패턴 (prototype default)

prototype 사이클에선 brand-guide의 Tokens(컬러·타이포·spacing·motion)가 방향만 박혀있어 시안 간 해석 차이가 자연. **2번 요청해서 비교**하는 패턴이 정합 — Apple 디자이너의 explore-converge 표준.

| Stage | dual-pass 권장 |
|---|---|
| `v*-prototype` | **권장 default** — Tokens 미확정 상태에서 alternative explore + 비교로 결정 신뢰도 ↑ |
| `v*-mvp` 이상 | Single-pass — Tokens fix됨, 변경 범위 좁음. 큰 redesign 시만 dual-pass |

#### Dual-pass prompt 템플릿

핵심 — **2차에 explore할 dimension 1개 명시 강제**. 추상 "다른 관점에서"는 LLM이 random 변경할 위험.

```
1차 요청: brand-guide.md 그대로 적용한 시안 — Tokens·voice·시각 시그널 lock.

2차 요청: brand-guide.md essence·voice 유지하되, [dimension] 차원만 다르게 explore.
  dimension 옵션 (하나만 골라):
  - color: 현재 accent → 다른 자연 톤 (예: warm olive → terracotta·sage·rust)
  - typography: 현재 sans → serif/handwritten accent 추가 또는 type scale 변경
  - layout: 현재 stack → asymmetric grid / centered / hero-large 등
  - motion: 현재 정적 → subtle parallax / spring entrance / staggered reveal
  - spacing: 현재 default → compact / expansive
```

#### 비교 결과 process

두 시안 받은 뒤 사용자에게:

```
1차·2차 비교 결과:
- 1차 lock 디폴트 / 2차 인사이트만 retro 기록 (보수적 — Tokens 안정)
- 2차로 전환 (1차 폐기, 새 방향 채택)
- 요소 mix (예: 1차 layout + 2차 color)

결정해줘. 또는 추가 dimension으로 3차 explore.
```

비교 결과는 `design/index.md` "탐색 기록" 섹션에 한 줄 — "v1 cycle: 1차 olive, 2차 terracotta 비교 → 1차 채택, 2차 인사이트 = '진행상황 카드에 살짝 채도 accent 시도 가능'".

### 3.7 Claude Design 한계점·운영 팁 (공식 docs 기준)

진행 중 마주칠 수 있는 한계 — 사전 숙지.

| 증상 | 대응 |
|---|---|
| **인라인 댓글이 읽히기 전 사라짐** | 인라인 댓글 대신 **채팅으로 붙여넣기 권장**. 인라인은 빠르게 처리되는 작은 수정에만. |
| **컴팩트 뷰 저장 오류** | **전체 뷰로 전환** 후 재시도. |
| **대규모 코드베이스 입력 시 처리 실패** | 전체 monorepo 대신 **특정 하위 디렉토리 link**로 좁혀 전달. |
| **`chat upstream error` 발생** | 같은 프로젝트 내 **새 채팅 탭** 시작. 컨텍스트는 프로젝트가 보유. |

**반복 작업 패턴 (공식 권장)**:

- **채팅**: 광범위 변경 (색·레이아웃 재정렬 등). 디폴트.
- **인라인 댓글**: 특정 요소 작은 수정 (버튼 padding·드롭다운 등). 단 사라질 위험.
- **버전 보존**: `"Save what we have and try a completely different approach"` 같이 명시 요청. 현재 버전 보존 후 새 방향 시도.
- **대안 요청**: "2~3가지 다른 방향으로 보여줘" — 단일 결과보다 비교 가능.

**실험적 상태 주의**: Anthropic Labs 연구 미리보기 단계. 안정성·기능 변경 가능성 있음. 결과물 받자마자 `design/files/`에 즉시 보존 (zip 다운로드 권장).

## 4. 완료 체크리스트

- [ ] **모든 화면 + 엣지** 산출물에 포함됨 (없으면 placeholder로 명시).
- [ ] **디자인 시스템** 별도 추출 또는 명시.
- [ ] **인터랙션 상태 표현** — hover/active/disabled/focus/loading 각각의 시각 명세(색 단계·timing·transform·focus outline)가 **디자인 시스템 문서에 박혀있고** 코드로 그대로 매핑 가능. "hover 어둡게" 같은 추상 표현은 미달 (실패 사례: v1-prototype cycle에서 체크는 통과됐으나 실제 명세 누락 → `planning/cycles/v1-prototype/design/interactions-spec.md` 회고 산출물로 보강).
- [ ] **자산 정량 명세** (UI 플랫폼 — 성능 직결. 미달 시 LCP·번들 사고): 폰트(subset 또는 dynamic subset 명시, full webfont 금지), 이미지(WebP/AVIF + responsive size 명시), 애니메이션 timing(color/opacity 160ms · transform 120ms 등 specific value).
- [ ] **`design/files/`** 산출물 보존됨.
- [ ] **§3.5 정합성 점검 통과** — 디자인·문서 갭 0 또는 사용자 결정으로 정리 완료. 변경 내역 `design/index.md`에 기록됨.
- [ ] **`design/index.md`** 화면 목록·receiving 방식·정합성 정리 결과.

## 5. 산출물 스펙

위치: `planning/cycles/v{N}-{label}/design/`.

```
design/
├── index.md                    ← 진입점 + 정합성 정리 결과
└── files/                      ← 산출물 (디폴트: HTML 두 파일)
    ├── design-system.html      ← 디자인 시스템 (디폴트 — 3번 방식)
    ├── screens.html            ← 모든 화면 + 엣지 (디폴트 — 3번 방식)
    └── ...                     ← (예외) handoff-command.txt / zip 풀린 내용 등
```

> `migration-analysis.md`·`migration-plan.md`는 6단계 Architecture 산출물로 이동.

`design/index.md` 구조:

```markdown
---
platform: ...
cycle: v1-prototype
receiving_method: handoff | web | zip | html
created_at: YYYY-MM-DD
---

# 화면 목록
- 핵심: 홈·체크리스트·공유·...
- 보조: 설정·도움말·계정·...
- 엣지: 빈 상태·에러·로딩·권한 거부·오프라인

# Receiving
방식: Send to local coding agent. 명령 사본 → handoff-command.txt.

# 정합성 정리 결과 (§3.5)
- 디자인에만 있던 화면 [N]개 → PRD에 반영 (F4 권한 요청 등)
- PRD에만 있던 기능 [M]개 → 디자인 추가 또는 PRD에서 제거 결정
- 충돌 [P]개 → ...
- 결과: 기획 frozen, 6단계 Architecture 진입 준비
```

## 6. 사이클 업데이트 모드 (v2 이상)

### 6.1 stage별 디자인 진행 룰

| 사이클 stage | 디자인 진행 |
|---|---|
| `v*-prototype` | Claude Design **신규 호출** → `claude-design-code/` SoT 보존 |
| `v*-mvp` 이상 | **Claude Design 재호출 X**. prototype에서 받은 디자인으로 이미 구축된 `src/` 코드를 직접 수정. `claude-design-code/` frozen 유지. |

**왜 mvp 이상에선 Claude Design 재호출 X**:
- mvp는 prototype 검증된 스택·`src/` 코드로 **베타 모집·정량 검증이 우선**. 디자인 형태 변경보다 측정·반복이 핵심.
- Claude Design 추가 핸드오프는 (a) 외부 의뢰 시간 비용, (b) 받은 코드를 기존 `src/`에 재이식하는 마이그레이션 부담을 만든다.
- 작은 변경분(화면 부분 수정·섹션 추가/제거·시각 강조 등)은 `src/` 직접 수정이 더 빠르고 안전.
- **예외**: 디자인 큰 개편이 필요하면 새 cycle(`v*-redesign` 등)을 띄워 prototype과 동일한 신규 호출 흐름을 다시 한 번 돌린다.

### 6.2 mvp 이상 사이클 진입 시 첫 질문

```
v1-prototype에서 받은 디자인은 이미 src/에 박혀있어. v2 design 변경분 어떻게 갈까?

- 화면 변경: v2 새 기능·PRD diff에 따른 부분 수정 (작은 변경분 권장)
- 처리 위치: src/ 코드 직접 수정. claude-design-code/ frozen 유지
- 정합성 정리: v1 정리 결과는 그대로 보존, v2 변경분에 대한 새 §v2 정합성 정리 섹션 추가
- 디자인 큰 개편이 필요하면: 별도 redesign cycle 권장 — 이 cycle에선 진행 X
```

### 6.3 산출물 업데이트 원칙

- **`design/index.md`** v2 변경분을 `§v{N} 정합성 정리 결과` 섹션으로 추가. v1 정리 결과는 frozen 보존(덮어쓰기 X).
- **`design/files/`**는 prototype cycle SoT 그대로 — v2 이상 사이클에서 손대지 X.
- **`src/` 코드 변경 가이드는 6단계 Architecture로 인계** — Architecture가 화면별 영향 범위·data-model 변화·API 명세 갱신을 함께 결정.

기술 스택 변경(예: v1 React → v2 Flutter)은 6단계 Architecture에서 다룸.

## 7. 좋은 예 vs 나쁜 예

핵심 차이는 **커버리지·시스템화·정합성 정리** vs **핵심만·inline·일반론**.

- **화면 커버리지** — 좋은: 핵심 + 보조 + 엣지 5종(빈·에러·로딩·권한·오프라인) 모두. / 나쁜: 핵심 화면 5개만.
- **디자인 시스템** — 좋은: 컬러 토큰·타이포 스케일·간격 시스템 별도 파일로 추출. / 나쁜: 화면 안에 inline 스타일.
- **정합성 정리** — 좋은: 4 카테고리별 갭 식별 + 사용자 결정 + 변경 내역 기록. / 나쁜: "디자인 받았으니 OK".

## 8. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. receiving 방식 결정 → Claude Design 입력 정리 → 산출물 보존 → 정합성 점검 → 기획 마감을 차례로.
- **코칭**: SKILL.md §1.4대로. 사용자가 Claude Design에 어떻게 의뢰할지 모르면 AI가 §3.3 입력 셋(intent·sketch·prd 요약)을 그대로 사용 가능한 프롬프트 템플릿으로 정리해 제공. 정합성 점검에서 갭 처리 우선순위가 헷갈리면 "디자인 우선" 디폴트 추천. 모르는 부분은 `TBD: ...`로 명시 후 6단계 진입 시 재확인.
