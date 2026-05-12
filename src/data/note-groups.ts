export const NOTE_GROUPS = {
  'discover-plan': {
    en: 'Discover & Plan',
    ko: '의도·기획',
    lead: '무엇을, 누구를 위해, 왜 만드는지부터 깎아내는 단계.',
    range: ['01', '04'] as const,
  },
  'design-architect': {
    en: 'Design & Architect',
    ko: '디자인·아키텍처',
    lead: '진짜 만들 모양을 시각·기술 결정으로 박는 단계.',
    range: ['05', '08'] as const,
  },
  'build-ship': {
    en: 'Build & Ship',
    ko: '빌드·배포',
    lead: '실제로 코드를 짜고 동작하는 상태로 만드는 단계.',
    range: ['09', '13'] as const,
  },
} as const;

export type NoteGroupKey = keyof typeof NOTE_GROUPS;
