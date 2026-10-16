import argparse,json,math
from pathlib import Path

def number(x):return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def map_analysis(analyses,clips):
    by={a['sourceId']:a for a in analyses}
    if len(by)!=len(analyses):raise ValueError('Duplicate source IDs')
    words=[];speech=[];issues=[];ids=set()
    for c in clips:
        if not c.get('id') or c['id'] in ids:raise ValueError('Unique clip id required')
        ids.add(c['id']);a=by.get(c.get('sourceId'))
        if a is None:raise ValueError('Missing source analysis')
        si,so,ts,rate=c.get('sourceIn'),c.get('sourceOut'),c.get('timelineStart'),c.get('rate',1)
        if not all(number(x) for x in [si,so,ts,rate]) or si<0 or so<=si or ts<0 or rate<=0:raise ValueError('Invalid clip timing')
        offset=a.get('audioOffsetSeconds')
        if not number(offset):raise ValueError('Explicit audio offset required')
        def mapped(t):return ts+(t-si)/rate
        for w in a.get('words',[]):
            if not number(w.get('start')) or not number(w.get('end')) or w['end']<=w['start']:
                issues.append({'clipId':c['id'],'type':'invalid_word_timing','text':w.get('text')});continue
            ws,we=w['start']+offset,w['end']+offset
            if we<=si or ws>=so:continue
            if ws<si or we>so:
                issues.append({'clipId':c['id'],'type':'partial_word_at_trim','text':w['text']});continue
            words.append({**w,'start':mapped(ws),'end':mapped(we),'clipId':c['id'],'sourceId':c['sourceId'],'sourceStart':ws,'sourceEnd':we})
        for s in a.get('speechRegions',[]):
            if not number(s.get('start')) or not number(s.get('end')) or s['end']<=s['start']:raise ValueError('Invalid speech interval')
            start,end=max(si,s['start']+offset),min(so,s['end']+offset)
            if end>start:speech.append({'start':mapped(start),'end':mapped(end),'clipId':c['id']})
    return {'timeBasis':'edited_timeline_seconds','words':sorted(words,key=lambda w:w['start']),'speechRegions':sorted(speech,key=lambda s:s['start']),'issues':issues,'note':'Constant positive playback rates only; speed ramps require a time-warp mapping.'}

def caption_phrases(words,max_words=6,max_chars=42,max_gap=.45):
    if max_words<1 or max_chars<1 or max_gap<0:raise ValueError('Invalid phrase settings')
    result=[];group=[]
    def flush():
        if group:result.append({'startSeconds':group[0]['start'],'endSeconds':group[-1]['end'],'text':' '.join(w['text'].strip() for w in group),'words':group.copy()})
    for w in words:
        if not number(w.get('start')) or not number(w.get('end')) or w['end']<=w['start']:raise ValueError('Invalid caption word')
        text=' '.join(x['text'].strip() for x in [*group,w])
        if group and (w.get('clipId')!=group[-1].get('clipId') or w['start']-group[-1]['end']>max_gap or len(group)>=max_words or len(text)>max_chars):flush();group=[]
        group.append(w)
        if w['text'].strip().endswith(('.', '?', '!')):flush();group=[]
    flush();return result

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');a=p.parse_args();d=json.loads(Path(a.input).read_text());result=map_analysis(d['analyses'],d['clips']);result['captions']=caption_phrases(result['words'])
    with open(a.output,'x') as f:json.dump(result,f,indent=2,allow_nan=False)
if __name__=='__main__':main()
