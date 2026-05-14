---
name: 14-pr-marketing
description: Production 사이클 홍보·마케팅 단계 가이드. 본격 multi-channel 캠페인 · 유료 광고 옵션 · 브랜드 캠페인 · 측정 정교화. MVP의 작은 실험과 다르게 scale·예산·정량 측정이 핵심. SKILL.md §3의 14번 단계.
---

production 마케팅은 **본격 캠페인**. MVP에서 PMF·채널 적합도 검증된 base 위에서 **scale·예산·정교 측정**으로 사용자 확보. 1인칭 이야기는 여전히 중요하지만 채널·예산·brand 차원이 추가됨.

## 1. 단계 목표

- **multi-channel 캠페인 plan** — 검증된 채널 + 신규 채널 확장
- **유료 광고 예산 운용** (선택) — ROI 측정 가능한 단위로
- **브랜드 캠페인 운영** — 브랜드 essence를 scale 게시물·콘텐츠에 일관 적용
- **정교 측정 framework** — funnel·cohort·attribution·LTV·CAC

## 2. 진행 절차

### 2.1 사이클 분기

- 첫 production 마케팅 (`v4-production`): launch 동시 본격 캠페인.
- 이후 사이클: 신규 feature·rebrand·시장 확장 시.

### 2.2 자동 점검 (AI 단독)

- MVP retro의 채널 적합도 결과 확인 (어디서 conversion 강했나)
- production 분석 활성 (signup·retention·revenue·attribution funnel)
- 예산 결정 — 사용자 확인 필요 (광고비 0 / 작게 / 본격)
- 브랜드 가이드라인 (brand-guide.md) 최신 상태

### 2.3 사용자 결정 — 캠페인 plan

```
production 마케팅 plan — 결정 필요:

1. 채널 mix
   - MVP 검증 채널 (확장)
   - 신규 채널 후보 (광고·PR·partnership)

2. 예산
   - 광고비 (0 / 월 N만원 / 본격)
   - 콘텐츠 제작 (자체 / 외주)

3. 브랜드 캠페인
   - 단발 게시 / 시리즈 / 캠페인 형식
   - brand essence 일관 가이드라인

4. 측정 framework
   - 핵심 KPI (signup·MRR·CAC·LTV·NPS)
   - cohort 분석 단위 (주·월)
   - attribution 방식 (last-click·multi-touch)

답에 따라 marketing-plan.md 작성.
```

### 2.4 캠페인 실행

**원칙**: **계획적·multi-channel·측정 가능**.

- 채널별 plan 동시 또는 순차 실행
- 게시물·광고 carbon brand-guide essence 정합 검증
- 예산 소진 페이스 daily 모니터링
- A/B 테스트 가능한 단위는 분리 측정

`channel-experiments.md`에 채널별 결과 기록 (MVP 패턴 그대로).

### 2.5 측정·분석

| metric | 목표 | 실제 (주 1) | 실제 (월 1) |
|---|---|---|---|
| signup (채널별) | N | | |
| CAC (채널별) | <$X | | |
| 90d retention | >Y% | | |
| LTV | >$Z | | |
| NPS | >50 | | |

미달 metric은 retro(15)에서 root cause·다음 사이클 input.

### 2.6 marketing-plan.md·channel-experiments.md

위치: `planning/cycles/v{N}-production/`

```markdown
# marketing-plan.md
---
cycle: v4-production
budget_total: ...
duration: ...
---

## 채널 mix
- ...

## 예산 분배
- ...

## 브랜드 캠페인 가이드라인
- ...

## 측정 KPI·target
- ...
```

## 3. 완료 체크리스트

- [ ] 채널 mix 결정·plan 작성
- [ ] 예산 사용자 확인
- [ ] 브랜드 가이드라인 일관 적용 점검
- [ ] 측정 framework 활성 (funnel·cohort·attribution)
- [ ] 캠페인 실행 + 결과 기록
- [ ] KPI 측정값 vs target 비교
- [ ] 미달 항목 root cause 분석

## 4. 산출물 스펙

위치:
- `planning/cycles/v{N}-production/marketing-plan.md`
- `planning/cycles/v{N}-production/channel-experiments.md`

## 5. 사이클 업데이트 모드

다음 production 사이클: 이전 캠페인 결과 base로 채널 mix·예산·메시지 조정.

## 6. 좋은 예 vs 나쁜 예

- **채널 mix** — 좋은: "MVP 검증 채널(Disquiet) 확장 + 신규(X 광고) 실험. 예산 70:30." / 나쁜: "처음부터 5개 채널 동시" (관리 폭주).
- **예산** — 좋은: "월 50만원, 채널별 CAC 측정 후 재분배." / 나쁜: "Performance 마케팅 대행사에 일괄 위임".
- **브랜드 일관** — 좋은: "모든 게시물·광고 brand-guide essence·voice 사전 점검." / 나쁜: "채널별 카피 따로따로 작성".
- **측정** — 좋은: "channel→signup→key action→90d retention funnel 분리 측정." / 나쁜: "총 signup만 카운트".

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게.
- **코칭**: SKILL.md §1.4대로. 예산 모호하면 MVP 데이터 base 작은 단위로 시작 권장. 측정 framework 모호하면 KPI 후보 표 제시. 광고 운영 경험 없으면 작은 예산·짧은 기간 실험부터.
