import React, { useState, useEffect, useRef } from 'react';
import type { VoiceSection } from '../../services/types';

interface Props {
  sections: VoiceSection[];
  audioUrl?: string;
}

export const VoiceGuidePlayer: React.FC<Props> = ({ sections, audioUrl }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentSection, setCurrentSection] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  const speak = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.rate = 0.95;
      utter.pitch = 1;
      utter.onend = () => setIsPlaying(false);
      utteranceRef.current = utter;
      window.speechSynthesis.speak(utter);
      setIsPlaying(true);
    }
  };

  const pause = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else if ('speechSynthesis' in window) {
      window.speechSynthesis.pause();
      setIsPlaying(false);
    }
  };

  const resume = () => {
    if (audioRef.current) {
      audioRef.current.play();
      setIsPlaying(true);
    } else if ('speechSynthesis' in window) {
      window.speechSynthesis.resume();
      setIsPlaying(true);
    }
  };

  const playSection = (idx: number) => {
    setCurrentSection(idx);
    if (audioUrl && audioRef.current) {
      // Audio file playback
      audioRef.current.play().catch(() => {
        // Fallback to TTS
        speak(sections[idx]?.script_text ?? '');
      });
    } else {
      speak(sections[idx]?.script_text ?? '');
    }
  };

  const skipNext = () => {
    const next = Math.min(currentSection + 1, sections.length - 1);
    playSection(next);
  };

  const skipPrev = () => {
    const prev = Math.max(currentSection - 1, 0);
    playSection(prev);
  };

  if (!sections.length) return null;

  return (
    <div className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${isOpen ? 'w-80' : 'w-auto'}`}>
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2.5 rounded-full shadow-lg transition-all hover:scale-105 text-sm font-medium"
        >
          🎙 Voice Guide
        </button>
      ) : (
        <div className="bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-indigo-900/30 border-b border-gray-700">
            <span className="text-sm font-semibold text-indigo-300">🎙 Voice Guide</span>
            <button onClick={() => { setIsOpen(false); pause(); }} className="text-gray-500 hover:text-white text-lg leading-none">×</button>
          </div>

          {/* Current Section */}
          <div className="px-4 py-3">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
              {currentSection + 1} / {sections.length}
            </p>
            <p className="text-sm font-semibold text-white">{sections[currentSection]?.section_title}</p>
            <p className="text-xs text-gray-400 mt-1 line-clamp-2">
              {sections[currentSection]?.script_text?.slice(0, 100)}…
            </p>
          </div>

          {/* Controls */}
          <div className="flex items-center justify-center gap-3 px-4 pb-3">
            <button onClick={skipPrev} disabled={currentSection === 0} className="text-gray-400 hover:text-white disabled:opacity-30 transition-colors text-lg">⏮</button>
            <button
              onClick={() => isPlaying ? pause() : (isPlaying === false && window.speechSynthesis.paused ? resume() : playSection(currentSection))}
              className="w-10 h-10 bg-indigo-600 hover:bg-indigo-500 rounded-full flex items-center justify-center text-white transition-all hover:scale-110"
            >
              {isPlaying ? '⏸' : '▶'}
            </button>
            <button onClick={skipNext} disabled={currentSection === sections.length - 1} className="text-gray-400 hover:text-white disabled:opacity-30 transition-colors text-lg">⏭</button>
          </div>

          {/* Section List */}
          <div className="border-t border-gray-700 max-h-40 overflow-y-auto">
            {sections.map((s, i) => (
              <button
                key={i}
                onClick={() => playSection(i)}
                className={`w-full text-left px-4 py-2 text-xs transition-colors hover:bg-gray-800 ${
                  i === currentSection ? 'bg-indigo-900/40 text-indigo-300' : 'text-gray-400'
                }`}
              >
                {i + 1}. {s.section_title}
              </button>
            ))}
          </div>

          {/* Hidden audio element */}
          {audioUrl && <audio ref={audioRef} src={audioUrl} onEnded={() => setIsPlaying(false)} />}
        </div>
      )}
    </div>
  );
};
