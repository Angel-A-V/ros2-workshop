# Part 2 — Workshop (follow along)

> **Before this:** finish [01-install.md](01-install.md). The turtle test in Step 6 must have worked.
> **Time:** about 75 minutes.

What you will do:

0. Learn how ROS 2 works: nodes, topics, messages (next section)
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

## How ROS 2 works (read this first)

### A robot is many small programs

A robot's software has to **sense** (cameras, lasers, joysticks), **think** (find objects, plan a path) and **act** (drive motors), all at the same time.
Instead of one giant program, ROS 2 splits this into many small programs called **nodes**. Each node does one job.

Here is a simple autonomous robot:

```text
 Camera Node  ──/camera/image──▶  Vision Node  ──/detected_objects──▶  Navigation Node  ──/cmd_vel──▶  Motor Controller
   (sense)                         (think)                               (decide)                         (act)
```

- The **boxes** are **nodes**: separate programs, one job each.
- The **arrows** are **topics**: named channels the data flows through.
- Each piece of data on a topic is a **message**. For example, one message on `/cmd_vel` says "go forward at 0.5 m/s and turn at 0.2 rad/s".

### Publishers and subscribers

| Word | Meaning | In the example above |
|---|---|---|
| **Node** | One program with one job | Camera Node, Vision Node, … |
| **Topic** | A named channel, like a group chat | `/camera/image`, `/cmd_vel` |
| **Message** | One piece of data on a topic, with a fixed type (shape) | One image; one velocity command |
| **Publisher** | A node that **sends** messages on a topic | Navigation Node publishes on `/cmd_vel` |
| **Subscriber** | A node that **listens** to a topic | Motor Controller subscribes to `/cmd_vel` |

Why this is useful:

- **Publishers don't know who is listening.** You can add a new node (a logger, a display) without changing anyone else's code.
- **Nodes are independent.** If the vision node crashes, the camera keeps running. Buy a better camera, and you replace one box.
- **Nodes find each other automatically.** There is no central server to start. Run two nodes and they connect by topic name.
- **Teams can work in parallel.** The vision team and the navigation team only need to agree on the topic name and message type.

### Other ways nodes talk

| Tool | Think of it as | Example |
|---|---|---|
| **Topic** | A group chat: a nonstop stream of messages | Camera images, velocity commands |
| **Service** | A question with one answer | "Spawn a turtle" → "done" |
| **Action** | A long task with progress updates you can cancel | "Drive to the door" → "50%… 80%… arrived" |
| **Parameter** | A setting you can change while a node runs | The robot's top speed |
| **Launch file** | A startup script | Start 5 nodes with one command |

In this workshop you will use topics, a service, parameters and launch files, and see each one live.

### How this maps to what you'll do today

| Robot | Today in turtlesim |
|---|---|
| Navigation Node (decides how to move) | `turtle_teleop_key` (your arrow keys) or our `draw_circle` code |
| `/cmd_vel` topic | `/turtle1/cmd_vel` topic |
| Motor Controller (moves the wheels) | `turtlesim_node` (moves the turtle) |

The club's real robot works the same way: `game controller node → driving logic node → motor driver nodes → motors`.

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

> 💡 **What just happened?** You started **two nodes**, two separate programs.
> `turtle_teleop_key` reads your keyboard and **publishes** velocity messages.
> `turtlesim_node` **subscribes** to those messages and moves the turtle.
> You never told them about each other. They found each other because they use the same **topic name**.
>
> `ros2 run <package> <program>` means "start this program from this package". `turtlesim` is the package; `turtlesim_node` and `turtle_teleop_key` are programs inside it.

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

Now ask ROS **about** the topic:

```bash
ros2 topic info /turtle1/cmd_vel
```

It shows the topic's **message type** (`geometry_msgs/msg/Twist`), how many nodes **publish** on it, and how many **subscribe** to it.

See what a `Twist` message contains:

```bash
ros2 interface show geometry_msgs/msg/Twist
```

A `Twist` is two sets of `x, y, z` numbers: **linear** (moving) and **angular** (turning). The turtle only uses `linear.x` (forward/back) and `angular.z` (turn left/right).
Real robots use this **same message type** for velocity commands.

> 💡 **Why this matters:** `ros2 topic echo` is a **subscriber you control from the terminal**. It's the #1 debugging tool:
> "Is my node actually sending anything? What values?" You'll use it constantly on the real robot.

### 2.3 See the whole system

```bash
rqt_graph
```

You see: `/teleop_turtle` → `/turtle1/cmd_vel` → `/turtlesim`. The ovals are **nodes**. The arrow is the **topic**.
Close the rqt window when done.

> 💡 Compare it with the robot diagram at the top of this page: `/teleop_turtle` is the "navigation node", `/turtle1/cmd_vel` is `/cmd_vel`,
> and `/turtlesim` is the "motor controller". Same pattern, simpler robot.

### 2.4 Be the controller yourself

Send a message by hand. The turtle drives in a curve:

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
```

Change the numbers and run it again. Negative `z` turns the other way.

> 💡 **What just happened?** The terminal became a **publisher**. The turtle doesn't care whether messages come from the keyboard node,
> from code, or from you typing: anything that publishes a `Twist` on `/turtle1/cmd_vel` can drive it.
> That's how we can test robot code with fake inputs before the real robot is involved.

### 2.5 Services: ask a node to do something

Topics are a stream of messages. A **service** is a single request with a reply. Ask turtlesim for a second turtle:

```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"
```

> 💡 **Topic vs service:** a topic is a stream nobody replies to. A service is a request that waits for a reply,
> and here the reply is the new turtle's name. Use services for "do this one thing" (reset, spawn, save a map).
> List all services with `ros2 service list`.

Now stop everything: **Ctrl + C** in Tab 1 and Tab 2.

---

## 3. Build a workspace with colcon

A **package** is a folder of ROS code. A **workspace** is a folder of packages. **`colcon build`** builds every package in the workspace.
`~/ws` already contains one package, `workshop_demos`.

```text
ws/                      ← the workspace: you ALWAYS build from here
├── src/                 ← source code: the only folder you edit
│   └── workshop_demos/  ← a package
│       ├── package.xml         ← the package's "ID card": name + what it depends on
│       ├── setup.py            ← tells the build which programs this package provides
│       ├── workshop_demos/     ← the Python code (nodes)
│       └── launch/             ← launch files
├── build/    ┐
├── install/  ├─ created by colcon build. Never edit these.
└── log/      ┘
```

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

> 💡 **What do these two commands actually do?**
>
> - **`colcon build`** finds every package in `src/`, builds it, and puts the runnable result in `install/`.
>   If you change your code, **build again**, or ROS keeps running the old version.
> - **`source install/setup.bash`** tells **this terminal** "also look in `install/` for ROS packages". Without it, the terminal
>   only knows about the built-in ROS packages, so yours shows up as "not found". It only affects the tab you run it in.
>
> The loop: **edit → build → source → run.**

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

> 💡 **Launch file:** `turtle_demo.launch.py` is a short Python file listing which nodes to start.
> On the real robot, one launch file starts the controller, the driving logic and the motor drivers together.
>
> **Parameters** are a node's settings. You just changed them **without restarting or editing code**. On a robot, that's how you tune things like top speed.

#### Read the code: what a node looks like

On your **laptop**, open `ros2-workshop/ws/src/workshop_demos/workshop_demos/draw_circle.py`. The important parts:

```python
class DrawCircle(Node):                                   # 1. Our program is a ROS "Node"

    def __init__(self):
        super().__init__('draw_circle')                   # 2. Give the node a name (what `ros2 node list` shows)
        self.declare_parameter('speed', 2.0)              # 3. Settings you can change with `ros2 param set`
        self.declare_parameter('turn', 1.0)
        self.publisher = self.create_publisher(           # 4. "I will PUBLISH Twist messages on /turtle1/cmd_vel"
            Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.send_command)  # 5. Call send_command every 0.1 s (10 times per second)

    def send_command(self):
        msg = Twist()                                     # 6. Make an empty velocity message
        msg.linear.x = float(self.get_parameter('speed').value)   #    forward speed
        msg.angular.z = float(self.get_parameter('turn').value)   #    turning speed
        self.publisher.publish(msg)                       # 7. Send it


def main(args=None):
    rclpy.init(args=args)                                 # 8. Start ROS
    node = DrawCircle()
    rclpy.spin(node)                                      # 9. Keep running and let the timer fire until Ctrl + C
```

That's the whole pattern: **create a node → create a publisher → publish messages**. A subscriber is the mirror image:
`self.create_subscription(Twist, '/turtle1/cmd_vel', self.callback, 10)`, and ROS calls `callback(msg)` every time a message arrives.

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

> 💡 `ros2 pkg create` writes the boilerplate for you: `package.xml`, `setup.py`, and a starter file at
> `my_first_pkg/my_first_pkg/hello_node.py`. `--node-name hello_node` also registers it as a program you can `ros2 run`.

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

> 💡 **What is RViz actually doing?** RViz is just another node. It **subscribes** to topics like `/scan` and `/joint_states`
> and draws what it receives. It doesn't simulate anything. If a topic stops publishing, that display goes blank.
>
> - The **robot model** (URDF) is a description of the robot's parts and joints.
> - **TF frames** track where every part is relative to every other part: "the laser is 10 cm above joint 2".
>   Robots need this to turn "the laser saw something 1 m ahead" into "there's an obstacle at this spot in the room".
>
> Run `rqt_graph` in Tab 2: RViz shows up as a node subscribed to the robot's topics.

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
