---
name: 13-launch
description: Production 사이클 출시(Launch) 단계 가이드. PMF 검증된 MVP를 전면 공개 launch하는 단계. broad audience · 공식 announce · 운영 모니터링 본격. SKILL.md §3의 13번 단계.
---

배포(12)는 production grade 인프라 켜기. 출시(13)는 **본격 공개 launch** — 폭넓은 사용자 대상, 공식 announce, 신뢰 가능한 운영. MVP 단계의 soft launch와 다르게 **scale·신뢰·예측 가능성**이 핵심.

## 1. 단계 목표

- **공식 launch announcement** — 채널 다수에 동시·계획적 공개
- **다수 사용자 즉시 처리 가능 상태** — 인프라·CS·모니터링 준비
- **첫 24~72h 인시던트 대응 체제** — 대기·핫픽스·롤백 준비
- **launch metric 기록** — signup·revenue·NPS·인시던트

## 2. 진행 절차

### 2.1 사이클 분기

- 첫 production 사이클(`v4-production` 등): 본격 launch.
- 이후 사이클(`v5-production-update` 등): 신규 feature 출시·rebrand·확장 시.

### 2.2 자동 점검 (AI 단독)

production launch 전 체크리스트:
- 인프라 scale 검증 (load test 통과)
- 모니터링 active (APM·error tracking·uptime)
- CS 창구 운영 가능 상태 (응답 SLA 정의)
- 인시던트 runbook 작성 (`ops/runbook.md` 등)
- legal·privacy 검토 완료 (ToS·privacy policy 게시)
- 분석 funnel 본격 (signup·retention·revenue)
- 백업·롤백 절차 검증

미충족 항목 있으면 launch 보류 또는 사용자 명시 강행 OK.

### 2.3 사용자 결정 — launch plan

```
production launch — 공개 범위·시점·채널 결정:

- 시점: 평일 오전? 특정 이벤트 연계? 점진적 rollout?
- 공개 범위: 전체 / 지역·플랫폼 한정 / waitlist 점진
- 마케팅 채널 (14단계와 연계): 동시 게시? 순차?
- D-Day 운영자 대기 시간: 24h? 첫 주?
- 가설 검증 metric: 어떤 수치가 "launch 성공" 신호인가?

답에 따라 launch-plan.md 작성.
```

### 2.4 launch 실행

**원칙**: **공식·계획적·관측 가능**.

D-Day:
1. 인프라 final check (load·error·monitoring dashboard open)
2. 마케팅 채널 동시 또는 순차 게시 (14단계 channel-plan.md 따름)
3. 운영자 대기 (인시던트·CS 즉시 대응)
4. metric 실시간 모니터링 (signup rate·error rate·response time)

**24~72h 대기**:
- 인시던트 발생 시 runbook 따라 대응 + 사후 분석
- CS 첫 응답 SLA 준수
- metric 시간대별 기록

### 2.5 launch metric 수집

| metric | 목표 | 실제 (24h) | 실제 (72h) |
|---|---|---|---|
| signup | N | | |
| key action (e.g., 첫 결제) | M | | |
| error rate | <X% | | |
| 99p response time | <Yms | | |
| CS 응답 SLA 준수율 | 100% | | |
| 인시던트 수·severity | 0 critical | | |

미달 metric은 launch retro(15)에서 분석.

### 2.6 launch-checklist.md 작성

`planning/cycles/v{N}-production/launch-checklist.md` 생성:

```markdown
---
cycle: v4-production
launch_date: YYYY-MM-DD
status: live
---

# Pre-launch 체크리스트
- [x] 인프라 load test 통과
- [x] 모니터링 active
- [x] 인시던트 runbook 작성
- [x] ToS·privacy policy 게시
- ...

# D-Day 실행
- 게시 일시: YYYY-MM-DD HH:MM
- 채널: [목록]
- 운영자 대기: 24h 직접

# 24h metric
- signup: N
- error rate: X%
- 인시던트: {목록}

# 72h metric
- ...

# 인시던트 사후 분석
- {Critical incident가 있었다면 root cause·대응·재발 방지}
```

## 3. 완료 체크리스트

- [ ] Pre-launch 체크리스트 모두 통과 (또는 사용자 명시 강행)
- [ ] D-Day 공식 게시 완료
- [ ] 24~72h 실시간 모니터링 + metric 기록
- [ ] 인시던트 발생 시 runbook 따라 대응
- [ ] `launch-checklist.md` 작성 완료
- [ ] 14단계(PR & Marketing) 진입 또는 후속 동작 결정

## 4. 산출물 스펙

위치:
- `planning/cycles/v{N}-production/launch-plan.md` (사전 계획)
- `planning/cycles/v{N}-production/launch-checklist.md` (실행·결과 기록)

## 5. 사이클 업데이트 모드

다음 production 사이클(`v5-production-update`):
- 새 feature·rebrand·확장 launch 시 동일 절차
- 이전 launch 인시던트 발견을 pre-launch 체크리스트에 추가

## 6. 좋은 예 vs 나쁜 예

- **launch 범위** — 좋은: "전체 공개. 점진적 rollout으로 24h마다 10%씩 확장." / 나쁜: "준비 안 됐는데 일단 전체 공개" (인시던트 처리 어려움).
- **모니터링** — 좋은: "운영자 24h 대기 + dashboard open + alert 설정." / 나쁜: "다음 날 아침에 확인" (golden window 놓침).
- **인시던트 대응** — 좋은: "Critical incident 시 30분 내 핫픽스·1h 내 사용자 공지." / 나쁜: "조용히 수정" (신뢰 erosion).

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. 단, production launch는 ceremony 영역 — 사전 점검 정확도 ↑.
- **코칭**: SKILL.md §1.4대로. 사용자가 pre-launch 체크리스트 미달 항목 강행 의향이면 위험 명시 후 OK 받기. metric 목표 모호하면 MVP retro의 PMF 시그널 base로 후보 제시.
