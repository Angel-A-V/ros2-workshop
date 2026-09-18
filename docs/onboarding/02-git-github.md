# Git and GitHub

> **Audience:** New members
> **Status:** DRAFT — written 2026-09-16. Club-specific items are marked `TODO — needs verification`.

> **Note:** this page comes from the club's robot project onboarding ([Autonomous-Robot](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot)). For the ROS 2 workshop you only need [../01-install.md](../01-install.md); this page is extra background.

## Purpose

Install Git, create a GitHub account, sign in from the terminal, and get access to the club organization.

- **Windows:** do everything in the **Ubuntu (WSL)** terminal from step 01, not in PowerShell.
- **macOS:** use Terminal.

We use the **GitHub CLI (`gh`)** to sign in, because it handles passwords and tokens for you.

## Steps

### 1. Create a GitHub account

Sign up at <https://github.com/signup> if you do not have one. Your UC Merced email is fine.

### 2. Install Git and GitHub CLI

**macOS**

**Run on: MAC — Terminal**

```bash
xcode-select --install
```

Click **Install** in the window that appears (skip if it says already installed). Then install **Homebrew** by
following the command on <https://brew.sh>. At the end it prints **"Next steps"** — **run those commands**, then open a new Terminal window.

```bash
brew install gh
```

**Windows**

**Run on: WSL — Ubuntu terminal**

```bash
sudo apt install -y git gh
```

### 3. Configure Git (both)

**Run on: MAC — Terminal** or **WSL — Ubuntu terminal**

```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "the-email-on-your-github-account@example.com"
git config --global init.defaultBranch main
```

### 4. Sign in to GitHub (both)

```bash
gh auth login
```

Answer the prompts:

```text
? Where do you use GitHub?                             GitHub.com
? What is your preferred protocol for Git operations?  HTTPS
? Authenticate Git with your GitHub credentials?       Yes
? How would you like to authenticate GitHub CLI?       Login with a web browser
```

Copy the one-time code and approve it in your browser. On Windows the browser may not open by itself —
go to <https://github.com/login/device> and enter the code.

```bash
gh auth setup-git
gh auth status
```

### 5. Get access to the club organization

The code lives at <https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot>.

Send your **GitHub username** to a project lead so they can invite you.
`TODO — needs verification: who sends invites and where members post their username (Discord channel?).`

Accept the invite from your email or at <https://github.com/orgs/Robotics-Society-at-UC-Merced/invitation>.

## Expected Result

- `git --version` prints a version number.
- `gh auth status` shows `Logged in to github.com account <your-username>`.
- You are a member of **Robotics-Society-at-UC-Merced** on GitHub.

## If It Fails

| Problem | Solution |
|---|---|
| `brew: command not found` (macOS) | You skipped Homebrew's "Next steps". Re-run the install from <https://brew.sh> and run the commands it prints. |
| Do not want Homebrew (macOS) | Download the `gh` installer from <https://cli.github.com>. |
| `Unable to locate package gh` (Windows) | Follow <https://github.com/cli/cli/blob/trunk/docs/install_linux.md>, then continue. |
| `git` asks for a password on push | Run `gh auth setup-git` again. |

## Related

- Club branch and pull request rules: [../development/git-workflow.md](https://github.com/Robotics-Society-at-UC-Merced/Autonomous-Robot/blob/main/docs/development/git-workflow.md) (`TODO`)
- Next: [03-docker-installation.md](03-docker-installation.md)
