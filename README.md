# Sofia's games

Small learning games for Sofia (3½), in Russian and Latvian, made to run in Safari on an iPad.

- `index.html` – game menu
- `jungle/` – София в джунглях: tap the bush, meet an animal, hear its sound and its name. There are 12 animals; each game picks 6 at random. After each animal a red mic button appears next to Sofia: one tap records her for 3 seconds and plays it straight back (nothing is saved).

Sofia walks through the jungle as a cartoon girl (inline SVG in `jungle/index.html`) drawn after her portrait `jungle/sofia.png`: round cheeks, side-swept bangs, a top-knot curling right. Her hair color is the `.hair` fill in the CSS.

## Family voices

The game speaks only with recorded family voices, no robot voice.

- On the start screen, press and hold the microphone button (top right) for about a second to open the recording page.
- Record each word and each animal sound. Recordings are kept on that iPad.
- Real animal sounds from Wikimedia Commons are in `jungle/audio/` (`<animal>-sound.mp3`, credits in `jungle/audio/CREDITS.txt`). The snake, gorilla and crocodile sounds are generated. A family recording of a sound replaces the real one.
- Backup option: put audio files in `jungle/audio/`, named after the clip, e.g. `monkey-ru.m4a`, `monkey-lv.m4a`, `monkey-sound.m4a`, `greet-ru.m4a`, `end-lv.m4a`. A recording made on the iPad takes priority over a file.

## Publishing

GitHub Pages: Settings → Pages → Deploy from a branch → `main` / root.
On the iPad, open the site in Safari and choose Share → Add to Home Screen.
