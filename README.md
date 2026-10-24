# Sofia's games

Small learning games for Sofia (3½), in Russian and Latvian, made to run in Safari on an iPad.

- `index.html` – game menu
- `jungle/` – София в джунглях: tap the bush, meet an animal, hear its sound and its name. There are 20 animals (jungle and farm); each game picks 6 at random. After each animal a red mic button appears next to Sofia: one tap records her for 3 seconds and plays it straight back (nothing is saved).

Sofia walks through the jungle as a cartoon girl (inline SVG in `jungle/index.html`) drawn after her portrait `jungle/sofia.png`: round cheeks, side-swept bangs, a top-knot curling right. Her hair color is the `.hair` fill in the CSS.

## Family voices

The game speaks only with recorded family voices, no robot voice.

- On the start screen, press and hold the microphone button (top right) for about a second to open the recording page.
- The first time on a device, enter the family code (kept on the server in `family-key.txt`, see below).
- Record each word and each animal sound. Recordings are saved on the server, so clearing Safari data or switching devices doesn't lose them. A new take replaces the old one, but the old one is archived: «Вернуть» brings it back. «Удалить» archives too.
- Real animal sounds from Wikimedia Commons are in `jungle/audio/` (`<animal>-sound.mp3`, credits in `jungle/audio/CREDITS.txt`). The snake, gorilla and crocodile sounds are generated. A family recording of a sound replaces the real one.
- Backup option: put audio files in `jungle/audio/`, named after the clip, e.g. `monkey-ru.m4a`, `monkey-lv.m4a`, `monkey-sound.m4a`, `greet-ru.m4a`, `end-lv.m4a`. A family recording takes priority over a file.

## Voice server

`server/voices.py` (Python, standard library only) stores the recordings, and Caddy proxies `/api/*` to it. Anyone can listen, but saving, deleting and restoring need the family code. Data lives outside the repo: `current/<key>.<ext>`, `history/<key>/` (the last 30 older takes per clip) and `family-key.txt`.

```
docker network create sofia && docker network connect sofia <caddy container>
docker run -d --name sofia-voices --restart unless-stopped --network sofia --user 1000:1000 \
  -v $PWD/server:/app:ro -v ~/sofia-voices:/data python:3.12-alpine python /app/voices.py
```

Without the server (e.g. on GitHub Pages) the game still works with the sound files and generated sounds, but recording isn't possible.

## Publishing

On the iPad, open the site in Safari and choose Share → Add to Home Screen.
