---
name: 7-build-plan
description: Build Plan 단계 가이드. 사이클 산출물(prd·architecture·data-model·design 등)을 받아 자동 정합성 점검 후 직렬 phase 실행 계획을 cycle 폴더 안 build/에 생성. SKILL.md §3의 7번 단계.
---

Build Plan은 앞 단계 산출물을 받아 **직렬 phase로 실행 가능한 빌드 계획**을 만드는 단계다. 만들어진 계획은 8번(Automation Setup) 통과 후 9번(Phase 빌드)에서 `scripts/run-phases.py`로 실행된다.

**핵심 설계 원칙**: 사이클 1개 = 1 빌드 = 다수 phase. **task 개념 없음**. 한 사이클의 모든 phase는 `build/` 단일 폴더 안에 직렬로 배치된다.

## 1. 단계 목표

- 입력 산출물 → **자동 정합성 점검** → **phase 분해**.
- phase는 **자기완결적**이어야 함 — 독립 Claude session이 phase 파일 하나 읽고 작업 완수 가능한 수준.
- AC(Acceptance Criteria)는 **실행 가능한 커맨드**로.
- needs_review 트리거 조건(보안·시크릿·DB 스키마 등)을 phase 단위로 식별.

## 2. 진행 절차

### 2.1 사이클 분기

- 첫 사이클이고 `build/` 비어있음: 정합성 점검 → phase 분해 인터뷰.
- 첫 사이클인데 `build/` 일부 있음: 미완료 phase 보완.
- 두 번째 이상 사이클: 직전 사이클 retro 보고 **변경된 산출물 부분만 새 phase로**. (v1 phase 직접 수정 X.)

### 2.2 sanity check (가벼운 산출물 재확인)

**본격 정합성 점검·기획 마감은 5-design.md §3.5에서 끝났고**, **기술 결정·data-model·API 명세·마이그레이션 계획은 6-architecture.md에서 디자인 코드를 base로 확정됐다**. 7단계는 빌드 진입 직전 한 번 더 가벼운 sanity check만.

**점검 항목** (플랫폼 무관 공통):

1. **6단계 산출물 존재 확인**: `architecture.md`, `data-model.md`, (UI 플랫폼이면) `design/migration-analysis.md`·`design/migration-plan.md`.
2. **PRD Must ↔ API 명세 1:1 추적**: PRD Must 기능 모두 architecture.md API 명세에 매핑됐나?
3. **data-model 완성도**: PRD 기능에 필요한 모든 필드가 엔티티에 있나?
4. **(UI) 마이그레이션 계획 누락 점검**: 스택이 React 계열이 아닌데 migration-plan.md 비어있으면 6단계로 돌려보냄.
5. **(직전 점검 이후 변경 감지)**: 6단계 ↔ 7단계 사이 사용자가 산출물 손댔으면 재점검 필요.

**갭 발견 시**:
- **기획·정합성 갭 (디자인 vs PRD/Sketch)**: 5-design.md §3.5로 돌려보냄.
- **기술 결정 갭 (data-model·API·마이그레이션)**: 6-architecture.md 해당 sub-section으로 돌려보냄.

**갭 0개면** "산출물 OK. phase 분해 시작할까?" 한 줄로 바로 진행.

### 2.3 Phase 분해 인터뷰

```
정합성 점검 통과. 이제 phase로 쪼개자. 권장 7~12개 (적정선).

분해 기준 후보:
- 레이어별: data → domain → ui 순으로 phase
- 모듈별: Architecture 모듈 경계 따라 phase 1개씩
- 기능별: PRD Must 1개당 1~2 phase
- Cross-platform: 공통 코어 → 플랫폼별 어댑터 순서로

디폴트 추천: phase0 셋업·디자인 마이그레이션 → phase1 데이터·도메인 코어 → phase2~ 기능별 또는 레이어별.

너 의견? 모르면 디폴트로 갈까?
```

### 2.4 Phase 분해 원칙

- **phase 개수 7~12** (적정선). 너무 적으면(<5) phase 비대, 너무 많으면(>15) 실패 시 재시작 비용 큼.
- **scope 최소화**: 한 phase에서 한 레이어 또는 한 모듈만. 여러 모듈 동시 수정 필요하면 phase 쪼개기.
- **순차 의존성 명시**: phase N이 phase N-1의 산출물을 base로. 직렬 실행 전제.
- **needs_review 트리거 조기 식별**: 보안·시크릿·DB 스키마·외부 호출·비결정성·권한 상승 변경이 들어갈 phase는 그 phase 주의사항에 명시.
- **AC는 실행 가능 커맨드**: `npm run build && npm test` 같은 형식.

### 2.5 누락 점검

phase 분해 후 한 번 더:

1. **핵심 phase 누락**: PRD Must 기능 모두 phase에 매핑됐나? Design 마이그레이션이 phase에 들어갔나? (UI + 스택이 React 계열 아닐 때) cross-platform이면 각 platform 어댑터 phase 있나?
2. **공통 누락**: 프로젝트 셋업·환경변수·CI/CD·배포 스크립트·타입체크·린트·테스트 인프라·로깅·관측성·시크릿 관리.

## 3. 완료 체크리스트

- [ ] **§2.2 정합성 점검 통과** (갭 처리 완료 또는 사용자 무시 결정).
- [ ] **phase 7~12개**로 분해됨.
- [ ] **PRD Must 기능 모두 phase에 매핑** — 추적 가능.
- [ ] **각 phase는 자기완결적** — 사전 준비·작업 내용·AC·needs_review 자체 점검·주의사항 5섹션 모두.
- [ ] **AC는 실행 가능 커맨드**로 작성됨.
- [ ] **needs_review 트리거 phase**는 주의사항에 명시.
- [ ] **Design 마이그레이션 phase 포함** (UI 플랫폼이고 스택이 React 계열 아닐 때).
- [ ] **Cross-platform** platforms 여러 개면 공통 코어 → 어댑터 phase 분리됨.

## 4. 산출물 스펙

### 4.1 디렉토리 구조

위치: `planning/cycles/v{N}-{label}/build/`. **단일 폴더, top-level index 없음.**

```
planning/cycles/v{N}-{label}/build/
├── index.json                  ← phase 인덱스 + 사이클 메타
├── phase0.md
├── phase1.md
├── phase2.md
└── ...
```

### 4.2 `build/index.json`

```json
{
  "project": "<프로젝트명>",
  "cycle": "v1-prototype",
  "prompt": "<사용자가 빌드 단계 시작할 때 입력한 최초 프롬프트 또는 사이클 의도 요약>",
  "totalPhases": 9,
  "created_at": "2026-05-04T10:00:00+0900",
  "phases": [
    { "phase": 0, "name": "setup-and-migration", "status": "pending" },
    { "phase": 1, "name": "data-model", "status": "pending" }
  ]
}
```

- `cycle`: 어느 사이클의 빌드인지 추적.
- `prompt`: 빌드 의도·맥락 보존.
- phase status는 `references/states.md`의 6상태 머신 따름 (`pending`/`in_progress`/`needs_review`/`blocked`/`error`/`completed`).
- 타임스탬프 ISO 8601. `created_at`만 생성 시 기록, 나머지는 `scripts/run-phases.py`가 자동.

### 4.3 Phase 파일 템플릿

`build/phase{N}.md` — **자기완결적**. 다른 phase 파일·외부 컨텍스트 없이 phase 파일 하나만 보고 독립 Claude session이 작업 완수 가능.

```markdown
# Phase {N}: {Phase 이름}

## 사전 준비

먼저 아래 산출물을 반드시 읽고 프로젝트의 전체 설계 의도를 완전히 이해하라:

- `planning/cycles/v{N}-{label}/intent.md` — 무엇·왜·누구·platform·platforms
- `planning/cycles/v{N}-{label}/prd.md` — 이 phase에 직접 관련된 Must 기능 명세
- `planning/cycles/v{N}-{label}/architecture.md` — 기술 스택·시스템 구조·API 명세
- `planning/cycles/v{N}-{label}/data-model.md` — (DB 있으면) 엔티티·관계·스키마
- `planning/cycles/v{N}-{label}/design/` — (UI 플랫폼이면) Claude Design 산출물·마이그레이션 계획
- `planning/cycles/v{N}-{label}/sketch.md` — (backup) 핵심 시나리오·플로우

이전 phase 산출물:

- {이전 phase에서 생성/수정된 파일 경로 나열}

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## 작업 내용

{구체 구현 지시. 파일 경로, 클래스/함수 시그니처, 로직 설명. 코드 스니펫은 인터페이스/시그니처 수준만, 구현체는 에이전트 재량. 단 핵심 비즈니스 규칙(멱등성·보안·데이터 무결성)은 명확히 박아라.}

## Acceptance Criteria

```bash
npm run build           # 컴파일 에러 없음
npm test                # 모든 테스트 통과
npm run typecheck       # 타입 에러 없음
```

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v{N}-{label}/build/index.json`의 phase {N} status를 `"completed"`로 변경.

수정 3회 이상 실패하면 status `"error"`, `error_message` 필드에 에러 내용.

작업 중 사용자 개입 필요(API key·외부 서비스 인증·수동 설정)면 즉시 중단, status `"blocked"`, `blocked_reason`에 사유 + 사용자가 따라할 단계.

## needs_review 트리거 자체 점검

작업 완료 후 다음 중 하나라도 해당하면 status를 `"needs_review"`로 변경하고 `review_summary`·`review_files`에 핵심 변경 요약 기록:

- 인증·권한·암호화 코드 신규/변경
- 외부 API 키·시크릿 신규 사용
- DB 스키마 변경(컬럼 추가/제거/타입 변경, 마이그레이션 파일)
- 외부 API 호출 신규 추가 (특히 비용·사용자 데이터 외부 전송)
- 비결정성(타임존·시스템 시간·무작위 시드) 의존
- sudo·root·OS 권한·파일시스템 외부 접근

## 주의사항

- {이 phase에서 하지 말아야 할 것, 엣지 케이스, 호환성 주의사항}
- 기존 테스트를 깨뜨리지 마라.
```

### 4.4 Phase 파일 작성 원칙

1. **자기완결성**: "이전 대화에서 논의한 바와 같이" 같은 외부 참조 금지. 필요 정보 전부 phase 파일 안에.
2. **사전 준비 필수**: 관련 산출물 경로 + 이전 phase 산출물 경로 명시.
3. **시그니처 수준 지시**: 함수·클래스 인터페이스만. 구현체는 에이전트 재량. 핵심 비즈니스 규칙만 강제.
4. **AC는 실행 가능 커맨드로**: 추상 서술 금지.
5. **scope 최소화**: 한 phase에서 한 레이어/모듈만.
6. **주의사항 구체적**: "조심해라" 대신 "X 하지 마라. 이유: Y" 형식.
7. **needs_review 자체 점검** 섹션 필수: 트리거 조건 자동 검토.

### 4.5 Runner 호출 방식

```bash
python3 .claude/skills/zero-to-prototype/scripts/run-phases.py v1-prototype
```

- 인자는 **사이클 라벨**. runner가 `planning/cycles/v1-prototype/build/index.json`을 읽고 다음 `pending` phase 찾아 실행.
- 자세한 실행 절차는 `references/9-phase-run.md` 참조.

## 5. 사이클 업데이트 모드 (v2 이상)

```
v1 build 회고 보니 [핵심 발견]였어. v2 build 어떻게 갈까?

- 새 phase: v2 새 기능을 phase로 분해.
- v1 phase 직접 수정 X: v1 폴더에 그대로 두고, v2는 새 phase만.
- 영향 받는 v1 코드(있으면): 데이터 마이그레이션 phase 포함.
```

**원칙**: v1 phase를 직접 수정하지 말고 v2에서 새 phase로. v1 산출물(코드)은 v2가 base로 받음.

## 6. 좋은 예 vs 나쁜 예

핵심 차이는 **자기완결성·실행 가능성·scope 최소화** vs **외부 참조·추상·복합**.

- **사전 준비** — 좋은: 구체 산출물 경로 6개 + 이전 phase 산출물 경로. / 나쁜: "이전 작업 참고".
- **작업 내용** — 좋은: 함수 시그니처·핵심 규칙·파일 경로 명시. / 나쁜: "기능 구현".
- **AC** — 좋은: `npm run build && npm test && npm run typecheck`. / 나쁜: "정상 동작 확인".

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. 정합성 점검 결과 보고 → phase 분해 기준 → AC 커맨드를 차례로.
- **코칭**: SKILL.md §1.4대로. 사용자가 phase 분해 기준 모르면 §2.3 디폴트 추천. phase 개수가 너무 많으면(>15) "쪼개진 phase 합치자", 너무 적으면(<5) "한 phase가 비대해, 쪼개자" 권유. AC 커맨드를 추상으로 답하면 플랫폼 표준 후보 제시. 모르는 부분은 `TBD: ...`.
