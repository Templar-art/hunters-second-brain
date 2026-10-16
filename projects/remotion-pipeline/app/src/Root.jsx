import React from 'react';
import { AbsoluteFill, Composition, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { PAGES_9573, PAGES_9577 } from './captions.js';

const C = { ink: '#141413', paper: '#F0EEE6', accent: '#D97757' };
const FONT = 'Inter, "Inter Display", sans-serif';
const FPS = 30;

// Spring that starts at a given time (seconds)
const useSpringAt = (startSec, config = { stiffness: 220, damping: 22 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - Math.round(startSec * fps), fps, config });
};

function Captions({ pages }) {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const page = pages.find((p) => t >= p.start && t < p.end);
  if (!page) return null;
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-start', alignItems: 'center', paddingTop: 1300 }}>
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 36px', width: 1000 }}>
        {page.words.map((w, i) => (
          <Word key={i} w={w} t={t} pageStart={page.start} />
        ))}
      </div>
    </AbsoluteFill>
  );
}

function Word({ w, t, pageStart }) {
  const s = useSpringAt(pageStart, { stiffness: 260, damping: 18 });
  const active = t >= w.start && t < w.end + 0.15;
  return (
    <span
      style={{
        fontFamily: FONT,
        fontWeight: 900,
        fontSize: 88,
        lineHeight: 1.15,
        textTransform: 'uppercase',
        color: w.accent || active ? C.accent : '#FFFFFF',
        WebkitTextStroke: '10px #000',
        paintOrder: 'stroke fill',
        textShadow: '0 8px 24px rgba(0,0,0,.45)',
        display: 'inline-block',
        opacity: interpolate(s, [0, 0.4], [0, 1], { extrapolateRight: 'clamp' }),
        transform: `translateY(${(1 - s) * 40}px) scale(${(0.7 + 0.3 * s) * (active ? 1.08 : 1)})`,
      }}
    >
      {w.text}
    </span>
  );
}

// Lower-third style name card, top of frame (keeps face + mic clear)
function NameCard({ dur }) {
  const frame = useCurrentFrame();
  const s = useSpringAt(0);
  const bar = useSpringAt(0.15, { stiffness: 180, damping: 20 });
  const out = interpolate(frame, [dur * FPS - 8, dur * FPS], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ paddingTop: 220, paddingLeft: 80, opacity: out }}>
      <div style={{ transform: `translateX(${(1 - s) * -120}px)`, opacity: s }}>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 150, color: C.paper, letterSpacing: -4, textShadow: '0 6px 30px rgba(0,0,0,.5)' }}>TYSON</div>
        <div style={{ height: 14, width: 520 * bar, background: C.accent, margin: '6px 0 18px' }} />
        <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 46, color: C.paper, textShadow: '0 4px 18px rgba(0,0,0,.6)' }}>
          Fitness &amp; Nutrition Coach · Gold Coast
        </div>
      </div>
    </AbsoluteFill>
  );
}

// Big stat callout
function Stat({ big, small, dur }) {
  const frame = useCurrentFrame();
  const s = useSpringAt(0, { stiffness: 200, damping: 14 });
  const out = interpolate(frame, [dur * FPS - 8, dur * FPS], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ paddingTop: 200, alignItems: 'center', opacity: out }}>
      <div style={{ transform: `scale(${0.5 + 0.5 * s}) rotate(${(1 - s) * -8}deg)`, textAlign: 'center' }}>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 260, lineHeight: 1, color: C.accent, WebkitTextStroke: '8px #000', paintOrder: 'stroke fill' }}>{big}</div>
        <div style={{ fontFamily: FONT, fontWeight: 800, fontSize: 58, color: '#fff', letterSpacing: 8, WebkitTextStroke: '6px #000', paintOrder: 'stroke fill' }}>{small}</div>
      </div>
    </AbsoluteFill>
  );
}

function FollowButton() {
  const s = useSpringAt(0, { stiffness: 240, damping: 12 });
  const frame = useCurrentFrame();
  const pulse = 1 + 0.04 * Math.sin(frame / 4);
  return (
    <AbsoluteFill style={{ paddingTop: 260, alignItems: 'center' }}>
      <div style={{ transform: `scale(${s * pulse})`, background: C.accent, color: '#fff', fontFamily: FONT, fontWeight: 900, fontSize: 84, padding: '28px 80px', borderRadius: 999, boxShadow: '0 16px 40px rgba(0,0,0,.4)' }}>
        + FOLLOW
      </div>
    </AbsoluteFill>
  );
}

const sec = (s) => Math.round(s * FPS);

export function Intro9573() {
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <OffthreadVideo src={staticFile('IMG_9573.mp4')} />
      <Sequence from={sec(6.2)} durationInFrames={sec(4.0)}><NameCard dur={4.0} /></Sequence>
      <Sequence from={sec(10.3)} durationInFrames={sec(2.4)}><Stat big="9 YRS" small="OF TRAINING" dur={2.4} /></Sequence>
      <Sequence from={sec(17.0)} durationInFrames={sec(2.6)}><Stat big="9 YRS" small="OF LESSONS → YOU" dur={2.6} /></Sequence>
      <Captions pages={PAGES_9573} />
    </AbsoluteFill>
  );
}

export function Outro9577() {
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <OffthreadVideo src={staticFile('IMG_9577.mp4')} />
      <Sequence from={sec(2.0)}><FollowButton /></Sequence>
      <Captions pages={PAGES_9577} />
    </AbsoluteFill>
  );
}

export function Full() {
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <Sequence durationInFrames={sec(25.19)}><Intro9573 /></Sequence>
      <Sequence from={sec(25.19)}><Outro9577 /></Sequence>
    </AbsoluteFill>
  );
}

export const Root = () => (
  <>
    <Composition id="Full" component={Full} durationInFrames={sec(25.19) + sec(4.07)} fps={FPS} width={1080} height={1920} />
    <Composition id="Intro9573" component={Intro9573} durationInFrames={sec(25.19)} fps={FPS} width={1080} height={1920} />
    <Composition id="Outro9577" component={Outro9577} durationInFrames={sec(4.07)} fps={FPS} width={1080} height={1920} />
  </>
);
