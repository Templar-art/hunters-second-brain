-- Jarvis push-to-talk. Hold right-option: record. Release: transcribe -> answer.
-- Cmd+Alt+J toggles mute (TTS off, overlay stays).

local DIR = os.getenv("HOME") .. "/Documents/Hunters Second Brain/projects/jarvis/voice"
local WAV = "/tmp/jarvis-ask.wav"
local FFMPEG = "/opt/homebrew/bin/ffmpeg"
local RIGHT_OPT = 61

local recTask = nil
local busy = false

local function overlay(msg, secs)
  hs.alert.closeAll(0)
  hs.alert.show(msg, { textSize = 16, radius = 8 }, hs.screen.mainScreen(), secs or 4)
end

local function startRecording()
  if busy or recTask then return end
  os.remove(WAV)
  recTask = hs.task.new(FFMPEG, nil, {
    "-y", "-f", "avfoundation", "-i", ":default",
    "-ar", "16000", "-ac", "1", WAV,
  })
  recTask:start()
  overlay("🎙 Jarvis listening…", 120)
end

local function stopAndAsk()
  if not recTask then return end
  local pid = recTask:pid()
  if pid then hs.execute("kill -INT " .. pid) end
  recTask = nil
  busy = true
  overlay("… thinking", 120)
  -- small delay so ffmpeg finalises the wav before we read it
  hs.timer.doAfter(0.4, function()
    hs.task.new(DIR .. "/jarvis-ask.sh", function(code, stdout, stderr)
      busy = false
      local answer = (stdout or ""):gsub("%s+$", "")
      if answer == "" then answer = "No answer. Check " .. DIR .. "/ask.log" end
      overlay(answer, 10)
    end, { WAV }):start()
  end)
end

jarvisTap = hs.eventtap.new({ hs.eventtap.event.types.flagsChanged }, function(e)
  if e:getKeyCode() ~= RIGHT_OPT then return false end
  if e:getFlags().alt then startRecording() else stopAndAsk() end
  return false
end)
jarvisTap:start()

hs.hotkey.bind({ "cmd", "alt" }, "J", function()
  local flag = DIR .. "/.muted"
  if hs.fs.attributes(flag) then
    os.remove(flag)
    overlay("Jarvis unmuted", 2)
  else
    io.open(flag, "w"):close()
    overlay("Jarvis muted", 2)
  end
end)

overlay("Jarvis voice loaded", 2)
