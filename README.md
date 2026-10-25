# Sofia's games

Small learning games for Sofia (3½), in Russian and Latvian, made to run in Safari on an iPad.

- `index.html` – game menu
- `jungle/` – София в джунглях: tap the bush, meet an animal, hear its sound and its name. There are 20 animals (jungle and farm); each game picks 6 at random. After each animal a red mic button appears next to Sofia: one tap records her for 3 seconds and plays it straight back (nothing is saved).

- `letters/` – Буквы · Burti: Russian or Latvian letters (one alphabet per game, each with its own colour). Sofia asks «Где буква М?» / «Kur ir burts M?» and three balloons float up; tapping the right one pops it and shows a card with a name («М — Миша!», «С — София!» with Sofia's own face; a simple word where no common name fits, e.g. Ц — цветок). After a quiet pause the right balloon starts to shake a little as a hint. A wrong tap wobbles the balloon and Sofia asks again; after two wrong tries, or 14 seconds without a tap, the right balloon glows. A letter she mixed up comes back later in the same game. Look-alike letters (Е/Ё, И/Й, A/Ā, S/Š…) never appear in the same round. 10 letters per game, then a sticker page. «Азбука» / «Ābece» opens every letter with its picture and name. Pictures are emoji. Letter data is the `RU`/`LV` arrays at the top of the script; a letter can have several names (В: Вероника, Ваграм), one is picked at random.
- `songs/` – Песенки · Dziesmiņas: picture karaoke on a little stage. Five traditional songs (Bingo, Old MacDonald, Finger Family, Baby Shark, Twinkle Twinkle), in English. The words are shown as pictures with the words under them for grown-ups, a ball hops from word to word and Sofia sings along. In Old MacDonald, Finger Family and Baby Shark she picks who comes next from big pictures (farm animals make their real sounds from `jungle/audio/`; one finger is "Sofia finger"). In Bingo the letters turn into claps, one more each verse. A singing voice sings every verse with its words (`songs/voice/`, one MP3 per verse, made with SoulX-Singer; see `songs/voice/CREDITS.txt`), and the band plays live in the browser (Web Audio) in time with it. The voice files start 0.5 s before the first note; if one is missing, that verse plays with the band only. 🎤 records her singing during the song and plays it back at the end; the recording stays on the device and is never uploaded. Songs are the `SONGS` table at the top of the script: words, notes, beats and chords per line.

Sofia walks through the jungle as a cartoon girl (inline SVG in `jungle/index.html`) drawn after her portrait `jungle/sofia.png`: round cheeks, side-swept bangs, a top-knot curling right. Her hair color is the `.hair` fill in the CSS.

## Family voices

The game speaks only with recorded family voices, no robot voice.

- On the start screen, press and hold the microphone button (top right) for about a second to open the recording page.
- The first time on a device, enter the family code (kept on the server in `family-key.txt`, see below).
- Record each word and each animal sound. Recordings are saved on the server, so clearing Safari data or switching devices doesn't lose them. A new take replaces the old one, but the old one is archived: «Вернуть» brings it back. «Удалить» archives too.
- Real animal sounds from Wikimedia Commons are in `jungle/audio/` (`<animal>-sound.mp3`, credits in `jungle/audio/CREDITS.txt`). The snake, gorilla and crocodile sounds are generated. A family recording of a sound replaces the real one.
- Backup option: put audio files in `jungle/audio/`, named after the clip, e.g. `monkey-ru.m4a`, `monkey-lv.m4a`, `monkey-sound.m4a`, `greet-ru.m4a`, `end-lv.m4a`. A family recording takes priority over a file.

The letters game talks with a computer voice (Piper, CC0 voices; see `letters/audio/CREDITS.txt`). Holding the mic button on its start screen opens «Голоса для букв», where each phrase can be replaced by a family recording, stored on the same voice server (keys start with `abc-`).

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
