# Instructor Notes (for the presenter)

> Members follow [01-install.md](01-install.md) at home, then [02-workshop.md](02-workshop.md) with you in the room.
> Put 02-workshop.md on the projector and walk through it section by section.

---

## A. Put the repo on GitHub

1. The repo is <https://github.com/Angel-A-V/ros2-workshop> (public). Members clone it with the URL in `docs/01-install.md` (Step 4).
2. Push this folder:

   **MAC — Terminal**

   ```bash
   cd "$HOME/Downloads/Robotics Autonomous/ros2-workshop"
   git init
   git add .
   git commit -m "ROS 2 workshop: install guide, follow-along guide, demo package"
   git branch -M main
   git remote add origin https://github.com/Angel-A-V/ros2-workshop.git
   git push -u origin main
   ```

   If `git push` asks for a password, your GitHub password won't work. Run `gh auth login` first (GitHub CLI), or upload instead:
   on the new repo page click **uploading an existing file** and drag in everything in this folder (`compose.yaml`, `README.md`, `docs`, `ws`).

3. Open the repo on GitHub and check you can see `compose.yaml`, `docs/` and `ws/src/workshop_demos/`.

## B. Rehearse exactly like a member (important)

Nothing here has been run yet, so do a full test run on your Mac.

```bash
docker rm -f ros            # removes your old hand-made test container, if it still exists
cd ~
git clone https://github.com/Angel-A-V/ros2-workshop.git
cd ros2-workshop
docker compose pull
docker image inspect tiryoh/ros2-desktop-vnc:humble --format '{{.Architecture}}'   # should say arm64 on an Apple-chip Mac
docker compose up -d
```

Do **all** of 01-install.md Step 6, then **all** of 02-workshop.md. Check off:

```text
[ ] localhost:6080 shows the desktop; ls ~/ws shows src
[ ] turtlesim + teleop + rqt_graph + topic pub + spawn
[ ] colcon build in ~/ws → workshop_demos Finished
[ ] turtle_demo.launch.py → turtle drives circles; ros2 param set changes it
[ ] my_first_pkg created, built, "Hi from my_first_pkg."
[ ] Edited hello_node.py on the Mac → rebuilt → new text
[ ] robot_demo.launch.py → RViz shows arm, red laser dots, map, TF
```

If anything fails, fix the doc or code **before** the workshop, then push again.
Afterwards, delete your test package so it doesn't end up in the repo: `rm -rf ~/ros2-workshop/ws/src/my_first_pkg`.
(`build/`, `install/` and `log/` are already ignored by Git.)

## C. Send members the pre-work (copy/paste)

```text
Hi everyone! For the ROS 2 workshop, please do the install at home BEFORE you come.
It takes about 45 minutes, mostly downloads, and campus Wi-Fi can't handle all of us downloading at once.

Guide: https://github.com/Angel-A-V/ros2-workshop/blob/main/docs/01-install.md

You're done when you see the turtle in your browser (Step 6).
Stuck? Screenshot the error and bring it — we'll fix it together at the start.
Bring your laptop and charger!
```

## D. Optional backup: USB stick with the image

For members who didn't download. This only works for **Apple-chip Macs** (your image is arm64):

```bash
docker save tiryoh/ros2-desktop-vnc:humble -o ~/Desktop/ros-desktop-arm64.tar
```

The member copies the file, then runs `docker load -i ros-desktop-arm64.tar` (no internet needed) and `git clone` (small).
Everyone else without the image pairs with a neighbor.

---

## E. Session plan (about 90 minutes)

| Time | Block | Notes |
|---|---|---|
| 0:00 | **Welcome + what ROS is** (5 min) | ROS = tools and conventions for building robot software from small programs (nodes) that pass messages (topics). |
| 0:05 | **Readiness check** (10 min) | Everyone runs `docker compose up -d` and opens localhost:6080. Helpers fix install problems; anyone stuck pairs up. |
| 0:15 | **Two computers** (5 min) | Draw the table from the top of 02-workshop.md. Rule for the room: *"`docker` goes in the laptop terminal, `ros2` goes in the browser terminal."* |
| 0:20 | **Section 2: turtlesim** (15 min) | Show `rqt_graph` on the projector. Let people play with `topic pub` numbers. |
| 0:35 | **Section 3: colcon + launch + params** (15 min) | Say the rule out loud: *build → source → run*. Open `draw_circle.py` on the projector and read it together. |
| 0:50 | **Section 4: own package** (15 min) | The edit-on-laptop, build-in-desktop loop is the key skill. Wait until most of the room gets their own message printed. |
| 1:05 | **Section 5: RViz** (10 min) | The "wow" moment. Rotate the view, untick displays, show `ros2 topic hz /scan`. |
| 1:15 | **Wrap-up** (15 min) | Recap table (section 6). Explain that the club robot uses the same ideas, and what comes next. Everyone runs `docker compose stop`. |

**Tip:** have 2–3 helpers who did the rehearsal walk around the room.

## F. Top problems in the room

| Symptom | Fix |
|---|---|
| `Cannot connect to the Docker daemon` | Open Docker Desktop, wait for *Engine running*. |
| `no configuration file provided` | Not in the folder: `cd ~/ros2-workshop`. |
| Windows: repo cloned under `C:\` or `/mnt/c/` | Clone again inside the Ubuntu window: `cd ~ && git clone ...`. |
| `~/ws` empty in the desktop | Started from the wrong folder: `cd ~/ros2-workshop && docker compose down && docker compose up -d`. |
| `Package ... not found` | `source ~/ws/install/setup.bash` in that tab. |
| `ros2` not found / `docker` not found | Wrong terminal (see the two-computers rule). |
| Black browser screen | Refresh; else `docker compose restart`, wait 30 s, refresh. |
| RViz black or crashes | `export LIBGL_ALWAYS_SOFTWARE=1`, relaunch. |
| Very slow Intel laptop with 8 GB RAM | Close other apps; Docker Desktop → Resources → Memory ≥ 4 GB; pair up if still too slow. |
