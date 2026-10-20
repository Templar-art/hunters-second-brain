---
type: project
tags: [final-cut-pro, plugins, editing, tools, research]
status: researched
updated: 2026-10-21
---

# Final Cut Pro plugin research

The goal is to work out which Final Cut Pro plugins and companion apps would make 10x edits faster or better, without paying for anything FCP already does or that's already installed. The prompts are in [projects/fcp-plugin-research/perplexity-prompts.md](../../projects/fcp-plugin-research/perplexity-prompts.md). **Prompt 2 (SFX sources) was answered on 21 Oct 2026: see [[sfx-sourcing-and-design]]. Prompt 1 (FCP plugins) was answered on 21 Oct 2026 by web research (five parallel research passes, not Perplexity) and is filed below.**

## The edit machine (checked 20 Oct 2026)
- Final Cut Pro **12.4** on an Apple **M5 Pro** running macOS 27.0.1. DaVinci Resolve is also installed.
- ⚠️ [[video-edit-pipeline]] says "Resolve or Premiere", but FCP is the working NLE on this Mac. Flagged on that page.

## Already installed (`~/Movies/Motion Templates.localized/`)
- **motionVFX:** mCaptions, mTracker 3D (plus Area and Expansions), mTracker Surface, mRotoAI (plus Expansions), mFilmLook, mFlare 2, mPuppet, DesignStudio and Freebies.
- **Pixel Film Studios:** FCPX Stabilizer, Shape Tracker, Timelines and Free Effects/Transitions.
- **Ripple Training (RN):** Shake Transitions, Mask Glow, Effects Expansion Pack, and the Sound Effects packs (8mm, Paper Tear, Glitch, Transitions).
- **Others:** Smooth Camera Zooms Pro, Smooth Transition Layers Free, Target Zoom Transitions, Halation (Lifted Eriks), Cinematic Rotate, BW / Motion Blur 2, Adjustment Layer, and Envato templates.
- Install paths and the Motion nesting rule are in auto-memory `reference-fcp-template-install.md`.

## Already solved locally
- **SFX:** [[sound-lab]] covers custom synth SFX, layering, LUFS levelling of SFX files and FCPXML export of cues. [[sfx-library]] (Ocular Sounds) covers recorded hits and whooshes.

---

# Prompt 1 results (21 Oct 2026)

## Read this first: three things changed in 2026
1. **FCP 12.0–12.3 absorbed a lot of plugin territory.** 12.0 (28 Jan 2026) added Transcript Search, Visual Search and Beat Detection. 12.3 (30 Jun 2026) added **Generate Captions** (burned-in, word-by-word animated), **Auto Mask**, a rebuilt **Match Color**, Edit Detection and HEVC proxies. 12.4 (29 Sep 2026) only added Cinematic-mode depth editing. All of these are in the one-off purchase as well as the subscription. ([Apple release notes](https://support.apple.com/en-us/102825); [ProVideo Coalition, Jul 2026](https://www.provideocoalition.com/surprise-its-final-cut-pro-12-3/); [TidBITS, 15 Jan 2026](https://tidbits.com/2026/01/15/apple-bundles-pro-apps-into-new-creator-studio-subscription/))
2. **Apple bought motionVFX on 16 Mar 2026.** The catalogue is still sold "for the time being"; nothing has been said about pricing, updates or folding it into Apple Creator Studio. Several standalone FCP packs (mTravel, mLowers Simple) now show "no longer available". Everything owned from motionVFX keeps working today but has an uncertain long-term path. ([9to5Mac, 16 Mar 2026](https://9to5mac.com/2026/03/16/apple-acquires-motionvfx-maker-of-popular-final-cut-pro-plugins-and-more/); [NewsShooter, 16 Mar 2026](https://www.newsshooter.com/2026/03/16/apple-acquires-motionvfx/))
3. **Boris FX bought iZotope (2 Jul 2026)**, so RX and CrumplePop are now one vendor. ([Boris FX](https://blog.borisfx.com/press/boris-fx-acquires-izotope-the-award-winning-leader-in-intelligent-audio-technology))

**Apple Creator Studio** (launched 28 Jan 2026): A$19.99/mo or A$199/yr (US$12.99 / $129) for FCP, Logic, Pixelmator Pro, Motion, Compressor and MainStage. One-off FCP is still A$499.99 / US$299.99. ([GadgetGuy, 14 Jan 2026](https://www.gadgetguy.com.au/apple-creator-studio-subscription-bundle-price); [9to5Mac, 13 Jan 2026](https://9to5mac.com/2026/01/13/apple-debuts-apple-creator-studio-subscription-heres-what-you-get/))

## What FCP 12.4 does natively (don't pay for these)
| Need | Native in FCP 12.x? | Limit |
|---|---|---|
| Burned-in word-by-word social captions | **Yes**, Generate Captions (12.3): Fade/Scale/Highlight/Fill by character, word or line, plus a 9:16 safe-zone option | US English only; thinner styling than mCaptions |
| Closed captions | Yes, Transcribe to Captions (11.0) | Apple silicon only |
| Caption translation | **No** | "Duplicate to new language" is a manual copy |
| Transcript / visual search of footage | **Yes** (12.0) | US English; can't view, edit or export the transcript, so no text-based editing; Visual Search misses synonyms |
| 16:9 → 9:16 | Smart Conform | One framing per clip; Apple doesn't say it tracks subjects over time |
| Dialogue cleanup | Voice Isolation, Noise Removal, Hum Removal | Fine for light noise; not a restoration tool |
| Auto-ducking | **No** | Manual range + volume keyframes |
| LUFS | **Measure only**: the MultiMeter effect reads integrated LUFS | No normalise-to-target |
| S-Log3 → Rec.709 | **Yes**: Camera LUT, S-Log3/S-Gamut3 and S-Log3/S-Gamut3.Cine built in, applied from metadata | Generic tone map; looks flat |
| Shot matching (drone to Sony) | **Yes**, Match Color (rebuilt 12.3) | No hands-on review yet |
| AI masking | Magnetic Mask (11.0), Auto Mask (12.3) | Auto Mask works frame by frame and can flicker |
| Proxies | HEVC or ProRes Proxy (12.3); background render now off by default | — |

Sources: [Apple release notes](https://support.apple.com/en-us/102825); [Apple guide: generate subtitles](https://support.apple.com/guide/final-cut-pro/verd6d52c4e8/mac); [Apple guide: enhance audio](https://support.apple.com/guide/final-cut-pro/enhance-audio-verc1fab873/mac); [Apple guide: Smart Conform](https://support.apple.com/guide/final-cut-pro/ver26664d93f/mac); [PVC, 28 Jan 2026](https://www.provideocoalition.com/whats-new-in-final-cut-pro-12-and-more/); [Apple Discussions, Apr 2025](https://discussions.apple.com/thread/256040406); [Larry Jordan, 4 Jul 2026](https://larryjordan.com/articles/new-features-in-apple-final-cut-pro-12-3/).

## Picks by area
Prices are USD from vendor pages read 21 Oct 2026 unless stated. **No vendor published AUD prices except Apple.** "FCP 12" means the vendor or a 2025–26 source says so; nothing below has a vendor statement for 12.4 specifically, so test each in 12.4 on a throwaway project first.

### 1. Audio (high importance for talking-head work)
- **Accentize dxRevive** (Accentize). $99 Standard / $299 Pro (iLok), one-off, 7-day trial. Final Cut is a listed host; Apple silicon recommended; v1.2.8, Jul 2025. Turns roomy or lav-poor dialogue into studio-sounding voice, well past Voice Isolation. *Weakness:* CPU-heavy, so render before scrubbing. ([accentize.com](https://www.accentize.com/dxrevive/))
- **Antinode Clear** (Antinode, formerly Supertone Clear). $69 on sale, regular price not found, one-off; AU, Apple silicon native. Cheaper real-time denoise and de-reverb. *Weakness:* FCP isn't named as a host, so trial it. Pick this **or** dxRevive. ([antinodeaudio.com](https://antinodeaudio.com/en/clear))
- **DipSync** (Pixel Film Studios). $39.95 one-off. FCP 10.8+, Apple silicon. Auto-ducks music under voice and can bake the result into ordinary volume keyframes, then be removed. Fills a real FCP gap. *Weakness:* vendor page only, no FCP 12 statement, and it needs two linked instances. ([pixelfilmstudios.com](https://pixelfilmstudios.com/plugins/dipsync/))
- **Loudness, -14 / -23 LUFS.** Measure with FCP's MultiMeter (free) or Youlean Loudness Meter 2 (free; Pro $49 one-off adds platform presets). Neither normalises. Measure the final mix, then trim with gain. *Weakness:* manual. ([youlean.co](https://youlean.co/youlean-loudness-meter/)) [[sound-lab]]'s LUFS levelling only covers SFX files, not the final mix.
- **iZotope RX 12** (Boris FX). Elements $99 / Standard $399 / Advanced $1,399, one-off. Excellent, but **FCP isn't on the official host list** and macOS 27 isn't listed yet. ([iZotope pricing](https://www.izotope.com/en/products/rx/pricing-options))
- **SFX inside FCP:** covered by Prompt 2, see [[sfx-sourcing-and-design]] (Soundly Pro + Sonniss is the pick). Epidemic Sound has a desktop drag-to-timeline app (Mar 2026), not a true FCP extension. Artlist has no FCP extension.

### 2. Captions and text (mostly solved natively)
- **FCP Generate Captions** (free, native). Covers about 80% of mCaptions use for English social captions. *Overlap:* mCaptions, which stays useful for heavier styling.
- **captionTranslator** (Intelligent Assistance). $34.99 one-off on the Mac App Store, macOS 15+. Workflow extension that translates FCP captions into 20+ languages on-device. The only clean fix for FCP's missing translation. *Weakness:* quality depends on Apple's translation models, and the listing doesn't show a 2025–26 version date. ([App Store](https://apps.apple.com/us/app/captiontranslator/id6737919696?mt=12))
- **Captionator for Final Cut** (Glide Slope). $19.99 one-off; listing says FCP 11 and 12. Whisper transcription in about 100 languages: use it for non-English speakers, since native captions are US English only. *Weakness:* few ratings, with reports of timing drift and breakage after FCP updates. ([App Store](https://apps.apple.com/us/app/captionator-for-final-cut/id1627843786?mt=12))
- **Simon Says**. From $15/hr pay-as-you-go or $15–150/mo. Cloud transcription and translation with an FCP extension. *Weakness:* per-hour cloud cost for things FCP now does free. Skip unless multilingual work becomes frequent. ([pricing](https://www.simonsaysai.com/pricing))

### 3. Reframing 16:9 → 9:16 (no plugin worth buying)
No third-party FCP auto-reframe plugin with subject tracking could be confirmed from a 2025–26 source. "mReframe" and a Pixel Film Studios auto-reframe don't exist; Keyflow Pro is an asset manager; Autopod is Premiere-only.
- **Smart Conform** (native) is the workflow: duplicate the project as Vertical with Smart Conform ticked, then fix the bad clips with Transform keyframes. Titles and lower thirds need re-placing by hand.
- **mTracker 3D** (owned) tracks well, but its data drives motionVFX elements, not the clip's Transform, so it's a fix-up tool rather than an auto-reframer (unverified for 2025–26).
- **Resolve Studio Smart Reframe** (Blackmagic, US$236 one-off at the current markdown) is the only proven tracking reframe, but it means an FCPXML round trip and Studio is a paid upgrade. ([Blackmagic](https://www.blackmagicdesign.com/products/davinciresolve/studio))

### 4. Colour
- **S-Log3 → Rec.709:** use FCP's built-in Camera LUT (S-Log3/S-Gamut3.Cine), applied from metadata. Free and already colour-managed. No official Sony technical s709 download for the a7S III / a7R V was found; Sony's published LUTs are creative looks. Paid conversion packs (Leeming LUT Pro) had no 2025–26 source or price and need specific in-camera settings. ([Apple guide: LUTs](https://support.apple.com/guide/final-cut-pro/ver24f966423/mac); [Sony pro LUTs](https://pro.sony/en_SL/technology/professional-video-lut-look-up-table))
- **Colour-managed workflow:** Wide Gamut HDR library + Rec.709 project + camera LUT is FCP's native path. No 2025–26 source documents ACES inside FCP.
- **Drone to Sony:** DJI's free D-Log M → Rec.709 LUT for the exact drone model, loaded as a custom camera LUT, then **Match Color** to a Sony reference frame. Free.
- **CineMatch** (FilmConvert). From $119 one-off. Camera-to-camera matching profiles. *Weakness:* FCP 12 support and profiles for the a7R V and current DJI drones are unconfirmed. Only buy if Match Color falls short and the drone has a profile. ([filmconvert.com](https://www.filmconvert.com/cinematch))
- **Color Finale 2 / 2 Pro** (Color Trix). $119 / $169; v2.15 shipped 28 Apr 2026. The nearest thing to a real grading panel in FCP (layers, curves, better scopes). *Weakness:* FCP 12 support, licence type and Apple silicon aren't stated on the store page; overlaps the much-improved native tools. There is no "Color Finale 3". ([colorfinale.com](https://colorfinale.com/store))
- **Dehancer Pro** (Dehancer). Subscription, Studio plan US$49/mo or $588/yr; FCP 11 and 12 compatibility stated in v7.4.2. Excellent film emulation. *Weakness:* expensive, a Sep 2026 G2 review complains about updates, and it **overlaps mFilmLook + Halation**, which are owned. ([dehancer.com](https://dehancer.com/pricing))
- **FilmConvert Nitrate**. From $119 one-off. *Overlaps mFilmLook + Halation.*

### 5. Speed and organisation (the biggest time saver)
- **Jumper** (Witchcraft Software). $169 lifetime with 1 year of updates; Pro $599 lifetime or $49/mo. Local visual and speech search across all footage, and since build 3032 (Mar 2026) a Script Editor for script-based editing in FCP, transcript export and frame-exact jumps into FCP. In PVC's tests it beat FCP's native Visual Search. *Weakness:* face and people search are Pro-only; no explicit Apple-silicon-native statement. ([Jumper, 3 Oct 2025](https://getjumper.io/blog/changes_product_lineup); [fcp.cafe, 21 Mar 2026](https://fcp.cafe/news/20260321/); [PVC, 28 Jan 2026](https://www.provideocoalition.com/whats-new-in-final-cut-pro-12-and-more/))
- **ScriptStar** (LateNite Films). $9.99 one-off; listing names FCP 12 / 12.3+. Turns transcripts into favourite ranges, transcribes locally (Whisper, Parakeet, Apple) and exports CSV/Word/PDF/SRT. Owning it also unlocks **CommandPost 2** (free, Apple silicon native: titles-to-keywords, timeline CSV, control surfaces). *Weakness:* indie tool; a workaround, not full text-based cutting. ([App Store](https://apps.apple.com/app/scriptstar/id6759045715); [CommandPost](https://commandpost.fcp.cafe/))
- **Arctic** (Hedge, formerly Final Cut Library Manager). $49 perpetual with 1 year of updates. Finds every library on every drive and purges render, cache and optimised media. *Weakness:* no version or FCP 12 statement on the page. ([hedge.co](https://hedge.co/products/arctic))
- **Lumberjack Builder NLE**. $199.99. Text-based editing, but no update since Apr 2025 and a report that it fails on FCP 11. **Risky.**
- **EditReady** (Hedge, $99/$149). Overlaps FCP 12.3's native HEVC proxies and Compressor.

### 6. Motion graphics (already owned)
- **mReal Estate** (111 titles + 5 transitions: price, area, address, floor-plan infographics, amenity icons), a minimal Real Estate collection and **mLogo Cinematic 2** are all part of **DesignStudio**, accessed through mExtension. Lower thirds: mLowers Universal. **Check mExtension before buying any real-estate title, price card or logo reveal.** ([motionVFX real-estate collection](https://www.motionvfx.com/collections/real-estate-30608))
- **mTracker 3D Estate Pack**: 30 tracked 3D callouts for walkthroughs, needs mTracker 3D (owned). *Weakness:* glowing style may fight a minimal brand look. ([motionVFX](https://www.motionvfx.com/store,mtracker-3d-estate-pack,p4653.html))
- **Maps are the one real gap.** **Globe Trotter 3** (Century Creatives via FxFactory), $39 one-off, Apple silicon native: stylised maps, globes and pins. *Weakness:* unclear whether it uses real map data; no FCP version listed. ([fxfactory.com](https://fxfactory.com/info/globetrotter/)) **FCPX Maps 2.0** (Pixel Film Studios), $39.95, draws real routes via Mapbox. *Weakness:* client work needs Mapbox's commercial media licence on top. ([pixelfilmstudios.com](https://store.pixelfilmstudios.com/product/fcpx-maps/)) GeoLayers is After Effects only.
- **Envato Elements** ($33/mo Core), **FCPX Full Access** ($99 bundle) and **Ripple** title packs all duplicate DesignStudio.

### 7. AI inside FCP
- **Neat Video 6** (ABSoft). FCP 12 supported since 6.1; 6.1.2 (Apr 2026) added M5 Pro/Max GPU support. The reference denoiser for low-light S-Log3 interiors, twilights and noisy AI clips. *Price unverified for v6:* the last confirmed figures were $79.90 Home / about $149.90 Pro, one-off. *Weakness:* render-heavy. ([Digital Production, 13 Apr 2026](https://digitalproduction.com/2026/04/13/neat-video-6-1-2-adds-vegas-2026-and-nuke-17/))
- **Topaz Video** (Topaz Labs). FCP plugin new in v1.7.0 (11 Aug 2026). Subscription only: Personal $299/yr, Pro $699/yr. *Weakness:* plugin install failures reported, Starlight models don't run locally on Mac, and 2x+ upscales need manual timeline changes. Upscaling AI clips is already available through Higgsfield and Magnific. ([Topaz](https://www.topazlabs.com/topaz-video); [Topaz community](https://community.topazlabs.com/t/topaz-video-1-7-0/104328))
- **Object removal:** no AI object-removal plugin for FCP with a 2025–26 source. mRotoAI and Auto Mask isolate but don't remove. Send the shot to Resolve or an AI inpaint tool instead.
- **Boris FX Continuum 2026.5**. From $325/yr. Object Brush ML, Upres ML. *Weakness:* subscription, and Object Brush overlaps mRotoAI and Auto Mask. Mocha Pro has no FCP plugin.
- **B-roll search:** Jumper (above) beats native Visual Search.

### 8. Interchange
- **FCP → Resolve:** Resolve 21 imports and exports FCP 12 FCPXML (since public beta 4); the current build is 21.1, Sep 2026. The free version is enough for grading round trips. *Weakness:* titles, Motion generators and role-based mixing don't transfer. ([Motion Media](https://www.motionmedia.com/mm-blog/davinci-resolve-21-beta-4-fcpxml-ai-updates)) XtoCC and SendToX target Premiere and aren't needed.
- **Frame.io V4:** free Mac app uploads to V4, but the FCP Share Destination can't create V4 projects or browse V4, and there's no comments-into-FCP panel (Premiere has one). Plans: Free (2 GB), Pro $15/member/mo, Team $25/member/mo. ([Frame.io help, 16 Jun 2026](https://help.frame.io/en/articles/9893008-what-to-expect-when-updating-to-v4-a-comprehensive-guide-for-enterprise-customers); [Frame.io pricing](https://frame.io/pricing))
- **Postlab** (Hedge) is library collaboration, not client review: overkill solo.

## Buy-first shortlist
Do the free steps first: Generate Captions, Camera LUT, Match Color for drone, Smart Conform, MultiMeter for LUFS, mReal Estate from DesignStudio, Resolve 21 free for grading.

| # | Item | Price (USD) | Why first |
|---|---|---|---|
| 1 | Jumper | $169 one-off | Selects + script editing across every job; the biggest time saver |
| 2 | Accentize dxRevive | $99 one-off | Talking-head audio quality jump |
| 3 | PFS DipSync | $39.95 one-off | Auto-ducking, a native gap on every music-plus-VO edit |
| 4 | Neat Video 6 Pro | ~$149.90 one-off (v5 price, unverified) | Low-light interiors, twilights and AI clips |
| 5 | ScriptStar (+ free CommandPost) | $9.99 one-off | Transcript export and keywording |
| 6 | Arctic | $49 one-off | Render and cache purging across drives |
| 7 | Globe Trotter 3 | $39 one-off | The only motion-graphics gap: location maps |
| 8 | captionTranslator | $34.99 one-off | Only when a client needs another language |

**Total: about US$591.83** (US$556.84 without #8). At an assumed ~1.53 AUD/USD (not sourced, check the day's rate) that's roughly **A$905** before GST. All one-off, no new subscriptions.

## Skip list
- **Dehancer, FilmConvert Nitrate:** duplicate mFilmLook + Halation.
- **CineMatch:** until Match Color has been tried on drone footage.
- **Color Finale 2 Pro:** optional only if native grading feels limiting; FCP 12 support unconfirmed.
- **Envato Elements, FCPX Full Access, Ripple title packs, Pixel Film Studios Members Club:** duplicate DesignStudio's mReal Estate and mLogo.
- **Magic Captions, Simon Says, extra caption plugins:** native Generate Captions plus mCaptions covers it.
- **iZotope RX, CrumplePop, Waves Clarity Vx:** FCP not a confirmed host, or overlaps dxRevive.
- **Lumberjack Builder NLE:** stale, fails on FCP 11.
- **EditReady, Kyno:** native HEVC proxies cover it; Kyno has no FCP integration.
- **Topaz Video:** subscription, and AI-clip upscaling is already available via Higgsfield and Magnific.
- **Boris FX Continuum, Sapphire, Mocha:** subscription, overlaps mRotoAI and Auto Mask; Mocha has no FCP host.
- **Resolve Studio for Smart Reframe, motionVFX CineStudio upgrade:** most of the value is already owned.
- **XtoCC, SendToX, Keyflow Pro:** wrong direction or wrong tool.

## Caveats
- Several product pages are live but undated (©2026). They were read on 21 Oct 2026 and are cited as current. Pre-2025 sources were excluded, which left gaps.
- No vendor confirms FCP 12.4 specifically. Pixel Film Studios plugins broke on FCP 11 until patched, so expect the same risk.
- The drone model (D-Log vs D-Log M) decides which DJI LUT is needed; not yet recorded.

Related: [[sfx-sourcing-and-design]] · [[sound-lab]] · [[sfx-library]] · [[video-edit-pipeline]] · [[audio-for-video]] · [[color-grading]]
