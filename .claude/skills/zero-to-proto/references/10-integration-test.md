---
name: 10-integration-test
description: 통합 테스트 단계 가이드. 빌드 끝난 후 phase 간 연동·E2E 시나리오·비기능 요구사항(성능·보안·접근성)을 검증하고 발견된 이슈를 처리. SKILL.md §3의 10번 단계.
---

통합 테스트는 9번 빌드에서 만든 코드 위에서 **시스템 전체 흐름**을 검증하는 단계다. 단위 테스트는 빌드 phase의 AC에서 이미 검증됐으니 여기는 **phase 간 연동·E2E 시나리오·비기능 요구사항**에 집중한다.

## 1. 단계 목표

- **E2E 시나리오 검증**: Sketch §시나리오 1~5를 실제로 처음부터 끝까지 실행.
- **phase 간 연동**: data-model ↔ ui ↔ api 같이 phase 경계를 넘는 흐름.
- **비기능 요구사항 검증**: PRD 성능·보안·접근성·다국어·호환성 지표를 측정값으로 확인.
- **발견된 이슈 처리**: 작은 건 인라인 fix, 큰 건 새 phase 또는 다음 사이클로.

## 2. 진행 절차

### 2.1 사이클 분기

- 첫 사이클: PRD·Sketch base로 통합 테스트 케이스 자동 생성 → 실행 → 이슈 처리.
- 두 번째 이상 사이클: 직전 사이클 `qa-report.md` 보고 회귀 테스트 + v2 새 기능 테스트.

### 2.2 통합 테스트 케이스 자동 생성 (AI 단독)

AI가 PRD·Sketch·Architecture를 읽고 테스트 케이스 자동 생성. 사용자 인터뷰 아님. 결과만 보고.

**생성 기준**:
- **E2E 시나리오**: Sketch §시나리오 1~5 각각을 1 테스트 케이스로. 트리거 → 핵심 작업 → 기대 결과 검증.
- **연동 테스트**: PRD Must 기능별로 phase 경계를 넘는 데이터 흐름. 예: F1 "특약 대조"는 ui 입력 → API → DB 조회 → 응답 → ui 표시 전체.
- **비기능**: PRD §비기능 요구사항의 각 숫자 지표(P95 응답 5초, NPS 8 이상 등) 검증.

생성된 케이스를 `qa-report.md` 초안에 정리해 사용자에게 보고:

```
통합 테스트 케이스 [N]개 자동 생성:

E2E 시나리오 (Sketch base):
1. 시나리오 1 [부동산 특약 대조] — 트리거→ 입력→ 결과
2. ...

연동 테스트 (PRD Must base):
6. F1 데이터 흐름 (ui→ API→ DB→ 응답)
7. ...

비기능 (PRD 지표 base):
11. P95 응답 ≤ 5초
12. WCAG 2.1 AA 통과
13. ...

우선순위 선택:
(a) 모두 실행 (시간 듬, 첫 사이클 권장 X)
(b) E2E + 연동 핵심만 (prototype 디폴트)
(c) 비기능까지 (mvp 이후 권장)

어느 거?
```

### 2.3 테스트 도구·실행 — 플랫폼 분기

`prd.md` `platform` + Architecture 스택 기반.

- **web**: E2E = Playwright·Cypress / 성능 = Lighthouse + PageSpeed Insights (CrUX 실 사용자 데이터) / 접근성 = axe·pa11y / 보안 = npm audit, OWASP ZAP 기본 스캔.
  - **Core Web Vitals 측정 표준**: 시크릿 창 + Lighthouse Mobile + Simulated throttling (worst-case) AND DevTools throttling=No throttle (실 환경) 둘 다 측정. 75th percentile 기준 LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1 (4-prd.md §2.5 표).
  - **Lighthouse 시뮬레이션 함정**: SI(Speed Index)와 LCP 큰 갭은 거의 항상 폰트 swap / late-arriving asset 때문. SI ≪ LCP면 자산 다운로드 검토.
- **mobile**: E2E = Detox(RN)·Maestro·XCUITest·Espresso / 성능 = Xcode Instruments·Android Profiler / 접근성 = native accessibility tools.
- **cli**: 명령어 시퀀스 = bash 스크립트로 실제 호출 + 출력 비교 / 성능 = `time` 측정·메모리 / 호환성 = 여러 OS 매트릭스.
- **library**: 사용 예시 코드 실행 = examples/ 안 sample 돌리기 / API 호환성 = 이전 버전 사용자 코드 컴파일/실행 / 의존성 footprint = bundle size 측정.
- **api-server**: HTTP 통합 = supertest·httpx / 부하 = k6·artillery / 보안 = OWASP API security 기본 / 응답 시간 P50/P95/P99 측정.
- **desktop**: E2E = Spectron(Electron)·OS 자동화 도구 / 성능 = OS 모니터.
- **other**: 사용자에게 "이 플랫폼에 익숙한 통합 테스트 도구 뭐 있어?" 묻고 자유 입력.

**Cross-platform**: 메인 + 추가 platforms 모두 분기 적용. Flutter면 `flutter integration_test` 한 번에 cover 가능.

테스트 코드 위치는 **프로젝트 루트 `tests/integration/`** (cycle 안 X — 코드는 cycle 무관 자산). cycle 안엔 `qa-report.md`만.

### 2.4 실행 + 이슈 검출

AI가 테스트 코드 작성 → 실행 → 결과 수집. 통과/실패별로 `qa-report.md`에 기록.

**실패한 테스트 처리** (이슈 카테고리별):

1. **작은 버그** (한 phase 안 코드 한두 줄 수정으로 해결): **인라인 fix**. 직접 수정 + 통합 테스트 재실행. `qa-report.md`에 "수정 완료" 기록.
2. **중간 변경** (여러 파일·여러 phase 영향): **새 phase 추가** — 9번으로 돌아가 phase 추가하고 빌드 재실행.
3. **큰 변경** (PRD·Architecture 변경 필요): 사용자에게 보고 + **다음 사이클로 미루기**. v2-mvp의 Intent 업데이트 입력으로.
4. **PRD/Architecture 충돌 발견**: 사용자에게 보고 + 산출물 업데이트 결정 (SKILL.md §1.4 코칭 따름).

각 케이스에서 **사용자가 결정**. AI는 옵션 제시.

### 2.5 이슈 보고 포맷

```
통합 테스트 결과:
✓ 통과 [N]개
✗ 실패 [M]개

실패 분류:
- 작은 버그 (인라인 fix 가능): [k]개 — 자동 수정할까?
- 중간 변경 (새 phase 필요): [m]개 — 케이스: ...
- 큰 변경 (다음 사이클): [p]개 — 케이스: ...
- PRD/Architecture 충돌: [q]개 — 산출물 업데이트 필요

어떻게 처리?
```

## 3. 완료 체크리스트

- [ ] **E2E 시나리오** Sketch §시나리오 모두 검증됨.
- [ ] **PRD Must 기능 연동** 모두 검증됨.
- [ ] **비기능 요구사항** PRD 지표 모두 측정값 확인 (또는 사용자가 "이 사이클에선 skip" 명시). 게이트 강도는 SKILL.md §5.1 stage별 매트릭스 — prototype 측정·기록 / mvp 경고 / prod 차단.
- [ ] **실패 테스트 모두 처리됨** — 인라인 fix 완료 / 새 phase 추가 / 다음 사이클로 미룸 결정 / 산출물 업데이트 완료.
- [ ] **`qa-report.md`** 결과·이슈·수정 내역 기록됨.
- [ ] **`tests/integration/`** 코드 commit됨 (CI에서 회귀 검증 가능).

## 4. 산출물 스펙

### 4.1 사이클 안 메타 — `qa-report.md`

위치: `planning/cycles/v{N}-{label}/qa-report.md`.

```markdown
---
cycle: v1-prototype
created_at: YYYY-MM-DD
total_cases: 13
passed: 11
failed: 2
---

# 통합 테스트 결과 요약
- 통과: 11/13
- 실패 → 처리: 인라인 fix 1, 새 phase 추가 1

# E2E 시나리오 (5)
- ✓ 시나리오 1 [부동산 특약 대조] — 4.2초
- ✓ 시나리오 2 [공유 링크 전송] — 1.8초
- ...

# 연동 테스트 (5)
- ✓ F1 데이터 흐름 (ui→ API→ DB→ 응답)
- ✗ F4 권한 요청 → ui 미반영 (인라인 fix 완료, commit abc123)
- ...

# 비기능 (3)
- ✓ P95 응답 4.7초 (목표 5초 이내)
- ✗ WCAG 2.1 AA 컬러 대비 미달 (3개 컴포넌트)
  - 처리: 새 phase 추가 (phase 9: a11y-fix)
- ...

# 다음 사이클로 미룬 이슈 (있으면)
- 모바일 오프라인 모드 미구현 — v2-mvp Intent에 반영
```

### 4.2 코드 위치

- 테스트 코드: **프로젝트 루트 `tests/integration/`** (cycle 무관, git tracked).
- 도구별 설정 (playwright.config.ts·k6 시나리오 등)도 프로젝트 루트.
- CI에서 회귀 실행 (8-automation-setup.md GitHub Actions 워크플로의 e2e job).

## 5. 사이클 업데이트 모드 (v2 이상)

- v1 `tests/integration/`는 **회귀 테스트로 그대로 실행**. v1 기능 깨졌나 점검.
- v2 새 기능별 테스트 추가.
- v1 회고에서 빠뜨린 비기능 (예: prototype에서 보안 skip했으면 v2-mvp에서 추가).

## 6. 좋은 예 vs 나쁜 예

- **테스트 케이스** — 좋은: 트리거·동작·기대 결과 명시 + 측정값. / 나쁜: "정상 동작 확인".
- **실패 처리** — 좋은: 카테고리 분류 + 사용자 결정 받음. / 나쁜: "고치자" 한 줄 후 무작정 fix.
- **비기능 검증** — 좋은: P95 응답 4.7초 (목표 5초). / 나쁜: "빠름".

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. 자동 생성 결과 보고 → 우선순위 선택 → 실행 → 이슈 카테고리별 결정.
- **코칭**: SKILL.md §1.4대로. 사용자가 통합 테스트 도구 모르면 §2.3 플랫폼 표준 후보 제시. 비기능 측정값이 모호하면 PRD §비기능 숫자 그대로 사용. 실패 카테고리 분류가 어려우면 AI가 추천 + 사용자 confirm. 다음 사이클로 미루는 이슈는 v2 Intent 업데이트 입력으로 명시.
