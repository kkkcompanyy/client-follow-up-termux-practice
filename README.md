CLIENT FOLLOW-UP — FULL RESTORE / RUN GUIDE
===========================================

Backup folder:
    /sdcard/Download/NEW APP BACKUPP

Main live project folder:
    ~/checker-lab

IMPORTANT
---------
This backup is meant to let you rebuild the current Client Follow-Up web app if something breaks.

Do NOT delete the backup after restoring.
Do NOT overwrite your only copy of clients.db.
Do NOT change static/no_refresh.js unless you know exactly why.

The Android app is a separate project and is NOT required just to run the Flask website.

============================================================
1) WHICH FILES ARE REALLY REQUIRED?
============================================================

To run the website with your CURRENT REAL DATA, the minimum important files are:

    ONE Python app version:
        app.py
        OR app_pro_theme.py
        OR cobra_finalwork.py
        OR another future version such as cobra_astra.py

    clients.db
        This contains the real client data used by the web app.

    static/no_refresh.js
        Important for the working Quick Action / no-refresh behavior.

For the cobra visual versions, also keep:

    static/cobra-reference.png

The first cobra version app_pro_theme.py directly references:

    /static/cobra-reference.png

So if that image is missing, the app may still run, but the cobra design/background will be incomplete.

Recommended:
Keep the ENTIRE backup folder together instead of trying to save only the minimum files.

You do NOT need HTML template files because the current Flask application stores its HTML/Jinja templates inside the Python file itself.

Python package required:
    Flask

The rest of the imports used by the app, such as sqlite3, csv, io, os and functools,
come with Python.

============================================================
2) RESTORE THE PROJECT FROM THIS BACKUP
============================================================

Run these commands in NORMAL TERMUX.

If this is a fresh Termux installation:

    termux-setup-storage

Allow storage permission when Android asks.

Install Python if needed:

    pkg update
    pkg install python

Install Flask:

    pip install flask

Create the project folder:

    mkdir -p ~/checker-lab

Copy EVERYTHING from this backup into the project folder:

    cp -r "/sdcard/Download/NEW APP BACKUPP/." ~/checker-lab/

Go into the project:

    cd ~/checker-lab

Check the files:

    ls -lah

Check the static folder:

    ls -lah ~/checker-lab/static

You should see clients.db, at least one Python app file, static/no_refresh.js,
and the cobra image if you want to run a cobra version.

============================================================
3) CHECK A PYTHON VERSION BEFORE STARTING IT
============================================================

Original version:

    cd ~/checker-lab
    python -m py_compile app.py

First cobra version:

    python -m py_compile app_pro_theme.py

cobra_finalwork:

    python -m py_compile cobra_finalwork.py

If the command returns to the prompt with NO error text, the Python syntax check passed.

============================================================
4) START THE WEBSITE
============================================================

Only ONE visual version should normally run on port 5000 at the same time.

ORIGINAL VERSION:

    cd ~/checker-lab
    python app.py

FIRST COBRA VERSION:

    cd ~/checker-lab
    python app_pro_theme.py

If you later renamed app_pro_theme.py to cobra.py:

    cd ~/checker-lab
    python cobra.py

COBRA FINALWORK VERSION:

    cd ~/checker-lab
    python cobra_finalwork.py

FUTURE VERSION EXAMPLE:

    cd ~/checker-lab
    python cobra_astra.py

To stop the running Flask app:

    CTRL + C

Then you can start a different visual version.

All versions should use the same:

    ~/checker-lab/clients.db

That is why a status change made in one version also appears in the other versions
and is available to the Android app through the Flask API.

============================================================
5) OPEN THE WEBSITE LOCALLY
============================================================

With Flask running, open:

    http://127.0.0.1:5000

Health check from Termux:

    curl http://127.0.0.1:5000/api/health

Expected general result:

    ok = true
    API online

If 127.0.0.1 refuses the connection, the Flask app is probably not running.

============================================================
6) NGROK METHOD — CURRENT RESERVED PUBLIC URL
============================================================

The Flask app must FIRST be running in normal Termux on port 5000.

Keep that Termux session open.

Open a SECOND terminal/session.

ngrok was previously used from the Ubuntu/proot environment.
Enter the same Ubuntu/proot environment where your ngrok command already works.

Then run:

    ngrok http --url=splatter-conch-theology.ngrok-free.dev http://127.0.0.1:5000

The public URL is:

    https://splatter-conch-theology.ngrok-free.dev

As long as ngrok is forwarding to port 5000, that same URL shows whichever
Python visual version is currently running on port 5000.

Example:

    python app.py
        -> public URL shows original version

Stop Flask with CTRL+C, then:

    python app_pro_theme.py
        -> same public URL now shows first cobra version

Stop Flask with CTRL+C, then:

    python cobra_finalwork.py
        -> same public URL now shows cobra_finalwork

IMPORTANT:
If ngrok says the upstream/local connection failed, first check that Flask is running:

    curl http://127.0.0.1:5000/api/health

If this local curl fails, fix/start Flask before troubleshooting ngrok.

A normal temporary ngrok tunnel can also be started with:

    ngrok http 5000

but that normally gives you a different public URL.
The reserved command above is the preferred command for the existing setup.

============================================================
7) CLOUDFLARED METHOD — QUICK TEMPORARY PUBLIC URL
============================================================

This is an alternative to ngrok.

First start Flask:

    cd ~/checker-lab
    python app.py

or whichever visual version you want.

Keep Flask running.

Open a SECOND terminal/session in the environment where cloudflared is installed.

Verify cloudflared exists:

    cloudflared --version

Then run:

    cloudflared tunnel --url http://127.0.0.1:5000

cloudflared should display a public address similar to:

    https://something-random.trycloudflare.com

Open that address in a browser.

IMPORTANT:
A quick trycloudflare.com address is normally temporary and can change when
cloudflared is restarted.

Do NOT run ngrok and cloudflared because you think both are required.
You only need ONE tunnel service for public access.

Flask itself works locally without either one.

If you later configure a permanent Cloudflare named tunnel/custom domain,
that uses a different Cloudflare configuration and should be documented separately.

============================================================
8) NORMAL STARTUP ORDER
============================================================

Recommended order every time:

STEP 1 — Start Flask in normal Termux:

    cd ~/checker-lab
    python app.py

OR choose another version:

    python app_pro_theme.py

    python cobra_finalwork.py

STEP 2 — Test locally:

    curl http://127.0.0.1:5000/api/health

STEP 3 — If you need public internet access, start ONE tunnel:

NGROK:

    ngrok http --url=splatter-conch-theology.ngrok-free.dev http://127.0.0.1:5000

OR CLOUDFLARED:

    cloudflared tunnel --url http://127.0.0.1:5000

STEP 4 — Open the public URL.

============================================================
9) FILES / BEHAVIOR THAT SHOULD NOT BE CASUALLY CHANGED
============================================================

Protect these:

    clients.db
    static/no_refresh.js
    app.py
    app_pro_theme.py
    cobra_finalwork.py

Important working behavior that must remain:

    Login / logout
    Categories
    Search
    Status filter
    Add Client
    CSV Import
    Bulk Mark Called
    Bulk Mark Not Called
    Quick Mark YES / NO
    Called At timestamp
    Selected category preservation
    Quick Action no-refresh behavior
    Android REST API
    Shared clients.db

Existing API routes include:

    /api/health
    /api/login
    /api/clients
    /api/stats
    /api/sync
    /api/clients/add
    /api/clients/<id>/toggle
    /api/clients/<id>/status
    /api/clients/bulk
    /api/clients/import

Do not rename/remove these casually because the Android app depends on the Flask API.

============================================================
10) VERY IMPORTANT DATABASE RULE
============================================================

clients.db is the source of truth for the current client information.

Before any dangerous backend/database experiment, make another copy:

    cp ~/checker-lab/clients.db ~/storage/downloads/clients_before_change.db

Or:

    cp ~/checker-lab/clients.db "/sdcard/Download/NEW APP BACKUPP/clients_extra_backup.db"

If clients.db is accidentally replaced by a blank database,
the website may look like your clients disappeared even though the Python code works.

To restore the backed-up database:

STOP FLASK FIRST with CTRL+C.

Then:

    cp "/sdcard/Download/NEW APP BACKUPP/clients.db" ~/checker-lab/clients.db

Then start Flask again.

============================================================
11) IF THE WEBSITE STARTS BUT THE COBRA IMAGE IS MISSING
============================================================

Check:

    ls -lh ~/checker-lab/static/cobra-reference.png

If the file exists, verify the Python version expects that exact filename.

The first cobra version uses:

    /static/cobra-reference.png

Do not randomly rename static assets without also checking the Python/CSS reference.

============================================================
12) IF QUICK ACTION STARTS REFRESHING/JUMPING AGAIN
============================================================

First verify this file still exists:

    ls -lh ~/checker-lab/static/no_refresh.js

Do NOT replace no_refresh.js with a guessed/recreated version.

The Flask Python file also contains an after_request hook that injects:

    /static/no_refresh.js

The Quick Action route also has special AJAX behavior and category preservation.
If this breaks, compare against the working backup instead of rewriting the feature from scratch.

============================================================
13) COMMON ERRORS
============================================================

ERROR:
    ModuleNotFoundError: No module named 'flask'

FIX:

    pip install flask


ERROR:
    Address already in use / port 5000 already occupied

MOST LIKELY REASON:
Another Flask version is still running.

FIX:
Go to the terminal where the old Flask app is running and press:

    CTRL + C

Then start the version you want.


ERROR:
    Connection refused on 127.0.0.1:5000

FIX:

    cd ~/checker-lab
    python app.py


ERROR:
    Tunnel opens but shows upstream / connection error

FIX:
Check Flask locally first:

    curl http://127.0.0.1:5000/api/health


ERROR:
    Website runs but real clients are missing

CHECK:

    ls -lh ~/checker-lab/clients.db

Make sure the correct backed-up clients.db was restored beside the Python file.

============================================================
14) VERIFY THIS BACKUP
============================================================

From Termux:

    ls -lah "/sdcard/Download/NEW APP BACKUPP"

Check its total size:

    du -sh "/sdcard/Download/NEW APP BACKUPP"

List files under it:

    find "/sdcard/Download/NEW APP BACKUPP" -maxdepth 2 -type f | sort

The backup should include at minimum:

    clients.db
    app.py
    app_pro_theme.py
    cobra_finalwork.py
    static/no_refresh.js
    static/cobra-reference.png

If a newer visual version is created later, copy it into the backup too.

Example:

    cp ~/checker-lab/cobra_astra.py "/sdcard/Download/NEW APP BACKUPP/"

============================================================
15) SIMPLE RECOVERY CHEAT SHEET
============================================================

Fresh Termux:

    termux-setup-storage
    pkg update
    pkg install python
    pip install flask

Restore:

    mkdir -p ~/checker-lab
    cp -r "/sdcard/Download/NEW APP BACKUPP/." ~/checker-lab/
    cd ~/checker-lab

Check:

    python -m py_compile app.py

Run:

    python app.py

Test:

    curl http://127.0.0.1:5000/api/health

Public with ngrok:

    ngrok http --url=splatter-conch-theology.ngrok-free.dev http://127.0.0.1:5000

Alternative public tunnel:

    cloudflared tunnel --url http://127.0.0.1:5000

============================================================
END
============================================================

Keep this README inside:

    /sdcard/Download/NEW APP BACKUPP/

That way the backup includes both the application files AND the instructions
needed to restore and run the system again.
