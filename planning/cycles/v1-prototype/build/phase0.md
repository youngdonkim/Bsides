# Phase 0: Setup & Tooling

## 사전 준비

먼저 아래 산출물을 반드시 읽고 프로젝트의 전체 설계 의도를 완전히 이해하라:

- `planning/cycles/v1-prototype/intent.md` — 무엇·왜·누구·platform
- `planning/cycles/v1-prototype/prd.md` — Must/Should/Could/Won't 명세 + 비기능 요구사항
- `planning/cycles/v1-prototype/architecture.md` — 기술 스택·시스템 구조·디렉토리·API 명세·횡단 룰 적용
- `planning/cycles/v1-prototype/data-model.md` — ProgressPost·NotePost·CurrentMember·OperatorMeta 4 엔티티
- `planning/cycles/v1-prototype/design/migration-analysis.md` — site/ 자산 인벤토리 + Astro 매핑
- `planning/cycles/v1-prototype/design/migration-plan.md` — 컴포넌트 매핑 표 + phase 분할
- `planning/cycles/v1-prototype/brand-guide.md` — 컬러·voice·시그널·금지 사항
- `planning/cycles/v1-prototype/sketch.md` — 시나리오 S1~S5 + 화면별 엣지 케이스
- `site/` — design SoT (현재 plain HTML+CSS+JS, 시각 정합 기준)
- `.claude/rules/perf-astro.md` — Astro 5 perf baseline (Image·Font·Critical CSS·Vercel adapter)

이전 phase 산출물:

없음 (첫 phase)

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

Astro 5 + @astrojs/vercel + TypeScript 프로젝트 초기 셋업. 빈 페이지가 dev server에서 응답하는 상태.

## 작업 내용

### 0.1 Astro 프로젝트 init

프로젝트 루트(`/Users/youngdonkim/dev/Bsides`)에서:

```bash
npm create astro@latest . -- --template minimal --typescript strict --no-install --no-git
```

기존 `site/`·`planning/`·`.claude/`·`Bsides.html`·`design-system.html`·`spooni-character.png` 등은 보존. Astro init이 만드는 파일과 conflict나면 `site/`·`planning/`·`.claude/`·이미지·HTML 파일들은 유지하고 `src/`·`astro.config.mjs`·`package.json`·`tsconfig.json`만 새로 생성.

### 0.2 의존성 설치

```bash
npm install
npm install @astrojs/vercel @astrojs/sitemap @vercel/analytics
```

(`@astrojs/sitemap`·`@vercel/analytics`는 Phase 6·7에서 사용. 0단계에 한 번에 설치.)

### 0.3 astro.config.mjs

```js
// astro.config.mjs
import { defineConfig, fontProviders } from 'astro/config';
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'static',
  site: 'https://bsides.kr',
  adapter: vercel({
    webAnalytics: { enabled: true },
    imageService: true,
    imagesConfig: { sizes: [320, 640, 1280] },
  }),
  // fonts·integrations는 Phase 1·6에서 추가
});
```

### 0.4 tsconfig.json

Astro init이 만든 strict tsconfig 유지. 추가 필요 없음. `astro/tsconfigs/strict` extends.

### 0.5 package.json scripts 정합

```json
"scripts": {
  "dev": "astro dev",
  "build": "astro build",
  "preview": "astro preview",
  "astro": "astro",
  "typecheck": "astro check"
}
```

### 0.6 .gitignore

Astro init 기본 + `.vercel/`, `dist/`, `.env*` 패턴 추가 확인.

### 0.7 빈 페이지 1개

`src/pages/index.astro`에 placeholder:

```astro
---
---
<html lang="ko">
  <head><meta charset="utf-8" /><title>Bsides</title></head>
  <body>setup OK</body>
</html>
```


## Acceptance Criteria

```bash
npm run dev &           # dev server background
sleep 5
curl -s http://localhost:4321/ | grep "setup OK"
npm run build           # 빌드 성공
npm run typecheck       # astro check 통과
```

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 0 status를 `"completed"`로 변경.

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

이 phase 특이사항: 0단계는 외부 호출·시크릿 신규 없음. needs_review 트리거 없음.

## 주의사항

- 기존 `site/`·`planning/`·`.claude/`·`Bsides.html`·`design-system.html`·이미지 폴더(`spooni-characters/`·`spponi-character.png` 등) **삭제 금지**.
- `npm create astro`가 conflict 경고하면 root에서 새 src/만 생성하는 식으로 수동 진행.
- `.env*`·`.vercel/` gitignore 누락 시 시크릿 노출 위험.
