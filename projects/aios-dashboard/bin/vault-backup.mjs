// Vault backup loop — commits and pushes whatever changed, hourly.
// Obsidian has no Git or Sync plugin, so without this the vault is only ever
// backed up when a Claude session remembers to commit. Node, not zsh: under
// launchd zsh has no TCC access to ~/Documents (see run-action.mjs).
import { execFileSync } from 'node:child_process';
import { appendFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';

const DASH = dirname(dirname(fileURLToPath(import.meta.url)));
const VAULT = dirname(dirname(DASH));
const LOGS = join(DASH, 'logs');
mkdirSync(LOGS, { recursive: true });
const LOG = join(LOGS, 'vault-backup.log');

const NVM_BIN = join(homedir(), '.nvm/versions/node/v24.16.0/bin');
const env = { ...process.env, PATH: `${NVM_BIN}:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin` };
const git = (...args) => execFileSync('git', args, { cwd: VAULT, env, encoding: 'utf8' }).trim();
const log = (line) => appendFileSync(LOG, `[${new Date().toLocaleString('sv').replace('T', ' ')}] ${line}\n`);

try {
  if (!git('status', '--porcelain')) {
    // Nothing staged locally, but a Claude session may have committed without
    // pushing — still try, then fall through quietly if the remote is current.
    const ahead = git('rev-list', '--count', 'origin/main..HEAD');
    if (ahead === '0') process.exit(0);
    git('push', 'origin', 'main');
    log(`pushed ${ahead} pending commit(s)`);
    process.exit(0);
  }

  git('add', '-A');
  const files = git('diff', '--cached', '--numstat').split('\n').filter(Boolean).length;
  git('commit', '-m', `vault backup: ${files} file(s) changed\n\nAutomated hourly snapshot from the AIOS backup loop.`);
  git('push', 'origin', 'main');
  log(`committed + pushed ${files} file(s)`);
} catch (e) {
  // Most likely cause is a diverged remote (another machine, or a session
  // mid-push). Leave it for the next hour rather than rebasing under a loop.
  log(`FAILED: ${String(e.stderr || e.message).trim().split('\n').slice(-3).join(' | ')}`);
  process.exit(1);
}
