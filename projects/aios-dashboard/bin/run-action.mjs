// AIOS loop runner — executes one action headless. Used by launchd; same
// engine the dashboard buttons use. Usage: node run-action.mjs <action-id>
//
// This is node, not zsh, on purpose. Under launchd /bin/zsh has no TCC access
// to ~/Documents, so the old run-action.sh died on "Operation not permitted"
// the moment it read a prompt file. The node binary is already permitted
// (server.mjs has been reading the vault under launchd for months), so the
// runner has to be node for the scheduled jobs to work at all.
import { readFileSync, mkdirSync, appendFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { homedir } from 'node:os';

const ACTION = process.argv[2];
if (!ACTION) {
  console.error('usage: run-action.mjs <action-id>');
  process.exit(2);
}

const DASH = dirname(dirname(fileURLToPath(import.meta.url)));
const VAULT = dirname(dirname(DASH));
const PROMPT_FILE = join(DASH, 'actions', `${ACTION}.md`);
const LOGS = join(DASH, 'logs');
mkdirSync(LOGS, { recursive: true });
const LOG = join(LOGS, `${new Date().toISOString().slice(0, 10)}-${ACTION}.log`);

const log = (line) => appendFileSync(LOG, `${line}\n`);
const stamp = () => new Date().toLocaleString('sv').replace('T', ' ');

if (!existsSync(PROMPT_FILE)) {
  log(`missing prompt ${PROMPT_FILE}`);
  process.exit(1);
}

// launchd hands us a bare PATH — add the nvm bin where claude and git live.
const NVM_BIN = join(homedir(), '.nvm/versions/node/v24.16.0/bin');
const PATH = `${NVM_BIN}:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:${process.env.PATH || ''}`;

const prompt = readFileSync(PROMPT_FILE, 'utf8');

log(`=== aios loop: ${ACTION} @ ${stamp()} ===`);

// Headless runs may edit vault files and use git, but get no MCP tools —
// the money gate (no credit spend from loops) is enforced here, not just in prompts.
const child = spawn(
  join(NVM_BIN, 'claude'),
  [
    '-p', prompt,
    '--output-format', 'text',
    '--permission-mode', 'acceptEdits',
    '--allowedTools', 'Read,Write,Edit,Glob,Grep,Bash(git add:*),Bash(git commit:*),Bash(git push:*),Bash(git status:*),Bash(git log:*),Bash(ls:*)',
    '--disallowedTools', 'mcp__magnific__*,mcp__higgsfield__*',
  ],
  { cwd: VAULT, env: { ...process.env, PATH }, stdio: ['ignore', 'pipe', 'pipe'] },
);

child.stdout.on('data', (d) => log(String(d).trimEnd()));
child.stderr.on('data', (d) => log(String(d).trimEnd()));

child.on('close', (code) => {
  log(`=== exit ${code} @ ${stamp()} ===`);
  if (code !== 0) {
    spawn('osascript', [
      '-e',
      `display notification "${ACTION} failed (exit ${code}) — see logs" with title "AIOS loop" sound name "Basso"`,
    ]);
  }
  process.exit(code ?? 1);
});
