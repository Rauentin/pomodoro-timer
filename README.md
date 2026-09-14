# Pomodoro Timer

A small desktop Pomodoro timer built with Python and tkinter. Set your work and
break lengths, hit Start, and it counts down and switches between periods
automatically, playing a sound at each transition. Pause and resume at any time.

## Requirements

- Python 3.8+
- `pygame` (for the notification sounds)

```bash
pip install -r requirements.txt
```

tkinter ships with most Python installs; on Debian/Ubuntu it may need
`sudo apt install python3-tk`.

## Running

```bash
python gui.py
```

## Sounds

Put your two notification sounds in the `sounds/` folder, named exactly:

```
sounds/start.wav   # played when a break ends and work begins
sounds/break.wav   # played when work ends and a break begins
```

If a file is missing the timer keeps running and just logs that it couldn't play
it, so the app works fine without sounds.

## Layout

- `timer.py` — timer logic (countdown, pause, work/break switching), no UI
- `gui.py` — tkinter interface and the one-second tick loop
- `sounds/` — your `start.wav` and `break.wav`
