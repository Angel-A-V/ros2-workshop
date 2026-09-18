# ROS 2 Workshop

Robotics Society at UC Merced — an introduction to **ROS 2** (Robot Operating System), no robot needed.

You get a full Ubuntu desktop with ROS 2 Humble **inside your web browser**, on Mac or Windows. In the workshop you will
drive a simulated turtle, see how ROS programs talk to each other, build your own ROS package, and look at a robot in **RViz**.

## 1. Before the workshop — install (about 45 minutes, at home on good Wi-Fi)

👉 **[docs/01-install.md](docs/01-install.md)**

Please finish this **before** you come. The download is several GB and campus Wi-Fi can't handle everyone at once.

## 2. At the workshop — follow along

👉 **[docs/02-workshop.md](docs/02-workshop.md)**

## Everyday commands

Run these in your **laptop** terminal, inside the `ros2-workshop` folder:

| I want to… | Command |
|---|---|
| Start the ROS desktop | `docker compose up -d` |
| Use it | open <http://localhost:6080> → **Connect** |
| Stop it | `docker compose stop` |
| Reset it (your files in `ws/` are kept) | `docker compose down` then `docker compose up -d` |

## What's in this repo

```text
ros2-workshop/
├── compose.yaml             ← starts the ROS desktop (one command)
├── docs/
│   ├── 01-install.md        ← do before the workshop
│   ├── 02-workshop.md       ← follow along in the workshop
│   └── instructor-notes.md  ← for the presenter
└── ws/                      ← the ROS workspace (shows up as ~/ws in the ROS desktop)
    └── src/
        └── workshop_demos/  ← demo package: turtle driver + RViz robot demo
```

The ROS desktop image is [Tiryoh/docker-ros2-desktop-vnc](https://github.com/Tiryoh/docker-ros2-desktop-vnc) (Apache-2.0).
