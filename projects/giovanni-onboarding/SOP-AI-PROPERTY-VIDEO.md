# SOP — AI Property Stills + Video (Vision style)

Hey Giovanni, we would really like you to have a go at making these, here is a SOP for what im about to explain thank you,

This a reference website for a company that does real estate video and property development, they primary are really good at incorporating AI (Artificial Intelligence) into their videos and or making the videos completely from AI and its really smooth and concise,

https://visioncinemahomes.com/

I would like you to go through this and digest everything about this website and take notes on what makes them so good and how they do it.

After that the link to their instagrams are

* https://www.instagram.com/visionstudios.au/?hl=en Which is the Primary Instagram (Vision Studio)
* https://www.instagram.com/visioncinemahomes/?hl=en is the Goldcoast Brisbane Based Agency instagram

Please go watch all the videos they have in their instagram, they dont have many so it wont take you very long to, take a couple of notes on cool shots you see and would like to replicate.

The rest of this is what to look for while you watch, the tools and the rules I have found on how this kind of video gets made, and a small test at the end so you can try it yourself. If any part of this is not clear, please just ask me and I will explain it again in a different way.

---

## 1. What we are trying to make

Most of it is not filmed with a camera.

An architect has 3D renders of a house that is not built yet. Those renders look flat and grey. You can tell they came from a computer.

We want to take one of those renders and make it look like a real photo, taken by a real photographer in a real room. Then we want to make that photo move for 3 to 5 seconds. Then we cut a few of those clips together into a video.

So the steps would be:

1. A render arrives
2. We make it look real. Same room, same camera angle, just believable
3. We turn that image into a short clip
4. We cut the clips together

One important thing. We are not designing a new house. The building must stay exactly as the architect drew it. We only change the light, how real it looks, and how the camera moves. If a window moves to a different place, or a benchtop changes shape, we cannot use that image. Even if it looks beautiful.

## 2. Phase 1, the research (please do this first)

Spend a couple of hours on the website and the two Instagram pages.

I do not need a summary of what they sell. I can read that myself. I want to understand how the videos are built. So while you watch, write down these things.

**About the shots**

* How does the camera move? Slow push in, slow pull back, rise up, slide sideways, or a reveal from behind a wall or a plant. Write the move, not just "nice shot"
* How long is the shot before it cuts? They look short to me. Please count them
* What do you see in the first frame, and what do you see in the last frame? I think many AI clips are only a start frame and an end frame. If you can see those two frames, you understand how the shot was made
* What time of day is it? To me, most of the good ones look like late afternoon or dusk. See if you agree
* Are there people in the shot? If yes, how are they used? It looks like a person walking past, or a hand doing something small. Never a face acting
* Are there small detail shots? Water moving, a curtain, light on a benchtop, a plant in the wind. I think these are what make it feel like a film and not a slideshow. Tell me what you think

**About the edit**

* How does one shot join the next one? A normal cut, or does the movement continue through the cut?
* The sound. Only music? Or also background sound like birds and water? Or a voice?
* Is there text on screen? When does it appear, and how long does it stay?
* The colour. Warm or cold? Strong contrast or soft? Are the shadows blue or black?

**What I would like from you**

One document. It does not need to look nice.

For each video: the link, how many shots it has, then one line for each shot, like this:

`slow push in, kitchen towards window, 4 seconds`

At the end, choose the 5 or 6 shots you like most and want to try to make yourself. Write one sentence for each one about why you think it works.

Please send me that document before you make anything. Then we will look at it together and choose which shots you try. I am interested in what you see, you may notice things I did not.

## 3. Phase 2, the images

The tool for this is Higgsfield. I will give you access. Please do not pay for anything yourself. And please only run generations on the files I give you, because every generation costs money from our account.

There are two different jobs, and each one needs a different model:

* **Make a render look real. Same room, nothing moved.** Use **Seedream 4.5**. This one stays close to the image you give it. That is what we want for someones render
* **Put furniture in an empty room, or change the style of a room.** Use **Nano Banana Pro**. This one is more creative. Good for furniture, bad for architecture

Before you start, check the size of the image so you use the right aspect ratio. A 16:9 image must be generated as 16:9. A square image as 1:1. If this is wrong the image comes back stretched or cropped, and the generation is wasted.

### How to write the prompt

This part decides if it works, so please read it twice.

**Describe the finished photo. Write it like the photo already exists.**

Do not write instructions. Try not to use the words "dont", "remove", "keep" or "avoid". These models do not understand "no" very well. If you write "no plates on the bench", you often get plates on the bench.

Not like this:

> make this render look realistic, dont change the kitchen, remove the grey look

Better like this:

> Photorealistic luxury real estate photograph. Open plan kitchen, large stone topped island bench, integrated appliances, full height cabinetry, pendant lighting over the island, floor to ceiling windows, natural light. Warm timber joinery, white plaster walls, blonde oak flooring. Identical camera angle. High resolution.

You can see the shape of it. Room, materials, light, floor, then camera angle. Nouns and materials, no instructions.

Other rules:

* **One job per prompt.** You want it photoreal, and you want a new sky, and you want a sofa added? That is three separate passes. Not one sentence with three jobs. The more you ask for at one time, the more the model changes other things
* **Always generate from the original file.** Do not put an AI result back in for a second try. It becomes soft and blurry each time. If something is wrong, go back to the original file and change the words
* **Short and simple works better than long and detailed**
* **Always finish with "Identical camera angle. High resolution."**
* **Use the same words for every room in the same house.** If one prompt says warm afternoon and the next says bright midday, the clips will not match when we edit them

### One thing to be careful with

Please do not run a full frame generation on a drone shot, or on a wide photo of the outside with a lot of small detail.

Full frame means the model rebuilds every pixel. So it also rebuilds the roofs, the fences and the neighbours houses. The result is always wrong.

For those images, we cover everything except the part we want to change (this is called a mask), so only that part is rebuilt. If you get an image like this and you are not sure, please ask me first.

Same for real photos, not renders. A real photo should not be fully regenerated. It needs a mask, or an upscale. Full frame generation is only for renders.

## 4. Phase 3, making it move

When a still image is approved, that image becomes the first frame of a clip. Kling is the tool for the video.

Keep the camera moves slow and simple. Slow looks expensive.

* Slow push in, through a door or towards a window
* Slow pull back, to show the whole room
* Slow rise, the camera lifts up
* Slow slide, left or right, past something close to the camera
* Small detail movement. Water, curtains, light changing

Rules:

One move per clip.

If the camera pushes in and pans and tilts at the same time, it looks like a video game
3 to 5 seconds.

Longer than that and the model starts inventing things and the room bends
Nothing solid can move.

Walls, benches, windows, taps. All fixed. If a wall bends or a bench melts, we cannot use that clip. 

Please do not hide it in the edit. Tell me and we run it again

Make two or three versions of the important shots.** Some will come back broken. That is normal

## 5. Files and names

Please use this structure from the beginning:

```
CLIENT NAME /
  PROPERTY ADDRESS /
    01_ORIGINALS      the renders as they arrived. Never edited, never renamed
    02_AI_IMAGES      your generated images
    03_VIDEO          your clips
    04_DELIVERED      only the final selected files
```

File names like this: `address_room_shotnumber_version`

Example: `28-smith-st_kitchen_01_v2.jpg`

No spaces. All lower case. Always keep the version number at the end.

Please never edit or rename the files in 01_ORIGINALS. Those are the original files. If we lose them, we cannot make anything again.

## 6. Check this before you send it to me

* Open every file. Make sure none are broken
* Put your image next to the original and zoom to 100%. Is it the same room? Same windows, same benchtop, same doors, same view outside? I think this check finds most of the problems, so please really do it
* Is the light the same across all the images? Or does one room look like a different time of day?
* Look for melted taps, bent door frames, extra lights, strange reflections, plants growing from nothing
* On the clips, watch the last second. That is usually where it breaks
* Then send me everything, with a short note about which files you are not happy with and why. I would much rather you tell me "shot 4 is soft" than me find it later

## 7. The test

When your research document arrives, I will send you 2 renders.

For each render I would like:

1. One photoreal image. Same camera angle, nothing moved
2. One clip of 3 to 5 seconds made from that image. One camera move only

So four files. Plus a few sentences about what was difficult, or what did not work.

Please take your time. I am not timing you. I want to see how you think about it, not how fast you are.

## 8. Please ask me instead of guessing

Ask me any time, it is never a problem:

* You have a drone shot, or a wide photo of the outside
* The file is a real photo and not a render
* You are about to run many generations on the same image
* There is something in the render and you do not know what it is
* Something failed two times. Please do not try a third time. Send me the result and the words you used, and we look at it together

Thank you Giovanni. Please take your time with the research part, I think that is the most valuable part of all of this. When you understand why their shots work, the rest is mostly repetition.
