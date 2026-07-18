// AIOS vault scanner — builds the live data payload for the dashboard.
// Zero dependencies; reads the vault directly on every /api/data call.
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const VAULT = fileURLToPath(new URL('../../..', import.meta.url)).replace(/\/$/, '');

function read(p) {
  try { return readFileSync(p, 'utf8'); } catch { return null; }
}

function frontmatter(text) {
  const m = text && text.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return {};
  const fm = {};
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^(\w[\w-]*):\s*(.*)$/);
    if (kv) fm[kv[1]] = kv[2].trim();
  }
  return fm;
}

function walk(dir, out = []) {
  let entries = [];
  try { entries = readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (e.name.startsWith('.')) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

function scanJobs() {
  const jobs = [];
  for (const p of walk(join(VAULT, 'projects'))) {
    if (!p.endsWith('JOB.md') || p.includes('JOB-template')) continue;
    const text = read(p);
    if (!text) continue;
    const fm = frontmatter(text);
    const cost = (fm.cost || '').match(/credits:\s*([\d.]+).*?aud:\s*([\d.]+)/);
    jobs.push({
      client: fm.client || p.split('/').slice(-2)[0],
      address: fm.address || '',
      status: (fm.status || 'unknown').split('#')[0].trim(),
      credits: cost ? Number(cost[1]) : 0,
      aud: cost ? Number(cost[2]) : 0,
      path: p.replace(VAULT + '/', ''),
    });
  }
  return jobs;
}

function scanWiki() {
  const now = Date.now();
  const week = 7 * 86400e3;
  let updatedThisWeek = 0;
  let followups = 0;
  const followupLines = [];
  for (const p of walk(join(VAULT, 'wiki'))) {
    if (!p.endsWith('.md')) continue;
    const text = read(p);
    if (!text) continue;
    const fm = frontmatter(text);
    if (fm.updated && now - Date.parse(fm.updated) < week) updatedThisWeek++;
    // Follow-ups are explicit only: tag a line with #followup (or ⏳) in any wiki page.
    for (const line of text.split('\n')) {
      if (/#followup\b|⏳/.test(line)) {
        followups++;
        followupLines.push({ page: p.split('/').pop().replace('.md', ''), path: p.replace(VAULT + '/', ''), line: line.replace(/^[-*\s]+/, '').replace(/#followup\b/, '').trim().slice(0, 140) });
      }
    }
  }
  return { updatedThisWeek, followups, followupLines: followupLines.slice(0, 12) };
}

function recentLog() {
  const text = read(join(VAULT, 'wiki', 'log.md')) || '';
  return text.split('\n').filter(l => l.startsWith('## ')).slice(-8).reverse();
}

function latestWeeklyReview() {
  let files = [];
  try {
    files = readdirSync(join(VAULT, 'wiki', 'sources'))
      .filter(f => /^weekly-review-\d{4}-\d{2}-\d{2}\.md$/.test(f)).sort();
  } catch { /* no sources dir */ }
  if (!files.length) return null;
  const name = files[files.length - 1];
  const text = read(join(VAULT, 'wiki', 'sources', name)) || '';
  const bullets = text.split('\n')
    .filter(l => /^\s*[-*] /.test(l))
    .map(l => l.replace(/^\s*[-*] /, '').slice(0, 200))
    .slice(0, 6);
  return { path: `wiki/sources/${name}`, date: name.match(/(\d{4}-\d{2}-\d{2})/)[1], bullets };
}

function dailyNote(dateStr) {
  const p = join(VAULT, `${dateStr}.md`);
  if (!existsSync(p)) return { exists: false, path: `${dateStr}.md` };
  return { exists: true, path: `${dateStr}.md`, content: read(p).slice(0, 4000), mtime: statSync(p).mtime };
}

export function scan() {
  const today = new Date();
  const dateStr = today.toLocaleDateString('en-CA'); // YYYY-MM-DD local
  const jobs = scanJobs();
  const wiki = scanWiki();
  const active = jobs.filter(j => !/delivered|closed|done/i.test(j.status));
  return {
    generatedAt: today.toISOString(),
    vaultName: VAULT.split('/').pop(),
    stats: {
      activeJobs: active.length,
      totalJobs: jobs.length,
      creditsSpent: jobs.reduce((s, j) => s + j.credits, 0),
      audSpent: jobs.reduce((s, j) => s + j.aud, 0),
      pagesUpdatedWeek: wiki.updatedThisWeek,
      followups: wiki.followups,
    },
    jobs,
    followupLines: wiki.followupLines,
    log: recentLog(),
    daily: dailyNote(dateStr),
    weekly: latestWeeklyReview(),
  };
}
