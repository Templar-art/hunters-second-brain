"""Reel 2 ambience stems (hallway, powder), 7.2s with soft fades. 0 credits."""
import subprocess, os
H = os.path.expanduser; O = H("~/Music/SFX Library/Ocular Sounds/The Provence"); D = H("~/Downloads")
F = "afade=in:st=0:d=0.3,afade=out:st=6.6:d=0.6"; S = "aformat=sample_rates=48000:channel_layouts=stereo"
def mk(out, inputs, fc):
    args = []
    for ss, src in inputs: args += (["-f", "lavfi", "-t", "7.2", "-i", src] if ss is None else ["-ss", str(ss), "-t", "7.2", "-i", src])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", fc, "-map", "[o]", "-c:a", "pcm_s16le", out], check=True, stdin=subprocess.DEVNULL)
mk("deliver/sfx/04_hallway_curtain_birds_room.wav",
   [(1.5, f"{D}/freesound_community-160170_wind-blowing-curtain_owi-102398.mp3"),
    (5, f"{O}/AMBForst/AMBForst_WOODS-Day Ambience Woodland Loop 03_Ocular_The Provence.wav"),
    (None, "anoisesrc=c=brown:a=0.02")],
   f"[0]{S},areverse,volume=0.85[a];[1]{S},lowpass=f=2500,highpass=f=300,volume=0.35[b];[2]{S},lowpass=f=300[c];[a][b][c]amix=inputs=3:normalize=0,loudnorm=I=-23:TP=-3,{S},{F}[o]")
mk("deliver/sfx/05_powder_breeze_leaves.wav",
   [(30, f"{D}/traian1984-ambience-wind-blowing-through-trees-01-186986.mp3"),
    (10, f"{O}/AMBGras/AMBGras_FIELD-Day Ambience Field Loop 02_Ocular_The Provence.wav")],
   f"[0]{S},lowpass=f=4500,volume=0.9[a];[1]{S},lowpass=f=3000,volume=0.3[b];[a][b]amix=inputs=2:normalize=0,loudnorm=I=-23:TP=-3,{S},{F}[o]")
