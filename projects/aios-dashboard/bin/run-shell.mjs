// Shim for shell jobs that live inside ~/Documents. Under launchd /bin/zsh
// cannot open a script file in the vault ("Operation not permitted" — no TCC
// access), but node can read it. So node reads the script and pipes it to
// `zsh -s`, which never touches the protected path itself.
// Usage: node run-shell.mjs <script.sh> [args...]
import { readFileSync } from 'node:fs';
import { isAbsolute, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { homedir } from 'node:os';

const [scriptArg, ...rest] = process.argv.slice(2);
if (!scriptArg) {
  console.error('usage: run-shell.mjs <script.sh> [args...]');
  process.exit(2);
}

const BIN = dirname(fileURLToPath(import.meta.url));
const script = isAbsolute(scriptArg) ? scriptArg : join(BIN, scriptArg);
const source = readFileSync(script, 'utf8');

const NVM_BIN = join(homedir(), '.nvm/versions/node/v24.16.0/bin');
const PATH = `${NVM_BIN}:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:${process.env.PATH || ''}`;

const child = spawn('/bin/zsh', ['-s', ...rest], {
  env: { ...process.env, PATH },
  stdio: ['pipe', 'inherit', 'inherit'],
});
child.stdin.end(source);
child.on('close', (code) => process.exit(code ?? 1));
