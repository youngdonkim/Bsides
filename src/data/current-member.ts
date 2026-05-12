export type CycleState = 'active' | 'between';

export interface CurrentMember {
  cycle_state: CycleState;
  project_title: string | null;
  member_name: string | null;
  member_kind: string | null;
  curriculum: string | null;
  progress_label: string | null;
  next_workshop_at: string | null;
  next_workshop_format: string | null;
  live_pill_label: string | null;
  current_round_slug: string | null;
}

export const CURRENT_MEMBER: CurrentMember = {
  cycle_state: 'active',
  project_title: '도토리룸 — 원룸 계약, 빠진 특약 같이 잡아요',
  member_name: '김도현',
  member_kind: '본인 프로젝트',
  curriculum: '아이템·기획·개발·디자인·출시·홍보 6단계',
  progress_label: '3회차 (6회차 사이클)',
  next_workshop_at: '2026-05-18T20:00:00+09:00',
  next_workshop_format: '온라인 화상',
  live_pill_label: '다음 워크샵 D-7',
  current_round_slug: 'round-3-mimirog-launch',
};
