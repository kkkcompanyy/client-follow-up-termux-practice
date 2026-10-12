# Client Follow-Up — Termux Practice Project

A beginner-friendly Flask + SQLite project designed for learning:

- Termux basics
- Linux commands
- Python and Flask
- SQLite
- HTML/CSS/JavaScript
- REST APIs
- Git and GitHub
- ngrok / Cloudflare Tunnel concepts

## Safety

This repository is a **sanitized learning copy**.

It intentionally does **not** contain:

- the real `clients.db`
- real client information
- private passwords
- private signing files
- ngrok tokens
- Cloudflare tokens

Never commit those things to GitHub.

## Versions

- `app.py` — original visual style
- `app_pro_theme.py` — first cobra style
- `cobra_finalwork.py` — stronger cobra style

They all create/use a local `clients.db` in the same folder.

## Termux quick start

```bash
pkg update -y
pkg install -y python git curl
pip install -r requirements.txt

python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Default **practice-only** login:

```text
username: student
password: practice123
```

Do not use those credentials for a real internet-facing deployment.

## Optional: choose your own login before starting

```bash
export APP_USERNAME="myuser"
export APP_PASSWORD="choose-a-better-password"
export FLASK_SECRET_KEY="choose-a-long-random-value"
python app.py
```

## Import sample clients

The repository includes:

```text
sample_clients.csv
```

Use the Import Clients function in the site.

## Test the API

With Flask running:

```bash
curl http://127.0.0.1:5000/api/health
```

## Good beginner exercises

1. Use `pwd`, `ls`, `cd`, `cp`, `mv`, `mkdir`, `cat`, and `nano`.
2. Change the page title.
3. Change one CSS color.
4. Add a new category.
5. Add a fake client from the browser.
6. Inspect `clients.db` with SQLite.
7. Call `/api/health` with `curl`.
8. Create a Git branch.
9. Make one change and commit it.
10. Push the branch to GitHub.
11. Compare the three visual versions.
12. Add a new Flask route such as `/hello`.
13. Create a simple JSON endpoint.
14. Learn what `127.0.0.1`, port `5000`, and a tunnel mean.

## SQLite practice

Install SQLite in Termux:

```bash
pkg install sqlite
```

Open the database after running the app at least once:

```bash
sqlite3 clients.db
```

Inside SQLite:

```sql
.tables
.schema clients
SELECT id, code, name, called, category FROM clients;
.quit
```

## Git practice

```bash
git status
git branch
git log --oneline
```

Create a branch:

```bash
git switch -c my-first-change
```

After editing a file:

```bash
git add .
git commit -m "My first practice change"
git push -u origin my-first-change
```

## Tunnels

A tunnel exposes your local Flask server to the internet.

Do not expose a learning app publicly until you understand the risks.

### ngrok

After installing/configuring ngrok:

```bash
ngrok http 5000
```

### Cloudflare Quick Tunnel

After installing `cloudflared`:

```bash
cloudflared tunnel --url http://127.0.0.1:5000
```

## Important

`clients.db` is ignored by `.gitignore` on purpose. Each learner should create their own local practice database.

Have fun, break the **practice copy**, restore it, and learn why it broke.
