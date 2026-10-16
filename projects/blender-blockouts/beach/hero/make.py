import json
KEY=("Image 2 is a flat colour label map of the same frame and is only a key: none of its flat colours appear in the photograph. "
"Wherever Image 2 is red the surface is warm spotted-gum timber; blue is clear turquoise pool water; light grey is smooth off-white honed concrete; white is crisp white render; "
"cyan is floor-to-ceiling low-iron glass in slim black frames reflecting sky with warm lived-in interiors visible through it; black is slim charcoal steel and bronze metalwork; "
"navy is the deep blue-green Pacific Ocean with rolling swell; pale lilac is white breaking surf and foam; yellow is pale golden Gold Coast beach sand; ochre is wet compacted sand at the waterline; "
"green is lush buffalo lawn and soft dune grass; dark green is tropical foliage; teal is a clipped dense hedge; brown is palm trunks and tree bark; magenta is linen upholstery, cushions and soft furnishings in natural white, sand and oatmeal tones; "
"orange is honed stone benchtops and white porcelain; dark grey is asphalt road; near-black is a switched-off wall-mounted screen; purple marks a real person.")
FR=("Keep the exact camera position, lens, crop and horizon of Image 1 with no zoom or re-crop, and every building, object and person exactly where it sits in Image 1.")
LOOK=("Bright clear Gold Coast morning sun, soft natural shadows, clean blue sky with light coastal haze, bright and airy, true-to-life colour, magazine-grade editorial architectural photography, "
"real photograph on a real camera, no CGI, no render look, no text, no watermark.")
S={
"01_surf":("A low drone photograph skimming just above the rolling surf of a Gold Coast beach looking toward a contemporary three-level beachfront home on the dunes between neighbouring white rendered homes, palms and dune grass along the beachfront.",["A","B"],"Far down the beach the two people in purple are the man and woman from the attached cast references walking together along the wet sand, small in frame."),
"02_pool":("An eye-level photograph gliding beside the infinity pool of a contemporary three-level Gold Coast beachfront home, timber deck, outdoor dining under the balcony, white sun loungers, umbrella, glass pool fence, lawn and dune path.",["B","D","C"],"The purple figures are real people from the attached cast references: the woman in the ivory slip dress standing at the pool edge, the man in the navy linen shirt on the upper balcony, the woman in the cream knit top beside him at the balcony glass."),
"03_living":("An interior photograph of the open-plan upper living level of a contemporary Gold Coast beachfront home looking through floor-to-ceiling glass to the ocean, kitchen island with bar stools, dining, sofa, shelving and plants.",["C"],"The purple figure behind the kitchen island is the woman in the cream knit top from the attached cast reference, relaxed, looking out to the ocean."),
"04_top":("A top-down drone photograph looking straight down onto a contemporary Gold Coast beachfront home roof with solar panels, the turquoise pool and timber deck below, palms, hedges and the beach beyond.",[],"Any purple marks are small real people seen from above."),
"05_walk":("An interior photograph looking through an open sliding glass door from the timber deck into the ground-floor lounge of a contemporary Gold Coast beachfront home, sofa facing a wall-mounted screen, bar with stools, floating timber stair, plants and art.",[],""),
"06_track":("A gimbal tracking photograph at chest height on a Gold Coast beach following a couple walking barefoot on the sand, beachfront homes, dune grass and palms behind them.",["A","B"],"The two purple figures are the man in the white linen shirt and the woman in the ivory slip dress from the attached cast references, mid-stride, relaxed and happy, natural candid moment."),
"07_car":("A low street-level photograph of a silver luxury supercar driving along a quiet coastal Gold Coast street lined with contemporary homes, palms and street lights, the car sharp and gleaming with a real modern hypercar design, wide low stance, full-width light bar, big alloy wheels.",[],""),
}
FRM={"01_surf":"0001","02_pool":"0193","03_living":"0385","04_top":"0577","05_walk":"0769","06_track":"1009","07_car":"1300"}
out={}
for k,(scene,cast,people) in S.items():
    p=f"Using Image 1 for the exact geometry, framing and layout, and Image 2 as the colour key for materials, create: {scene} {FR} {KEY} {people} {LOOK}"
    out[k]={"prompt":p,"guide":f"guides/shot_{FRM[k]}.png","id":f"id/id_{FRM[k]}.png","cast":[f"cast/outfit_{c}.png" for c in cast]}
json.dump(out,open("hero/jobs.json","w"),indent=1)
print(len(out))
