---
type: concept
tags: [audio, sfx, final-cut-pro, licensing, research]
status: researched
updated: 2026-10-21
---

# SFX sourcing and sound design

Research answering Prompt 2 of [[fcp-plugin-research]] (SFX sources), run 21 Oct 2026 on the web instead of Perplexity. It covers which libraries to pay for, which licences hold up for client work and paid social, how to make SFX sound expensive, which design tools are worth it, and how to drop SFX on the cut in Final Cut Pro 12.4.

**Starting point:** Hunter already owns a lot of designed cinematic SFX. Since 20 Oct, [[sfx-library]] holds 1,547 Ocular sounds (Foundation, Forged, Velocity, Shift, Mechanica, Utility, Aperture, Cityscapes, Pendulum, Rainforest…), plus the Ripple Training packs and [[sound-lab]]. **The cheap sound comes from synthesis and mixing, not from a lack of library.** So the money should go on search and workflow, not on more trailer packs.

Prices are USD unless stated, converted at roughly US$1 = A$1.53. Most figures come from third-party listings because vendor pricing pages render in JavaScript, so **check the checkout page before buying.**

## 1. Libraries

### Subscriptions

| Service | Price | SFX | Client work and paid social |
|---|---|---|---|
| **Soundly Pro** | US$14.99/mo (~A$275/yr); yearly option exists but its price wasn't found. Free tier: 3,000 sounds, indexes 10k local files | 250k cloud library, and it **indexes your own drives** | ✅ The EULA covers your own and third-party productions, including advertising. Projects made while subscribed stay cleared after you cancel. Single workstation. Freesound add-on: use CC0 only |
| **Epidemic Sound Pro** | ~US$16.99/mo annual (US$203.88/yr ≈ A$312); $39.99 month-to-month | 250k, plus music | ✅ Client work (full sublicensing) and **online digital ads**. ❌ Cinema, TV shows and TV ads, government ads, and companies over US$10m revenue |
| Epidemic **Creator** | cheaper | same | ❌ Personal channels only. No client work, no ads |
| **Artlist Music & SFX Pro** | US$24.92/mo annual (US$299/yr ≈ A$458) | yes, plus music | ✅ Client work, paid ads, broadcast. The **Social** plan (US$119.88/yr) ❌ excludes commercial and client work |
| **Envato** (Core) | US$16.50/mo annual (US$198/yr ≈ A$303); $33–39 month-to-month | yes, plus templates | ✅ Commercial and client work, but **licensed per project**: register each download against the project. Finished projects stay licensed after you cancel; new projects need an active subscription |
| **Splice Sounds+** | ~US$12.99/mo | thin on video SFX | ✅ Royalty-free, including commercial use. Built for music producers, so it's the wrong tool here |
| **Krotos Studio** | US$119.88/yr list (US$14.99/mo); Pro US$279.99/yr | performable presets plus a library | ✅ "Cleared for commercial use". Needs an internet connection |

### One-off packs

| Pack | Price | Licence | Verdict |
|---|---|---|---|
| **Sonniss GDC Game Audio Bundles** (2015–2026) | **Free** (the 2026 bundle is 7.47 GB, from 17 vendors) | Royalty-free, commercial use, unlimited projects, no attribution. ❌ No AI/ML training | **Grab every year**. The best free source there is |
| **BOOM Library** Cinematic Trailers Designed | €129 (vol 1); Designed 2 is about €210 / £163 / US$170 | Single user, worldwide, royalty-free, covers advertising. Watermarked per buyer | Top quality, but it overlaps Ocular Foundation and Forged. Skip for now |
| **SoundMorph** Evolved Whooshes | US$199 | Single user, perpetual, royalty-free | Overlaps Ocular Velocity and Shift. Skip |
| "Cinematic Sound Design" | No brand by that exact name was found. Near matches: Flame Sound PYRO starter (US$14–49), Cineplug (US$29) | royalty-free, but check each vendor's terms | Cheap Gumroad packs vary a lot in quality. Skip |

### Is Soundly worth it?
**Yes, as the search layer.** One window searches Ocular, Ripple, the Sonniss archive and the 250k cloud library together, with waveform preview, pitch and speed before you drag, and spot-to-timeline. Soundly opened a **Final Cut Pro integration beta** in July 2025 that sends sounds straight to the timeline. Its site still lists only Premiere and After Effects, so **check FCP 12.4 support on the free tier before paying.** Even without the integration, dragging from Soundly into FCP works. The free tier's 10k-file index is too small for 1,547 Ocular sounds plus Sonniss, so Pro is the tier that fits.

## 2. Licensing

- **Cleared for client work and paid social with no extra licence:** Soundly Pro, Epidemic Pro (online ads only, not TV), Artlist Music & SFX Pro, Envato (per-project registration), Splice, Krotos, BOOM, SoundMorph, Sonniss GDC, ElevenLabs paid plans, Stable Audio Pro, and Apple's 1,300 built-in FCP sounds. **Ocular and Ripple:** owned and royalty-free. Re-check each EULA once and note it on [[sfx-library]].
- **Not cleared:** Epidemic Creator and Artlist Social (personal only). ElevenLabs free (needs attribution). Freesound non-CC0 sounds (CC-BY needs credit, CC-NC is non-commercial). Any Epidemic plan for TV or cinema ads.
- **Watch:** Adobe Firefly's commercial-safety promise covers its own models, but partner models in the dropdown are the user's responsibility. Its explicit "universally licensed" wording is attached to Music, not clearly to SFX yet. [[sound-lab]] is MIT plus Commons Clause: the rendered WAVs are fine in client videos, but the tool can't be sold.

## 3. Sound-design technique: making SFX sound expensive

1. **Three layers per hit: transient + body + tail.** A high click for definition, a mid body for character, and low weight for size. Body with no transient sounds muffled; transient with no body sounds toy-like. Align the transients on the same frame, then nudge the body 5–15 ms late for extra size. Keep detail layers lower and let the tail run past the others.
2. **High-pass every non-bass layer at 80–120 Hz** and carve the mids so layers don't mask each other. Glue them with light compression. That is the chain Krotos recommends: HPF, then a transient shaper, then a small plate.
3. **Vary pitch and time.** Never fire the same file twice in a row. Shift it ±1–3 semitones and trim it slightly differently each time; repeats read as cheap. For scale, duplicate a whoosh an octave down under a low-pass. For movement, add Doppler: pitch up on approach, down on the pass, and pan across the frame.
4. **Match the length to the motion.** A UI swipe or fast cut takes a 0.25–0.5 s whoosh. A slow push-in takes a long, airy one. **The whoosh peaks on the cut, not starting on it.**
5. **Match the reverb to the scene.** Diegetic sounds (doors, footsteps, shutters) get a short room that matches the space on screen. Graphic sounds (titles, UI) stay dry or get one shared small plate across the whole video, so they sit in one consistent "graphics space". Drone and exterior shots: almost no reverb, just air from EQ. Synth sounds are dry by nature, and that dryness is part of why they sound cheap.
6. **Duck the music, not the SFX.** FCP has no native sidechain. Options: range-select and pull the music 3–6 dB under big hits with keyframes; **Pixel Film Studios DipSync** (US$39.95) bakes ducking into keyframes; or round-trip the mix to Logic for a real sidechain.
7. **Loudness.** Measure the finished mix, not individual SFX: **-14 LUFS integrated, true peak no higher than -1 dBTP** (YouTube's reference; Instagram and TikTok often run hotter, around -10 to -12). No published SFX-to-music offset was found, so these are rules of thumb: VO is the anchor; music sits 8–12 dB under VO; impacts can peak level with VO for a frame; UI clicks and ambience sit 15–25 dB under VO and should be felt more than heard. [[sound-lab]]'s LUFS levelling suits SFX stems.
8. **Synth SFX get "recorded" texture.** Add saturation, a little noise or room tone, and a real recorded transient layered on top. Use synth sounds as the body, never alone.

## 4. Tools for designing custom SFX on a Mac

| Tool | Cost | Quality | Licence | Use it for |
|---|---|---|---|---|
| **Logic Pro** (Alchemy, Sample Alchemy, Quick Sampler, Space Designer) | US$199.99 one-off (A$ price unconfirmed) | pro | your output is yours | layering, resampling, true sidechain, convolution rooms. **Best value if not owned** |
| **Vital** | Free (Basic, full engine); Plus $25, Pro $80, or $5/mo | excellent synth | output yours; EULA not checked | risers, sweeps, sub drops, UI tones |
| **Krotos Studio** | US$119.88/yr (Pro $279.99) | good, fast, performable | cleared commercial | quick performed whooshes from an XY pad. A nice-to-have |
| **Tonsturm Whoosh** | US$99 one-off (sales to $69) | very good for passes and Doppler | perpetual | designing whooshes from any source. Add later |
| **Sound Particles** Indie / SkyDust | Indie ~US$399; SkyDust Stereo $149 (sale $89) | film-grade spatial | perpetual | overkill for social. Skip |
| **ElevenLabs SFX** | Starter ~US$5–6/mo; free tier needs attribution | decent for ambience and oddities, weak transients | paid: royalty-free, commercial | one-off foley you can't find. Use as a raw layer |
| **Stable Audio** Pro | ~US$12/mo | good textures and beds | commercial, trained on licensed data | ambience beds, risers |
| **Adobe Firefly Generate Sound Effects** (Aug 2026) | Firefly credits | matches sounds to video timing and voice imitation | commercially safe only for Adobe's own model | a test if Creative Cloud is already paid |

The earlier Magnific/ElevenLabs takes in `sfx-lib/_magnific/` confirmed the AI pattern: only the clicks and pops survived. Generated sounds are layers, not finished sounds.

## 5. Final Cut Pro workflow

1. **Put the library inside FCP:** make an alias of `~/Music/SFX Library/` and drop it into `/Library/Audio/Apple Loops/Apple/Final Cut Pro Sound Effects/`, then relaunch FCP. It appears in the Sound Effects sidebar of the Photos, Videos and Audio browser, searchable and skimmable, with no extension needed.
2. **Faster still:** build a "10x SFX" FCP library and import the curated kit (leave files in place) with keyword collections: Whoosh, Hit, Riser, UI, Ambience, Shutter. Mark the favourites. Keep it open next to every job.
3. **Land the peak on the cut:** in the browser, set a range whose **out point sits on the whoosh or riser peak**, park the playhead on the cut, and press **Shift-Q (backtimed connect)**. The peak lands exactly on the cut. Impacts: in point on the transient, then **Q**.
4. **On the beat:** mark beats with **M** while playing, or use **BeatMark X** (~US$3.99, a separate app that makes an FCPXML of beat markers), then snap with N on.
5. **Batch cueing:** [[sound-lab]] already does cut detection and **FCPXML export** of picture-synced cues. That is the in-house answer to an SFX browser that auto-places.
6. **Browsers outside FCP:** Soundly (FCP beta, see above). The **Epidemic desktop app** drags SFX and music straight into FCP and has an AI assistant, but it has no in-FCP panel. **Artlist's** library extension is Premiere-only. **Audio Design Desk** with its Audio Bridge workflow extension is the only true SFX-in-FCP panel found (40k+ sounds; old pricing ~US$299 lifetime Personal; Bridge still labelled beta). It's pricey and duplicates Soundly.

## Recommended starter setup (under about A$300/yr)

| Item | Cost/yr |
|---|---|
| **Soundly Pro** (monthly; switch to yearly if it's cheaper) | ~A$275 |
| **Sonniss GDC bundles**, all years, indexed in Soundly | A$0 |
| **Vital** Basic, with [[sound-lab]] for UI sounds | A$0 |
| FCP Sound Effects alias plus a keyworded SFX library, and the Shift-Q habit | A$0 |
| **Total** | **~A$275** |

- **If music is needed too:** swap Soundly for **Epidemic Pro** (~A$312/yr). It's a little over budget but covers music, SFX and online ads in one plan. It can't index Ocular, though, and that is the reason Soundly wins on SFX alone.
- **One-off adds, in order:** Logic Pro, if not owned (sidechain plus Space Designer fixes most of the "cheap" sound); then DipSync (US$39.95); then Tonsturm Whoosh (US$99).
- **Skip:** Artlist (over budget for SFX), Splice (music focus), Boom and SoundMorph packs (duplicate Ocular), Sound Particles.

## Sources
- Soundly: [plans FAQ](https://getsoundly.com/faq/what-are-the-differences-between-the-subscriptions/) · [EULA](https://getsoundly.com/assets/Soundly-EULA.pdf) · [usage FAQ](https://getsoundly.com/faq/how-can-I-use-the-sounds/) · [Freesound CC0 note](https://getsoundly.com/faq/how-can-i-use-the-freesound-library) · [$14.99 price](https://postaudiotips.beehiiv.com/p/sfx-library-manager) · [FCP beta, fcp.cafe Jul 2025](https://fcp.cafe/news/20250703)
- Epidemic: [Pro plan](https://epidemicsound.com/our-plans/pro-plan) · [pricing](https://photutorial.com/epidemic-sound-pricing) · [FCP desktop app](https://www.epidemicsound.com/plugins/final-cut-pro)
- Artlist: [pricing](https://photutorial.com/artlist-pricing) · [plans explained](https://artlist.io/blog/personal-plan-vs-unlimited-plan/) · [Premiere-only extension](https://help.artlist.io/hc/en-us/articles/29671103091613)
- Envato: [subscription](https://help.elements.envato.com/hc/en-us/articles/360000621663-About-Envato-Subscription) · [licence terms](https://help.elements.envato.com/hc/en-us/articles/360000628966-License-Terms) · [per-project review](https://josephnilo.com/blog/envato-elements-review/)
- Splice: [pricing](https://pricingsaas.com/companies/splice) · Sonniss: [GDC 2026](https://rekkerd.org/sonniss-releases-gdc-2026-game-audio-bundle/) · [licence summary](https://app.cinevva.com/guides/free-sound-effects-music)
- BOOM: [EULA/T&Cs](https://www.boomlibrary.com/?p=480427) · [pricing](https://www.bestservice.com/en/cinematic_trailers_designed_2.html) · SoundMorph: [Evolved Whooshes](https://www.motionmedia.com/soundmorph-soundpack-evolved-whooshes)
- Krotos: [pricing](https://krotos.studio/pricing) · [2026 sale list prices](https://krotos.studio/blog/stop-waiting-sale) · [whoosh tips](https://webflow.krotos.studio/guide/4-whoosh-sound-effects-tips) · [whoosh presets](https://krotos.studio/blog/whoosh-sound-effects-krotos-studio)
- Tonsturm: [KVR](https://www.kvraudio.com/product/whoosh-by-tonsturm) · Sound Particles: [summer sale 2026](https://lp.soundparticles.com/summer-sale-2026) · [Plugin Boutique](https://www.pluginboutique.com/manufacturers/275-Sound-Particles) · Vital: [tiers](https://producelikeapro.com/blog/vital-synth-review/)
- AI: [ElevenLabs commercial SFX](https://elevenlabs.io/sound-effects/commercial) · [Stable Audio pricing](https://costbench.com/software/ai-music-generators/stable-audio/) · [Adobe Firefly audio](https://itwire.com/business-it-news/business-software/adobe-makes-firefly-a-full-audio-studio-and-the-licence-is-the-actual-product) · [Firefly SFX resale thread](https://community.adobe.com/questions-404/can-i-sell-adobe-firefly-generated-sound-effects-as-an-asset-pack-1643734)
- Technique: [Morphic layering](https://morphic.com/resources/how-to/how-to-layer-sound-effects) · [Violet whooshes](https://violetrecording.com/how-to-make-whoosh-sounds/) · [Wayline attack/body/tail](https://www.wayline.io/learn/game-audio/1) · [Frame.io loudness](https://workflow.frame.io/guide/loudness-for-youtube) · [LUFS for social](https://filmandflow.beehiiv.com/p/the-ultimate-lufs-guide-perfect-audio-for-social-media)
- FCP: [custom SFX folder (Apple)](https://support.apple.com/guide/final-cut-pro/ver5fb43c4b4/mac) · [workflow extensions](https://support.apple.com/en-au/101630) · [DipSync](https://pixelfilmstudios.com/newsroom/pixel-film-studios-introduces-dipsync/) · [BeatMark](https://fcp.co/final-cut-pro/news/2590-beatmark-pro-music-driven-video-editing-for-final-cut-pro) · [ADD Audio Bridge](https://www.mixonline.com/technology/news-products/add-audio-bridge-for-final-cut-pro-beta-launched) · [ADD pricing](https://www.toolfarm.com/buy/audio_design_desk/)

Related: [[sfx-library]] · [[sound-lab]] · [[fcp-plugin-research]] · [[audio-for-video]] · [[sfx-sorter]]
