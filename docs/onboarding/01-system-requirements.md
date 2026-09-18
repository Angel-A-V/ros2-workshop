# System Requirements

> **Audience:** New members
> **Status:** DRAFT — written 2026-09-16 for the first software workshop. Club-specific items are marked `TODO — needs verification`.
> **Do steps 01–04 before the workshop.** Downloads are large; campus Wi-Fi during a workshop is slow.

> **Note:** this page comes from the club's robot project onboarding ([Autonomous-Robot](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot)). For the ROS 2 workshop you only need [../01-install.md](../01-install.md); this page is extra background.

## Purpose

Check that your laptop can run the project, and (Windows only) install WSL 2, which every later step needs.

Each command block says where to run it:

| Label | Where |
|---|---|
| **Run on: MAC — Terminal** | Terminal app (Applications → Utilities → Terminal) |
| **Run on: WINDOWS — PowerShell** | Normal Windows terminal |
| **Run on: WSL — Ubuntu terminal** | The Linux terminal you install below (Windows only) |
| **Run on: CONTAINER** | The ROS 2 terminal inside Docker (step 03) |

Most "command not found" problems come from typing a command in the wrong terminal.

## Requirements

| | Windows | macOS |
|---|---|---|
| Operating system | Windows 11 64-bit **23H2+**, or Windows 10 64-bit **22H2** (build 19045) | Current or two previous major macOS releases |
| Processor | 64-bit x86 with hardware virtualization enabled. ARM (Snapdragon) laptops: Docker support is Early Access — tell a lead | Apple Silicon (M1–M4) or Intel |
| Memory | 8 GB | 4 GB minimum, 8 GB+ recommended |
| Free disk | 20 GB+ (club guidance) | 20 GB+ (club guidance) |
| Admin rights | Needed for WSL install | Needed for Xcode tools and Homebrew |

Linux laptop? Install Docker Engine and Git with your package manager and follow the macOS-style commands. `TODO — write a Linux section if members need it.`

## Steps

### macOS — check your Mac

Open  → **About This Mac** and note the **Chip** and **macOS** version. Or:

**Run on: MAC — Terminal**

```bash
uname -m
sw_vers
```

`arm64` = Apple Silicon (same CPU architecture as the robot's Orange Pi 5). `x86_64` = Intel.
You need this to download the right Docker version in step 03.

If macOS is too old, update it: System Settings → General → Software Update.

That is all for macOS. Continue to [02-git-github.md](02-git-github.md).

### Windows — 1. check your PC

- Version: press **Win + R**, type `winver`, press Enter.
- Virtualization: **Task Manager → Performance → CPU** should show **Virtualization: Enabled**.

### Windows — 2. install WSL 2 and Ubuntu

WSL (Windows Subsystem for Linux) runs a real Ubuntu Linux inside Windows. ROS 2 and Docker both use it,
and we do all Git work inside it.

Right-click Start → **Terminal (Admin)**:

**Run on: WINDOWS — PowerShell (Administrator)**

```powershell
wsl --install
```

**Restart** when asked. After restarting, an Ubuntu window opens (or open **Ubuntu** from the Start menu).
Create a Linux **username** and **password** — the password does not show while typing. Remember it; `sudo` asks for it.

**Run on: WINDOWS — PowerShell**

```powershell
wsl --version
wsl -l -v
```

**Run on: WSL — Ubuntu terminal**

```bash
sudo apt update && sudo apt upgrade -y
```

## Expected Result

- macOS: you know your chip type and macOS is up to date.
- Windows: `wsl --version` shows **WSL 2.1.5 or newer** (Docker's minimum), and `wsl -l -v` lists **Ubuntu** with **VERSION 2**.

## If It Fails

| Problem | Solution |
|---|---|
| Windows version too old | Run Windows Update, then check again. |
| Virtualization: Disabled | Restart into BIOS/UEFI (often F2, F10, or Del) and enable **Intel VT-x** or **AMD-V / SVM Mode**. Ask a lead if unsure. |
| `wsl` not recognized, or version below 2.1.5 | `wsl --update`, then restart. |
| Ubuntu shows VERSION 1 | `wsl --set-version Ubuntu 2` |
| WSL error mentioning virtualization | Enable virtualization (above). |

## Related

- [../platforms/windows.md](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot/blob/main/docs/platforms/windows.md)
- [../platforms/macos.md](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot/blob/main/docs/platforms/macos.md)
- Next: [02-git-github.md](02-git-github.md)
