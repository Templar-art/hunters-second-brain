// AIOS dashboard server — serves the UI, live vault data, and runs actions
// (headless `claude -p` sessions) on button press. Zero dependencies.
import { createServer } from 'node:http';
import { readFileSync, existsSync, mkdirSync, appendFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn, execSync } from 'node:child_process';
import { homedir } from 'node:os';
import { scan, VAULT } from './lib/scan.mjs';

const ROOT = dirname(fileURLToPath(import.meta.url));
const PORT = 8770;
const LOGS = join(ROOT, 'logs');
mkdirSync(LOGS, { recursive: true });

// Under launchd the process has a bare PATH, so `spawn('claude')` fails with
// ENOENT. Resolve the CLI to an absolute path once, and build a PATH that
// includes wherever it lives so claude's own child processes (git) resolve too.
function resolveClaude() {
  const candidates = [];
  const nvm = join(homedir(), '.nvm/versions/node');
  try { for (const v of readdirSync(nvm)) candidates.push(join(nvm, v, 'bin/claude')); } catch {}
  candidates.push('/usr/local/bin/claude', '/opt/homebrew/bin/claude', join(homedir(), '.local/bin/claude'));
  for (const c of candidates) if (existsSync(c)) return c;
  try { return execSync('command -v claude', { shell: '/bin/zsh', encoding: 'utf8' }).trim(); } catch {}
  return 'claude'; // last resort — will ENOENT, but error surfaces to the console
}
const CLAUDE_BIN = resolveClaude();
const RUN_ENV = { ...process.env, PATH: `${dirname(CLAUDE_BIN)}:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:${process.env.PATH || ''}` };
console.log(`AIOS: claude → ${CLAUDE_BIN}`);

const actions = JSON.parse(readFileSync(join(ROOT, 'actions', 'actions.json'), 'utf8'));

// Headless runs may edit vault files and use git, but get no MCP tools —
// the money gate (no credit spend from loops) is enforced here, not just in prompts.
const CLAUDE_ARGS = (prompt) => [
  '-p', prompt,
  '--output-format', 'text',
  '--permission-mode', 'acceptEdits',
  '--allowedTools', 'Read,Write,Edit,Glob,Grep,Bash(git add:*),Bash(git commit:*),Bash(git push:*),Bash(git status:*),Bash(git log:*),Bash(ls:*)',
  '--disallowedTools', 'mcp__magnific__*,mcp__higgsfield__*',
];

let current = null; // { id, child, startedAt }

function json(res, code, obj) {
  res.writeHead(code, { 'content-type': 'application/json' });
  res.end(JSON.stringify(obj));
}

const server = createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');

  if (req.method === 'GET' && url.pathname === '/') {
    res.writeHead(200, { 'content-type': 'text/html' });
    return res.end(readFileSync(join(ROOT, 'index.html')));
  }

  if (req.method === 'GET' && url.pathname === '/api/data') {
    try { return json(res, 200, { ...scan(), actions, running: current ? current.id : null }); }
    catch (e) { return json(res, 500, { error: String(e) }); }
  }

  if (req.method === 'POST' && url.pathname === '/api/kill') {
    if (current) {
      const c = current;
      c.child.kill('SIGTERM');
      // Escalate to SIGKILL and free the lock even if the child ignores SIGTERM.
      setTimeout(() => { try { c.child.kill('SIGKILL'); } catch {} if (current === c) current = null; }, 3000);
    }
    return json(res, 200, { ok: true });
  }

  if (req.method === 'POST' && url.pathname === '/api/run') {
    let body = '';
    req.on('data', (c) => (body += c));
    req.on('end', () => {
      const { id } = JSON.parse(body || '{}');
      const action = actions.find((a) => a.id === id);
      if (!action) return json(res, 404, { error: 'unknown action' });
      if (action.disabled) return json(res, 400, { error: action.disabledReason || 'action disabled' });
      if (current) return json(res, 409, { error: `"${current.id}" already running` });

      const promptPath = join(ROOT, 'actions', action.prompt);
      if (!existsSync(promptPath)) return json(res, 500, { error: `missing prompt file ${action.prompt}` });
      const prompt = readFileSync(promptPath, 'utf8');

      res.writeHead(200, { 'content-type': 'text/plain; charset=utf-8', 'x-accel-buffering': 'no' });
      res.write(`> aios run: ${action.label}\n`);

      const child = spawn(CLAUDE_BIN, CLAUDE_ARGS(prompt), { cwd: VAULT, env: RUN_ENV, stdio: ['ignore', 'pipe', 'pipe'] });
      current = { id, child, startedAt: Date.now() };
      const logFile = join(LOGS, `${new Date().toISOString().slice(0, 10)}-${id}.log`);

      const pipe = (chunk) => {
        res.write(chunk);
        appendFileSync(logFile, chunk);
      };
      child.stdout.on('data', pipe);
      child.stderr.on('data', pipe);
      child.on('close', (code) => {
        const secs = Math.round((Date.now() - current.startedAt) / 1000);
        res.end(`\n> done (exit ${code}, ${secs}s)\n`);
        current = null;
      });
      child.on('error', (e) => {
        res.end(`\n> spawn error: ${e.message}\n`);
        current = null;
      });
      req.on('close', () => {}); // keep running even if client disconnects
    });
    return;
  }

  res.writeHead(404).end('not found');
});

server.listen(PORT, () => console.log(`AIOS dashboard → http://localhost:${PORT} (vault: ${VAULT})`));
