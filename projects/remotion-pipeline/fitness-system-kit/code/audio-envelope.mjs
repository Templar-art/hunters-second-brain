export function musicGainAt(t,speech,{baseDb=-22,duckDb=-9,attack=.12,release=.35,fadeIn=.25,fadeOut=.35,duration}={}){
 if(![t,baseDb,duckDb,attack,release,fadeIn,fadeOut,duration].every(Number.isFinite)||duration<=0||duckDb>0||[attack,release,fadeIn,fadeOut].some(x=>x<0))throw Error('Invalid config');
 if(!Array.isArray(speech)||speech.some(s=>!Number.isFinite(s.start)||!Number.isFinite(s.end)||s.start<0||s.end<=s.start))throw Error('Invalid speech');
 if(t<0||t>=duration)return 0;
 const clamp=x=>Math.max(0,Math.min(1,x));let depth=0;
 for(const s of speech){let d=0;if(t>=s.start&&t<=s.end)d=1;else if(t<s.start&&attack>0)d=clamp((t-s.start+attack)/attack);else if(t>s.end&&release>0)d=clamp(1-(t-s.end)/release);depth=Math.max(depth,d);}
 return 10**((baseDb+duckDb*depth)/20)*Math.min(fadeIn===0?1:clamp(t/fadeIn),fadeOut===0?1:clamp((duration-t)/fadeOut));
}
