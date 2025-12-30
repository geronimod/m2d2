:set -XOverloadedStrings
:set prompt ""
:set prompt-cont ""

import Sound.Tidal.Context

-- start SuperDirt connection
(tidal, tidalStream) <- startStream
  (superdirtTarget { oLatency = 0.1
                   , oAddress = "127.0.0.1"
                   , oPort    = 57120 })
  (defaultConfig { cFrameTimespan = 1/20 })

-- create the pattern aliases (d1, d2, etc.)
let
  d1  = streamReplace tidal 1
  d2  = streamReplace tidal 2
  d3  = streamReplace tidal 3
  d4  = streamReplace tidal 4
  d5  = streamReplace tidal 5
  d6  = streamReplace tidal 6
  d7  = streamReplace tidal 7
  d8  = streamReplace tidal 8
  d9  = streamReplace tidal 9
  d10 = streamReplace tidal 10

  -- some common utilities
  hush = streamHush tidal
  list = streamList tidal
  mute = streamMute tidal
  unmute = streamUnmute tidal
  solo = streamSolo tidal
  unsolo = streamUnsolo tidal
  once = streamOnce tidal
  nudgeAll = streamNudgeAll tidal
  all = streamAll tidal
  resetCycles = streamResetCycles tidal
  setcps = asapTidal tidal . cps
  getcps = streamGetcps tidal
  getnow = streamGetnow tidal

  -- MIDI friendly tempo
  setbpm bpm = setcps (bpm / 120)

default (Pattern String, Integer, Double)
