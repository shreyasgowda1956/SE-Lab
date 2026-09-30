# Lab 4: VibeCoding — Flappy Bird

This folder contains the completed Flappy Bird Lab 4 implementation.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Completed tasks

1. **Refined collision detection** — collision uses swept rectangles across the bird and moving pipe positions to reduce clipping at higher speeds.
2. **Game Over screen** — ground, ceiling, and pipe collisions stop the game and display the final score on screen.
3. **Replay / difficulty** — after Game Over, press `1` for Easy, `2` for Medium, `3` for Hard, or `ESC` to exit.
4. **Sound feedback** — generated Pygame audio effects are used for flap, score, and death; audio initialization failures are handled gracefully.

## Controls

- `Space` or mouse click: flap
- `1`: Easy replay after Game Over
- `2`: Medium replay after Game Over
- `3`: Hard replay after Game Over
- `ESC`: exit from Game Over

## Folder structure

```text
lab-4/
├── main.py
├── requirements.txt
├── README.md
└── game/
    ├── __init__.py
    ├── bird.py
    ├── game_engine.py
    └── pipe.py
```

## Submission evidence

The supplied before-change video was inspected and is approximately 4.23 seconds long, so it does **not** meet the stated 10-second minimum and should be re-recorded before final submission. The supplied after-change video is approximately 12.73 seconds long and meets the 10-second duration requirement.

The lab handout also requires the before/after videos and an exported LLM/ChatGPT conversation. Add those evidence files to this folder before the final submission if the instructor requires the files themselves rather than links.
