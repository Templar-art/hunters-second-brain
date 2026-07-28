# SOP — AI Property Stills + Video (Vision style)

Hey Giovanni, we would really like you to have a go at making these, here is a SOP for what im about to explain thank you,

This a reference website for a company that does real estate video and property development, they primary are really good at incorporating AI (Artificial Intelligence) into their videos and or making the videos completely from AI and its really smooth and concise,

https://visioncinemahomes.com/

I would like you to go through this and digest everything about this website and take notes on what makes them so good and how they do it.

After that the link to their instagrams are

* https://www.instagram.com/visionstudios.au/?hl=en Which is the Primary Instagram (Vision Studio)
* https://www.instagram.com/visioncinemahomes/?hl=en is the Goldcoast Brisbane Based Agency instagram

Please go watch all the videos they have in their instagram, they dont have many so it wont take you very long to, take a couple of notes on cool shots you see and would like to replicate.

Below is the rest of it, the detail on what to look for, how we actually make this stuff, and a small test job at the end so you can have a go yourself.

---

## 1. What we are actually doing here

Most of the work is not filming. A developer or an architect sends us their 3D renders, which are usually flat and grey and obviously computer made. Our job is to turn those into images that look like a real photographer stood there with a real camera, and then bring those images to life as short moving clips that we cut into a video.

So the order is always the same:

1. Client render (or a real photo) comes in
2. We make it photoreal, same room, same camera angle, just believable
3. We animate that finished image into a 3 to 5 second clip
4. We cut the clips together into the final video

The most important thing to understand before you start: we are not designing a new house. The building stays exactly as the architect drew it. We are only changing how it is lit, how real it looks, and how the camera moves. If a client sees his window in a different spot he will never send us work again.

## 2. Phase 1, the research (do this first)

Give yourself a couple of hours on the website and the two Instagrams. What I want out of this is not a summary of what they sell, I can read that myself. I want you to work out how the videos are built. So while you watch, note down:

**On the shots themselves**

* How the camera moves. Is it a slow push in, a slow pull back, a rise up, a slide sideways, a reveal from behind a wall or a plant. Write down the move, not just "nice shot"
* How long each shot is before it cuts. Most of theirs are short, count them
* Where the shot starts and where it ends. A lot of AI clips are just a start frame and an end frame, if you can see what those two frames were you have basically reverse engineered the shot
* What time of day it is. Almost everything good is either warm late afternoon or dusk, notice how often they use it
* Whether there are people in the shot, and if so how they are used. Usually a person walking through frame or a hand doing something small, never a face doing acting
* The little detail shots. Water moving, a curtain, light across a benchtop, a plant in the breeze. These are the glue that make a video feel like film instead of a slideshow

**On the edit**

* How they get from one shot to the next. Straight cut, or a match cut where the movement carries through
* The sound. Is it music only, is there ambience like birds and water underneath, is there a voice over
* Any text on screen, when it appears, how long it stays
* The colour. Is it warm, is it contrasty, are the shadows blue or are they black

**What I want back from you**

One document, doesnt need to be pretty. For every video you watch: the link, roughly how many shots are in it, and then a line per shot in the format "camera move, what is in frame, how long". Then at the bottom, a list of the 5 or 6 shots you personally think are the best and would like to have a go at recreating, and one sentence each on why that shot works.

Send that to me before you start making anything. Once we have both looked at the same list we will pick which ones you try.

## 3. Phase 2, how we make the images

We use Higgsfield for this. I will sort out your access, do not pay for anything yourself and do not spend credits on anything outside of the job I have given you, every generation costs money and it comes out of our account.

Two different jobs, two different models:

* **Making a render look real, same room, nothing moved.** Use Seedream 4.5. This one respects the original image very closely which is exactly what we want on a clients render
* **Putting furniture into an empty room, or restyling a room.** Use Nano Banana Pro. This one is more creative, which is good for furniture and bad for architecture

Before you run anything, check the size of the source image so you can set the right aspect ratio. A 16:9 image must be generated as 16:9, a square as 1:1. If you get this wrong the image gets stretched or cropped and it is wasted.

### How to write the prompt

This is the part people get wrong, so read it twice.

**Describe the finished photo, as if you are describing a photo that already exists.** Do not write instructions and do not use the words "dont", "remove", "keep" or "avoid". The model does not really understand no. If you write "no clutter on the bench" you often get clutter on the bench.

So not this:

> make this render look realistic, dont change the kitchen, remove the grey look

This:

> Photorealistic luxury real estate photograph. Open plan kitchen, large stone topped island bench, integrated appliances, full height cabinetry, pendant lighting over the island, floor to ceiling windows, natural light. Warm timber joinery, white plaster walls, blonde oak flooring. Identical camera angle. High resolution.

The other rules that go with it:

* **One job per prompt.** If you want it photoreal and you also want the sky changed and you also want a sofa added, that is three passes, not one sentence with three jobs in it. Every extra job you add makes the model take liberties with the rest of the frame
* **Always generate from the original file.** Never feed an AI output back in for a second go. It gets softer and mushier every time. If a result is wrong, go back to the original and fix the prompt
* **Short and dense beats long and careful.** Materials, light, floor, camera. Thats it
* **Always end with "Identical camera angle. High resolution."** Every single time
* **Same wording across every shot in a house.** If one room says warm afternoon light and the next says bright midday, the video will not cut together

### The one thing you must never do

Do not run a full frame generation on a drone shot or a wide exterior with a lot of fine detail in it. It regenerates every pixel, which means it rebuilds the roofs and the fences and the neighbours houses, and it always comes back looking wrong. On those, the sky or whatever you are fixing gets masked and only the masked part is regenerated. If you get given a drone wide and you are not sure, ask me first, dont guess.

Same goes for real photos, not renders. A real photo we shot does not get fully regenerated, it gets fixed in a masked way or upscaled. Full frame generation is for renders.

## 4. Phase 3, how we make it move

Once a still is approved, that still becomes the first frame of a clip. We use Kling for the video. Keep the moves boring and slow, that is what makes it look expensive:

* Slow push in through a doorway or towards a window
* Slow pull back to reveal the room
* Slow rise, camera lifting up
* Slow slide left or right past a foreground object
* Small detail moves, water, curtains, light shifting

Rules for the clips:

* One move per clip. A camera that pushes in and pans and tilts looks like a video game
* 3 to 5 seconds. Anything longer and the AI starts inventing things and the room warps
* Nothing structural is allowed to move. Walls, benches, windows, taps, all fixed. If the clip bends a wall or a bench melts, that clip is a reject, do not try to hide it in the edit, we will re run it
* Generate a couple of versions of the important shots. Some come back broken, that is normal, thats why we always make options

## 5. Files, naming and delivery

Keep it in this shape, it matters more than you think when there are 80 files:

```
CLIENT NAME /
  PROPERTY ADDRESS /
    01_ORIGINALS      the clients renders, never touched, never edited
    02_AI_IMAGES      your generated stills
    03_VIDEO          your clips
    04_DELIVERED      the final selects only
```

Naming: `address_room_shotnumber_version`, for example `28-smith-st_kitchen_01_v2.jpg`. No spaces, all lower case, keep the version number.

Never rename or edit anything in 01_ORIGINALS. That folder is the source of truth and if we lose it we cannot redo anything.

## 6. Check this before you send me anything

* Open every file, make sure none of them are corrupt
* Put the output next to the original and zoom to 100%. Is the room still the same room. Same windows, same benchtop, same doors, same view outside. This is the check that catches the problems, please actually do it
* Is the light consistent across the whole set, or does one room look like a different time of day
* Any melted taps, bent door frames, extra light fittings, weird reflections, hands or plants growing out of nothing
* Do the clips have any warping in the last second, thats usually where it falls apart
* Then send me the whole set with a short note on which ones you are not happy with and why. I would much rather hear "shot 4 is soft" from you than find it myself

## 7. The test job

Once you have sent me your research notes, I will send you 2 renders. For each one I would like:

1. One photoreal still, same camera angle, nothing moved
2. One 3 to 5 second clip made from that still, one camera move only

Four files total, plus a couple of sentences on what you found hard. Take your time on it, I am not timing you, I want to see how you think about it more than how fast you are.

## 8. When to ask me instead of guessing

Please ask, it is never annoying:

* You have been given a drone shot or a wide exterior
* The source is a real photo and not a render
* You are about to run more than a handful of generations on the same image
* The client render has something in it you cannot identify
* Something has failed twice. Dont go for the third try, send me what you have and what you prompted, and I will look at it with you

Thank you Giovanni, take your time with the research part, that is honestly the most valuable bit. Once you have an eye for why their shots work the rest of it is just repetition.
