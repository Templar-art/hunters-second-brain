import json
p = json.load(open("picks.json"))
T = {
 "sunrise": ("Sunrise / dawn", "sun −6° → +6°",
  "Before the sun clears the horizon: a thin orange-to-peach band sitting on the horizon, fading up into pale lilac then clean blue. Opposite the sun a pink 'Belt of Venus' sits above a grey-blue earth shadow. Once the sun is up the disc is yellow-white, low cloud undersides glow orange, everything above stays cool. Air is clean and cool, less haze than evening.",
  "pre-dawn sky, thin peach-orange band low on the horizon fading through pale lilac to soft clear blue above, cool clean air, sun just cresting, undersides of low clouds lit warm orange, long soft shadows"),
 "morning": ("Morning", "sun 10–35°",
  "Bright, clean, crisp. The sky is a saturated mid-blue that pales toward a near-white horizon. Shadows are long, sharp and slightly cool. Light is neutral-to-warm and directional; cumulus build slowly and stay small and white.",
  "crisp mid-morning sky, saturated clear blue fading to pale near-white at the horizon, a few small bright white cumulus, low raking sunlight from the side, long crisp shadows, clean fresh air"),
 "midday": ("Midday", "sun 50–80°",
  "Hardest light of the day. The deepest blue sits overhead and the sky pales strongly toward a hazy horizon. Shadows are short and sit directly under objects. Fair-weather cumulus are bright white with flat grey bases, and contrast is high. Shoot with the sun behind the camera for the deepest blue; facing the sun the sky washes out.",
  "high-noon sky, deep cobalt blue overhead grading to soft pale haze at the horizon, scattered bright white fair-weather cumulus clouds with flat grey bases, hard overhead sunlight, short shadows, high contrast"),
 "afternoon": ("Afternoon", "sun 20–45°",
  "Like the morning but warmer and hazier. More humidity means taller cumulus and wispy cirrus streaks. Light picks up a hint of gold and shadows lengthen again. This is the classic real-estate blue-sky look when the sun is behind the camera.",
  "late-afternoon sky, clear warm blue with wispy high cirrus streaks and puffy white cumulus, gentle golden tint in the sunlight, lengthening soft shadows, slight atmospheric haze toward the horizon"),
 "sunset": ("Golden hour / sunset", "sun +6° → 0°",
  "Warm, low, directional light. The sun disc is orange and the sky near it glows gold and amber. Higher up and away from the sun the sky stays blue, so there's a big warm-to-cool split across the frame. Clouds catch colour on their sun-facing edges: gold on top, grey-violet in their shadows. Long warm shadows; façades facing the sun glow.",
  "golden hour sunset, low orange sun disc on the horizon, warm amber and gold glow across the lower sky, scattered clouds lit gold on their edges with violet-grey shadows, sky above stays soft blue, long warm shadows across the ground"),
 "dusk": ("Dusk / blue hour", "sun 0° → −8°",
  "The sun is down, so there are no shadows: all light comes from the sky dome. For a few minutes after sunset clouds can light up pink-orange from below (afterglow). Then a smooth gradient takes over: a warm peach/orange band on the horizon, then rose-lilac, then deep saturated blue overhead. The opposite horizon shows the pink Belt of Venus over the blue earth shadow. Interior and street lights now match the sky brightness: this is the real-estate twilight window.",
  "blue hour twilight about fifteen minutes after sunset, sun below the horizon, smooth gradient from a warm peach-orange band at the horizon through soft rose and lilac into deep saturated blue above, no shadows, soft even ambient light, warm interior lights glowing in the windows"),
 "night": ("Night", "sun < −18°",
  "Real night is dark. The sky is a deep navy, not black, and near towns the horizon glows orange-brown from light pollution. On a moonlit night the sky goes faint blue and the land reads as cool silver. Stars only show up away from city lights. Artificial lights dominate the ground.",
  "clear night sky, deep navy blue, faint stars, subtle warm light-pollution glow on the horizon, scene lit by warm artificial lights, cool moonlit tones in the shadows"),
}
SHOW = ["sunset", "dusk"]  # Hunter 2026-10-21: only golden hour + blue hour matter
cards = []
for t, (title, sun, desc, prompt) in ((t, T[t]) for t in SHOW):
    imgs = "".join(f'''<figure><img src="picks/{t}_{k}_sun.jpg" loading="lazy"><img src="picks/{t}_{k}_away.jpg" loading="lazy">
<img class="strip" src="picks/{t}_{k}_strip.jpg" loading="lazy"><figcaption>{'★ best · ' if i==0 else ''}<b>{k}</b> · <a href="https://polyhaven.com/a/{k}">polyhaven</a></figcaption></figure>''' for i, k in enumerate(p[t]))
    cards.append(f'''<section id="{t}"><h2>{title} <span>{sun}</span></h2><p>{desc}</p>
<div class="prompt"><small>prompt language</small><code>{prompt}</code></div><div class="grid">{imgs}</div></section>''')
nav = " · ".join(f'<a href="#{t}">{T[t][0]}</a>' for t in SHOW)
html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sky Library</title><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>:root{{--bg:#0e1013;--fg:#e8ecf0;--mut:#8b95a1;--acc:#61a8d8;--card:#171a1f}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 Poppins,sans-serif}}main{{max-width:1500px;margin:auto;padding:24px 16px}}
h1{{font-weight:600;margin:0}}nav{{margin:8px 0 24px;color:var(--mut)}}a{{color:var(--acc)}}
section{{margin:48px 0}}h2{{font-weight:600;margin:0 0 6px}}h2 span{{color:var(--mut);font-weight:400;font-size:.7em;margin-left:8px}}
p{{max-width:900px;color:#c9d1d9}}.prompt{{background:var(--card);border-left:3px solid var(--acc);padding:10px 14px;margin:12px 0 18px;max-width:900px}}
.prompt small{{display:block;color:var(--mut);text-transform:uppercase;letter-spacing:.08em;font-size:11px}}code{{font-family:inherit;user-select:all}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}figure{{margin:0;background:var(--card);padding:6px;border-radius:6px}}
figure img{{width:49.4%;display:inline-block}}figure img.strip{{width:100%}}figcaption{{font-size:12px;color:var(--mut);padding:4px 2px}}figcaption b{{color:var(--fg);font-weight:600}}</style></head>
<body><main><h1>Sky Library</h1><p>Real skies from 299 Poly Haven HDRIs (CC0), rendered as the camera actually sees them. Each card shows three views: looking toward the sun (left), sun behind the camera (right), and a 360° strip of the 0–40° band. Blue hour includes dawn skies: the sky looks the same with the sun 0–8° below the horizon either side of the night. Other times of day stay in times.json and sheets/. Use these images as AI references and the prompt lines as wording.</p>
<nav>{nav}</nav>{"".join(cards)}</main></body></html>'''
open("index.html", "w").write(html)
json.dump({t: {"title": v[0], "sun": v[1], "look": v[2], "prompt": v[3]} for t, v in T.items()}, open("times.json", "w"), indent=1)
