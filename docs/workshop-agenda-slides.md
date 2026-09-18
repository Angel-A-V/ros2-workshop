# ROS 2 Workshop — Agenda + Live-Demo Slides

> Short version of the deck, built around today's plan:
> **Why (Docker, GitHub, ROS 2) → Install together → Live workshop (question on the board → live demo → answer)**.
> Every demo comes from the published repo: <https://github.com/Angel-A-V/ros2-workshop>
> (`docs/01-install.md` for installs, `docs/02-workshop.md` for the workshop). Times are suggestions for about 2 hours.

---

## Slide 1 — Title

**On the slide**

- **ROS 2 Workshop: From Your Laptop to a Robot**
- Robotics Society at UC Merced
- Repo: `github.com/Angel-A-V/ros2-workshop`

---

## Slide 2 — Today's agenda

**On the slide**

| # | Part | What we do | Time |
|---|---|---|---|
| 1 | **Why?** | What is Docker? Why GitHub? Why ROS 2? | 15 min |
| 2 | **Install together** | WSL (Windows only) → Docker Desktop → Git → download the workshop → download the ROS desktop | 40 min |
| 3 | **Live workshop** | Start the ROS desktop → drive a turtle → build code → make your own package → RViz | 50 min |
| 4 | **Wrap-up** | Recap + what's next on the robot | 10 min |

**Say this:** "First 15 minutes: why we use these tools. Then we install everything together. Then the fun part: we run ROS 2 live."

---

# PART 1 — WHY? (15 min)

## Slide 3 — Why ROS 2?

**On the slide**

- A robot = **many small programs running at once**: camera, vision, navigation, motors
- **ROS 2** is the framework that lets those programs **talk to each other**, plus tools to see what's happening
- Our robot already works this way:
  `game controller → driving logic → motor drivers → motors`

**Visual:** `Camera → Vision → Navigation → Motors` as four boxes with arrows.

**Remember:** ROS 2 = how robot programs talk to each other.

---

## Slide 4 — Why GitHub?

**On the slide**

- **Git** = a time machine for code: every version is saved
- **GitHub** = the shared online copy the whole team (and the robot) pulls from
- Today you'll use one command: **`git clone`** → "download this whole project to my laptop"
- No GitHub account needed today; the workshop repo is public

**Visual:** GitHub in the middle, arrows to several laptops and the robot.

**Remember:** GitHub is how code gets from one laptop to everyone, and to the robot.

---

## Slide 5 — What is Docker? (and why WSL on Windows?)

**On the slide**

- ROS 2 runs on **Ubuntu Linux**. Your laptop runs Mac or Windows
- **Docker** runs a complete, pre-built **Ubuntu + ROS 2 computer inside your laptop**
- **Image** = the downloaded setup · **Container** = that setup running
- Everyone gets **the exact same setup**: no "works on my machine"
- **Windows:** Docker needs real Linux underneath, and **WSL** provides it. **Mac:** Docker Desktop handles it for you

**Visual:** The stack, bottom to top: `Your laptop → (WSL on Windows) → Docker → Ubuntu + ROS 2 → our code`

**Remember:** Docker = the same Linux + ROS 2 computer for everyone.

---

# PART 2 — INSTALL TOGETHER (40 min)

Follow **`docs/01-install.md`** live on the projector. One slide per step so everyone knows where we are.

> 💡 The ROS desktop download (Step 5) is **several GB**. Start it the moment Docker works, then help with other steps while it downloads.

## Slide 6 — Install checklist (keep this up during Part 2)

**On the slide**

```text
[ ] Step 1  Windows only: WSL installed  →  wsl -l -v shows Ubuntu, VERSION 2
[ ] Step 2  Docker Desktop says "Engine running"  →  docker run --rm hello-world
[ ] Step 3  git --version prints a version
[ ] Step 4  git clone the workshop  →  ls shows README.md compose.yaml docs ws
[ ] Step 5  docker compose pull  →  every line says "Pulled"
[ ] Step 6  docker compose up -d  →  localhost:6080  →  a turtle appears 🐢
```

**What each command does** (for the side of the slide):

| Command | What it actually does |
|---|---|
| `wsl --install` | Installs Ubuntu Linux inside Windows |
| `docker run --rm hello-world` | Runs a tiny test container to prove Docker works, then deletes it (`--rm`) |
| `git clone <url>` | Downloads the whole project, with its history, into a new folder |
| `docker compose pull` | Downloads the image named in `compose.yaml` (the big ROS 2 download) |
| `docker compose up -d` | Starts the ROS desktop in the background |

**Say this:** "Raise your hand when you see the turtle. If you get stuck, don't sit on it: flag a helper."

---

# PART 3 — LIVE WORKSHOP (50 min)

Each slide has a **question on the board**. Ask the room first, run the **live demo**, then reveal the **answer**.
All demos are from **`docs/02-workshop.md`**. The section numbers are listed so everyone can follow along.

## Slide 7 — ❓ "Where is my code actually running?"

**Live demo** (`02-workshop.md` §1)

1. Laptop terminal: `cd ~/ros2-workshop` → `docker compose up -d`
2. Browser: `http://localhost:6080` → **Connect** → Applications → System Tools → **MATE Terminal**
3. In the ROS desktop terminal: `ls ~/ws`. Then show the same `ws` folder in Finder / File Explorer on your laptop

**Answer (reveal)**

- You **edit** on your laptop → the code **runs** in the container → you **see** it in the browser
- `ros2-workshop/ws` on the laptop = `~/ws` in the container: the same files
- **Laptop terminal** → `docker`, `git` · **ROS desktop terminal** → `ros2`, `colcon`

---

## Slide 8 — ❓ "What is a node?"

**Live demo** (§2.1)

- Tab 1: `ros2 run turtlesim turtlesim_node` → starts **one program**: the simulator
- Tab 2: `ros2 run turtlesim turtle_teleop_key` → starts **another program**: the keyboard controller. Drive with the arrow keys
- Tab 3: `ros2 node list` → lists every program that's running

**Answer (reveal)**

- A **node** = one program with one job
- `/turtlesim` moves the turtle · `/teleop_turtle` reads your keys
- A robot = many nodes working together

---

## Slide 9 — ❓ "How do nodes talk to each other?"

**Live demo** (§2.2–2.3)

- `ros2 topic list` → every channel that exists
- `ros2 topic echo /turtle1/cmd_vel` → drive the turtle and **watch the messages** print
- `rqt_graph` → the live picture of who talks to whom

**Answer (reveal)**

- **Topic** = a named channel (`/turtle1/cmd_vel`)
- **Message** = one piece of data on it (forward speed + turning speed)
- **Publisher** sends (teleop) → **subscriber** listens (turtlesim)

**Visual:** A screenshot of `rqt_graph` next to the robot version:

| Turtlesim | Real robot |
|---|---|
| `turtle_teleop_key` | Navigation / game controller |
| `/turtle1/cmd_vel` | `/cmd_vel` (velocity commands) |
| `turtlesim_node` | Motor controller |

---

## Slide 10 — ❓ "Can I control the robot without the keyboard node?"

**Live demo** (§2.4–2.5)

- `ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"`
  → **you** become the publisher and send one message by hand. Let the room pick the numbers
- `ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"`
  → asks turtlesim to **do one thing**, and gets a reply

**Answer (reveal)**

- Anything that publishes the right message can drive the robot: a keyboard, code, a person
- **Topic** = a nonstop stream · **Service** = one request, one reply

---

## Slide 11 — ❓ "How does my code become something ROS can run?"

**Live demo** (§3)

- `cd ~/ws` → `ls src` → `colcon build` → point out `Finished <<< workshop_demos`
- `ls` → show the new `build/`, `install/` and `log/` folders
- `source install/setup.bash`
- `ros2 launch workshop_demos turtle_demo.launch.py` → the turtle drives circles **by itself**

**Answer (reveal)**

- **Workspace** = folder of packages: you write in `src/`
- **`colcon build`** = builds everything in `src/` → puts the runnable result in `install/`
- **`source install/setup.bash`** = tells **this terminal** where the built packages are (every new tab!)
- **Launch file** = starts several nodes with one command

---

## Slide 12 — ❓ "Where's the code that's driving the turtle?"

**Live demo** (§3.1)

- Open `ws/src/workshop_demos/workshop_demos/draw_circle.py` on the projector (VS Code on the laptop). It's about 20 lines
- Point out: **create a publisher** on `/turtle1/cmd_vel` → **send a message 10 times per second**
- Tab 2: `ros2 param set /draw_circle speed 4.0` and `ros2 param set /draw_circle turn -2.0`

**Answer (reveal)**

- A node is just normal Python using ROS: **publisher + timer + message**
- **Parameters** = settings you can change while the node runs

---

## Slide 13 — ❓ "How do I make my own?"

**Live demo** (§4), with **everyone doing it**

- `cd ~/ws/src` → `ros2 pkg create --build-type ament_python --node-name hello_node my_first_pkg`
  → generates a new package with a starter node
- `cd ~/ws` → `colcon build` → `source install/setup.bash` → `ros2 run my_first_pkg hello_node`
- Change the `print(...)` text in VS Code on the laptop → save → build → source → run again

**Answer (reveal)**

- **The loop you'll use forever: edit → build → source → run**

---

## Slide 14 — ❓ "How do we see what a robot sees?"

**Live demo** (§5)

- `ros2 launch workshop_demos robot_demo.launch.py`
- Rotate the view, zoom, untick displays
- Tab 2: `ros2 topic hz /scan` → how many laser scans per second

**Answer (reveal)**

- **RViz** shows a robot's model, sensors (the red laser dots) and coordinate frames in 3D
- It's the main tool for checking and debugging the real robot

---

# PART 4 — WRAP-UP (10 min)

## Slide 15 — Something broke? Check in this order

**On the slide**

1. **Right terminal?** `ros2` → ROS desktop · `docker` → laptop
2. **Container running?** `docker ps`
3. **Built?** `cd ~/ws && colcon build`
4. **Sourced?** `source ~/ws/install/setup.bash` (in this tab)
5. **Is it talking?** `ros2 node list`, `ros2 topic echo <topic>`, `rqt_graph`

---

## Slide 16 — What you learned today

**On the slide**

| Question | Answer |
|---|---|
| What is ROS 2? | How robot programs talk to each other, plus tools |
| Node? | One program, one job |
| Topic? | A named channel nodes publish and subscribe to |
| Why Docker? | The same Ubuntu + ROS 2 computer for everyone |
| Why GitHub? | One shared copy of the code, which reaches the robot |
| `colcon build`? | Turns `src/` into runnable programs in `install/` |
| `source`? | Tells this terminal where your built packages are |
| Where does my code run? | In the container; edited on your laptop, seen in the browser |

**Next time:** the real robot's code uses the same pattern: `game controller → driving logic → motors`.

**Before you leave:** `docker compose stop` (in the laptop terminal).
