"""Convenience wrapper: ingest then approved local transcription. Not an editor."""
import argparse,subprocess,sys
from pathlib import Path
from ingest import probe_and_extract

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output_directory');p.add_argument('--source-id',required=True);p.add_argument('--model',required=True);p.add_argument('--allow-model-download',action='store_true');p.add_argument('--audio-stream-index',type=int);p.add_argument('--audio-offset',type=float);p.add_argument('--language');p.add_argument('--device',choices=['cpu','cuda'],default='cpu');p.add_argument('--compute-type');p.add_argument('--timeout-seconds',type=int,default=3600);a=p.parse_args()
    if not 1<=a.timeout_seconds<=86400:p.error('timeout must be 1–86400 seconds')
    if not Path(a.model).exists() and not a.allow_model_download:raise RuntimeError('Prepare model or explicitly approve download')
    manifest=probe_and_extract(a.input,a.output_directory,a.source_id,a.audio_stream_index,a.audio_offset)
    cmd=[sys.executable,str(Path(__file__).with_name('transcribe.py')),manifest['analysisAudio'],str(Path(a.output_directory)/'analysis.json'),'--source-id',a.source_id,'--audio-offset',str(manifest['audioOffsetSeconds']),'--model',a.model,'--device',a.device]
    if a.allow_model_download:cmd.append('--allow-model-download')
    if a.language:cmd+=['--language',a.language]
    if a.compute_type:cmd+=['--compute-type',a.compute_type]
    r=subprocess.run(cmd,timeout=a.timeout_seconds)
    if r.returncode:raise SystemExit(r.returncode)
if __name__=='__main__':main()
