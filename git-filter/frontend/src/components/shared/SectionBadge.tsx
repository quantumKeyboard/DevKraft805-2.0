import React from 'react';
import type { Section } from '../../services/types';

const SECTION_STYLES: Record<Section, string> = {
  UI:       'bg-blue-500/20 text-blue-300 border-blue-500/30',
  Backend:  'bg-green-500/20 text-green-300 border-green-500/30',
  Utils:    'bg-gray-500/20 text-gray-300 border-gray-500/30',
  Config:   'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
  Tests:    'bg-purple-500/20 text-purple-300 border-purple-500/30',
  External: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
};

interface Props {
  section: Section | string;
  size?: 'sm' | 'md';
}

export const SectionBadge: React.FC<Props> = ({ section, size = 'sm' }) => {
  const style = SECTION_STYLES[section as Section] ?? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30';
  return (
    <span
      className={`inline-block font-semibold rounded-full border ${style} ${
        size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-sm px-3 py-1'
      }`}
    >
      {section}
    </span>
  );
};
