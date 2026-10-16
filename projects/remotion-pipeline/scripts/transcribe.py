"""Optional inference adapter; requires approved faster-whisper install and model."""
import argparse, hashlib, importlib.metadata, json, math
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('audio');p.add_argument('output');p.add_argument('--source-id',required=True);p.add_argument('--audio-offset',type=float,required=True);p.add_argument('--model',required=True);p.add_argument('--allow-model-download',action='store_true');p.add_argument('--device',choices=['cpu','cuda'],default='cpu');p.add_argument('--compute-type');p.add_argument('--language');p.add_argument('--initial-prompt',default='');a=p.parse_args()
    if not math.isfinite(a.audio_offset):p.error('offset must be finite')
    if Path(a.output).exists():raise FileExistsError('Use a new versioned analysis path')
    if not Path(a.audio).is_file():raise FileNotFoundError(a.audio)
    if not Path(a.model).exists() and not a.allow_model_download:raise RuntimeError('Supply a prepared local model path or approve --allow-model-download; VAD dependencies can also require initial download')
    from faster_whisper import WhisperModel
    from faster_whisper.audio import decode_audio
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    compute=a.compute_type or ('int8' if a.device=='cpu' else 'float16')
    audio=decode_audio(a.audio,sampling_rate=16000)
    vad_options=VadOptions(min_silence_duration_ms=500)
    speech=get_speech_timestamps(audio,vad_options=vad_options)
    model=WhisperModel(a.model,device=a.device,compute_type=compute,local_files_only=not a.allow_model_download)
    segments,info=model.transcribe(audio,word_timestamps=True,vad_filter=True,vad_parameters=vad_options,language=a.language,initial_prompt=a.initial_prompt or None)
    words=[];records=[]
    for s in segments:
        records.append({'start':s.start,'end':s.end,'text':s.text})
        for w in s.words or []:
            flags=[]
            if w.start is None or w.end is None or w.end<=w.start:flags.append('invalid_or_missing_timing')
            if w.probability is None or w.probability<.6:flags.append('review_word_probability')
            words.append({'start':w.start,'end':w.end,'text':w.word,'probability':w.probability,'reviewFlags':flags})
    sha=hashlib.sha256()
    with open(a.audio,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):sha.update(chunk)
    result={'sourceId':a.source_id,'audioSha256':sha.hexdigest(),'timeBasis':'audio_relative_seconds','audioOffsetSeconds':a.audio_offset,'durationSeconds':len(audio)/16000,'language':info.language,'model':a.model,'device':a.device,'computeType':compute,'fasterWhisperVersion':importlib.metadata.version('faster-whisper'),'vadSettings':{'minSilenceDurationMs':500},'speechRegions':[{'start':x['start']/16000,'end':x['end']/16000} for x in speech],'segments':records,'words':words,'humanTranscriptReviewed':False}
    with open(a.output,'x') as f:json.dump(result,f,indent=2,allow_nan=False)
if __name__=='__main__':main()
