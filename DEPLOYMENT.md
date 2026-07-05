# Git & Netlify Deployment Notes

## Repository Information

**Repository Name:** `portfolio`

**GitHub Repository:**
https://github.com/surya-murugasen/portfolio

**Branch:**
`main`

**Deployment:**
Netlify is connected to this GitHub repository. Every successful push to the `main` branch automatically triggers a new Netlify deployment.

---

# Normal Workflow

## 1. Check repository status
```bash
git status
```

## 2. Stage all changes
```bash
git add .
```

## 3. Commit changes
```bash
git commit -m "Your commit message"
```

## 4. Push to GitHub
```bash
git push origin main
```

---

# Troubleshooting

## If you get a 403 Permission Denied error

Example:
```text
remote: Permission denied to <wrong-account>.
fatal: unable to access ...
```

### Fix
1. Open **Credential Manager** in Windows.
2. Open **Windows Credentials**.
3. Delete all GitHub credentials (look for `git:https://github.com`).
4. Run:
```bash
git push origin main
```
5. A popup will appear. Sign in using the correct GitHub account that owns the repository.

---

## If Git says Updates were rejected

Example:
```text
Updates were rejected because the remote contains work that you do not have locally.
```

### Check commit history
```bash
git fetch origin
git log --oneline --graph --decorate --all -10
```

### Keep both local and remote commits (Recommended)
```bash
git pull --rebase origin main
git push origin main
```

### Replace the remote repository with your local version
> **Warning:** Use only if your local project is the latest version and you want to completely overwrite the remote.
```bash
git push --force origin main
```

---

# Verify Deployment

```bash
git status
```

**Expected output:**
```text
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

### Netlify Deployment
Once the push succeeds:
- Netlify automatically detects the new commit.
- A new deployment starts automatically.
- Refresh the live site after the deployment finishes (usually within a minute).
- No manual deployment is required.
