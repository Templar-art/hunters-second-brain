# SOP — AI Property Stills + Video (Vision style)

Hey Giovanni, we would really like you to have a go at making these, here is a SOP for what im about to explain thank you,

This a reference website for a company that does real estate video and property development, they primary are really good at incorporating AI (Artificial Intelligence) into their videos and or making the videos completely from AI and its really smooth and concise,

https://visioncinemahomes.com/

I would like you to go through this and digest everything about this website and take notes on what makes them so good and how they do it.

After that the link to their instagrams are

* https://www.instagram.com/visionstudios.au/?hl=en Which is the Primary Instagram (Vision Studio)
* https://www.instagram.com/visioncinemahomes/?hl=en is the Goldcoast Brisbane Based Agency instagram

Please go watch all the videos they have in their instagram, they dont have many so it wont take you very long to, take a couple of notes on cool shots you see and would like to replicate.

Below is the rest of it, what to look for while you are watching, the tools and the rules I have gathered on how this sort of thing gets made, and a small test at the end so you can have a go yourself.

---

## 1. What we are trying to make

The idea is that most of it is not filmed. An architect or a developer has 3D renders of a house that is not built yet, and those renders are usually flat and grey and obviously computer made. What we want to be able to do is turn one of those into an image that looks like a real photographer stood there with a real camera, and then bring that image to life as a short moving clip, and then cut a few of those clips together into a video.

So the order would be:

1. A render (or a photo) comes in
2. Make it look photoreal, same room, same camera angle, just believable
3. Animate that finished image into a 3 to 5 second clip
4. Cut the clips together into the video

One thing to have in your head the whole way through: we are not designing a new house. The building has to stay exactly as the architect drew it. We are only changing how it is lit and how real it looks and how the camera moves. If a window ends up in a different spot, or the benchtop changes shape, that image is no good to us no matter how nice it looks.

## 2. Phase 1, the research (please do this first)

Give yourself a couple of hours on the website and the two Instagrams. What I am after is not a summary of what they sell, I can read that myself. I want to work out how the videos are actually built. So while you watch, note down:

**On the shots themselves**

* How the camera moves. Is it a slow push in, a slow pull back, a rise up, a slide sideways, a reveal from behind a wall or a plant. Write down the move, not just "nice shot"
* How long each shot is before it cuts. Most of theirs look short to me, count them properly
* Where the shot starts and where it ends. I think a lot of AI clips are just a start frame and an end frame, so if you can work out what those two frames were you have basically reverse engineered the shot
* What time of day it is. It looks to me like most of the good ones are warm late afternoon or dusk, see if that holds up
* Whether there are people in the shot, and if so how they are used. Looks like mostly a person walking through frame or a hand doing something small, never a face doing acting
* The little detail shots. Water moving, a curtain, light across a benchtop, a plant in the breeze. I have a feeling these are what stop it feeling like a slideshow, see what you think

**On the edit**

* How they get from one shot into the next. Straight cut, or a match cut where the movement carries through
* The sound. Music only, or is there ambience like birds and water underneath, or a voice over
* Any text on screen, when it comes in, how long it stays
* The colour. Warm or cool, is it contrasty, are the shadows blue or black

**What I would like back from you**

One document, it doesnt need to be pretty. For every video you watch: the link, roughly how many shots are in it, then a line per shot in the format "camera move, what is in frame, how long". Then at the bottom, the 5 or 6 shots you reckon are the best and would like to have a go at recreating, and one sentence each on why you think that shot works.

Send that through before you start making anything, and we will go through it together and pick which ones you try. Honestly I am interested in what you see in them, you might pick up things I have missed.

## 3. Phase 2, the images

The tool we would be using is Higgsfield. I will sort out your access to it, please dont pay for anything yourself, and please dont run generations on anything outside of what I have given you, because every generation costs money off our account.

From what I understand there are two different jobs and they want two different models:

* **Making a render look real, same room, nothing moved.** Seedream 4.5. This one sticks closely to the image you give it, which is what we want on someones render
* **Putting furniture into an empty room, or restyling a room.** Nano Banana Pro. This one is more creative, which is good for furniture and bad for architecture

Before you run anything, check the size of the source image so you can set the right aspect ratio. A 16:9 image has to be generated as 16:9, a square as 1:1, otherwise it comes back stretched or cropped and the generation is wasted.

### Writing the prompt

This seems to be the part that decides whether it works, so read it twice.

**Describe the finished photo, like you are describing a photo that already exists.** Dont write instructions, and try to avoid the words "dont", "remove", "keep" and "avoid". These models dont really deal with no. If you write "no clutter on the bench" you can easily end up with clutter on the bench.

So not this:

> make this render look realistic, dont change the kitchen, remove the grey look

More like this:

> Photorealistic luxury real estate photograph. Open plan kitchen, large stone topped island bench, integrated appliances, full height cabinetry, pendant lighting over the island, floor to ceiling windows, natural light. Warm timber joinery, white plaster walls, blonde oak flooring. Identical camera angle. High resolution.

The rest of what goes with it:

* **One job per prompt.** If you want it photoreal and you also want the sky changed and you also want a sofa added, thats three passes, not one sentence with three jobs in it. The more you ask for at once the more it takes liberties with the rest of the frame
* **Always generate from the original file.** Dont feed an AI output back in for a second go, it gets softer and mushier each time. If something is wrong, go back to the original and change the prompt
* **Short and dense seems to beat long and careful.** Materials, light, floor, camera angle
* **End with "Identical camera angle. High resolution."** every time
* **Use the same wording across every room in the one house.** If one prompt says warm afternoon and the next says bright midday, the clips wont cut together at the end

### The one I would really like you to be careful with

Please dont run a full frame generation on a drone shot or a wide exterior with a lot of fine detail in it. It regenerates every single pixel, so it rebuilds the roofs and the fences and the neighbours houses, and it comes back looking wrong. On those, the sky or whatever you are fixing should be masked so only that part gets regenerated. If you get one of those and you are not sure, ask me first rather than guessing.

Same with real photos rather than renders. A real photo shouldnt get fully regenerated, it wants a masked fix or an upscale. Full frame generation is for renders.

## 4. Phase 3, making it move

Once a still is signed off, that still becomes the first frame of a clip. Kling is the one for the video side. Keep the moves slow and boring, that seems to be what makes it look expensive:

* Slow push in through a doorway or towards a window
* Slow pull back to reveal the room
* Slow rise, camera lifting up
* Slow slide left or right past something in the foreground
* Small detail moves, water, curtains, light shifting

What to stick to:

* One move per clip. A camera that pushes in and pans and tilts all at once looks like a video game
* 3 to 5 seconds. Longer than that and it starts inventing things and the room warps
* Nothing structural can move. Walls, benches, windows, taps, all fixed. If a wall bends or a bench melts thats a reject, dont try and hide it in the edit, tell me and we will run it again
* Make a couple of versions of the shots that matter. I expect some will come back broken, so options are better than one go

## 5. Files, naming and delivery

Lets keep it in this shape from the start, it will get messy fast otherwise:

```
CLIENT NAME /
  PROPERTY ADDRESS /
    01_ORIGINALS      the renders as they were sent, never touched, never edited
    02_AI_IMAGES      your generated stills
    03_VIDEO          your clips
    04_DELIVERED      the final selects only
```

Naming: `address_room_shotnumber_version`, so `28-smith-st_kitchen_01_v2.jpg`. No spaces, all lower case, keep the version number on the end.

Please dont rename or edit anything in 01_ORIGINALS. Thats the source of truth, and if it gets lost we cant go back and redo anything.

## 6. Before you send anything over

* Open every file and make sure none of them are corrupt
* Put the output next to the original and zoom in to 100%. Is it still the same room. Same windows, same benchtop, same doors, same view outside. I think this is the check that catches most of the problems, so please actually do it
* Is the light consistent across the set, or does one room look like a different time of day
* Melted taps, bent door frames, extra light fittings, strange reflections, plants growing out of nothing
* On the clips, check the last second, thats usually where it falls apart
* Then send me the lot with a short note on which ones you are not happy with and why. I would much rather hear "shot 4 is soft" from you than find it myself

## 7. The test

Once your research notes come through, I will send you 2 renders. For each one I would like:

1. One photoreal still, same camera angle, nothing moved
2. One 3 to 5 second clip made from that still, one camera move only

So four files, plus a couple of sentences on what you found hard or what didnt work. Take your time with it, I am not timing you, I am more interested in how you think about it than how fast you are.

## 8. Ask me rather than guessing

Please ask, it is never annoying:

* You have been given a drone shot or a wide exterior
* The source is a real photo rather than a render
* You are about to run a lot of generations on the same image
* Theres something in the render you cant identify
* Something has failed twice. Dont go for a third, send me what you have and the prompt you used and we will look at it together

Thank you Giovanni. Take your time on the research part, I think thats honestly the most valuable bit of this. Once you have an eye for why their shots work the rest of it is mostly repetition.
