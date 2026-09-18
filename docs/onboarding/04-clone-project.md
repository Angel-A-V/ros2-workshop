# Clone the Project

> **Audience:** New members
> **Status:** DRAFT — written 2026-09-16. Repository layout section is `TODO`.

> **Note:** this page comes from the club's robot project onboarding ([Autonomous-Robot](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot)). For the ROS 2 workshop you only need [../01-install.md](../01-install.md); this page is extra background.

## Purpose

Clone the Autonomous-Robot repository and open it in an editor.

## Steps

### 1. Clone

**Run on: MAC — Terminal** or **WSL — Ubuntu terminal**

```bash
mkdir -p ~/robotics
cd ~/robotics
git clone https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot.git
cd Autonomous-Robot
git log --oneline -3
ls
```

> ⚠️ **Windows:** clone inside Ubuntu (`~/robotics`), **not** in `C:\Users\...` or `/mnt/c/...`.
> Windows folders are slow in Docker and can change line endings in a way that breaks Linux scripts.
> To see the files in File Explorer, run `explorer.exe .` from inside the folder.

> ⚠️ **macOS:** do not clone into iCloud-synced Desktop or Documents folders. Syncing can corrupt Git folders.

### 2. (Recommended) Open in VS Code

1. Install VS Code from <https://code.visualstudio.com/>.
2. **Windows:** install the **WSL** extension (Microsoft).
   **macOS:** press **⌘ + Shift + P** → **Shell Command: Install 'code' command in PATH**.
3. Open the project:

```bash
cd ~/robotics/Autonomous-Robot
code .
```

On Windows, the bottom-left corner of VS Code should say **WSL: Ubuntu**.

### 3. Repository layout

`TODO — describe robot/src/master, robot/src/ros_odrive, robot/src/joystick, and docs/.`

> ⚠️ **Do not build the whole repository yet.** The inherited code has known build problems
> (see [../lead/known-issues.md](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot/blob/main/docs/lead/known-issues.md)). The club Docker environment for this repo is `TODO — not yet created`.

## Expected Result

`git log` shows recent commits, and `ls` shows folders such as `robot` and `docs`.

## If It Fails

| Problem | Solution |
|---|---|
| `Repository not found` | You are not in the organization yet, or not signed in. Check `gh auth status` and step 02.5. |
| `Permission denied` / asks for password | Run `gh auth setup-git`. |
| `code: command not found` | Redo step 2 above, then open a new terminal. |

## Setup checklist (steps 01–04)

```text
[ ] Windows only: wsl -l -v shows Ubuntu, VERSION 2
[ ] gh auth status shows you logged in
[ ] docker run --rm hello-world works
[ ] ros:humble downloaded and the /chatter test worked
[ ] ~/robotics/Autonomous-Robot exists
```

## Related

- Next: [../02-workshop.md](../02-workshop.md) (workshop)
