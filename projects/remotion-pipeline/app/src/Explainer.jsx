// Explainer-style edit (reference: "Definitions" Webhooks/SQL reels), fitness palette.
// Talking head ↔ full-screen graphic scenes with iris wipes, face-in-circle,
// eyebrow + condensed titles, UI cards/diagrams, highlight-box captions.
import React from 'react';
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from 'remotion';
import '@fontsource/barlow-condensed/700.css';
import '@fontsource/barlow-condensed/800.css';
import '@fontsource/jetbrains-mono/500.css';
import '@fontsource/inter/600.css';
import { CameraMotionBlur } from '@remotion/motion-blur';
import { LightLeak } from '@remotion/light-leaks';
import { Dumbbell3D } from './Dumbbell3D.jsx';
import WORDS from './words.json';
import FACES from './faces.json';
import S from './script.json';

export const FPS = 30;
const sec = (s) => Math.round(s * FPS);
// Dead-air trim (must match tools/make_edit.sh). Times are "source time":
// IMG_9573 = 0–25.19, IMG_9577 = 25.19 + its own time.
const KEEP = [[0.15, 3.22], [3.53, 5.56], [6.28, 10.18], [10.38, 12.63], [12.80, 15.15], [16.27, 23.19], [23.49, 25.0], [25.46, 28.93]];
const SEG_START = KEEP.reduce((acc, [a, b], i) => [...acc, acc[i] + (b - a)], [0]);
// source time -> edit time (times inside a removed gap snap to the next kept frame)
export const M = (g) => {
  for (let i = 0; i < KEEP.length; i++) {
    const [a, b] = KEEP[i];
    if (g < a) return SEG_START[i];
    if (g <= b) return SEG_START[i] + (g - a);
  }
  return SEG_START[KEEP.length];
};
const EDIT_LEN = SEG_START[KEEP.length];
const B_START = M(25.46);
const END_LEN = 2.2;
export const TOTAL = sec(EDIT_LEN) + sec(END_LEN);

const C = {
  dark: '#0E1411', dark2: '#17201B', light: '#F2F3EE', card: '#FFFFFF',
  lime: '#C3F067', limeDeep: '#8DBF2E', ink: '#0E1411', muted: '#7C857F', line: '#D9DDD5',
};
const TITLE = '"Barlow Condensed", sans-serif';
const MONO = '"JetBrains Mono", monospace';
const BODY = 'Inter, sans-serif';

const useT = () => useCurrentFrame() / FPS;
const sp = (t, start, cfg = { stiffness: 90, damping: 20 }) =>
  spring({ frame: Math.round((t - start) * FPS), fps: FPS, config: cfg });
const lerp = (t, a, b, from = 0, to = 1, ease = Easing.out(Easing.cubic)) =>
  interpolate(t, [a, b], [from, to], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease });

// ---------- shared pieces ----------

// Music-synced pulse (96 bpm bed): 1 on each beat, decaying
const beatPulse = () => {
  const f = useCurrentFrame() / FPS;
  const ph = (f / (60 / 96)) % 1;
  return Math.exp(-ph * 6);
};
const faceAt = (frame) => FACES[Math.max(0, Math.min(FACES.length - 1, Math.round(frame) || 0))];

function Eyebrow({ text, t, at = 0, color = C.limeDeep }) {
  const s = sp(t, at);
  return (
    <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 30, letterSpacing: 6, textTransform: 'uppercase', color, opacity: s, transform: `translateX(${(1 - s) * -30}px)` }}>
      {text}
    </div>
  );
}

// Masked slide-up title, word by word
function Title({ text, t, at = 0, color, size = 150 }) {
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0 26px', fontFamily: TITLE, fontWeight: 800, fontSize: size, lineHeight: 0.95, color, letterSpacing: -1 }}>
      {text.split(' ').map((w, i) => {
        const s = sp(t, at + 0.12 * i, { stiffness: 80, damping: 18 });
        return (
          <span key={i} style={{ overflow: 'hidden', display: 'inline-block', paddingBottom: 8 }}>
            <span style={{ display: 'inline-block', transform: `translateY(${(1 - s) * 110}%)` }}>{w}</span>
          </span>
        );
      })}
    </div>
  );
}

function Header({ eyebrow, title, t, dark }) {
  return (
    <div style={{ position: 'absolute', left: 80, top: 150, width: 600 }}>
      <Eyebrow text={eyebrow} t={t} at={0.05} color={dark ? C.lime : C.limeDeep} />
      <div style={{ height: 14 }} />
      <Title text={title} t={t} at={0.1} color={dark ? C.light : C.ink} size={124} />
    </div>
  );
}

// Corner shards (the reference's triangle confetti), lime family
function Shards({ t, at = 0, corner = 'br', seed = 1 }) {
  const tris = [
    [0, 0, 150, 40, 30, 150, C.lime, 0],
    [120, 60, 230, 10, 200, 170, C.limeDeep, 0.08],
    [40, 140, 140, 190, 10, 260, '#5E8A1E', 0.14],
  ];
  const flip = corner === 'bl' || corner === 'tl' ? -1 : 1;
  const top = corner[0] === 't';
  return (
    <svg width="320" height="300" viewBox="0 0 260 280"
      style={{ position: 'absolute', [top ? 'top' : 'bottom']: top ? 40 : 300, [flip === 1 ? 'right' : 'left']: 20, transform: `scaleX(${flip})`, overflow: 'visible' }}>
      {tris.map(([x1, y1, x2, y2, x3, y3, fill, d], i) => {
        const s = sp(t, at + d, { stiffness: 140, damping: 14 });
        const cx = (x1 + x2 + x3) / 3, cy = (y1 + y2 + y3) / 3;
        const drift = Math.sin(t * 1.3 + i * 2 + seed) * 6 + beatPulse() * 10;
        return (
          <polygon key={i} points={`${x1},${y1} ${x2},${y2} ${x3},${y3}`} fill={fill} opacity={0.95}
            transform={`translate(${(1 - s) * 120},${(1 - s) * 80 + drift}) rotate(${(1 - s) * 90 + drift} ${cx} ${cy}) scale(${s})`}
            style={{ transformOrigin: `${cx}px ${cy}px` }} />
        );
      })}
    </svg>
  );
}

// Face in a circle (muted copy of the source, synced via startFrom)
function FaceCircle({ t, at = 0, src, startFrom, size = 300, x = 700, y = 120 }) {
  const s = sp(t, at, { stiffness: 180, damping: 20 });
  const f = faceAt(startFrom + useCurrentFrame()); // tracked face (tools/track.py)
  const k = (size * 0.62) / f.w; // face fills ~62% of the circle
  return (
    <div style={{ position: 'absolute', left: x, top: y, width: size, height: size, borderRadius: '50%', overflow: 'hidden', transform: `scale(${s})`, boxShadow: '0 18px 40px rgba(0,0,0,.25)', border: `6px solid ${C.lime}` }}>
      <div style={{ position: 'absolute', left: size / 2 - f.cx * k, top: size / 2 - (f.cy + f.w * 0.12) * k, width: 1080 * k, height: 1920 * k }}>
        <OffthreadVideo src={staticFile(src)} startFrom={startFrom} muted style={{ width: '100%', height: '100%' }} />
      </div>
    </div>
  );
}

// Iris wipe wrapper: scene circle-reveals in from a point and closes out
function Scene({ dur, origin = [540, 960], children, bg }) {
  const t = useT();
  const R = 2300;
  const open = lerp(t, 0, 0.9, 0, R, Easing.inOut(Easing.cubic));
  const close = lerp(t, dur - 0.8, dur, R, 0, Easing.inOut(Easing.cubic));
  const r = Math.min(open, close);
  return (
    <AbsoluteFill style={{ clipPath: `circle(${r}px at ${origin[0]}px ${origin[1]}px)`, background: bg }}>
      {children}
    </AbsoluteFill>
  );
}

function Card({ children, style, s = 1 }) {
  return (
    <div style={{ background: C.card, borderRadius: 22, boxShadow: '0 14px 40px rgba(14,20,17,.14)', padding: '26px 30px', opacity: Math.min(1, s * 1.5), transform: `translateY(${(1 - s) * 60}px) scale(${0.92 + 0.08 * s})`, ...style }}>
      {children}
    </div>
  );
}

const ICONS = {
  hotel: 'M6 30 V8 H26 V30 M3 30 H29 M11 13 H13 M19 13 H21 M11 19 H13 M19 19 H21 M14 30 V25 H18 V30',
  dumbbell: 'M4 16 H28 M7 10 V22 M10 8 V24 M22 8 V24 M25 10 V22',
};
function Icon({ name, active, draw = 1 }) {
  const col = active ? C.ink : C.lime;
  return (
    <div style={{ width: 74, height: 74, borderRadius: 16, background: active ? C.lime : C.dark, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
      <svg width="44" height="44" viewBox="0 0 32 32">
        <path d={ICONS[name]} fill="none" stroke={col} strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - draw} />
      </svg>
    </div>
  );
}

// ---------- graphic scenes ----------

const SRC_A = 'edit.mp4';

// 10.3–12.7  "training for about 9 years"
function SceneYears({ dur, start }) {
  const t = useT();
  const years = Array.from({ length: 10 }, (_, i) => 2017 + i);
  const fill = lerp(t, 0.5, 2.0, 0, 1, Easing.inOut(Easing.cubic));
  const count = Math.round(fill * S.years.value);
  return (
    <Scene dur={dur} bg={C.light} origin={[540, 760]}>
      <Header eyebrow={S.years.eyebrow} title={S.years.title} t={t} />
      <FaceCircle t={t} at={0.25} src={SRC_A} startFrom={sec(start)} />
      <div style={{ position: 'absolute', left: 80, right: 80, top: 640 }}>
        <Card s={sp(t, 0.3)} style={{ padding: '40px 44px' }}>
          <div style={{ fontFamily: MONO, fontSize: 26, color: C.muted, letterSpacing: 3 }}>{S.years.label}</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 40, margin: '20px 0 24px' }}>
            <svg width="260" height="260" viewBox="0 0 260 260">
              <circle cx="130" cy="130" r="108" fill="none" stroke={C.line} strokeWidth="22" />
              <circle cx="130" cy="130" r="108" fill="none" stroke={C.lime} strokeWidth="22" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - fill} transform="rotate(-90 130 130)" />
              <text x="130" y="158" textAnchor="middle" fontFamily="Barlow Condensed" fontWeight="800" fontSize="96" fill={C.ink}>{count}</text>
            </svg>
            <div style={{ fontFamily: TITLE, fontWeight: 800, fontSize: 120, lineHeight: 0.9, color: C.ink }}>
              years<br /><span style={{ color: C.limeDeep }}>training</span>
            </div>
          </div>
          <div style={{ position: 'relative', height: 70 }}>
            <div style={{ position: 'absolute', top: 16, left: 0, right: 0, height: 10, borderRadius: 5, background: C.line }} />
            <div style={{ position: 'absolute', top: 16, left: 0, width: `${fill * 100}%`, height: 10, borderRadius: 5, background: C.lime }} />
            {years.map((y, i) => {
              const on = fill >= i / 9 - 0.001;
              return <div key={y} style={{ position: 'absolute', left: `calc(${(i / 9) * 100}% - 13px)`, top: 8, width: 26, height: 26, borderRadius: 13, background: on ? C.lime : C.card, border: `4px solid ${on ? C.ink : C.line}` }} />;
            })}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: MONO, fontSize: 24, color: C.muted }}>
            <span>DAY 1</span><span>NOW</span>
          </div>
        </Card>
      </div>
      <Shards t={t} at={0.4} corner="br" />
    </Scene>
  );
}

// 12.7–15.5  "I also work full time at a hotel"
function SceneHotel({ dur, start }) {
  const t = useT();
  const rows = S.hotel.rows;
  return (
    <Scene dur={dur} bg={C.dark} origin={[540, 1200]}>
      <Header eyebrow={S.hotel.eyebrow} title={S.hotel.title} t={t} dark />
      <FaceCircle t={t} at={0.2} src={SRC_A} startFrom={sec(start)} />
      <div style={{ position: 'absolute', left: 120, right: 120, top: 640 }}>
        {rows.map((r, i) => {
          const s = sp(t, 0.5 + i * 0.5);
          return (
            <React.Fragment key={i}>
              {i > 0 && (
                <div style={{ display: 'flex', justifyContent: 'center', height: 110 }}>
                  <div style={{ width: 4, height: `${lerp(t, 0.55, 0.9) * 100}%`, background: `repeating-linear-gradient(${C.lime} 0 10px, transparent 10px 20px)` }} />
                </div>
              )}
              <Card s={s} style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
                <Icon name={r.icon} active={i === 1 && t > 1.1} draw={lerp(t, 0.6 + i * 0.5, 1.4 + i * 0.5)} />
                <div>
                  <div style={{ fontFamily: TITLE, fontWeight: 700, fontSize: 64, color: C.ink, lineHeight: 1 }}>{r.name}</div>
                  <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted, letterSpacing: 3, marginTop: 6 }}>{r.sub}</div>
                </div>
              </Card>
            </React.Fragment>
          );
        })}
        <div style={{ textAlign: 'center', marginTop: 34, opacity: sp(t, 1.2) }}>
          <span style={{ fontFamily: MONO, fontSize: 26, background: C.lime, color: C.ink, padding: '8px 20px', borderRadius: 30 }}>{S.hotel.pill}</span>
        </div>
      </div>
      <Shards t={t} at={0.3} corner="bl" seed={3} />
    </Scene>
  );
}

// 16.1–19.6  "sharing things that took me 9 years to learn"
function SceneLessons({ dur, start }) {
  const t = useT();
  const posts = S.lessons.posts;
  return (
    <Scene dur={dur} bg={C.light} origin={[880, 270]}>
      <Header eyebrow={S.lessons.eyebrow} title={S.lessons.title} t={t} />
      <FaceCircle t={t} at={0.2} src={SRC_A} startFrom={sec(start)} />
      <div style={{ position: 'absolute', left: 80, right: 80, top: 660, display: 'flex', flexDirection: 'column', gap: 26 }}>
        {posts.map((p, i) => {
          const s = sp(t, 0.5 + i * 0.4);
          const saved = t > 1.2 + i * 0.5;
          return (
            <Card key={i} s={s} style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
              <div style={{ width: 120, height: 150, borderRadius: 14, background: C.dark, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ width: 0, height: 0, borderTop: '22px solid transparent', borderBottom: '22px solid transparent', borderLeft: `36px solid ${C.lime}`, marginLeft: 8 }} />
              </div>
              <div style={{ flex: 1 }}>
                <span style={{ fontFamily: MONO, fontSize: 22, background: C.dark, color: C.lime, padding: '4px 14px', borderRadius: 20 }}>{p.tag}</span>
                <div style={{ fontFamily: TITLE, fontWeight: 700, fontSize: 60, color: C.ink, marginTop: 10 }}>{p.title}</div>
              </div>
              <div style={{ fontFamily: MONO, fontSize: 22, padding: '10px 18px', borderRadius: 30, background: saved ? C.lime : C.light, color: C.ink, border: `2px solid ${saved ? C.lime : C.line}` }}>
                {saved ? '✓ SAVED' : 'SAVE'}
              </div>
            </Card>
          );
        })}
      </div>
      <Shards t={t} at={0.3} corner="br" seed={5} />
    </Scene>
  );
}

// 19.6–23.3  "skip all the mistakes I made along the way"
function SceneShortcut({ dur, start }) {
  const t = useT();
  const long = lerp(t, 0.4, 2.0, 0, 1, Easing.inOut(Easing.quad));
  const short = lerp(t, 1.9, 2.6, 0, 1, Easing.out(Easing.cubic));
  const LONG = 'M 120 1500 C 120 1250, 900 1350, 880 1150 S 160 1000, 220 820 S 960 760, 900 600';
  const marks = [[480, 1350], [700, 1080], [330, 930], [650, 760]];
  return (
    <Scene dur={dur} bg={C.dark} origin={[540, 1500]}>
      <Header eyebrow={S.shortcut.eyebrow} title={S.shortcut.title} t={t} dark />
      <FaceCircle t={t} at={0.2} src={SRC_A} startFrom={sec(start)} />
      <svg width="1080" height="1920" style={{ position: 'absolute', inset: 0 }}>
        <path d={LONG} fill="none" stroke="#3A463F" strokeWidth="14" strokeLinecap="round" />
        <path d={LONG} fill="none" stroke={C.muted} strokeWidth="14" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - long} />
        {marks.map(([x, y], i) => {
          const s = sp(t, 0.6 + i * 0.32, { stiffness: 260, damping: 14 });
          return (
            <g key={i} transform={`translate(${x} ${y}) scale(${s})`}>
              <circle r="34" fill="#E5484D" />
              <path d="M -12 -12 L 12 12 M 12 -12 L -12 12" stroke="#fff" strokeWidth="7" strokeLinecap="round" />
            </g>
          );
        })}
        <path d="M 120 1500 L 900 600" fill="none" stroke={C.lime} strokeWidth="18" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - short} />
        <circle cx="120" cy="1500" r="26" fill={C.light} />
        <g transform={`translate(900 600) scale(${sp(t, 2.4, { stiffness: 260, damping: 12 })})`}>
          <circle r="44" fill={C.lime} />
          <path d="M -18 0 L -4 14 L 20 -12" fill="none" stroke={C.ink} strokeWidth="8" strokeLinecap="round" strokeLinejoin="round" />
        </g>
      </svg>
      <div style={{ position: 'absolute', left: 80, top: 470, fontFamily: MONO, fontSize: 26, color: C.muted, opacity: sp(t, 0.5) }}>{S.shortcut.mine}</div>
      <div style={{ position: 'absolute', left: 80, top: 515, fontFamily: MONO, fontSize: 26, color: C.lime, opacity: sp(t, 2.0) }}>{S.shortcut.yours}</div>
    </Scene>
  );
}

// ---------- overlays on talking head ----------

function TopTitle({ eyebrow, title, dur }) {
  const t = useT();
  const out = Math.min(lerp(t, 0, 0.6), lerp(t, dur - 0.7, dur, 1, 0));
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 0, height: 560, background: 'linear-gradient(rgba(14,20,17,.75), rgba(14,20,17,0))' }} />
      <div style={{ position: "absolute", left: 80, top: 150, width: 720 }}>
        <Eyebrow text={eyebrow} t={t} at={0.05} color={C.lime} />
        <div style={{ height: 14 }} />
        <Title text={title} t={t} at={0.1} color={C.light} size={150} />
      </div>
      <Shards t={t} at={0.15} corner="tr" seed={2} />
    </AbsoluteFill>
  );
}

function NameTag({ dur }) {
  const t = useT();
  const s = sp(t, 0, { stiffness: 80, damping: 18 });
  const out = lerp(t, dur - 0.7, dur, 1, 0);
  const pin = sp(t, 1.9, { stiffness: 110, damping: 16 });
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: 'absolute', left: 70, top: 220, display: 'flex', alignItems: 'center', gap: 24, background: C.card, borderRadius: 24, padding: '24px 34px 24px 24px', boxShadow: '0 18px 50px rgba(0,0,0,.3)', transform: `translateX(${(1 - s) * -700}px)` }}>
        <div style={{ width: 96, height: 96, borderRadius: 18, background: C.dark, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: TITLE, fontWeight: 800, fontSize: 64, color: C.lime }}>T</div>
        <div>
          <div style={{ fontFamily: TITLE, fontWeight: 800, fontSize: 70, color: C.ink, lineHeight: 1 }}>{S.name.name}</div>
          <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, letterSpacing: 3, marginTop: 6 }}>{S.name.role}</div>
        </div>
      </div>
      <div style={{ position: 'absolute', left: 90, top: 400, transform: `scale(${pin})`, transformOrigin: 'left center', fontFamily: MONO, fontSize: 26, background: C.lime, color: C.ink, padding: '10px 22px', borderRadius: 30 }}>
        📍 {S.name.pin}
      </div>
    </AbsoluteFill>
  );
}

function FollowCTA({ dur }) {
  const t = useT();
  const s = sp(t, 0, { stiffness: 90, damping: 18 });
  const clickAt = 1.0;
  const cursorX = lerp(t, 0.2, clickAt, 900, 640, Easing.inOut(Easing.cubic));
  const cursorY = lerp(t, 0.2, clickAt, 900, 495, Easing.inOut(Easing.cubic));
  const press = t > clickAt && t < clickAt + 0.15 ? 0.94 : 1;
  const done = t > clickAt + 0.1;
  const out = lerp(t, dur - 0.3, dur, 1, 0);
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: 'absolute', left: 140, right: 140, top: 260 }}>
        <Card s={s} style={{ padding: '30px 34px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 22, marginBottom: 26 }}>
            <div style={{ width: 84, height: 84, borderRadius: 42, background: C.dark, color: C.lime, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: TITLE, fontWeight: 800, fontSize: 52 }}>T</div>
            <div>
              <div style={{ fontFamily: TITLE, fontWeight: 800, fontSize: 52, color: C.ink, lineHeight: 1 }}>{S.follow.handle}</div>
              <div style={{ fontFamily: MONO, fontSize: 20, color: C.muted, letterSpacing: 2 }}>{S.follow.sub}</div>
            </div>
          </div>
          <div style={{ transform: `scale(${press})`, background: done ? C.lime : C.dark, color: done ? C.ink : C.light, borderRadius: 16, padding: '22px 0', textAlign: 'center', fontFamily: BODY, fontWeight: 600, fontSize: 40 }}>
            {done ? '✓ Following' : 'Follow'}
          </div>
        </Card>
      </div>
      <svg width="60" height="70" viewBox="0 0 24 28" style={{ position: 'absolute', left: cursorX, top: cursorY, opacity: lerp(t, 0.1, 0.3) * lerp(t, 1.6, 1.9, 1, 0) }}>
        <path d="M2 2 L2 22 L8 17 L12 26 L16 24 L12 15 L20 15 Z" fill="#fff" stroke="#000" strokeWidth="1.6" strokeLinejoin="round" />
      </svg>
    </AbsoluteFill>
  );
}

function EndCard() {
  const t = useT();
  return (
    <Scene dur={END_LEN + 1} bg={C.dark} origin={[540, 1100]}>
      <AbsoluteFill style={{ justifyContent: 'center', padding: 90 }}>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 220, height: 640 }}><Dumbbell3D t={t} /></div>
        <div style={{ height: 520 }} />
        <Eyebrow text={S.end.eyebrow} t={t} at={0.2} color={C.lime} />
        <div style={{ height: 14 }} />
        <Title text={S.end.name} t={t} at={0.25} color={C.light} size={240} />
        <div style={{ height: 12, width: 420 * sp(t, 0.45), background: C.lime, marginTop: 10 }} />
        <div style={{ fontFamily: MONO, fontSize: 28, color: C.muted, letterSpacing: 4, marginTop: 26, opacity: sp(t, 0.6) }}>{S.end.sub}</div>
      </AbsoluteFill>
      <Shards t={t} at={0.3} corner="tr" seed={7} />
    </Scene>
  );
}

// ---------- captions: small, highlight box behind active word ----------

function Captions({ hidden, light, scenes }) {
  const t = useT();
  const frame = useCurrentFrame();
  const onLight = light.some(([a, b]) => t >= a && t < b);
  if (hidden.some(([a, b]) => t >= a && t < b)) return null;
  const pages = [];
  let cur = [];
  for (const w of WORDS) {
    cur.push(w);
    if (cur.length >= 3 || /[.,]$/.test(w.text)) { pages.push(cur); cur = []; }
  }
  if (cur.length) pages.push(cur);
  const page = pages.find((p, i) => t >= p[0].start && t < (pages[i + 1] ? Math.min(pages[i + 1][0].start, p[p.length - 1].end + 0.5) : p[p.length - 1].end + 0.4));
  if (!page) return null;
  return (
    <AbsoluteFill style={{ alignItems: 'center', paddingTop: scenes.some(([a, b]) => t >= a && t < b) ? 1560 : Math.max(1100, Math.min(1260, faceAt(frame).cy + 420)) }}>
      <div style={{ display: 'flex', gap: 10, fontFamily: TITLE, fontWeight: 700, fontSize: 60 }}>
        {page.map((w, i) => {
          const active = t >= w.start && t < w.end + 0.1;
          const s = sp(t, w.start, { stiffness: 160, damping: 24 });
          return (
            <span key={i} style={{ position: 'relative', padding: '0 12px', color: active || onLight ? C.ink : '#fff', textShadow: active || onLight ? 'none' : '0 2px 4px rgba(0,0,0,.8), 0 4px 18px rgba(0,0,0,.6)', opacity: Math.max(0.85, Math.min(1, s * 2)) }}>
              {active && <span style={{ position: 'absolute', inset: '6px 0 2px', background: C.lime, borderRadius: 10, transform: `scaleX(${s})` }} />}
              <span style={{ position: 'relative' }}>{w.text.replace(/[.,]$/, '')}</span>
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
}

// ---------- assembly ----------

// [sourceStart, sourceEnd, component] — mapped onto the trimmed edit
const SCENES = [
  [9.9, 12.9, SceneYears],
  [12.55, 16.6, SceneHotel],
  [16.27, 19.9, SceneLessons],
  [19.55, 23.6, SceneShortcut],
].map(([a, b, C]) => [M(a), M(b), C]);

// Camera: face-centred punch-ins on alternate cuts, slow push-in through each take,
// zoom bumps on key words and a short shake on impacts. Plus a light grade.
const BUMPS = WORDS.filter((w) => S.bumpWords.includes(w.text)).map((w) => w.start);
const SHAKES = []; // filled once SCENES is known (impact times)
function cameraAt(t, frame) {
  const seg = Math.max(0, SEG_START.findIndex((s, i) => t >= s && t < (SEG_START[i + 1] ?? 1e9)));
  const segT = t - SEG_START[seg], segLen = (SEG_START[seg + 1] ?? EDIT_LEN) - SEG_START[seg];
  let z = (seg % 2 ? 1.12 : 1) * (1 + 0.035 * (segT / segLen));
  for (const b of BUMPS) if (t >= b) z *= 1 + 0.045 * Math.exp(-(t - b) * 7) * Math.min(1, (t - b) * 20);
  let sx = 0, sy = 0;
  for (const s0 of SHAKES) {
    const d = t - s0;
    if (d >= 0 && d < 0.18) { const a = 14 * (1 - d / 0.18); sx += a * Math.sin(frame * 2.7); sy += a * Math.cos(frame * 3.3); }
  }
  return { z, sx, sy };
}
function BaseVideo() {
  const t = useT(), frame = useCurrentFrame();
  const { z, sx, sy } = cameraAt(t, frame);
  const f = faceAt(frame);
  return (
    <AbsoluteFill style={{ transform: `translate(${sx}px, ${sy}px) scale(${z})`, transformOrigin: `${f.cx}px ${f.cy}px`, filter: 'contrast(1.07) saturate(1.1) brightness(1.02)' }}>
      <OffthreadVideo src={staticFile(SRC_A)} />
    </AbsoluteFill>
  );
}

// Text behind the subject: big title, then the person cutout (tools/track.py) on top
function BehindTitle({ eyebrow, word, dur, from }) {
  const t = useT(), frame = useCurrentFrame();
  const g = from + frame; // global frame -> matte index
  const { z, sx, sy } = cameraAt(g / FPS, g);
  const f = faceAt(g);
  const inn = sp(t, 0.1, { stiffness: 70, damping: 16 });
  const out = lerp(t, dur - 0.6, dur, 1, 0);
  const cam = { transform: `translate(${sx}px, ${sy}px) scale(${z})`, transformOrigin: `${f.cx}px ${f.cy}px` };
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <AbsoluteFill style={{ alignItems: 'center', paddingTop: 300 }}>
        <div style={{ fontFamily: MONO, fontSize: 30, letterSpacing: 8, color: C.lime, textTransform: 'uppercase', opacity: inn, marginBottom: 10 }}>{eyebrow}</div>
        <div style={{ fontFamily: TITLE, fontWeight: 800, fontSize: 300, lineHeight: 0.85, color: C.lime, letterSpacing: -4, transform: `translateY(${(1 - inn) * 160}px) scale(${0.9 + 0.1 * inn})`, opacity: Math.min(1, inn * 1.4), textShadow: '0 20px 60px rgba(0,0,0,.35)' }}>{word}</div>
      </AbsoluteFill>
      <AbsoluteFill style={{ ...cam, filter: 'contrast(1.07) saturate(1.1) brightness(1.02)' }}>
        <Img src={staticFile(`matte/f${String(g).padStart(4, '0')}.png`)} style={{ width: 1080, height: 1920 }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
}

// Film grain + vignette (seeded per frame, deterministic)
function Grain() {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.28) 100%)' }} />
      <svg width="1080" height="1920" style={{ position: 'absolute', inset: 0, opacity: 0.07, mixBlendMode: 'overlay' }}>
        <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={frame % 60} /><feColorMatrix type="saturate" values="0" /></filter>
        <rect width="1080" height="1920" filter="url(#g)" />
      </svg>
    </AbsoluteFill>
  );
}

const Blur = ({ children }) => <CameraMotionBlur shutterAngle={180} samples={6}>{children}</CameraMotionBlur>;

// Global SFX level: keep effects well under the voice
const SFX_GAIN = 0.25;
const Sfx = ({ at, src, vol = 0.5 }) => (
  <Sequence from={Math.max(0, sec(at))}><Audio src={staticFile(`audio/${src}.wav`)} volume={vol * SFX_GAIN} /></Sequence>
);

function SoundDesign() {
  const sc = SCENES.map(([a]) => a);
  const e = [];
  // scene iris wipes
  sc.forEach((a, i) => { e.push([a - 0.15, 'whoosh', 0.35]); });
  SCENES.forEach(([, b]) => e.push([b - 0.8, 'whoosh-out', 0.22]));
  // titles over talking head
  e.push([0.05, 'shimmer', 0.18], [0.15, 'pop', 0.25], [M(3.53) + 0.1, 'pop', 0.25]);
  // name tag + pin
  e.push([M(6.28), 'whoosh', 0.25], [M(6.28) + 1.9, 'pop-high', 0.3]);
  // years: ticks while counting, ding at the end
  for (let k = 0; k < 9; k++) e.push([sc[0] + 0.5 + k * (1.5 / 9), 'tick', 0.18]);
  e.push([sc[0] + 2.05, 'ding', 0.2]);
  // hotel cards
  e.push([sc[1] + 0.5, 'pop', 0.3], [sc[1] + 1.0, 'pop', 0.3], [sc[1] + 1.2, 'pop-high', 0.2]);
  // lesson cards + save clicks
  [0, 1, 2].forEach((i) => e.push([sc[2] + 0.5 + i * 0.4, 'pop', 0.25], [sc[2] + 1.2 + i * 0.5, 'click', 0.35]));
  // shortcut: mistakes thud, straight line, check
  [0, 1, 2, 3].forEach((i) => e.push([sc[3] + 0.6 + i * 0.32, 'thud', 0.4]));
  e.push([sc[3] + 1.9, 'whoosh', 0.25], [sc[3] + 2.4, 'ding', 0.3]);
  // get there faster, follow click, end card
  e.push([M(23.49) + 0.05, 'pop', 0.25]);
  e.push([B_START + 1.6 + 1.0, 'click', 0.5], [B_START + 1.6 + 1.05, 'ding', 0.22]);
  e.push([EDIT_LEN - 0.2, 'whoosh', 0.35], [EDIT_LEN + 0.5, 'shimmer', 0.2]);
  LEAKS.forEach(([at]) => e.push([at - 0.6, 'whoosh', 0.3]));
  BUMPS.forEach((b) => e.push([b, 'pop', 0.12]));
  return <>{e.map(([at, src, vol], i) => <Sfx key={i} at={at} src={src} vol={vol} />)}</>;
}

// Light leaks over the big section changes (into graphics, into the CTA, into the end card)
const LEAKS = [[SCENES[0][0] + 0.2, 3], [B_START, 11], [EDIT_LEN, 21]];
SCENES.length && [0, 1, 2, 3].forEach((i) => SHAKES.push(SCENES[3][0] + 0.6 + i * 0.32));
SHAKES.push(SCENES[3][0] + 2.4);

export function FullExplainer() {
  const end = sec(EDIT_LEN);
  return (
    <AbsoluteFill style={{ background: C.dark }}>
      <Sequence durationInFrames={end}><BaseVideo /></Sequence>

      <Sequence from={0} durationInFrames={sec(M(3.22))}><BehindTitle eyebrow={S.hook.eyebrow} word={S.hook.behind} dur={M(3.22)} from={0} /></Sequence>
      <Sequence from={sec(M(3.53))} durationInFrames={sec(M(5.56) - M(3.53))}><Blur><TopTitle eyebrow={S.about.eyebrow} title={S.about.title} dur={M(5.56) - M(3.53)} /></Blur></Sequence>
      <Sequence from={sec(M(6.28))} durationInFrames={sec(M(9.9) - M(6.28) + 0.3)}><Blur><NameTag dur={M(9.9) - M(6.28) + 0.3} /></Blur></Sequence>
      {SCENES.map(([a, b, Comp], i) => (
        <Sequence key={i} from={sec(a)} durationInFrames={sec(b - a)}><Blur><Comp dur={b - a} start={a} /></Blur></Sequence>
      ))}
      <Sequence from={sec(M(23.49))} durationInFrames={sec(B_START - M(23.49))}><BehindTitle eyebrow={S.faster.eyebrow} word={S.faster.behind} dur={B_START - M(23.49)} from={sec(M(23.49))} /></Sequence>
      <Sequence from={sec(B_START + 1.6)} durationInFrames={sec(EDIT_LEN - B_START - 1.6)}><Blur><FollowCTA dur={EDIT_LEN - B_START - 1.6} /></Blur></Sequence>
      {LEAKS.map(([at, seed], i) => (
        <Sequence key={`l${i}`} from={sec(at) - 25} durationInFrames={50}><LightLeak durationInFrames={50} seed={seed} hueShift={45} /></Sequence>
      ))}

      <Captions hidden={[[EDIT_LEN, 99]]} light={[[SCENES[0][0] + 0.4, SCENES[0][1] - 0.4], [SCENES[2][0] + 0.4, SCENES[2][1] - 0.4]]} scenes={SCENES.map(([a, b]) => [a + 0.4, b - 0.4])} />
      <Sequence from={end}><EndCard /></Sequence>
      <Grain />

      <Audio src={staticFile('audio/music.wav')} volume={(f) => interpolate(f, [0, 15, end - 10, end + 10], [0, 0.06, 0.06, 0.25], { extrapolateRight: 'clamp' })} />
      <SoundDesign />
    </AbsoluteFill>
  );
}
