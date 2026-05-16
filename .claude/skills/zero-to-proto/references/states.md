---
name: states
description: Phase 빌드 단계의 phase 상태 머신 정의. 6가지 상태와 전이, needs_review 트리거 조건을 규정.
---

빌드 단계의 phase 상태는 다음 6가지 중 하나다. 각 phase의 상태는 `tasks/{task-name}/index.json`의 phase 항목 안 `status` 필드에 기록된다.

## 1. 상태 정의

### `pending`
- **의미**: 아직 시작하지 않은 phase.
- **다음 가능 상태**: `in_progress`.
- **필드**: 없음.

### `in_progress`
- **의미**: 현재 작업 중.
- **다음 가능 상태**: `completed`, `needs_review`, `blocked`, `error`.
- **필드**: `started_at`.

### `needs_review`
- **의미**: 코드 동작 OK, 자동 검증(테스트·타입체크 등) 통과. **단, 사람의 검토가 필요한 변경**이 포함되어 있어 자동으로 다음 phase 진입을 보류한 상태.
- **자동 트리거 조건** (이 중 하나라도 해당하면 `in_progress` → `needs_review` 전이):
  - **보안**: 인증·권한·암호화 관련 코드 신규/변경.
  - **시크릿**: 외부 API 키·토큰·시크릿 신규 사용 또는 저장 방식 변경.
  - **DB 스키마**: 컬럼 추가/제거/타입 변경, 인덱스 변경, 마이그레이션 파일 생성.
  - **외부 호출**: 외부 API/서비스 호출 신규 추가, 특히 (a) 비용 발생, (b) 사용자 데이터 외부 전송, (c) 비결정적 응답.
  - **비결정성**: 타임존·시스템 시간·무작위 시드·외부 환경 의존 코드.
  - **권한 상승**: sudo·root·OS 권한 호출, 파일시스템 외부 영역 접근.
- **다음 가능 상태**:
  - `completed` — 사용자가 검토 후 승인 (자연어로 "OK", "통과", "다음으로").
  - `in_progress` — 사용자가 재작업 요청 (자연어로 "고쳐줘", "다시 해").
- **필드**: `review_reasons` (트리거된 조건 배열), `review_summary` (사람이 봐야 할 핵심 변경 한두 줄 요약), `review_files` (검토 대상 파일 경로 배열).
- **원칙**: **사용자 승인 없이 `completed`로 자동 통과 금지.**

### `blocked`
- **의미**: 외부 조건 미충족으로 진행 불가. AI 스스로 해결할 수 없는 상태.
- **예시**: 환경변수 누락, 외부 서비스 다운, 사용자 결정 대기, API 키 미발급, 사용자 입력 필요, 의존성 패키지 설치 권한 부재.
- **`error`와 구분**: `error`는 "시도해봤지만 실패", `blocked`는 "시도조차 불가능한 외부 조건".
- **다음 가능 상태**: `pending` (외부 조건 해제 후 재시도).
- **필드**: `blocked_reason` (구체적 원인), `unblock_action` (해제하려면 사용자가 무엇을 해야 하는지 단계별 안내).

### `error`
- **의미**: 구현·테스트 중 실패. AI가 시도했으나 성공하지 못함.
- **예시**: 컴파일 오류, 단위 테스트 실패, 타입 체크 실패, 외부 API 5xx, AI 자체 한계(Anthropic API 500 등).
- **다음 가능 상태**: `pending` (수정 후 재시도).
- **필드**: `error_message` (현재 에러 원인), `prev_error_message` (이전 시도의 에러; 재시작 시 보존).
- **외부 장애 구분**: phase output(`tasks/{task-name}/phase-{N}-output.json`)에서 Anthropic API 5xx, 외부 서비스 장애 등이 감지되면 `error_message`에 `[external]` prefix를 붙여 사용자 코드 문제와 구분.

### `completed`
- **의미**: phase 완료. 다음 phase 진입 가능.
- **다음 가능 상태**: 없음 (terminal).
- **필드**: `completed_at`, `ac_results` (acceptance criteria 검증 결과 배열).

## 2. 전이 다이어그램

```
pending
  │
  ▼ (시작)
in_progress
  ├─→ completed                              (정상 종료, AC 통과)
  ├─→ needs_review                           (트리거 조건 충족)
  │     ├─→ completed                        (사용자 승인)
  │     └─→ in_progress                      (사용자 재작업 요청)
  ├─→ blocked                                (외부 조건 미충족)
  │     └─→ pending                          (외부 조건 해제 후)
  └─→ error                                  (구현 실패)
        └─→ pending                          (수정 후 재시도)
```

## 3. 운영 원칙

### 3.1 종료 코드만으로 성공 판단 금지

`scripts/run-phases.py`가 exit 0으로 끝나도 phase는 `error`/`blocked`/`needs_review`일 수 있다. 항상 `tasks/{task-name}/index.json`의 모든 phase `status` 필드를 확인하고, **모두 `completed`일 때만** 성공으로 간주.

### 3.2 needs_review는 자동 통과 금지

자동 검증(테스트·타입체크)이 다 통과해도 `needs_review` 트리거 조건이 잡히면 멈춘다. 사용자에게 `review_summary`와 `review_files`를 제시하고 명시적 승인을 받아야 `completed`로 간다.

### 3.3 재시작 시 자동 상태 리셋

사용자가 자연어로 재개 지시("다시 해", "재시작", "고쳤어")하면 AI가 다음을 자동으로 처리한다.

1. 해당 phase status를 `error`/`blocked` → `pending`으로 변경.
2. `error_message` → `prev_error_message`로 보존 (디버깅 컨텍스트 유지).
3. `blocked_reason` → `prev_blocked_reason`으로 보존.
4. 동일한 실행 방식(foreground/background)으로 `scripts/run-phases.py` 재호출. 사용자가 변경 명시 시 변경.

**사용자는 `index.json` 수동 편집 불필요.**

### 3.4 사전 검증 (재시작 전, 가능한 경우)

`blocked` 해제 후 재시작 요청 시, AI가 해제 조건을 프로그램적으로 확인할 수 있으면 먼저 검증한다.

- 환경변수 존재 여부.
- 파일 경로 유효성.
- 외부 서비스 ping 또는 health check.
- 의존성 패키지 설치 여부.

검증 실패 시 사용자에게 재확인. 검증 불가 사안은 사용자에게 "정말 해결됐는지 확인해주세요. 재시작해도 될까요?" 1회 확인 후 진행.

### 3.5 상태 보고 포맷

사용자에게 phase 상태 보고 시 다음 포맷을 따른다. 톤은 SKILL.md §1.3대로 반말·친근·짧게.

- **`completed`**: `✅ Phase {n} 완료` + 다음 권장 액션 (예: "다음 phase 자동 진행", "task 완료. 통합 테스트 갈까?").
- **`needs_review`**: `🔍 Phase {n} 검토 필요: {review_summary}` + 검토 대상 파일 목록 + "OK면 다음 phase 갈게, 수정할 거면 알려줘".
- **`blocked`**: `⚠️ Phase {n} 차단: {blocked_reason}` + `unblock_action` (사용자가 따라할 단계).
- **`error`**: `❌ Phase {n} 실패: {error_message}` + 원인 분석 + 권장 수정. `[external]` prefix면 외부 장애로 명시.
