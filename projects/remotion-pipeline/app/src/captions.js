// Phrase timings from the Whisper small.en pass (cleaned SRT). Word timings are
// estimated by spreading each phrase's duration across its words by character
// length — replace with real word timestamps once analyse_media.py can run.
const PHRASES_9573 = [
  [0.0, 1.7, "Hey guys, if you're seeing this,"],
  [1.7, 3.378, 'you do not follow me yet.'],
  [3.378, 5.715, 'So let me tell you a little bit about myself.'],
  [6.195, 8.2, 'My name is Tyson.'],
  [8.2, 10.279, "I'm a fitness and nutrition coach on the Gold Coast."],
  [10.279, 12.714, "I've been training for about 9 years now."],
  [12.714, 15.472, 'I also work full time at a hotel.'],
  [16.151, 19.6, "On my page, I'll be sharing things that took me 9 years to learn,"],
  [19.6, 23.341, 'so you can skip all the mistakes I made along the way'],
  [23.341, 25.194, "and you'll get there faster."],
];

const PHRASES_9577 = [
  [0.196, 2.0, 'So now you know who I am,'],
  [2.0, 3.847, "hit follow and I'll see you in the next one."],
];

// Words that get the accent colour
const EMPHASIS = new Set(['follow', 'tyson', 'fitness', 'nutrition', 'gold', 'coast', '9', 'years', 'skip', 'mistakes', 'faster', 'hotel']);

function toWords(phrases) {
  const words = [];
  for (const [start, end, text] of phrases) {
    const parts = text.split(' ');
    const total = parts.reduce((n, w) => n + w.length + 1, 0);
    let t = start;
    for (const w of parts) {
      const d = ((w.length + 1) / total) * (end - start);
      const key = w.toLowerCase().replace(/[^a-z0-9]/g, '');
      words.push({ text: w, start: t, end: t + d, accent: EMPHASIS.has(key) });
      t += d;
    }
  }
  return words;
}

// Group into short caption pages (max 4 words, break on punctuation)
function toPages(words) {
  const pages = [];
  let cur = [];
  for (const w of words) {
    cur.push(w);
    if (cur.length >= 4 || /[.,]$/.test(w.text)) { pages.push(cur); cur = []; }
  }
  if (cur.length) pages.push(cur);
  return pages.map((ws, i) => ({
    words: ws,
    start: ws[0].start,
    end: i + 1 < pages.length ? Math.min(pages[i + 1][0].start, ws[ws.length - 1].end + 0.6) : ws[ws.length - 1].end + 0.4,
  }));
}

export const PAGES_9573 = toPages(toWords(PHRASES_9573));
export const PAGES_9577 = toPages(toWords(PHRASES_9577));

// One continuous word list for the combined edit (9577 starts at 25.19s)
export const WORDS_ALL = [...toWords(PHRASES_9573), ...toWords(PHRASES_9577).map((w) => ({ ...w, start: w.start + 25.19, end: w.end + 25.19 }))];
