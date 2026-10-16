import argparse,hashlib,json,math,subprocess
from pathlib import Path

def probe_and_extract(source,outdir,source_id,audio_index=None,offset_override=None):
    source=Path(source)
    if not source.is_file():raise FileNotFoundError(source)
    outdir=Path(outdir)
    if outdir.exists():raise FileExistsError('Use a new versioned analysis directory')
    r=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(source)],capture_output=True,text=True,timeout=60)
    if r.returncode:raise RuntimeError(r.stderr)
    metadata=json.loads(r.stdout);streams=metadata.get('streams',[]);audios=[s for s in streams if s.get('codec_type')=='audio'];videos=[s for s in streams if s.get('codec_type')=='video']
    if not audios:raise ValueError('No audio stream')
    audio=audios[0] if audio_index is None else next((s for s in audios if s['index']==audio_index),None)
    if audio is None:raise ValueError('Requested global audio stream index absent')
    video=videos[0] if videos else None
    if offset_override is not None:
        offset=float(offset_override);origin='explicit_user_override'
    else:
        # Refuse to invent offset when stream starts are unavailable.
        start=audio.get('start_time');base=video.get('start_time') if video else start
        if start is None or base is None:raise ValueError('Stream start unavailable: supply --audio-offset after checking sync')
        offset=float(start)-float(base);origin='stream_start_difference_requires_sync_verification'
    if not math.isfinite(offset):raise ValueError('Invalid offset')
    outdir.mkdir(parents=True)
    wav=outdir/'analysis.wav'
    r=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-n','-i',str(source),'-map',f'0:{audio["index"]}','-vn','-ar','16000','-ac','1','-c:a','pcm_s16le',str(wav)],capture_output=True,text=True,timeout=600)
    if r.returncode:raise RuntimeError(r.stderr[-4000:])
    sha=hashlib.sha256()
    with source.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):sha.update(chunk)
    manifest={'sourceId':source_id,'sourcePath':str(source.resolve()),'sourceSha256':sha.hexdigest(),'selectedAudioGlobalStreamIndex':audio['index'],'audioOffsetSeconds':offset,'offsetProvenance':origin,'syncVerified':False,'analysisAudio':str(wav.resolve()),'probe':metadata,'note':'Validate a real sync point. Discontinuous timestamps/VFR/conforms may require a richer mapping.'}
    with (outdir/'asset.json').open('x') as f:json.dump(manifest,f,indent=2)
    return manifest

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output_directory');p.add_argument('--source-id',required=True);p.add_argument('--audio-stream-index',type=int);p.add_argument('--audio-offset',type=float);a=p.parse_args();probe_and_extract(a.input,a.output_directory,a.source_id,a.audio_stream_index,a.audio_offset)
if __name__=='__main__':main()
