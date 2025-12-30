import { pattern } from "@strudel/core";
import pkg from "@tonejs/midi";
import fs from "fs";

const { Midi } = pkg;
const p = pattern("0 3 5 7").take(16);

const midi = new Midi();
const track = midi.addTrack();
const bpm = 120;
const spb = 60 / bpm;

for (const ev of p.events()) {
  if (ev.value != null) {
    track.addNote({
      midi: 60 + ev.value,
      time: ev.time * spb,
      duration: ev.duration * spb,
    });
  }
}

fs.writeFileSync("melody.mid", Buffer.from(midi.toArray()));
console.log("✅ Exported melody.mid");
