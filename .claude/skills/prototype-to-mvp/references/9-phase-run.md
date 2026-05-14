---
name: 9-phase-run
description: Phase 빌드 단계 가이드. scripts/run-phases.py를 호출해 build/ 안 phase들을 직렬 실행하고, 상태 보고·error/blocked/needs_review 처리·자동 재시작·외부 장애 구분을 운영. SKILL.md §3의 9번 단계.
---

Phase 빌드는 7번 Build plan에서 만든 `build/` 안의 phase들을 **`scripts/run-phases.py`로 직렬 실행**하는 단계다. 다른 references와 결이 다름 — **사용자 인터뷰 거의 없고, 스크립트 운영 가이드**다. AI(메인 세션)가 스크립트 호출·상태 해석·사용자 보고를 담당.

## 1. 단계 목표

- `build/index.json`의 phase들을 **직렬 실행** (phase0 → phase1 → ...).
- 각 phase는 별도 `claude -p` 세션이 실행. 메인 세션 토큰은 운영 보고에만 씀.
- **상태 머신**(`references/states.md`)에 따라 phase 진행. `pending` → `in_progress` → `completed`/`needs_review`/`blocked`/`error`.
- error/blocked/needs_review 발생 시 사용자에게 **구체적 다음 액션과 함께 보고**.
- 사용자 자연어 재개 지시 시 **status 자동 리셋 + 재실행**.

## 2. 진행 절차

### 2.1 실행 전 점검 (AI 단독)

- `planning/cycles/v{N}-{label}/build/index.json` 존재? phase 파일들 다 있나? (없으면 7단계로 돌려보내기.)
- 환경변수 8-automation-setup.md에서 셋업한 것들 다 있나? (없으면 사용자에게 안내.)
- git 상태 — 작업 브랜치 있으면 그대로, 없으면 자동 생성될 거 안내.

### 2.2 실행 방식 결정 — foreground vs background

사용자에게 추천 + 확인. 추천 로직:

- **foreground** 추천: phase 수 ≤ 3, 또는 사용자가 실시간 로그 보고 싶다 명시.
- **background** 추천 (디폴트): phase 수 ≥ 4, 또는 phase별 예상 시간 합산이 15분 이상. 백그라운드면 사용자가 다른 작업 가능, 완료 시 자동 알림.

```
빌드 시작하자. 실행 방식:
- foreground: 현재 세션에서 실행. 실시간 로그 직접 관찰. 다른 대화 못 함.
- background: 백그라운드 실행. 다른 대화·수정 가능. 완료 시 자동 알림.

이번 빌드 phase {N}개, 예상 [예상시간] — [추천 방식] 추천. 어떻게?
```

### 2.3 스크립트 호출

```bash
python3 .claude/skills/zero-to-prototype/scripts/run-phases.py <cycle-label>
```

예: `python3 .claude/skills/zero-to-prototype/scripts/run-phases.py v1-prototype`.

- **foreground**: Bash 도구 직접 호출, 출력 stream.
- **background**: Bash 도구의 `run_in_background: true` 옵션. 완료 시 자동 알림.

### 2.4 백그라운드 실행 중 진행 상황 보고

사용자가 "어디까지 됐어?" 같이 물으면 즉시:

1. `build/index.json` 읽어 phase별 status 확인.
2. 마지막 git commit log 한 줄 (현재 phase·완료 phase).
3. 다음 형식으로 답:

```
v1-prototype 빌드 진행 중:
- ✓ phase 0 setup (2025-05-04 10:32, 8분)
- ✓ phase 1 data-model (10:40, 5분)
- ⟳ phase 2 ui-core (진행 중, 3분 경과)
- ○ phase 3~8 (대기)

3/9 완료, 약 [예상 남은 시간].
```

(이모지는 plan-and-build의 기존 컨벤션 따라 ✓·⟳·○ 사용. 강제 아님.)

### 2.5 종료 후 status 검사 (가장 중요)

스크립트 종료 신호(foreground 명령 반환 또는 background 알림) 받으면 **종료 코드만 보고 성공 판단 금지**. 반드시:

1. **`build/index.json` 전체 조회.** 모든 phase의 status 검사.
2. **하나라도 `error`/`blocked`/`needs_review`면** 해당 phase의 메시지 추출해 보고.
3. **모두 `completed`일 때만 빌드 성공으로 간주.**

스크립트는 phase 하나 실패해도 정상 종료(exit 0)할 수 있음 — index.json만이 진실의 원천.

## 3. 상태별 보고·처리

### 3.1 모두 completed (빌드 성공)

```
✅ v1-prototype 빌드 완료 ({N} phases, 총 [경과시간])

다음 권장 액션:
- 로컬 실행 확인: [스택별 명령]
- 통합 테스트 (10단계) 시작할까?
- 또는 main에 머지(8-automation-setup.md §2.4.4의 1인 개발 흐름 따라)
```

### 3.2 error 발견

```
❌ v1-prototype phase {n} {phase-name} 실패

원인: {error_message}

원인 분석:
{AI가 error_message를 읽고 한국어로 풀어줌. 외부 장애([external] prefix)면 외부 장애로 명시}

권장 수정:
- {구체 수정 단계}

수정 후 "다시 해" / "재시작" 자연어 지시하면 그 phase부터 자동 재개.
```

**[external] prefix가 붙은 error_message** (Anthropic API 5xx, 외부 서비스 장애)는 사용자 코드 문제가 아닌 **외부 장애로 구분해 안내**. 사용자에게 "코드는 OK, 외부 서비스 일시 장애라 잠시 후 재시작 가능" 식으로.

### 3.3 blocked 발견

```
⚠️ v1-prototype phase {n} {phase-name} 차단

원인: {blocked_reason}

해제 방법:
{unblock_action — 사용자가 따라할 단계별 안내}

해제 후 "재시작" 자연어 지시 → 자동 재개.
```

전형 케이스:
- API key 누락 → `.env`에 `KEY=value` 추가 또는 GitHub Secrets 추가
- 외부 서비스 다운 → 서비스 복구 대기 후 재시도
- 의존성 미설치 → `npm install` 등 명령
- 사용자 결정 필요 → 결정 사항을 답으로 받음

### 3.4 needs_review 발견 (사용자 승인 흐름)

코드 동작은 OK인데 사람이 검토해야 하는 변경. **자동 통과 절대 금지** — 사용자 명시 승인 필요.

```
🔍 v1-prototype phase {n} {phase-name} 검토 필요

이유: {review_reasons 배열, 예: 보안·DB 스키마 변경}

핵심 변경:
{review_summary}

검토 대상 파일:
{review_files 목록}

OK면 "통과"·"OK"·"다음으로" → status를 completed로 자동 변경 후 다음 phase 진행.
수정 필요하면 어떻게 고칠지 알려줘 → 그 phase 재작업.
```

### 3.5 자동 재시작 절차

사용자가 자연어로 재개 지시("다시 해", "재시작", "고쳤어", "통과") 받으면 AI가 자동으로:

1. 해당 phase의 status를:
   - error/blocked → `pending`으로 리셋
   - needs_review → `completed`로 변경 (사용자가 명시 승인했을 때만)
2. 메시지 보존:
   - `error_message` → `prev_error_message`
   - `blocked_reason` → `prev_blocked_reason`
3. **사전 검증 (가능하면)**: blocked 해제 시 환경변수 존재·외부 서비스 ping 등 프로그램적 확인. 검증 실패 시 사용자에게 재확인.
4. **검증 불가 사안**은 "정말 해결됐어? 재시작해도 돼?" 한 번 더 확인.
5. 동일 실행 방식(foreground/background)으로 `run-phases.py` 재호출. 사용자가 명시적으로 변경하면(예: "이번엔 foreground로") 변경.
6. **사용자는 `index.json` 수동 편집 불필요.**

## 4. 완료 체크리스트

- [ ] `build/index.json` 모든 phase status `completed`.
- [ ] git 작업 브랜치에 phase별 commit 누적됨 (메시지 컨벤션 따름).
- [ ] 외부 산출물(코드 변경) 모두 commit됨.
- [ ] `automation-setup.md` 남은 액션(예: GitHub Secrets 추가) 사용자가 처리했는지 확인.

## 5. 사이클 업데이트 모드 (v2 이상)

v2 빌드는 v1 코드 base 위에 새 phase만 실행. 절차는 v1과 동일 — 단, 첫 phase가 보통 "v1 코드 검증 + v2 변경 prep" 형태가 됨 (7-build-plan.md §2.4 참조).

v1 빌드 끝나고 v2 시작할 때 사용자가 "v2-mvp 빌드 시작" 명시하면, runner는 새 사이클의 build/ 안 phase부터 실행.

## 6. 외부 장애 구분 운영

`build/phase{N}-output.json` (스크립트가 저장한 stdout/stderr)에서 다음 패턴 감지 시 `error_message`에 `[external]` prefix 자동 추가 (스크립트가 처리):

- Anthropic API 5xx 응답
- HTTP timeout (외부 의존성 호출 시)
- 외부 서비스 도메인의 connection refused/reset

[external] error는 **사용자 코드 문제가 아님**. 보고 시 명확히 구분 ("외부 서비스 일시 장애야, 코드 문제 아님. 잠시 후 재시작해도 됨").

## 7. 사용자 응대 톤

다른 references와 달리 이 단계는 인터뷰가 거의 없다. 톤은 SKILL.md §1.3대로 반말·짧게. 핵심 케이스:

- **빌드 시작 시**: 실행 방식 추천 한 줄 + 확인.
- **진행 보고**: 표 한 줄로 진척률.
- **error/blocked**: 원인·권장 수정 명확히. "재시작" 자연어 받기.
- **needs_review**: 검토 대상 명확히 + 사용자 결정 기다림.
- **빌드 완료**: 다음 권장 액션.

**금지**: phase 진행 중 사용자에게 불필요한 질문(인터뷰)하지 않음. 자동 진행이 디폴트.

## 8. scripts/run-phases.py와의 분담

이 가이드는 **AI(메인 세션) 운영**을 다룬다. 실제 phase 실행 로직(`claude -p` 호출, status 기록, git commit)은 `scripts/run-phases.py`가 담당. AI는 스크립트를 호출하고 결과를 해석해 사용자에게 보고.

- 스크립트가 하는 일: phase 파일 읽기 → 프롬프트 임베딩 → `claude -p` 실행 → output 저장 → status 확인 → git commit → 다음 phase.
- AI(메인)가 하는 일: 스크립트 호출 결정 → 종료 후 index.json 검사 → 사용자에게 보고 → 자연어 지시받아 재시작.
