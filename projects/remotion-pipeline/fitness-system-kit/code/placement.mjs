const finite=x=>Number.isFinite(x);
export function rectOK(r){return !!r&&['x','y','w','h'].every(k=>finite(r[k]))&&r.w>0&&r.h>0;}
export function intersects(a,b){if(!rectOK(a)||!rectOK(b))throw Error('Invalid rectangle');return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;}
export function mapRect(r,crop,out){if(!rectOK(r)||!rectOK(crop)||!finite(out?.w)||!finite(out?.h)||out.w<=0||out.h<=0)throw Error('Invalid transform');return {x:(r.x-crop.x)*out.w/crop.w,y:(r.y-crop.y)*out.h/crop.h,w:r.w*out.w/crop.w,h:r.h*out.h/crop.h};}
export function sweptBounds(rects){if(!rects.length||rects.some(r=>!rectOK(r)))throw Error('Invalid motion bounds');const x=Math.min(...rects.map(r=>r.x)),y=Math.min(...rects.map(r=>r.y));return {x,y,w:Math.max(...rects.map(r=>r.x+r.w))-x,h:Math.max(...rects.map(r=>r.y+r.h))-y};}
export function selectPlacement({candidates,samples,allowedZone,exclusions=[],padding=24,coverage='unknown'}){
 if(!Array.isArray(candidates)||!Array.isArray(samples)||!rectOK(allowedZone)||!finite(padding)||padding<0||exclusions.some(r=>!rectOK(r)))throw Error('Invalid placement input');
 if(!samples.length||samples.some(s=>s.status!=='reviewed'||!Array.isArray(s.protected)||s.protected.some(r=>!rectOK(r))))return {status:'REQUIRES_REVIEW',selected:null};
 const protectedRects=[...exclusions,...samples.flatMap(s=>s.protected.map(r=>({x:r.x-padding,y:r.y-padding,w:r.w+2*padding,h:r.h+2*padding})))];
 for(const c of candidates){if(!Array.isArray(c.motionBounds)||!c.motionBounds.length||c.motionBounds.some(r=>!rectOK(r)))continue;const r=sweptBounds(c.motionBounds);if(r.x>=allowedZone.x&&r.y>=allowedZone.y&&r.x+r.w<=allowedZone.x+allowedZone.w&&r.y+r.h<=allowedZone.y+allowedZone.h&&!protectedRects.some(p=>intersects(p,r)))return {status:coverage==='all_render_frames_reviewed'?'GEOMETRY_CLEAR':'PROVISIONAL_SAMPLED_CLEAR',selected:c.id};}
 return {status:'NO_FEASIBLE_PLACEMENT',selected:null};
}
