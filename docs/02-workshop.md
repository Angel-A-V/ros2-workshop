# Part 2 — Workshop (follow along)

> **Before this:** finish [01-install.md](01-install.md). The turtle test in Step 6 must have worked.
> **Time:** about 75 minutes.

What you will do:

1. Start the ROS desktop
2. Drive a turtle and see how ROS programs talk to each other
3. Build a ROS workspace with `colcon build`
4. Create, build and change **your own** ROS package
5. See a robot in **RViz**

---

## The one idea to remember: two computers

| | Your laptop | The ROS desktop (in the browser) |
|---|---|---|
| What it is | macOS, or Windows + Ubuntu (WSL) | Ubuntu 22.04 + ROS 2 Humble, running in Docker |
| What you type there | `docker compose ...`, `git ...`, open VS Code | `ros2 ...`, `colcon build`, `rqt_graph`, `rviz2` |
| The workspace folder | `~/ros2-workshop/ws` | `~/ws` (**the same folder**, shared) |

A file you save in `ros2-workshop/ws` on your laptop shows up instantly in `~/ws` in the ROS desktop, and the other way around.
Keep all your work in `~/ws`. Files saved elsewhere in the ROS desktop can be lost.

---

## 1. Start the ROS desktop

**LAPTOP — Terminal** (Mac: Terminal · Windows: Ubuntu)

```bash
cd ~/ros2-workshop
docker compose up -d
```

Open **<http://localhost:6080>** → **Connect**.

Open a terminal in the ROS desktop: **Applications** → **System Tools** → **MATE Terminal**.

Useful in the ROS desktop terminal:

- **New tab:** **Ctrl + Shift + T** (you will use 3 tabs)
- **Stop a running program:** **Ctrl + C**
- **Auto-complete:** press **Tab** while typing. It saves a lot of typing.
- **Paste from your laptop:** open the small tab on the left edge of the browser page → 📋 **Clipboard** → paste your text there → in the terminal press **Ctrl + Shift + V**.

From here on, **every command runs in the ROS desktop terminal** unless it says LAPTOP.

---

## 2. Nodes and topics with turtlesim

A ROS system is made of small programs called **nodes**. Nodes send each other messages on named channels called **topics**.

### 2.1 Start two nodes

**Tab 1** — the simulator (a window with a turtle opens):

```bash
ros2 run turtlesim turtlesim_node
```

**Tab 2** — the keyboard controller:

```bash
ros2 run turtlesim turtle_teleop_key
```

Click inside **Tab 2** and press the **arrow keys**. The turtle moves.

> Arrow keys only work while Tab 2 is selected. If the turtle doesn't move, click Tab 2 again.

### 2.2 Look inside

**Tab 3:**

```bash
ros2 node list
```

```text
/teleop_turtle
/turtlesim
```

```bash
ros2 topic list
```

The important one is `/turtle1/cmd_vel` ("command velocity"). Watch the messages on it:

```bash
ros2 topic echo /turtle1/cmd_vel
```

Drive with the arrow keys in Tab 2 and watch Tab 3. Each key press is a message: a **linear** (forward) speed and an **angular** (turning) speed.
Stop the echo with **Ctrl + C**.

### 2.3 See the whole system

```bash
rqt_graph
```

You see: `/teleop_turtle` → `/turtle1/cmd_vel` → `/turtlesim`. The ovals are **nodes**. The arrow is the **topic**.
Close the rqt window when done.

### 2.4 Be the controller yourself

Send a message by hand. The turtle drives in a curve:

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
```

Change the numbers and run it again. Negative `z` turns the other way.

### 2.5 Services: ask a node to do something

Topics are a stream of messages. A **service** is a single request with a reply. Ask turtlesim for a second turtle:

```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"
```

Now stop everything: **Ctrl + C** in Tab 1 and Tab 2.

---

## 3. Build a workspace with colcon

A **package** is a folder of ROS code. A **workspace** is a folder of packages. **`colcon build`** builds every package in the workspace.
`~/ws` already contains one package, `workshop_demos`.

**Tab 1:**

```bash
cd ~/ws
ls src
colcon build
```

```text
Starting >>> workshop_demos
Finished <<< workshop_demos [1.5s]

Summary: 1 package finished
```

> A yellow `stderr output` / `SetuptoolsDeprecationWarning` message is normal. Only **`Failed`** is a problem.

`colcon build` created three folders: `build/`, `install/` and `log/`. Now tell this terminal about the new package:

```bash
source install/setup.bash
```

> ⚠️ **Remember this rule:** after every build, **and in every new tab**, run `source ~/ws/install/setup.bash`.
> Most "package not found" errors come from forgetting it.

### 3.1 Launch several nodes with one command

A **launch file** starts several nodes at once. This one starts turtlesim and our `draw_circle` node:

```bash
ros2 launch workshop_demos turtle_demo.launch.py
```

The turtle drives in circles by itself. That is code publishing to `/turtle1/cmd_vel`, the same thing you did by hand in 2.4.

**Tab 2** — change the node's **parameters** while it runs:

```bash
source ~/ws/install/setup.bash
ros2 param list /draw_circle
ros2 param set /draw_circle speed 4.0
ros2 param set /draw_circle turn -2.0
```

Now read the code. On your **laptop**, open `ros2-workshop/ws/src/workshop_demos/workshop_demos/draw_circle.py`.
It is about 20 lines: create a publisher, then send a message 10 times per second.

Stop with **Ctrl + C** in Tab 1.

---

## 4. Your own package

### 4.1 Create it

**Tab 1:**

```bash
cd ~/ws/src
ros2 pkg create --build-type ament_python --node-name hello_node my_first_pkg
```

ROS generates a package called `my_first_pkg` with a ready-to-run Python node, `hello_node`.

### 4.2 Build it and run it

Always build from the **top** of the workspace (`~/ws`), never from `src`:

```bash
cd ~/ws
colcon build
source install/setup.bash
ros2 run my_first_pkg hello_node
```

```text
Hi from my_first_pkg.
```

### 4.3 Change it on your laptop

1. Open the workspace in VS Code (or any editor) on your **laptop**:

   **LAPTOP — Terminal**

   ```bash
   code ~/ros2-workshop/ws
   ```

   No `code` command? Open VS Code → **File → Open Folder** → pick `ros2-workshop/ws`.
   (Windows: install the **WSL** extension in VS Code first, then run `code ~/ros2-workshop/ws` from Ubuntu.)

2. Open `src/my_first_pkg/my_first_pkg/hello_node.py`.
3. Change the text inside `print(...)` and **save**.
4. Back in the **ROS desktop, Tab 1**:

   ```bash
   cd ~/ws
   colcon build
   source install/setup.bash
   ros2 run my_first_pkg hello_node
   ```

Your new message prints. **This is the loop you'll use for all ROS code: edit → `colcon build` → `source` → run.**

### 4.4 Challenge (if you finish early)

In `workshop_demos/draw_circle.py`, change the default `speed` and `turn` values, rebuild, and launch `turtle_demo.launch.py` again.
Can you make the turtle drive a **tiny** circle? A **huge** one?

---

## 5. RViz: see a robot

**RViz** shows what a robot "sees" and "thinks": its 3D model, sensor data, maps and coordinate frames.

**Tab 1:**

```bash
cd ~/ws
source install/setup.bash
ros2 launch workshop_demos robot_demo.launch.py
```

RViz opens with a simulated robot:

| In RViz | What it is | Topic |
|---|---|---|
| Moving 2-joint arm | The robot's 3D model, with joints moving | `/robot_description`, `/joint_states` |
| Red dots | A laser scanner's measurements | `/scan` |
| Gray and black squares | A map | `/map` |
| Colored axes with names | **TF frames**: where every part of the robot is | `/tf` |

Move the view: **left-drag** to rotate, **scroll** to zoom, **Shift + left-drag** to pan.
Untick and tick the boxes in the **Displays** panel on the left.

**Tab 2** — the same data as text:

```bash
source ~/ws/install/setup.bash
ros2 topic list
ros2 topic hz /scan
ros2 topic echo /joint_states --once
rqt_graph
```

Stop with **Ctrl + C** in Tab 1.

---

## 6. What you learned

| Concept | What it means | Command you used |
|---|---|---|
| **Node** | A program in a ROS system | `ros2 run`, `ros2 node list` |
| **Topic** | A named channel nodes publish and subscribe to | `ros2 topic list / echo / pub / hz` |
| **Service** | A single request and reply | `ros2 service call` |
| **Parameter** | A setting you can change while a node runs | `ros2 param set` |
| **Package** | A folder of ROS code | `ros2 pkg create` |
| **Workspace + colcon** | Where packages live, and how they are built | `colcon build`, `source install/setup.bash` |
| **Launch file** | Starts many nodes with one command | `ros2 launch` |
| **RViz** | 3D view of robot data | `rviz2` |

A real robot works exactly the same way. A game controller is a node publishing joystick messages, a driving node turns them into
velocity commands (like `/turtle1/cmd_vel`), and a motor-driver node sends them to the motors.

## 7. Stop the ROS desktop

**LAPTOP — Terminal**

```bash
cd ~/ros2-workshop
docker compose stop
```

Next time: `docker compose up -d` and open <http://localhost:6080>. Your packages in `ws/` are still there.

---

## If something fails

| Problem | What to do |
|---|---|
| `Package 'workshop_demos' not found` / `Package 'my_first_pkg' not found` | Run `source ~/ws/install/setup.bash` in that tab. Still failing? `cd ~/ws && colcon build` first. |
| `ros2 run` still prints the old message | Save the file, then `colcon build` and `source install/setup.bash` again. |
| `ros2: command not found` / `colcon: command not found` | You are in your **laptop** terminal. Use the terminal inside the browser desktop. |
| `docker: command not found` | You are in the **ROS desktop** terminal. Use your laptop terminal. |
| `build/`, `install/`, `log/` appeared inside `src/` | You ran `colcon build` inside `src`. Delete those three folders from `src`, then `cd ~/ws && colcon build`. |
| `Summary: 0 packages finished` | Wrong folder. Build from `~/ws`. |
| Arrow keys don't move the turtle | Click inside the `turtle_teleop_key` tab. |
| A window didn't appear | Check the taskbar at the bottom of the ROS desktop, or behind other windows. |
| RViz: *Frame [world] does not exist* | Wait 5 seconds. If it stays, read Tab 1 for red error text. |
| RViz window is black or crashes | Run `export LIBGL_ALWAYS_SOFTWARE=1` in that tab, then launch again. |
| RViz shows no robot model | **Displays → RobotModel → Description Topic → Durability Policy:** set **Transient Local**. |
| `~/ws` is empty in the ROS desktop | You started Docker from the wrong folder. On your laptop: `cd ~/ros2-workshop && docker compose down && docker compose up -d`. |
| Everything is slow | Close windows you aren't using. Docker Desktop → Settings → Resources → Memory: at least 4 GB. |

### Build the RViz view by hand (backup, or to learn how)

```bash
ros2 launch dummy_robot_bringup dummy_robot_bringup.launch.py
```

In another tab run `rviz2`, then:

1. **Global Options → Fixed Frame:** type `world`.
2. **Add** (bottom left) → **RobotModel** → OK. Expand it → **Description Topic:** `/robot_description`, **Durability Policy:** `Transient Local`.
3. **Add** → **By topic** tab → `/scan` → **LaserScan** → OK.
4. **Add** → **TF** → OK.

## Keep learning

- Official ROS 2 Humble tutorials (start with *Beginner: CLI tools*): <https://docs.ros.org/en/humble/Tutorials.html>
