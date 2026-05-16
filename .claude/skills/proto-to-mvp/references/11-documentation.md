---
name: 11-documentation
description: 문서화 단계 가이드. 사이클 산출물(intent·prd·architecture·design)을 base로 프로젝트 루트 문서(README·ARCHITECTURE·API·CHANGELOG)를 자동 생성하고 사용자 검토. SKILL.md §3의 11번 단계.
---

문서화는 **유지보수 가능한 상태로 사이클을 마감**하는 단계다. 사이클 안에 이미 있는 산출물(intent·prd·architecture·design 등)을 base로 **프로젝트 루트 문서**를 자동 생성. 사용자 부담 작음 — AI가 추출·정리, 사용자는 검토만.

## 1. 단계 목표

- **README.md** (프로젝트 루트): 설치·실행·핵심 사용법.
- **ARCHITECTURE.md** (`docs/`): 현재 시점 시스템 구조 (사이클 산출물 architecture.md base).
- **API.md** (플랫폼에 따라): 외부 노출 인터페이스 레퍼런스.
- **CHANGELOG.md**: 사이클별 변경사항 누적 (SemVer 옵션).

## 2. 진행 절차

### 2.1 사이클 분기

- 첫 사이클 (v1-prototype): 모든 문서 신규 생성. 최소 셋(README + ARCHITECTURE)만.
- 두 번째 이상: 기존 문서 업데이트 + CHANGELOG에 새 섹션 추가.

### 2.2 사이클 안 산출물 vs 루트 문서 구분

| | 사이클 안 산출물 | 프로젝트 루트 문서 |
|---|---|---|
| 위치 | `planning/cycles/v{N}/intent.md` 등 | `/README.md`, `/docs/ARCHITECTURE.md` |
| 역할 | 사이클별 의사결정 기록, 시점 frozen | 현재 상태, 항상 최신 |
| 독자 | 다음 사이클의 base | 외부 사용자·기여자·미래의 본인 |
| 변경 | 사이클 종료 후 변경 X | 사이클마다 갱신 |

같은 정보가 두 곳에 있을 수 있지만 **시점·역할이 달라** 둘 다 필요.

### 2.3 자동 생성 (AI 단독)

AI가 사이클 산출물 읽고 루트 문서 생성. 인터뷰 없이.

#### 2.3.1 README.md

base 산출물:
- `intent.md` → 프로젝트 한 문장 설명·타겟 사용자·핵심 가설
- `prd.md` → 핵심 기능 목록 (Must)
- `architecture.md` → 기술 스택 (간단히)
- `automation-setup.md` → 설치·실행 명령어

생성 구조:
```markdown
# {프로젝트명}

{intent.md 문제 정의 한 문단}

## 누구를 위한 거예요
{intent.md 타겟 사용자}

## 핵심 기능
- {prd.md Must F1}
- {Must F2}
- ...

## 시작하기
\`\`\`bash
{설치 명령}
{실행 명령}
\`\`\`

## 기술 스택
{architecture.md 핵심 4~5개 한 줄로}

## 더 자세히
- 아키텍처: docs/ARCHITECTURE.md
- API: docs/API.md (해당 시)
- 변경사항: CHANGELOG.md
```

#### 2.3.2 ARCHITECTURE.md

base: `architecture.md` + `data-model.md`. 거의 그대로 옮기되 **현재 시점 기준**으로 다듬기 (v2 진입 시점이면 v2 결정 반영). 사이클 산출물은 history, ARCHITECTURE.md는 latest.

#### 2.3.3 API.md (플랫폼 분기)

플랫폼별 자동 생성:

- **api-server**: `architecture.md` API 명세 + 코드의 OpenAPI/Swagger 추출. `/docs/API.md` 또는 `swagger.json`.
- **library**: 코드 주석(JSDoc·TSDoc·Sphinx·rustdoc·godoc·dartdoc) 추출. 도구로 자동 생성 + `/docs/API.md`에 진입 링크.
- **cli**: 명령어·옵션·플래그 표. `architecture.md` API 명세 base + `--help` 출력 비교.
- **web/mobile/desktop**: 백엔드 API 호출하는 외부 API가 있다면 그것만. 내부 컴포넌트 인터페이스는 코드 주석으로 충분.
- **other**: 사용자에게 "이 플랫폼의 외부 노출 인터페이스가 뭐야?" 묻기.

#### 2.3.4 CHANGELOG.md

base: 모든 사이클 산출물(retro 포함). 사이클별 섹션:

```markdown
# Changelog

## [v1-prototype] - 2026-05-04
### Added
- {prd.md Must 기능들}

### Changed
- (v1은 신규라 비어있음)

### Notes
- {retro.md 핵심 결정·검증 결과 한 줄}
```

SemVer 적용 여부:
- **library는 SemVer 권장** (외부 의존자 있어서). v1-prototype = 0.1.0, v2-mvp = 0.x 또는 1.0.0-beta.
- 그 외 플랫폼은 사이클 라벨 그대로 (`v1-prototype`).

### 2.4 사이클별 확장 (사이클 라벨 따라 자동)

- **v1-prototype**: README + ARCHITECTURE (최소)
- **v2-mvp**: + API.md + 사용자 가이드 (`docs/USER-GUIDE.md`)
- **v3-production**: + 운영 가이드 + 트러블슈팅 + CHANGELOG SemVer 정착

### 2.5 사용자 검토 + 결정

자동 생성 후 사용자에게 보고:

```
문서 생성 끝났어:
- README.md (생성)
- docs/ARCHITECTURE.md (생성)
- CHANGELOG.md (생성, v1-prototype 섹션)

검토할 부분:
- README "시작하기" 명령어가 실제로 동작하는지 확인 (npm install / npm run dev 등)
- ARCHITECTURE 핵심 다이어그램 — ASCII로 박았는데 Mermaid로 바꿀까?
- (api-server 또는 library면) API.md 추가할까?

수정할 곳 알려줘. 또는 "OK"면 12단계 배포로.
```

사용자 답에 따라 수정 또는 진행.

## 3. 완료 체크리스트

- [ ] **README.md** 5섹션(소개·타겟·기능·시작하기·더 자세히) 모두 채워짐.
- [ ] **docs/ARCHITECTURE.md** 현재 시점 architecture.md 반영됨.
- [ ] **API.md** (해당 플랫폼) 작성됨 또는 사용자가 "skip" 결정.
- [ ] **CHANGELOG.md** 현재 사이클 섹션 추가됨.
- [ ] **README "시작하기" 명령어 검증됨** (사용자가 직접 실행 또는 AI가 sandbox 실행 확인).
- [ ] **`documentation.md`** 사이클 안 메타에 변경된 파일·결정 기록.

## 4. 산출물 스펙

### 4.1 사이클 안 메타 — `documentation.md`

위치: `planning/cycles/v{N}-{label}/documentation.md`.

```markdown
---
cycle: v1-prototype
created_at: YYYY-MM-DD
---

# 생성·갱신된 루트 문서
- /README.md (생성)
- /docs/ARCHITECTURE.md (생성)
- /CHANGELOG.md (v1-prototype 섹션 추가)

# 사용자 결정
- API.md skip (mvp에서 추가)
- ARCHITECTURE 다이어그램 = ASCII (Mermaid는 mvp에서)

# 사용자 검토 결과
- README "시작하기" 명령어 OK (npm run dev 동작 확인)
- ARCHITECTURE 컴포넌트 트리 한 군데 수정 (사용자 피드백 반영)
```

### 4.2 프로젝트 루트 문서

```
/
├── README.md                ← 진입점
├── CHANGELOG.md             ← 사이클별 변경 누적
└── docs/
    ├── ARCHITECTURE.md      ← 최신 시스템 구조
    ├── API.md               ← (해당 플랫폼) 외부 노출 인터페이스
    └── USER-GUIDE.md        ← (mvp 이상) 사용자 가이드
```

`docs/`는 옵션. 작은 프로젝트는 README 한 파일로 충분.

## 5. 사이클 업데이트 모드 (v2 이상)

- **README.md**: 새 기능 추가 + 시작하기 명령어 갱신.
- **ARCHITECTURE.md**: v1 내용 위에 v2 변경 반영. v1과의 차이 한 단락 추가.
- **API.md**: v2 새 엔드포인트·함수 추가. Breaking change면 v1 호환 정책 명시.
- **CHANGELOG.md**: `## [v2-mvp] - ...` 새 섹션 추가. Added/Changed/Removed/Fixed 카테고리.

## 6. 좋은 예 vs 나쁜 예

- **README** — 좋은: 설치 1줄·실행 1줄·핵심 사용법 1예. / 나쁜: 추상적 소개만, 실행 명령어 없음.
- **ARCHITECTURE** — 좋은: 모듈 트리·데이터 흐름·핵심 결정 이유. / 나쁜: "MVC 패턴 사용".
- **CHANGELOG** — 좋은: Added/Changed/Removed 카테고리 + 영향 한 줄. / 나쁜: "이것저것 개선".

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. 자동 생성 보고 → 검토 결과 받기 → 수정 또는 다음 단계.
- **코칭**: SKILL.md §1.4대로. 사용자가 검토 결과 모호하면 "직접 README 한 번 실행해봐 — 막히면 알려줘". API.md 도구 모르면 플랫폼 표준 후보(OpenAPI/JSDoc/Sphinx 등) 자동 적용. 사용자가 "이 정도면 OK" 하면 그대로 진행.
