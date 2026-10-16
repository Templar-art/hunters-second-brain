// Trusted local command configuration only. Not a sandbox or autonomous AI critic.
import fs from 'node:fs';import {spawnSync} from 'node:child_process';import {validateReview} from './validate-review.mjs';
const cfgPath=process.argv[2];if(!cfgPath)throw Error('Supply trusted config path');const c=JSON.parse(fs.readFileSync(cfgPath));
if(!Number.isInteger(c.maxPasses)||c.maxPasses<0||c.maxPasses>2||!Number.isInteger(c.timeoutMs)||c.timeoutMs<100||c.timeoutMs>1800000)throw Error('Invalid pass/time limit');
if(!c.reviewFile||!c.outputFile||!c.expectedRenderVersion)throw Error('Paths/version required');if(fs.existsSync(c.outputFile))throw Error('Refusing output overwrite');
function run(cmd){if(!Array.isArray(cmd)||!cmd.length||cmd.some(x=>typeof x!=='string'||!x))throw Error('Explicit reviewed command array required');const r=spawnSync(cmd[0],cmd.slice(1),{cwd:c.cwd??process.cwd(),timeout:c.timeoutMs,encoding:'utf8',shell:false,maxBuffer:4*1024*1024});if(r.error||r.status!==0)throw Error(`Command failed: ${cmd[0]}`);}
const trace=[];let status='REQUIRES_HUMAN_REVIEW';
for(let pass=0;pass<=c.maxPasses;pass++){
 if(c.evaluateCommand)run(c.evaluateCommand);
 const review=JSON.parse(fs.readFileSync(c.reviewFile));const errors=validateReview(review);if(review.renderVersion!==c.expectedRenderVersion)errors.push('version mismatch');if(errors.length)throw Error(errors.join('; '));
 const issues=review.issues.filter(i=>i.severity!=='preference');trace.push({pass,issueCount:issues.length});if(!issues.length)break;
 if(pass===c.maxPasses){status='ESCALATE_UNRESOLVED';break;}
 if(!c.fixCommand||!c.renderCommand||!c.evaluateCommand){status='BLOCKED_MISSING_INTEGRATION';break;}
 run(c.fixCommand);run(c.renderCommand);
}
fs.writeFileSync(c.outputFile,JSON.stringify({status,trace,humanApprovalRequired:true,autoDelivery:false},null,2),{flag:'wx'});
