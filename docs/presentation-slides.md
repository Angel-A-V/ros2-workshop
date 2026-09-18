# ROS 2 Workshop — Slide Content

> For the presenter. Each slide has: **On the slide** (copy this onto the slide), **Visual**, **Say this** (speaker notes),
> and **Remember** (the one-line takeaway, good as a footer).
> Commands match the `ros2-workshop` repo (`docs/01-install.md`, `docs/02-workshop.md`). Mental model first, commands second.

**Story:** Why ROS 2 → How ROS 2 works → Why an environment → Git/GitHub → Linux/WSL2/macOS → Docker → Workspace → Our repo → First ROS system → Debugging → Everyday workflow

---

## Slide 1 — Title

**On the slide**

- **From Laptop to Robot: How Our ROS 2 Setup Works**
- Robotics Society at UC Merced — Software Workshop 1

**Say this:** "Today isn't about copying 20 commands. It's about understanding the system, so when something breaks, you know where to look."

---

## Slide 2 — By the end of today you can explain…

**On the slide**

- What is ROS 2, and why does our robot use it?
- What are a **node** and a **topic**?
- Why do I need **Git**, **Linux/WSL2** and **Docker**?
- What do **`colcon build`** and **`source`** do?
- Where is my code actually running?
- What do I do when something doesn't work?

**Say this:** "Keep these questions in mind. We'll come back to this exact list at the end."

---

# PART 1 — WHY ROS 2?

## Slide 3 — What does a robot's software actually do?

**On the slide**

- **Sense** → cameras, lidar, joysticks, encoders
- **Think** → detect objects, plan a path, decide
- **Act** → drive motors, move arms
- All of this runs **at the same time**, **nonstop**, often written by **different people**

**Visual:** A loop: `Sensors → Processing → Decisions → Actuators → (back to) Sensors`.

**Say this:** "A robot isn't one program. It's lots of small programs running at once and constantly passing data around.
The camera doesn't wait for the motors, and the motors don't wait for the camera."

**Remember:** Robot software = many programs running at once, sharing data.

---

## Slide 4 — What is ROS 2?

**On the slide**

- **ROS 2 = Robot Operating System 2**
- It's **not** an operating system. It's a **framework** (plus tools) that runs on Linux
- It gives you:
  - A standard way for programs to **talk to each other**
  - Ready-made **tools** to inspect, record and visualize data
  - Thousands of **existing packages** (camera drivers, navigation, simulators…)
- We use **ROS 2 Humble**, a long-term support release for Ubuntu 22.04

**Visual:** ROS 2 logo, plus logos of companies/robots that use it (optional).

**Say this:** "Without ROS, every team would have to invent their own way for the camera code to send images to the vision code.
ROS standardizes that 'plumbing,' so we can focus on the interesting parts."

**Remember:** ROS 2 is the **communication system and toolbox** for robot programs.

---

## Slide 5 — Why does *our* robot use ROS 2?

**On the slide**

- The robot's pieces are separate programs:
  **game controller → driving logic → motor drivers → motors**
- Teams can work **in parallel**: vision, navigation, drive
- You can **swap parts**: test with a fake camera or fake motors today, the real hardware later
- We can use existing drivers instead of writing everything ourselves

**Visual:** The real robot's current software:
`joy_node → gamepad_control → ODrive CAN nodes → CAN bus → motors`

**Say this:** "Our robot already works this way. The controller is one program, the driving logic is another, the motor drivers are another.
Because they only talk through ROS, you can write and test your part on your laptop without the robot."

**Remember:** ROS lets many people build **separate pieces** that plug together.

---

# PART 2 — HOW ROS 2 WORKS

## Slide 6 — Nodes: the building blocks  ⭐ (diagram 2, part A)

**On the slide**

- A **node** = one program with **one job**
- A robot = many nodes working together

**Visual (diagram 2): a simple autonomous robot**

```text
 ┌─────────────┐   /camera/image    ┌──────────────────┐  /detected_objects  ┌─────────────────┐   /cmd_vel   ┌──────────────────┐
 │ Camera Node │ ─────────────────▶ │ Vision Node      │ ──────────────────▶ │ Navigation Node │ ───────────▶ │ Motor Controller │
 │ (sensor)    │                    │ (finds objects)  │                     │ (decides)       │              │ (moves wheels)   │
 └─────────────┘                    └──────────────────┘                     └─────────────────┘              └──────────────────┘
     SENSE                                THINK                                    DECIDE                           ACT
```

Boxes = **nodes**. Arrows = **topics**. (Draw it left to right, one color per stage.)

**Say this:** "Each box is a separate program. If the vision node crashes, the camera node keeps running.
If we buy a better camera, we replace just one box."

**Remember:** **Node = one program, one job.**

---

## Slide 7 — Topics, messages, publishers, subscribers  ⭐ (diagram 2, part B)

**On the slide**

- **Topic** = a named channel, like `/cmd_vel`
- **Message** = one piece of data sent on it, with a fixed type
- **Publisher** = a node that **sends** on a topic
- **Subscriber** = a node that **listens** to a topic

| Topic | Published by | Subscribed by | Message type (what's inside) |
|---|---|---|---|
| `/camera/image` | Camera Node | Vision Node | An image (pixels) |
| `/detected_objects` | Vision Node | Navigation Node | A list of objects + positions |
| `/cmd_vel` | Navigation Node | Motor Controller | A velocity: forward speed + turning speed |

**Visual:** Zoom in on one arrow of diagram 2: `Navigation Node --(publishes)--> [ /cmd_vel ] --(subscribes)--> Motor Controller`, with a message card:
`linear.x: 0.5   angular.z: 0.2`.

**Say this:** "Think of a topic like a group chat. Anyone can post and anyone can read. The publisher doesn't know or care who's listening.
That's why we can add a logging or visualization node without touching anyone else's code."

**Remember:** **Nodes talk by publishing and subscribing to topics.**

---

## Slide 8 — Other ways nodes talk (just know they exist)

**On the slide**

| | Analogy | Example |
|---|---|---|
| **Topic** | Group chat: a nonstop stream | Camera images, velocity commands |
| **Service** | Asking a question and getting one answer | "Spawn a new turtle" → "done" |
| **Action** | Ordering food with updates: long task with progress and cancel | "Drive to the door" → "50%… 80%… arrived" |
| **Parameter** | A setting you can change while it runs | Max speed of the robot |
| **Launch file** | A startup script | Starts 5 nodes with one command |

**Say this:** "Topics are 90% of what you'll use. Today you'll also try a service, a parameter, and launch files."

**Remember:** Topics for streams, services for requests, actions for long tasks.

---

# PART 3 — WHY WE NEED A DEVELOPMENT ENVIRONMENT

## Slide 9 — The problem

**On the slide**

- ROS 2 Humble is built for **Ubuntu Linux 22.04**
- The robot's computer (Orange Pi 5) runs **Linux**
- Your laptop runs **macOS or Windows**
- 30 people × different laptops = **"it works on my machine"** chaos

**The fix:** everyone runs the **same Linux + ROS 2 environment** inside their laptop.

**Say this:** "If everyone installed ROS their own way, half the room would spend today fighting installs.
Instead, we give everyone an identical Linux computer inside their laptop."

**Remember:** Same environment for everyone → code that works for you works for everyone.

---

## Slide 10 — The complete development stack  ⭐⭐ (the most important slide)

**On the slide / Visual (diagram 1)**, drawn as stacked layers, bottom to top, with the "what you use it for" on the right:

```text
 ┌──────────────────────────────────────────────────────────────┐
 │ 7  ROBOT SOFTWARE        Sensors → Processing → Decisions → Actuators │  ← what we're building
 ├──────────────────────────────────────────────────────────────┤
 │ 6  CLUB ROS 2 WORKSPACE  Packages + your source code (ws/src)          │  ← where your code lives
 ├──────────────────────────────────────────────────────────────┤
 │ 5  ROS 2 HUMBLE          Nodes · Topics · Services · Actions           │  ← how programs talk
 ├──────────────────────────────────────────────────────────────┤
 │ 4  DOCKER CONTAINER      The club's Ubuntu 22.04 + ROS 2 desktop       │  ← identical for everyone
 ├──────────────────────────────────────────────────────────────┤
 │ 3  LINUX ENVIRONMENT     WSL2 (Windows) · Docker's Linux VM (macOS)    │  ← Linux engine
 ├──────────────────────────────────────────────────────────────┤
 │ 2  HOST TOOLS            Git · GitHub · VS Code · web browser          │  ← you edit & share here
 ├──────────────────────────────────────────────────────────────┤
 │ 1  YOUR COMPUTER         Windows PC or Mac                              │
 └──────────────────────────────────────────────────────────────┘
```

**Say this (walk up the stack):** "Your laptop is at the bottom. On it you use normal tools: Git, VS Code, a browser.
Docker needs Linux, so Windows provides it with WSL2, and on a Mac Docker Desktop runs a small Linux virtual machine for you.
Inside that runs our container, the same Ubuntu + ROS 2 for everyone. ROS 2 runs inside it. Our workspace and packages are built with ROS 2.
And at the top is what we actually care about: robot software."

**Remember:** **Git, Linux/WSL2, Docker and ROS 2 aren't four random installs. They're layers of one pipeline.**

> Tip: reuse this diagram as a small "you are here" graphic in the corner of the Git, Linux, Docker and Workspace section slides, with that layer highlighted.

---

# PART 4 — GIT & GITHUB

## Slide 11 — Why Git and GitHub?

**On the slide**

- **Git** = a **time machine** for your code: every saved version (commit), and you can go back
- **GitHub** = the **shared online copy** everyone pulls from and pushes to
- Robotics = many people editing the same code → without Git, you're emailing zip files
- The robot's computer pulls the **same code** from GitHub that you wrote on your laptop

**Command, explained:**

`git clone https://github.com/Angel-A-V/ros2-workshop.git`
→ "Download a full copy of this project, **including its history**, into a new folder on my computer."

**Visual:** GitHub in the middle, arrows to 3 laptops and the robot (`push ↑` / `pull ↓`).

**Say this:** "Today you only needed `git clone`. On the robot project you'll use branches and pull requests,
so your changes get reviewed before they reach the real robot."

**Remember:** **GitHub is how code gets from your laptop to everyone else, and to the robot.**

---

# PART 5 — LINUX, WSL2 & macOS

## Slide 12 — Why Linux? Why WSL2?

**On the slide**

- ROS 2 and robot computers live on **Linux**
- Docker containers are Linux too, so they need a **Linux engine** underneath
- **Windows:** **WSL2** = a real Ubuntu Linux built into Windows. Docker Desktop runs on top of it
- **macOS:** Docker Desktop quietly runs a **small Linux virtual machine** for you. Nothing extra to install
- Apple-chip Macs are **ARM64**, the same chip family as the robot's Orange Pi 5

**Say this:** "Windows users installed WSL because Docker needs Linux. Mac users got it for free inside Docker Desktop.
Windows folks: keep your files **inside Ubuntu** (`~/ros2-workshop`), not `C:\`, because it's much faster and avoids line-ending bugs."

**Remember:** **Robots run Linux, so we develop in Linux**, even on a Mac or Windows laptop.

---

## Slide 13 — The #1 rule: which terminal am I in?

**On the slide**

| | **Laptop terminal** | **ROS desktop terminal** (in the browser) |
|---|---|---|
| Mac | Terminal app | MATE Terminal |
| Windows | Ubuntu (WSL) window | MATE Terminal |
| Commands | `git`, `docker compose` | `ros2`, `colcon`, `rviz2`, `rqt_graph` |

- `ros2: command not found` → you're in the **laptop** terminal
- `docker: command not found` → you're in the **ROS desktop** terminal

**Visual:** Two screenshots side by side, prompts circled: `angel@MacBook ~ %` vs `ubuntu@…:~$`.

**Remember:** **Read the prompt. It tells you which computer you're on.**

---

# PART 6 — DOCKER

## Slide 14 — Why Docker? Image vs container

**On the slide**

- **Image** = a saved, read-only snapshot of a whole computer setup (Ubuntu + ROS 2 + tools)
- **Container** = a **running copy** of that image
- Programmer analogy: **image = class, container = object**
- Everyone downloads the **same image**, so everyone gets the **same computer**
- Broke something? Throw the container away and start a fresh one from the image

**Say this:** "Instead of a 3-hour install guide that goes differently on every laptop, we ship the finished computer.
The big download in your install guide was the image."

**Remember:** **Docker gives everyone an identical, disposable Linux + ROS 2 computer.**

---

## Slide 15 — Our container: the ROS desktop in your browser

**On the slide**

- Image: `tiryoh/ros2-desktop-vnc:humble`, Ubuntu 22.04 + ROS 2 Humble + RViz + turtlesim + colcon
- It includes a **full desktop** you open at **http://localhost:6080**
- `compose.yaml` = the **recipe** for starting it (which image, which port, which folder to share)

**Commands, explained** (run in the **laptop** terminal, inside `ros2-workshop`):

| Command | What it actually does |
|---|---|
| `docker compose up -d` | Reads `compose.yaml` and **starts** the container in the background (`-d` = detached, so you get your prompt back) |
| `docker compose stop` | **Pauses** it. Everything inside is kept |
| `docker compose down` | **Deletes** the container (a reset). Your `ws/` files are safe |
| `docker ps` | Lists running containers. Is mine on? |

**Visual:** Screenshot of the browser showing the Ubuntu desktop at `localhost:6080`.

**Remember:** **`compose.yaml` is the recipe; `docker compose up -d` bakes it.**

---

# PART 7 — THE ROS 2 WORKSPACE

## Slide 16 — Workspace and packages

**On the slide**

- **Package** = a folder of ROS code (nodes, launch files, config) with a `package.xml` "ID card"
- **Workspace** = a folder that holds packages in `src/`

```text
ws/                     ← the workspace (you build from HERE)
├── src/                ← your source code
│   ├── workshop_demos/ ← the club demo package
│   └── my_first_pkg/   ← the one you'll create
├── build/   ┐
├── install/ ├─ created by colcon build (never edit these)
└── log/     ┘
```

**Say this:** "`src` is what you write. `build`, `install` and `log` are what the computer generates. You never edit those three."

**Remember:** **You write code in `src/`; you build from the workspace root.**

---

## Slide 17 — What does `colcon build` do?

**On the slide**

- `colcon build` = **"find every package in `src/` and build it"**
- Python packages get installed; C++ packages get compiled
- The results go into **`install/`**
- Changed your code? → **build again**, or ROS still runs the old version

**Visual:** `src/ → [ colcon build ] → install/` as an arrow with a gear icon, plus the terminal output:
`Finished <<< workshop_demos … Summary: 1 package finished`

**Say this:** "Yellow warnings are normal. Only the word **Failed** is a problem. And always run it from `~/ws`, not from inside `src`."

**Remember:** **`colcon build` turns `src/` into runnable programs in `install/`.**

---

## Slide 18 — Why do I `source install/setup.bash`?

**On the slide**

- Building puts your programs in `install/`, but your terminal **doesn't know that yet**
- `source install/setup.bash` = **"hey terminal, also look in here for ROS packages"**
- It only affects **this terminal tab**
- New tab or new build → **source again**

**Analogy:** Installing an app, then adding it to your phone's home screen so you can find it.

**Visual:** Before/after: `ros2 run my_first_pkg hello_node` → ❌ `Package not found` … `source` … ✅ `Hi from my_first_pkg.`

**Remember:** **Build → source → run.** Most "package not found" errors = forgot to source.

---

# PART 8 — OUR REPOSITORY

## Slide 19 — Tour of `ros2-workshop`

**On the slide**

```text
ros2-workshop/
├── compose.yaml      ← starts the ROS desktop
├── docs/             ← install guide + today's workshop guide
└── ws/               ← the ROS 2 workspace
    └── src/workshop_demos/
        ├── workshop_demos/draw_circle.py   ← a node (~20 lines)
        ├── launch/                          ← turtle + RViz demos
        └── rviz/                            ← saved RViz view
```

- **This practice repo** teaches the concepts
- **The robot's repo** (`Autonomous-Robot`) uses the same ideas: packages, launch files, colcon, topics

**Say this:** "Everything you learn today transfers directly. The robot repo is just a bigger workspace with real hardware nodes."

**Remember:** **Practice here, then the same workflow runs the real robot.**

---

## Slide 20 — Where is my code actually running?  ⭐

**On the slide / Visual**

```text
 YOUR LAPTOP                                   DOCKER CONTAINER (Ubuntu + ROS 2)
 ┌─────────────────────────────┐               ┌──────────────────────────────────┐
 │ VS Code edits               │   shared      │ colcon build / ros2 run           │
 │ ~/ros2-workshop/ws/...  ◀───┼── folder ────▶│ ~/ws/...          ← code RUNS here│
 │                             │  (same files) │                                   │
 │ Browser: localhost:6080 ◀───┼── screen ─────┤ desktop, turtlesim, RViz windows  │
 └─────────────────────────────┘               └──────────────────────────────────┘
```

- You **edit** on your laptop
- The code **runs** inside the container (Linux)
- You **see** it through the browser
- `ros2-workshop/ws` on your laptop **=** `~/ws` in the container: the same files, two names

**Remember:** **Edit on the laptop, run in the container, watch in the browser.**

---

# PART 9 — RUNNING OUR FIRST ROS 2 SYSTEM

## Slide 21 — Start it and check it works

**On the slide**

1. **Laptop terminal:** `cd ~/ros2-workshop` → `docker compose up -d`
2. **Browser:** `http://localhost:6080` → **Connect**
3. **ROS desktop:** Applications → System Tools → **MATE Terminal**

**Is ROS working?** (in the ROS desktop terminal)

| Command | What it does | ✅ Working if… |
|---|---|---|
| `ros2 run turtlesim turtlesim_node` | Starts one node: a simulator | A window with a turtle appears |
| `ros2 node list` | Lists every node running right now | You see `/turtlesim` |
| `ros2 topic list` | Lists every topic that exists | You see `/turtle1/cmd_vel` |

**Remember:** **If you can see a node and its topics, ROS 2 is working.**

---

## Slide 22 — Live demo: turtlesim IS the robot diagram

**On the slide**

| Robot diagram | Turtlesim |
|---|---|
| Navigation Node | `turtle_teleop_key` (your arrow keys) |
| `/cmd_vel` | `/turtle1/cmd_vel` |
| Motor Controller | `turtlesim_node` (moves the turtle) |

**Demo, explained:**

| Command | What it does |
|---|---|
| `ros2 run turtlesim turtle_teleop_key` | Starts a node that **publishes** velocity messages when you press arrow keys |
| `ros2 topic echo /turtle1/cmd_vel` | **Subscribes** from the terminal and prints every message |
| `rqt_graph` | Draws the live graph of nodes and topics |
| `ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"` | **You** become the publisher: sends one velocity message by hand |

**Visual:** Screenshot of `rqt_graph`: `/teleop_turtle → /turtle1/cmd_vel → /turtlesim`, next to diagram 2.

**Say this:** "This is exactly the navigation → `/cmd_vel` → motors chain from earlier. Replace the turtle with real wheels and it's our robot."

**Remember:** **Turtlesim is a tiny robot using the same pattern as the real one.**

---

## Slide 23 — Code, launch files, parameters, RViz

**On the slide**

| Command | What it does |
|---|---|
| `ros2 launch workshop_demos turtle_demo.launch.py` | Starts **two nodes at once**: turtlesim + our `draw_circle` node (code publishing to `/turtle1/cmd_vel`) |
| `ros2 param set /draw_circle speed 4.0` | Changes a node's setting **while it runs** |
| `ros2 pkg create --build-type ament_python --node-name hello_node my_first_pkg` | Generates a new package with a starter node, so you don't start from a blank page |
| `ros2 launch workshop_demos robot_demo.launch.py` | Starts a simulated robot arm with a laser + **RViz** to see it in 3D |

**Visual:** Screenshot of RViz: robot arm, red laser dots, TF axes.

**Say this:** "RViz is how you see what the robot sees and thinks. It's the tool you'll use most when debugging the real robot."

**Remember:** **Launch files start systems, parameters tune them, RViz shows them.**

---

# PART 10 — DEBUGGING

## Slide 24 — Something's not working: ask these in order

**On the slide**

1. **Which terminal am I in?** Read the prompt (laptop vs ROS desktop)
2. **Is the container running?** `docker ps` → is `ros-workshop` listed?
3. **Did I build?** `cd ~/ws && colcon build` → any **Failed**?
4. **Did I source?** `source ~/ws/install/setup.bash` in **this** tab
5. **Is my node running?** `ros2 node list`
6. **Are messages flowing?** `ros2 topic echo <topic>` / `ros2 topic hz <topic>` / `rqt_graph`

**Visual:** A flowchart that follows the stack from diagram 1: laptop → Docker → build → source → nodes → topics.

**Say this:** "Debugging is walking up the stack from slide 10. Most problems are in steps 1–4, not in your code."

**Remember:** **Debug from the bottom of the stack up.**

---

## Slide 25 — The 5 errors you'll see most

**On the slide**

| You see… | It means… | Fix |
|---|---|---|
| `ros2: command not found` | Wrong terminal (laptop) | Use the ROS desktop terminal |
| `docker: command not found` | Wrong terminal (ROS desktop) | Use the laptop terminal |
| `Package '…' not found` | Not built or not sourced | `colcon build`, then `source install/setup.bash` |
| `Cannot connect to the Docker daemon` | Docker Desktop is closed | Open it, wait for *Engine running* |
| Old output after editing code | Didn't rebuild | Save → `colcon build` → `source` → run |

**Remember:** **Read the error message. It usually tells you which layer is broken.**

---

# PART 11 — EVERYDAY WORKFLOW

## Slide 26 — The development loop

**On the slide**

```text
  git pull  →  edit (laptop, VS Code)  →  colcon build  →  source  →  ros2 run / launch  →  test
      ▲                                                                                   │
      └──────────────  commit + push to GitHub  →  test on the real robot  ◀──────────────┘
```

- Starting your day: `docker compose up -d` → `localhost:6080`
- Ending your day: `docker compose stop`

**Say this:** "That's it. Every feature on the robot, from vision to navigation, is built with this loop."

**Remember:** **Edit → build → source → run → test → push.**

---

## Slide 27 — Recap: can you explain it now?

**On the slide**

| Question | One-line answer |
|---|---|
| What is ROS 2? | A framework that lets robot programs talk to each other, plus tools |
| Why does our robot use it? | Separate parts (controller, logic, motors) built and tested independently |
| What is a node? | One program with one job |
| What is a topic? | A named channel nodes publish and subscribe to |
| Why GitHub? | One shared copy of the code, with full history, that reaches the robot |
| Why WSL2? | Windows needs a real Linux for Docker and ROS 2 |
| Why Docker? | Everyone gets the identical Ubuntu + ROS 2 computer |
| What is a workspace? | A folder of packages: `src/` in, `install/` out |
| What does `colcon build` do? | Builds `src/` into runnable programs in `install/` |
| Why `source setup.bash`? | Tells this terminal where the built packages are |
| Where does my code run? | Inside the container; edited on the laptop, seen in the browser |
| How do I start it? | `docker compose up -d` → `localhost:6080` |
| How do I check ROS works? | `ros2 node list` / `ros2 topic list` / turtlesim |
| Something broke? | Right terminal? Running? Built? Sourced? Then echo the topics |

**Say this:** "If you can answer these, you understand the system, not just the commands. Next: pick a team (vision, navigation, drive/simulation, docs)."
