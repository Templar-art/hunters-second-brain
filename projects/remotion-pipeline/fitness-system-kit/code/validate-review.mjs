export function validateReview(r){
 if(!r||typeof r!=='object')return ['review object required'];const errors=[];
 if(typeof r.renderVersion!=='string'||!r.renderVersion.trim())errors.push('renderVersion required');
 const c=r.capabilities??{};
 for(const k of ['stills','temporalVideo','audioListening','audioAnalysis','transcript'])if(typeof c[k]!=='boolean')errors.push(`capability ${k} required`);
 for(const [k,v] of Object.entries(r.scores??{})){
  if(v!==null&&(!Number.isFinite(v)||v<1||v>5))errors.push(`invalid ${k} score`);
  if(v!==null&&['motion','editing'].includes(k)&&!c.temporalVideo)errors.push(`${k} requires temporal video`);
  if(v!==null&&k==='audio'&&!c.audioListening)errors.push('audio requires listening');
  if(v!==null&&['hierarchy','typography','graphicRelevance'].includes(k)&&!c.stills&&!c.temporalVideo)errors.push(`${k} requires visuals`);
 }
 if(!Array.isArray(r.issues))errors.push('issues array required');
 for(const i of r.issues??[]){if(!i||!['blocker','important','preference'].includes(i.severity)||!Number.isFinite(i.start)||!Number.isFinite(i.end)||i.start<0||i.end<i.start||typeof i.observation!=='string'||!i.observation.trim()||typeof i.fix!=='string'||!i.fix.trim()||typeof i.evidence!=='string'||!i.evidence.trim()||!Array.isArray(i.preserve))errors.push('invalid issue');}
 if(!['pending','approved','rejected'].includes(r.humanApproval))errors.push('humanApproval required');return errors;
}
