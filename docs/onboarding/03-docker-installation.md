# Docker Installation

> **Audience:** New members
> **Status:** DRAFT — written 2026-09-16. Steps follow Docker's official install guides. Steps follow Docker's official install guides.

> **Note:** this page comes from the club's robot project onboarding ([Autonomous-Robot](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot)). For the ROS 2 workshop you only need [../01-install.md](../01-install.md); this page is extra background.

## Purpose

Install Docker Desktop on macOS or Windows (WSL 2), verify it runs, and run a first ROS 2 test.

Docker runs ROS 2 (a Linux program) in a **container**, so everyone has the same setup no matter what laptop they use.

## Steps

### 1. Install Docker Desktop

**macOS**

1. Go to <https://docs.docker.com/desktop/setup/install/mac-install/>.
2. Download the version for your chip from step 01: **Apple silicon** or **Intel**. Picking the wrong one is the most common mistake.
3. Open `Docker.dmg` and drag **Docker** into **Applications**.
4. Open Docker, accept the agreement, choose **Use recommended settings**. A Docker account is optional.
5. Apple Silicon (recommended): install Rosetta 2.

   **Run on: MAC — Terminal**

   ```bash
   softwareupdate --install-rosetta --agree-to-license
   ```

**Windows** (finish WSL in [01-system-requirements.md](01-system-requirements.md) first)

1. Download **Docker Desktop for Windows** from <https://docs.docker.com/desktop/setup/install/windows-install/>
   (normal x86_64 installer unless you have an ARM laptop).
2. Run **Docker Desktop Installer.exe** and keep **Use WSL 2 instead of Hyper-V** selected.
3. Start **Docker Desktop** and accept the agreement. A Docker account is optional.
4. **Settings → Resources → WSL integration** → turn on **Ubuntu** → **Apply & restart**.

Wait until Docker Desktop shows **Engine running**. Docker Desktop must be open whenever you use Docker.

### 2. Verify Docker

**Run on: MAC — Terminal** or **WSL — Ubuntu terminal**

```bash
docker run --rm hello-world
```

### 3. Download ROS 2 Humble

The robot uses ROS 2 **Humble**. The official image has native Apple Silicon and Intel/AMD versions; Docker picks the right one.
It is several hundred MB — use good Wi-Fi.

```bash
docker pull ros:humble
```

### 4. First ROS 2 test

Start a container named `ros-test`:

```bash
docker run -it --rm --name ros-test ros:humble bash
```

The prompt changes to something like `root@3f2a1b...:/#` — you are **inside the container**.

**Run on: CONTAINER (terminal 1)**

```bash
ros2 topic pub /chatter std_msgs/msg/String "{data: 'hello robot'}"
```

Leave it running. Open a **second** terminal (Mac: **⌘ + N** in Terminal; Windows: a new Ubuntu window) and attach to the same container:

**Run on: MAC — Terminal** or **WSL — Ubuntu terminal** (terminal 2)

```bash
docker exec -it ros-test bash
```

**Run on: CONTAINER (terminal 2)**

```bash
source /opt/ros/humble/setup.bash
ros2 topic list
ros2 topic echo /chatter
```

Stop with **Ctrl + C** in each terminal, then type `exit`. The container is removed automatically (`--rm`); the image stays downloaded.

## Expected Result

- `hello-world` prints `Hello from Docker!`
- `ros2 topic list` includes `/chatter`, and `ros2 topic echo` repeats:

  ```text
  data: hello robot
  ---
  ```

You just ran two ROS 2 programs talking over a **topic** — the same way the robot's gamepad node talks to its motor nodes.

## If It Fails

| Problem | Solution |
|---|---|
| `docker: command not found` (macOS) | Open Docker Desktop, then open a new Terminal window. |
| `docker: command not found` (Windows, Ubuntu) | Turn on WSL integration for Ubuntu (step 1.4), then reopen the Ubuntu terminal. |
| `Cannot connect to the Docker daemon` | Docker Desktop is not running. Start it and wait for **Engine running**. |
| "This app cannot run on this Mac" | Wrong chip version. Download the other one. |
| Docker Desktop says WSL needs updating | `wsl --update` in PowerShell, then restart Docker Desktop. |
| `ros2: command not found` in terminal 2 | Run `source /opt/ros/humble/setup.bash`. `docker exec` terminals need it every time. |
| `No such container: ros-test` | Terminal 1 is not running. Check with `docker ps`. |
| `container name "/ros-test" is already in use` | `docker rm -f ros-test`, then try again. |
| `echo` shows nothing | Wait a few seconds for discovery; make sure terminal 1 is still publishing. |

## Related

- [../platforms/macos.md](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot/blob/main/docs/platforms/macos.md)
- [../platforms/windows.md](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot/blob/main/docs/platforms/windows.md)
- Next: [04-clone-project.md](04-clone-project.md)
