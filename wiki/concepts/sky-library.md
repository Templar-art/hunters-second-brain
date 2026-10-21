---
type: concept
tags: [sky, time-of-day, ai-reference, hdri, plate-vfx]
status: active
updated: 2026-10-21
---

# Sky Library

This is a reference of what real sky looks like at each time of day. It holds the best-looking real skies for each time, to use as AI reference images and prompt wording. Built 2026-10-21 after day-to-dusk was shelved in [[plate-vfx-roadmap]], when Hunter decided to "just use AI" for time-of-day changes.

**Deliverable:**
- [`projects/sky-library/index.html`](../../projects/sky-library/index.html): picks, physics notes and prompt language per time.
- `sheets/` and `sheets_away/` hold ranked contact sheets of all 299 skies.

## Source
- All 299 Poly Haven sky HDRIs (CC0), tagged by `time_of_day`. The metadata is in `polyhaven_skies.json`.
- Downloads:
  - every sky at 1k, in `hdr_1k/` (gitignored)
  - the 28 picks at 2k, in `hdr_2k/` (gitignored)
  - re-fetch from `https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/<res>/<id>_<res>.hdr`
- Each sky is rendered as the camera sees it (84° hfov), in two directions: 30° off the sun, and with the sun behind the camera. Each also gets a 360° strip of the 0–40° band.
- **Lesson:**
  - Daytime skies must be judged sun-behind. Facing the sun, every midday sky looks blown and grey. Sun-behind is how real-estate exteriors are shot.
  - Night must be exposed dark. Auto-exposure turns a real night into a fake day.

## Picks (★ = best)

**Hunter, 2026-10-21: only golden hour and blue hour matter.** The page now shows just those two, with 10 options each. Dawn-twilight skies (kiara_1_dawn, venice_dawn_1, signal_hill_dawn) count as blue hour because the sky looks the same at sun 0 to −8°. The other times are kept below for reference.

- Extra golden-hour picks: wasteland_clouds_puresky, wildflower_field, evening_field, qwantani_sunset, sunset_meadow_path, venice_sunset
- Extra blue-hour picks: sunset_fairway, kiara_1_dawn, venice_dawn_1, qwantani_dusk_1_puresky, signal_hill_dawn, syferfontein_0d_clear_puresky

| Time | Sun elevation | ★ Best | Alternates |
|---|---|---|---|
| Sunrise / dawn | −6° → +6° | umhlanga_sunrise | kiara_1_dawn (pre-sun pink band), citrus_orchard_road, qwantani_sunrise_puresky |
| Morning | 10–35° | museumplein | driving_school, rustig_koppie_puresky, kiara_4_mid-morning |
| Midday | 50–80° | kloofendal_48d_partly_cloudy_puresky | rosendal_plains_2, clarens_midday, sunflowers_puresky |
| Afternoon | 20–45° | skidpan | oberer_kuhberg, waterkloof_farm (cirrus), kiara_6_afternoon (clear) |
| Golden hour / sunset | +6° → 0° | grasslands_sunset | sunset_in_the_chalk_quarry, minedump_flats, kloppenheim_06_puresky |
| Dusk / blue hour | 0° → −8° | the_sky_is_on_fire (afterglow) | qwantani_dusk_2_puresky (Belt of Venus), rosendal_park_sunset_puresky, kiara_9_dusk (deep blue) |
| Night | < −18° | rogland_clear_night | clarens_night_02 (moonlit), kloppenheim_02_puresky, satara_night_no_lamps |

Poly Haven only has 10 dusk skies. The real-estate twilight look is the stretch from afterglow into blue hour (sun 0 to −8°), and the dusk picks cover it.

## What real sky does (short version)
- **Sunrise:**
  - A thin peach-orange band sits on the horizon, then lilac, then cool blue.
  - Clean air, with less haze than evening.
  - Opposite the sun: the pink Belt of Venus over a blue earth shadow.
- **Morning:**
  - Crisp saturated blue that pales to near-white at the horizon.
  - Long, sharp, cool shadows.
- **Midday:**
  - Deepest blue overhead, a strong pale haze at the horizon.
  - Cumulus with flat grey bases, short hard shadows.
- **Afternoon:**
  - Like morning but warmer and hazier.
  - Taller cumulus plus cirrus streaks, with a gold tint coming in.
- **Golden hour:**
  - A big warm-to-cool split across the frame: gold near the sun, blue above and away.
  - Clouds are gold-edged with violet shadows.
- **Blue hour:**
  - No shadows; the sky dome is the only light.
  - Gradient: peach band → rose/lilac → deep blue.
  - Interior and street lights balance with the sky. This is the twilight-listing window.
- **Night:**
  - Deep navy, not black. Orange light-pollution glow near towns.
  - Moonlight reads cool silver.
- Prompt lines for each time are in `times.json` and on the page.

Physics sources: PetaPixel (golden/blue hour), Scott Kelby (blue hour), PhotoEphemeris (twilight zones), timeanddate (blue hour).

## Related
[[plate-vfx]] · [[plate-vfx-roadmap]] · [[higgsfield-pipelines]] · [[staging-rules]]
