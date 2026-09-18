# Part 1 — Install (do this before the workshop)

> **Time:** about 45 minutes, mostly waiting for downloads. Do it **at home on good Wi-Fi**.
> **You need:** a Mac or Windows laptop, 8 GB RAM or more, 20 GB free disk space. No GitHub account needed.

When you finish, you will have a full Ubuntu + ROS 2 desktop running in your web browser.
If you get stuck, take a **screenshot of the error** and bring it to the workshop. We will fix it together.

---

## How to read this guide

Every command box says **where** to type it:

| Label | Where |
|---|---|
| **MAC — Terminal** | macOS: press **⌘ + Space**, type `Terminal`, press Enter |
| **WINDOWS — PowerShell (Admin)** | Start menu → type `PowerShell` → right-click → **Run as administrator** |
| **WINDOWS — Ubuntu** | Start menu → **Ubuntu** (you install it in step 1) |

Type (or copy/paste) the command, then press **Enter**. Do the steps **in order**.

---

## Step 1 — Windows only: install WSL (Ubuntu on Windows)

Mac users: skip to **Step 2**.

Docker on Windows uses WSL, a built-in way to run Ubuntu Linux inside Windows.

**WINDOWS — PowerShell (Admin)**

```powershell
wsl --install
```

1. When it finishes, **restart your computer**.
2. After restarting, an **Ubuntu** window opens by itself (if not: Start menu → **Ubuntu**).
3. It asks you to create a **username** and **password**. Pick something simple you will remember.
   The password shows nothing while you type. That is normal.

Check it:

**WINDOWS — PowerShell**

```powershell
wsl -l -v
```

You should see `Ubuntu` with `VERSION` **2**.

> ⚠️ **Windows users: from now on, type every command in the Ubuntu window**, not PowerShell.

---

## Step 2 — Install Docker Desktop

Docker runs the ROS 2 desktop for you, so you don't have to install ROS on your laptop.

### macOS

1. Find your chip: Apple menu  → **About This Mac**. It says **Apple M1/M2/M3/M4…** (Apple chip) or **Intel**.
2. Go to <https://docs.docker.com/desktop/setup/install/mac-install/> and download the version for **your chip**.
3. Open the downloaded `Docker.dmg` and drag **Docker** into **Applications**.
4. Open **Docker** from Applications. Accept the agreement → **Use recommended settings** → enter your Mac password if asked.
   Signing in to a Docker account is **optional**. You can skip it.
5. Apple chip only, install Rosetta (helps some programs run):

   **MAC — Terminal**

   ```bash
   softwareupdate --install-rosetta --agree-to-license
   ```

### Windows

1. Go to <https://docs.docker.com/desktop/setup/install/windows-install/> and download **Docker Desktop for Windows – x86_64**.
2. Run the installer. Keep **Use WSL 2 instead of Hyper-V** checked.
3. Open **Docker Desktop**, accept the agreement. Signing in is **optional**.
4. In Docker Desktop: ⚙️ **Settings** → **Resources** → **WSL integration** → turn on **Ubuntu** → **Apply & restart**.

### Check Docker works (both)

Wait until Docker Desktop says **Engine running** (bottom-left of its window). Then:

**MAC — Terminal** or **WINDOWS — Ubuntu**

```bash
docker run --rm hello-world
```

✅ You should see **`Hello from Docker!`**

> Docker Desktop must be **open** whenever you use Docker.

---

## Step 3 — Check you have Git

Git downloads the workshop files.

**MAC — Terminal** or **WINDOWS — Ubuntu**

```bash
git --version
```

- ✅ It prints something like `git version 2.x` → go to Step 4.
- **Mac:** if a window pops up asking to install **command line developer tools**, click **Install**, wait until it finishes, then run `git --version` again.
- **Windows:** if it says `command not found`, run `sudo apt update && sudo apt install -y git` (it asks for the Ubuntu password from Step 1).

---

## Step 4 — Download the workshop files

**MAC — Terminal** or **WINDOWS — Ubuntu**

```bash
cd ~
git clone https://github.com/Angel-A-V/ros2-workshop.git
cd ros2-workshop
ls
```

✅ You should see `README.md  compose.yaml  docs  ws`.

> ⚠️ **Windows:** do this in the **Ubuntu** window, so the folder is in Ubuntu (`~/ros2-workshop`), not in `C:\`.

---

## Step 5 — Download the ROS 2 desktop (the big download)

**MAC — Terminal** or **WINDOWS — Ubuntu**

```bash
cd ~/ros2-workshop
docker compose pull
```

This downloads several GB. It can take 10–30 minutes. ✅ It is done when every line says **Pulled**.
If it stops or fails, run the same command again. It continues where it left off.

---

## Step 6 — Test it

**1. Start the ROS desktop:**

**MAC — Terminal** or **WINDOWS — Ubuntu**

```bash
cd ~/ros2-workshop
docker compose up -d
```

✅ You see `Container ros-workshop  Started`.

**2. Open it:** wait **20 seconds**, then open **<http://localhost:6080>** in your web browser and click **Connect**.
✅ You see an Ubuntu desktop.

**3. Open a terminal inside it:** click **Applications** (top-left) → **System Tools** → **MATE Terminal**. Type:

```bash
ros2 run turtlesim turtlesim_node
```

✅ A window with a **turtle** appears. 🎉 **You are ready for the workshop.**

Close it with **Ctrl + C** in that terminal.

**4. Stop the ROS desktop:** back in your **laptop** terminal (Mac Terminal / Windows Ubuntu):

```bash
cd ~/ros2-workshop
docker compose stop
```

---

## Checklist — bring this to the workshop

```text
[ ] Docker Desktop installed and it says "Engine running"
[ ] docker run --rm hello-world  →  "Hello from Docker!"
[ ] ~/ros2-workshop folder exists
[ ] docker compose pull finished
[ ] The turtle appeared at http://localhost:6080
[ ] Laptop + charger
```

---

## If something fails

| Problem | What to do |
|---|---|
| `docker: command not found` (Mac) | Open Docker Desktop, then open a **new** Terminal window. |
| `docker: command not found` (Windows Ubuntu) | Docker Desktop → Settings → Resources → WSL integration → turn on **Ubuntu** → Apply & restart. Reopen Ubuntu. |
| `Cannot connect to the Docker daemon` | Docker Desktop is not open or still starting. Open it and wait for **Engine running**. |
| "This app cannot run on this Mac" | You downloaded the wrong chip version. Download the other one. |
| Docker Desktop says WSL needs updating | In PowerShell: `wsl --update`, then restart Docker Desktop. |
| `wsl --install` shows help text instead of installing | WSL is already there. Run `wsl --install -d Ubuntu`. |
| `no configuration file provided: not found` | You are not in the workshop folder. Run `cd ~/ros2-workshop` first. |
| `fatal: destination path 'ros2-workshop' already exists` | You already downloaded it. Just `cd ~/ros2-workshop`. |
| `no space left on device` | Free up disk space (you need ~20 GB), then run `docker compose pull` again. |
| Browser: *can't connect* / *connection reset* | Wait 30 seconds and refresh. Check it is running: `docker ps` should list `ros-workshop`. |
| `port is already allocated` | Something else uses port 6080. Run `docker ps`, then `docker stop <that name>`. |
| Black screen after **Connect** | Refresh the page. Still black: `docker compose restart`, wait 30 s, refresh. |
| Desktop is too big for the window | Open the small tab on the left edge of the page → ⚙️ **Settings** → **Scaling mode: Local scaling**. |
| Typed `docker` in the desktop's terminal → `command not found` | That is expected. `docker` commands go in your **laptop** terminal, not the one in the browser. |

Next: **[02-workshop.md](02-workshop.md)** (we do this together at the workshop).
