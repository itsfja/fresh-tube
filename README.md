# fresh-tube

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](fresh_tube.py)
[![Depends on](https://img.shields.io/badge/depends%20on-yt--dlp-orange)](https://github.com/yt-dlp/yt-dlp)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

### A Ladybird-style book about seeing what's new

---

## Page 1: Hello

*Picture: a person at a table with a computer. A friendly ladybird sits on the screen, watching videos.*

This is YouTube.

YouTube is a place where people put videos. Every day, millions of new videos arrive.

But YouTube does not show you all of them. YouTube picks some videos and says, "You will like these."

Maybe you will. Maybe you won't. Wouldn't you rather look for yourself?

This book is about a small program called **fresh-tube**.

---

## Page 2: The big pile

*Picture: an enormous pile of parcels. A tiny hand picks one out at random.*

Think of every video put on YouTube today as one enormous pile of parcels.

Most of the parcels have never been opened. Nobody has watched them yet.

YouTube only shows you the shiny parcels at the top of the pile.

fresh-tube digs into the pile and brings you parcels you have never seen.

It cannot bring you *all* of them — the pile is far too big. But it brings a good handful, chosen without anyone deciding for you.

---

## Page 3: The trick

*Picture: the ladybird with a magnifying glass, looking under everyday words like "the" and "how".*

How does fresh-tube find parcels in the pile?

It uses a trick. It asks YouTube a lot of very plain questions.

"Show me new videos with the word **the** in them."

"Show me new videos with the word **how** in them."

Nearly every video in the world has one of these little words somewhere in its name. So each plain question finds lots of fresh videos.

fresh-tube asks the question again and again with different words. Then it puts all the answers together and throws away the doubles.

---

## Page 4: The rubbish bin

*Picture: a wastepaper basket. In it: a singing star, a games controller, a cartoon rabbit, a megaphone, a politician's rosette, a film reel, a tiny blurry television.*

Not every parcel is worth opening. Some of them are things you did not ask for.

So fresh-tube has a rubbish bin, and it is very busy.

- Songs go in. Music videos, albums, singing stars.
- Games go in. Minecraft, Fortnite, people playing games.
- Children's cartoons go in.
- Adverts and silly spam go in.
- Bits of telly and films go in. Trailers and whole episodes.
- Politics and news go in.
- Very short videos go in. Very long ones too.
- Blurry, fuzzy videos go in.

Whatever is left goes into your basket.

The bin is not perfect. Sometimes a song sneaks past. When that happens, you can open the list in the program and add the word yourself. The bin learns.

---

## Page 5: Pressing Run

*Picture: a finger about to press a big button marked "go". A clock on the wall shows it is nearly bedtime.*

Before you start, you ask the computer for the helper:

```bash
pip install yt-dlp
```

Then you say the magic word:

```bash
python3 fresh_tube.py
```

fresh-tube gets to work. It asks YouTube one plain question after another. It takes a little nap between questions, so it never seems rude.

After a few minutes it says: **done**.

If you want a bigger handful of parcels, say:

```bash
python3 fresh_tube.py --words 50 --keep 100
```

---

## Page 6: The basket

*Picture: a woven basket full of photographs, all different. The ladybird points at one.*

When it is finished, fresh-tube has made you a basket in a folder called `out`.

- **links.txt** is a plain list of today's videos, all mixed up. Not sorted. Not chosen for you. Just found.
- **index.html** is a page of pictures you can open in your browser. Click a picture to watch.

Most of the videos are from very small rooms. One person, one camera, something they wanted to show you today. Hardly anybody has watched them yet.

Now you have.

---

## Page 7: Being gentle

*Picture: the ladybird holding up one wing, like a crossing guard.*

One last thing.

fresh-tube asks YouTube lots of questions, and YouTube is only so patient.

If you ask for hundreds and hundreds of words all at once, YouTube may say, "Are you a robot?" and stop for a rest.

So be gentle. Twenty-five words is plenty for one day.

There is no key, no password, no cost. The program is small and the licence is called MIT, which means you may look inside it, change it, and share it.

Happy digging.

---

## License

fresh-tube is licensed under the MIT license.
