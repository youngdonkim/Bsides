#!/bin/bash
# no-auto-deploy.sh — PreToolUse(Bash) guard
#
# 사용자가 명시적으로 "배포해" / "deploy해" 라고 지시하지 않은 한
# Claude가 자동으로 production deploy 명령을 호출하지 못하게 차단.
# 차단 대상:
#   - vercel --prod / vercel deploy --prod / vercel deploy / vercel --target production
#   - git push to main (PR 워크플로 우회 차단)
#       - 명령어에 main이 명시된 경우 (예: git push origin main)
#       - 현재 브랜치가 main인 상태의 모든 git push (gap 봉쇄)
#
# 정밀화: shell separator(&&, ||, ;, | , &)로 sub-command 분리 후
# 각 sub-command의 첫 토큰이 vercel/git일 때만 검사.
# → commit message 등 quote 안 텍스트의 우연한 매칭 회피.
#
# 자세히: .claude/rules/deploy.md

set -euo pipefail

INPUT=$(cat)
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')

[ -z "$COMMAND" ] && exit 0

# shell separator로 sub-command 분리
NORMALIZED=$(printf '%s' "$COMMAND" | sed -E 's/(&&|\|\||;|\| |&[^&])/\n/g')

block_reason=""
while IFS= read -r sub; do
  # leading/trailing 공백 제거
  sub_trimmed=$(printf '%s' "$sub" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')
  [ -z "$sub_trimmed" ] && continue

  # 첫 토큰
  first=$(printf '%s' "$sub_trimmed" | awk '{print $1}')

  case "$first" in
    vercel)
      if printf '%s' "$sub_trimmed" | grep -qE '(^| )(--prod|--target[= ]production|deploy)( |$)'; then
        block_reason="vercel-deploy"
        break
      fi
      ;;
    git)
      # main 명시 패턴
      if printf '%s' "$sub_trimmed" | grep -qE 'git +push( +[^ ]+)* +(origin +)?main([: ]|$)|git +push( +[^ ]+)* +main:main'; then
        block_reason="main-push"
        break
      fi
      # 현재 브랜치가 main인 상태의 모든 git push 차단 (gap 봉쇄)
      if printf '%s' "$sub_trimmed" | grep -qE '^git +push( |$)'; then
        current_branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        if [ "$current_branch" = "main" ]; then
          block_reason="main-push"
          break
        fi
      fi
      ;;
  esac
done <<EOF
$NORMALIZED
EOF

case "$block_reason" in
  vercel-deploy)
    cat >&2 <<'MSG'
BLOCKED: Vercel deploy 명령은 사용자 명시 요청 시에만 실행.

이유: 코드 수정 후 자동 배포 금지가 프로젝트 룰. 모든 배포는
"배포해" 같은 사용자 명시 지시 후에만 진행. PR을 main에 머지하면
Vercel GitHub integration이 자동 배포하므로, 수동 vercel CLI 호출은
대개 불필요함.

참고: .claude/rules/deploy.md
MSG
    exit 2
    ;;
  main-push)
    cat >&2 <<'MSG'
BLOCKED: main branch 직접 push 금지.

이유: 모든 변경은 PR 워크플로를 거쳐야 함 (CI 통과 게이트).
feature branch → push -u → PR → CI → merge 흐름 사용.

참고: .claude/rules/deploy.md
MSG
    exit 2
    ;;
esac

exit 0
