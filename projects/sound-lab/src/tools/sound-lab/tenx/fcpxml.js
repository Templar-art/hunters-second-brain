// Final Cut Pro XML (v1.11 — FCP 10.6.6+, also reads into DaVinci Resolve) for picture-sync cues:
// one project, a gap the length of the clip, every SFX connected below it on its own WAV.

const RATES = {
  23.976: { num: 1001, den: 24000, base: 24 },
  24: { num: 100, den: 2400, base: 24 },
  25: { num: 100, den: 2500, base: 25 },
  29.97: { num: 1001, den: 30000, base: 30, drop: true },
  30: { num: 100, den: 3000, base: 30 },
  50: { num: 100, den: 5000, base: 50 },
  60: { num: 100, den: 6000, base: 60 }
};

export const rateOf = fps => RATES[fps] || RATES[25];

const escape = value =>
  String(value).replace(/[<>&"']/g, char => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&apos;' })[char]);

const fileUrl = path =>
  `file://${path
    .split('/')
    .map(part => encodeURIComponent(part))
    .join('/')}`;

// clips: [{ name, file, frame (connected offset, in frames), frames (length in frames) }]
export function buildFcpxml({ project, folder, clips, totalFrames, width = 1920, height = 1080 }) {
  const rate = rateOf(project.fps);
  const time = frames => (frames ? `${frames * rate.num}/${rate.den}s` : '0s');
  const root = `${project.mediaPath.replace(/\/+$/, '')}/${folder}`;
  const title = `${project.name || 'Sound Lab'} SFX`;
  const assets = clips
    .map(
      (clip, index) =>
        `    <asset id="a${index + 1}" name="${escape(clip.name)}" start="0s" duration="${time(clip.frames)}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">
      <media-rep kind="original-media" src="${escape(fileUrl(`${root}/${clip.file}`))}"/>
    </asset>`
    )
    .join('\n');
  const connected = clips
    .map(
      (clip, index) =>
        `              <asset-clip ref="a${index + 1}" lane="-1" offset="${time(clip.frame)}" name="${escape(clip.name)}" start="0s" duration="${time(clip.frames)}" audioRole="effects"/>`
    )
    .join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
  <resources>
    <format id="r1" name="Sound Lab ${project.fps}p" frameDuration="${time(1)}" width="${width}" height="${height}"/>
${assets}
  </resources>
  <library>
    <event name="${escape(title)}">
      <project name="${escape(title)}">
        <sequence format="r1" duration="${time(totalFrames)}" tcStart="0s" tcFormat="${rate.drop ? 'DF' : 'NDF'}" audioLayout="stereo" audioRate="48k">
          <spine>
            <gap name="Picture" offset="0s" start="0s" duration="${time(totalFrames)}">
${connected}
            </gap>
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
`;
}
