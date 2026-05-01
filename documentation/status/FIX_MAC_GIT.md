# Fix Git on Your Mac

## Problem

Your Mac's local copy doesn't have the GitHub remote configured, so `git pull origin main` fails.

## Solution - Run These Commands on Your Mac

### Step 1: Open Terminal on Mac

```bash
cd ~/Downloads/ALPHAVOXWAKESUP-main
```text
### Step 2: Check Current Remote

```bash
git remote -v
```text
**If you see nothing**, the remote isn't configured at all.

**If you see a different URL**, it's pointing to the wrong place.

### Step 3: Add or Fix the Remote

**If remote doesn't exist:**

```bash
git remote add origin <https://github.com/Nathaniel-AI/ALPHAVOXWAKESUP.git>
```text
**If remote exists but wrong URL:**

```bash
git remote set-url origin <https://github.com/Nathaniel-AI/ALPHAVOXWAKESUP.git>
```text
### Step 4: Verify It's Fixed

```bash
git remote -v
```text
**Should show:**

```text
origin  <https://github.com/Nathaniel-AI/ALPHAVOXWAKESUP.git> (fetch)
origin  <https://github.com/Nathaniel-AI/ALPHAVOXWAKESUP.git> (push)
```text
### Step 5: Pull the Latest Code

```bash
git fetch origin
git reset --hard origin/main
```text
**Warning:** `git reset --hard` will **delete any local changes** you haven't committed. If you have changes you want to keep, do this instead:

```bash
git fetch origin
git status  # Check if you have uncommitted changes
git stash   # Save your changes temporarily (if any)
git reset --hard origin/main
git stash pop  # Restore your changes (if you stashed)
```text
### Step 6: Verify You Have the Latest

```bash
git log --oneline -3
```text
**Should show:**

```text
e265685 Add security framework, testing suite, performance tools, and funding proposal
ce56738 upgrade
1a25fcf Update README.md
```text
### Step 7: Check for New Files

```bash
ls -la | grep -E "(FUNDING|SECURITY|security_module|tests)"
```text
**Should show:**
- `FUNDING_PROPOSAL.md`
- `SECURITY_APPLIED.md`
- `security_module.py`
- `tests/` directory
- `CRITICAL_TECHNICAL_REVIEW.md`
- `CRITICAL_ISSUES_ROADMAP.md`

---

## Why This Happened

You likely downloaded the repository as a ZIP file from GitHub, which doesn't include the git configuration. When you ran `git init`, it created a new empty git repository without any remote connection.

## Alternative: Fresh Download

If the above doesn't work, you can:

1. **Delete the old folder:**

   ```bash
   cd ~/Downloads
   rm -rf ALPHAVOXWAKESUP-main
   ```

2. **Clone fresh from GitHub:**

   ```bash
   git clone <https://github.com/Nathaniel-AI/ALPHAVOXWAKESUP.git>
   cd ALPHAVOXWAKESUP
   ```

3. **Verify:**

   ```bash
   git log --oneline -3
   ls -la FUNDING_PROPOSAL.md
   ```

---

## Quick Copy-Paste Script for Mac

Save this as `fix_git.sh` and run it:

```bash
#!/bin/bash

echo "Fixing git remote..."
cd ~/Downloads/ALPHAVOXWAKESUP-main

# Remove old remote if exists

git remote remove origin 2>/dev/null

# Add correct remote

git remote add origin <https://github.com/Nathaniel-AI/ALPHAVOXWAKESUP.git>

# Verify

echo ""
echo "Remote configured:"
git remote -v

# Fetch latest

echo ""
echo "Fetching latest from GitHub..."
git fetch origin

# Show status

echo ""
echo "Current status:"
git status

echo ""
echo "Latest commits on GitHub:"
git log origin/main --oneline -3

echo ""
echo "To update your local files, run:"
echo "  git reset --hard origin/main"
```text
**To use:**

```bash
chmod +x fix_git.sh
./fix_git.sh
```text
---

## Need Help?

If you still get errors, copy the **exact error message** and I can help debug it.

Common issues:

- **"fatal: not a git repository"** - You're in the wrong folder
- **"Permission denied"** - Need to authenticate with GitHub
- **"Could not resolve host"** - Internet connection issue
