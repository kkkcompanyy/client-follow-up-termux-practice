from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    render_template_string,
    flash
)

from functools import wraps

import sqlite3
import csv
import io
import os


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "practice-change-me")


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_FILE = os.path.join(
    BASE_DIR,
    "clients.db"
)


def get_db():

    db = sqlite3.connect(DB_FILE)

    db.row_factory = sqlite3.Row

    return db


def init_db():

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            phone TEXT,
            called INTEGER NOT NULL DEFAULT 0,
            called_at TEXT,
            category TEXT NOT NULL DEFAULT 'New',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = {
        row[1]
        for row in db.execute("PRAGMA table_info(clients)").fetchall()
    }

    if "called_at" not in columns:
        db.execute("ALTER TABLE clients ADD COLUMN called_at TEXT")

    if "category" not in columns:
        db.execute(
            "ALTER TABLE clients "
            "ADD COLUMN category TEXT NOT NULL DEFAULT 'New'"
        )

    db.commit()
    db.close()


# =========================================================
# USERS
# =========================================================

USERS = {
    os.environ.get("APP_USERNAME", "student"):
    os.environ.get("APP_PASSWORD", "practice123")
}


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(function):

    @wraps(function)

    def wrapper(*args, **kwargs):

        if "username" not in session:

            return redirect(
                url_for("login")
            )

        return function(
            *args,
            **kwargs
        )

    return wrapper


# =========================================================
# DESIGN
# =========================================================

PAGE = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0"
>

<title>{{ title }}</title>

<style>

* {

    box-sizing: border-box;

}

body {

    margin: 0;

    font-family:
    Arial,
    Helvetica,
    sans-serif;

    background:
    #07111f;

    color:
    #f1f5f9;

}


.topbar {

    background:
    #0b1728;

    border-bottom:
    1px solid #23354d;

    padding:
    15px 20px;

    display: flex;

    align-items: center;

    justify-content:
    space-between;

}


.brand {

    font-size: 20px;

    font-weight: bold;

}


.lab {

    display:
    inline-block;

    background:
    #11341f;

    color:
    #86efac;

    border:
    1px solid #27613d;

    padding:
    6px 10px;

    border-radius:
    30px;

    font-size:
    11px;

    font-weight:
    bold;

}


.container {

    max-width:
    1200px;

    margin:
    auto;

    padding:
    18px;

}


.grid {

    display:
    grid;

    grid-template-columns:
    repeat(
        auto-fit,
        minmax(170px, 1fr)
    );

    gap:
    12px;

}


.card {

    background:
    #0f1d30;

    border:
    1px solid #263a55;

    border-radius:
    14px;

    padding:
    16px;

}


.number {

    font-size:
    30px;

    font-weight:
    bold;

    margin-top:
    5px;

}


.green {

    color:
    #86efac;

}


.red {

    color:
    #fca5a5;

}


.muted {

    color:
    #94a3b8;

}


input,
select {

    width:
    100%;

    padding:
    12px;

    border-radius:
    9px;

    border:
    1px solid #344861;

    background:
    #081525;

    color:
    white;

}


button,
.button {

    border:
    none;

    border-radius:
    9px;

    padding:
    11px 14px;

    background:
    #2563eb;

    color:
    white;

    font-weight:
    bold;

    text-decoration:
    none;

    cursor:
    pointer;

}


.success {

    background:
    #18794e;

}


.danger {

    background:
    #a8323c;

}


.secondary {

    background:
    #27384f;

}


.toolbar {

    display:
    grid;

    grid-template-columns:
    2fr
    1fr
    auto;

    gap:
    9px;

    margin:
    15px 0;

}


.row {

    display:
    grid;

    grid-template-columns:
    1fr
    2fr
    auto;

    gap:
    9px;

}


.actions {

    display:
    flex;

    gap:
    8px;

    flex-wrap:
    wrap;

    align-items:
    center;

}


.table-wrapper {

    overflow-x:
    auto;

    border:
    1px solid #263a55;

    border-radius:
    12px;

}


table {

    width:
    100%;

    min-width:
    700px;

    border-collapse:
    collapse;

    background:
    #0f1d30;

}


th {

    background:
    #14243a;

    color:
    #b4c2d6;

}


th,
td {

    padding:
    12px;

    text-align:
    left;

    border-bottom:
    1px solid #263750;

}


.status {

    display:
    inline-block;

    padding:
    5px 9px;

    border-radius:
    20px;

    font-size:
    11px;

    font-weight:
    bold;

}


.yes {

    background:
    #123522;

    color:
    #86efac;

}


.no {

    background:
    #3b181c;

    color:
    #fca5a5;

}


.flash {

    background:
    #14243a;

    border:
    1px solid #344861;

    padding:
    11px;

    border-radius:
    9px;

    margin-bottom:
    12px;

}


.login {

    max-width:
    420px;

    margin:
    10vh auto;

}


.small {

    font-size:
    12px;

}


@media (
    max-width: 700px
) {

    .toolbar,
    .row {

        grid-template-columns:
        1fr;

    }

}


body {
    background: #000000 !important;
}

.topbar {
    background: #000000 !important;
}

main {
    background: transparent !important;
}


.call-time {
    margin-top: 5px;
    font-size: 10px;
    color: #8b98a8;
    white-space: nowrap;
}



/* PRO_COBRA_THEME_START */
:root {
    --bg0: #02070d;
    --bg1: #06111d;
    --panel: rgba(5, 20, 31, 0.84);
    --panel-strong: rgba(4, 17, 28, 0.94);
    --line: rgba(63, 126, 168, 0.46);
    --text: #f7fbff;
    --muted2: #9eb0c5;
    --blue: #1687ff;
    --green2: #12e785;
    --red2: #ff4655;
}

html {
    background: var(--bg0);
}

body {
    min-height: 100vh;
    background:
        radial-gradient(circle at 78% 13%, rgba(0, 255, 119, 0.20), transparent 27%),
        radial-gradient(circle at 24% 82%, rgba(0, 141, 255, 0.15), transparent 30%),
        linear-gradient(180deg, #02070d 0%, #04101a 47%, #02070d 100%) !important;
    color: var(--text);
}

.topbar {
    position: relative;
    z-index: 50;
    padding: 12px 4.7vw !important;
    background: rgba(2, 11, 18, 0.90) !important;
    border-bottom: 1px solid rgba(31, 126, 181, 0.55) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.brand {
    font-size: clamp(20px, 2vw, 30px) !important;
    letter-spacing: -0.7px;
    color: #ffffff;
}

.brand .brand-accent {
    color: var(--green2);
}

.lab {
    background: rgba(5, 78, 47, 0.52) !important;
    color: #92ffc8 !important;
    border: 1px solid #12c978 !important;
    box-shadow: 0 0 18px rgba(18, 231, 133, 0.18);
}

.topbar .secondary {
    background: rgba(8, 26, 42, 0.84) !important;
    border: 1px solid rgba(100, 157, 198, 0.45);
}

.container {
    max-width: 1480px !important;
    padding: 22px clamp(14px, 4vw, 60px) 48px !important;
}

.client-dashboard {
    position: relative;
    isolation: isolate;
    min-height: calc(100vh - 90px);
}

.client-dashboard::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: -5;
    pointer-events: none;
    background:
        radial-gradient(circle at 80% 24%, rgba(12, 255, 126, 0.13), transparent 25%),
        radial-gradient(circle at 18% 73%, rgba(20, 121, 255, 0.08), transparent 28%);
}

.cobra-hero {
    position: absolute;
    z-index: -2;
    pointer-events: none;
    top: -52px;
    right: -18px;
    width: min(650px, 48vw);
    height: 390px;
    overflow: hidden;
    opacity: 0.92;
    filter: saturate(1.08) contrast(1.03);
    mask-image: linear-gradient(90deg, transparent 0%, #000 21%, #000 88%, transparent 100%);
    -webkit-mask-image: linear-gradient(90deg, transparent 0%, #000 21%, #000 88%, transparent 100%);
}

.cobra-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("/static/cobra-reference.png");
    background-repeat: no-repeat;
    background-size: 1536px 1024px;
    background-position: right -64px;
    transform: scale(1.03);
    transform-origin: right top;
}

.cobra-hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(90deg, #02070d 0%, rgba(2,7,13,0.15) 26%, transparent 65%),
        linear-gradient(180deg, transparent 62%, #02070d 100%);
}

.hero-copy {
    position: relative;
    z-index: 2;
    max-width: 780px;
    padding-top: 20px;
}

.hero-title {
    margin: 0;
    font-size: clamp(34px, 4.5vw, 58px);
    line-height: 1;
    letter-spacing: -1.8px;
    text-shadow: 0 2px 20px rgba(0, 0, 0, 0.42);
}

.hero-title .accent {
    color: var(--green2);
    text-shadow: 0 0 18px rgba(18, 231, 133, 0.25);
}

.hero-subtitle {
    margin: 14px 0 18px;
    color: #c4d2e2;
    font-size: clamp(15px, 1.7vw, 20px);
    font-weight: 600;
}

.stats-grid {
    position: relative;
    z-index: 3;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    max-width: 870px;
    margin-top: 10px;
}

.stat-card {
    min-height: 112px;
    padding: 18px 20px;
    border-radius: 14px;
    border: 1px solid rgba(82, 148, 191, 0.48);
    background: linear-gradient(145deg, rgba(8, 30, 48, 0.94), rgba(5, 18, 30, 0.84));
    box-shadow:
        0 12px 30px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: grid;
    grid-template-columns: 58px 1fr;
    align-items: center;
    column-gap: 14px;
}

.stat-card.total-card {
    border-color: rgba(30, 140, 255, 0.95);
    box-shadow: 0 0 24px rgba(22, 135, 255, 0.24), 0 12px 30px rgba(0,0,0,0.28);
}

.stat-card.called-card {
    border-color: rgba(18, 231, 133, 0.75);
    background: linear-gradient(145deg, rgba(6, 49, 35, 0.96), rgba(4, 28, 24, 0.84));
    box-shadow: 0 0 24px rgba(18, 231, 133, 0.16), 0 12px 30px rgba(0,0,0,0.28);
}

.stat-card.pending-card {
    border-color: rgba(255, 70, 85, 0.68);
    background: linear-gradient(145deg, rgba(63, 20, 29, 0.94), rgba(28, 13, 20, 0.84));
    box-shadow: 0 0 24px rgba(255, 70, 85, 0.16), 0 12px 30px rgba(0,0,0,0.28);
}

.stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 28px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(19, 91, 157, 0.42);
}

.called-card .stat-icon { background: rgba(12, 120, 72, 0.42); }
.pending-card .stat-icon { background: rgba(150, 44, 54, 0.44); }

.stat-label {
    color: #c7d4e2;
    font-size: 15px;
    font-weight: 600;
}

.stat-number {
    margin-top: 4px;
    font-size: 32px;
    line-height: 1;
    font-weight: 800;
}

.total-card .stat-number { color: #ffffff; }
.called-card .stat-number { color: #5affad; }
.pending-card .stat-number { color: #ff858f; }

.category-tabs {
    position: relative;
    z-index: 3;
    display: flex;
    gap: 10px;
    overflow-x: auto;
    margin: 18px 0 20px;
    padding: 2px 2px 5px;
    scrollbar-width: none;
    white-space: nowrap;
}

.category-tabs::-webkit-scrollbar { display: none; }

.category-chip {
    flex: 0 0 auto;
    padding: 10px 18px;
    border-radius: 10px;
    border: 1px solid rgba(77, 136, 181, 0.50);
    color: #d7e4f2;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    background: rgba(8, 27, 43, 0.83);
    transition: 0.18s ease;
}

.category-chip:hover {
    transform: translateY(-1px);
    border-color: rgba(18, 231, 133, 0.85);
}

.category-chip.active {
    border-color: #18f18e;
    color: #ffffff;
    background: linear-gradient(135deg, rgba(7, 100, 60, 0.85), rgba(4, 39, 33, 0.92));
    box-shadow: 0 0 18px rgba(18, 231, 133, 0.22);
}

.work-grid {
    position: relative;
    z-index: 3;
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 18px;
    margin-bottom: 18px;
}

.pro-panel {
    margin: 0 !important;
    padding: 20px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(41, 149, 177, 0.70) !important;
    background:
        linear-gradient(145deg, rgba(4, 24, 37, 0.91), rgba(5, 17, 28, 0.84)) !important;
    box-shadow:
        0 16px 38px rgba(0,0,0,0.32),
        inset 0 1px 0 rgba(255,255,255,0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.panel-title {
    margin: 0 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
}

.panel-title .panel-icon {
    display: inline-grid;
    place-items: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #11df82;
    color: #03140d;
    font-weight: 900;
    box-shadow: 0 0 18px rgba(18, 231, 133, 0.26);
}

.client-dashboard input,
.client-dashboard select {
    min-height: 48px;
    border-radius: 9px !important;
    border: 1px solid rgba(69, 132, 177, 0.58) !important;
    background: rgba(3, 17, 29, 0.92) !important;
    color: #eff7ff !important;
    outline: none;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}

.client-dashboard input:focus,
.client-dashboard select:focus {
    border-color: #21a3ff !important;
    box-shadow: 0 0 0 3px rgba(33, 163, 255, 0.10);
}

.client-dashboard input::placeholder {
    color: #9aabc0;
}

.add-form {
    grid-template-columns: 1fr 1.12fr 0.95fr !important;
}

.full-width-btn {
    grid-column: 1 / -1;
    min-height: 48px;
}

.client-dashboard button,
.client-dashboard .button {
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 7px 18px rgba(0,0,0,0.22);
    transition: transform 0.15s ease, filter 0.15s ease;
}

.client-dashboard button:active {
    transform: translateY(1px);
}

.primary-blue {
    background: linear-gradient(180deg, #1d8cff, #0967ef) !important;
}

.primary-green {
    background: linear-gradient(180deg, #24e98e, #0dbd67) !important;
    color: #03130c !important;
}

.import-form {
    display: grid !important;
    grid-template-columns: 1fr auto;
    gap: 12px;
    align-items: center;
}

.import-form input[type="file"] {
    max-width: none !important;
}

.import-form .primary-green {
    min-width: 210px;
    min-height: 48px;
}

.import-help {
    margin: 10px 0 0 !important;
    line-height: 1.55;
}

.control-strip {
    position: relative;
    z-index: 3;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 18px;
    align-items: start;
    margin: 18px 0 12px;
}

.search-toolbar {
    display: grid !important;
    grid-template-columns: minmax(220px, 1.8fr) minmax(150px, 0.72fr) 165px !important;
    gap: 10px !important;
    margin: 0 !important;
}

.search-toolbar button {
    min-height: 48px;
}

.bulk-actions {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.bulk-actions .success {
    background: linear-gradient(180deg, rgba(11, 125, 72, 0.98), rgba(4, 78, 48, 0.98)) !important;
    border: 1px solid #1ae384;
    box-shadow: 0 0 18px rgba(18, 231, 133, 0.16);
}

.bulk-actions .danger {
    background: linear-gradient(180deg, rgba(152, 34, 44, 0.98), rgba(95, 22, 31, 0.98)) !important;
    border: 1px solid #ff4d5b;
    box-shadow: 0 0 18px rgba(255, 70, 85, 0.13);
}

.bulk-help {
    width: 100%;
    text-align: right;
    margin-top: -3px;
}

.results-panel {
    position: relative;
    z-index: 3;
    overflow-x: auto;
    border: 1px solid rgba(41, 132, 176, 0.62) !important;
    border-radius: 14px !important;
    background: rgba(3, 15, 25, 0.88);
    box-shadow: 0 18px 42px rgba(0,0,0,0.34);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.results-panel table {
    min-width: 940px;
    background: transparent !important;
}

.results-panel th {
    background: rgba(7, 34, 52, 0.94) !important;
    color: #e4edf7 !important;
    font-size: 13px;
    font-weight: 800;
}

.results-panel td {
    background: rgba(3, 18, 29, 0.58);
    color: #eef6ff;
}

.results-panel tbody tr:hover td {
    background: rgba(7, 36, 53, 0.70);
}

.results-panel th,
.results-panel td {
    border-bottom: 1px solid rgba(55, 97, 128, 0.48) !important;
    padding: 12px 14px !important;
}

.results-panel input[type="checkbox"] {
    min-height: 0;
    width: 18px;
    height: 18px;
    accent-color: #13e584;
}

.status.yes {
    color: #b9ffd8 !important;
    background: linear-gradient(180deg, rgba(8, 112, 64, 0.92), rgba(5, 73, 45, 0.95)) !important;
    border: 1px solid rgba(23, 205, 119, 0.5);
}

.status.no {
    color: #ffd0d4 !important;
    background: linear-gradient(180deg, rgba(136, 30, 42, 0.93), rgba(91, 21, 31, 0.96)) !important;
    border: 1px solid rgba(255, 73, 86, 0.48);
}

.called-at-cell {
    color: #c6d3e1 !important;
    white-space: nowrap;
    font-size: 12px;
}

.quick-button {
    min-width: 96px;
    background: linear-gradient(180deg, #294662, #1b3047) !important;
    border: 1px solid rgba(100, 157, 198, 0.28) !important;
}

.empty-state {
    text-align: center !important;
    padding: 34px !important;
    color: #9fb1c6 !important;
}

@media (max-width: 980px) {
    .cobra-hero {
        width: 590px;
        right: -180px;
        opacity: 0.58;
    }

    .hero-copy {
        max-width: 64%;
    }

    .work-grid,
    .control-strip {
        grid-template-columns: 1fr;
    }

    .bulk-actions,
    .bulk-help {
        justify-content: flex-start;
        text-align: left;
    }

    .import-form {
        grid-template-columns: 1fr;
    }

    .import-form .primary-green {
        width: 100%;
    }
}

@media (max-width: 700px) {
    .container {
        padding: 14px 12px 34px !important;
    }

    .topbar {
        padding: 10px 12px !important;
    }

    .brand {
        font-size: 18px !important;
    }

    .topbar .actions {
        gap: 6px;
    }

    .topbar .button,
    .topbar .lab {
        padding: 7px 9px !important;
        font-size: 10px !important;
    }

    .client-dashboard {
        padding-top: 4px;
    }

    .cobra-hero {
        top: -18px;
        right: -275px;
        width: 640px;
        height: 300px;
        opacity: 0.48;
    }

    .hero-copy {
        max-width: 100%;
        padding-top: 8px;
        padding-right: 42px;
    }

    .hero-title {
        font-size: 30px;
    }

    .hero-subtitle {
        font-size: 13px;
        max-width: 78%;
    }

    .stats-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 7px;
        max-width: none;
    }

    .stat-card {
        min-height: 94px;
        padding: 11px 8px;
        grid-template-columns: 1fr;
        row-gap: 4px;
        text-align: left;
    }

    .stat-icon {
        width: 31px;
        height: 31px;
        font-size: 16px;
    }

    .stat-label {
        font-size: 10px;
    }

    .stat-number {
        font-size: 22px;
    }

    .category-tabs {
        gap: 6px;
        margin: 10px 0 14px;
    }

    .category-chip {
        padding: 7px 10px;
        font-size: 10px;
    }

    .work-grid {
        gap: 12px;
    }

    .pro-panel {
        padding: 14px !important;
    }

    .panel-title {
        font-size: 15px;
        margin-bottom: 12px;
    }

    .add-form,
    .search-toolbar {
        grid-template-columns: 1fr !important;
    }

    .control-strip {
        gap: 10px;
        margin-top: 12px;
    }

    .bulk-actions {
        justify-content: flex-start;
    }

    .bulk-actions button {
        flex: 1 1 140px;
    }

    .bulk-help {
        font-size: 10px;
    }

    .results-panel {
        border-radius: 10px !important;
    }

    .results-panel table {
        min-width: 820px;
    }

    .results-panel th,
    .results-panel td {
        padding: 10px !important;
        font-size: 11px;
    }
}
/* PRO_COBRA_THEME_END */

</style>

</head>


<body>


<div class="topbar">

    <div class="brand">
        Client <span class="brand-accent">Follow-Up</span>
    </div>


    <div class="actions">

        <span class="lab">

            LOCAL LAB

        </span>


        {% if session.get("username") %}

        <a
        href="{{ url_for('logout') }}"
        class="button secondary"
        >

            Logout

        </a>

        {% endif %}

    </div>

</div>


<div class="container">


{% with messages = get_flashed_messages() %}

    {% for message in messages %}

        <div class="flash">

            {{ message }}

        </div>

    {% endfor %}

{% endwith %}


{{ content|safe }}


</div>


<script>

function selectAll(source) {

    document
    .querySelectorAll(
        ".client-checkbox"
    )
    .forEach(function(box) {

        box.checked =
        source.checked;

    });

}

</script>


<script>
document.addEventListener("submit", function () {
    sessionStorage.setItem("clientScrollPosition", window.scrollY);
});

window.addEventListener("load", function () {
    const savedPosition = sessionStorage.getItem("clientScrollPosition");

    if (savedPosition !== null) {
        window.scrollTo(0, parseInt(savedPosition));
        sessionStorage.removeItem("clientScrollPosition");
    }
});
</script>



</body>

</html>
"""


def render_page(
    title,
    body,
    **context
):

    content = render_template_string(
        body,
        **context
    )

    return render_template_string(
        PAGE,
        title=title,
        content=content
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        if USERS.get(username) == password:

            session[
                "username"
            ] = username

            return redirect(
                url_for("clients")
            )

        flash(
            "Wrong username or password."
        )


    body = """

    <div class="card login">

        <span class="lab">
            LOCAL
        </span>

        <h1 class="king-title" >
            &#9818; Client Follow-Up &#9818;
        </h1>

        <form method="POST">

            <label>
                Username
            </label>

            <input
            name="username"
            required
            >

            <br><br>


            <label>
                Password
            </label>

            <input
            name="password"
            type="password"
            required
            >

            <br><br>


            <button
            style="width:100%;"
            >

                Login

            </button>

        </form>


        <p
        class="muted small"
        style="margin-top:20px;"
        >

            God son

            <br>

             

        </p>

    </div>

    """

    return render_page(
        "Login",
        body
    )


@app.route("/")
def home():

    if "username" in session:

        return redirect(
            url_for("clients")
        )

    return redirect(
        url_for("login")
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# CLIENT LIST
# =========================================================

@app.route("/clients")
@login_required
def clients():

    search = request.args.get(
        "search",
        ""
    ).strip()

    status = request.args.get(
        "status",
        "all"
    )


    category = request.args.get(
        "category",
        "All"
    ).strip()

    allowed_categories = {
        "All",
        "New",
        "Prospect",
        "Projects",
        "PT Commerce",
        "Restaurant",
        "Integrations",
        "GN"
    }

    if category not in allowed_categories:
        category = "All"

    conditions = []

    values = []


    if search:

        conditions.append("""
            (
                code LIKE ?
                OR
                name LIKE ?
            )
        """)

        term = (
            "%"
            + search
            + "%"
        )

        values.extend([
            term,
            term
        ])


    if status == "called":

        conditions.append(
            "called = 1"
        )


    if status == "pending":

        conditions.append(
            "called = 0"
        )


    if category != "All":
        conditions.append(
            "category = ?"
        )
        values.append(
            category
        )

    sql = """

        SELECT *

        FROM clients

    """


    if conditions:

        sql += (
            " WHERE "
            +
            " AND ".join(
                conditions
            )
        )


    sql += """

        ORDER BY
        name COLLATE NOCASE

    """


    db = get_db()


    rows = db.execute(
        sql,
        values
    ).fetchall()


    if category == "All":

        total = db.execute("""
            SELECT COUNT(*)
            FROM clients
        """).fetchone()[0]

        called = db.execute("""
            SELECT COUNT(*)
            FROM clients
            WHERE called = 1
        """).fetchone()[0]

    else:

        total = db.execute("""
            SELECT COUNT(*)
            FROM clients
            WHERE category = ?
        """,
        (
            category,
        )).fetchone()[0]

        called = db.execute("""
            SELECT COUNT(*)
            FROM clients
            WHERE category = ?
            AND called = 1
        """,
        (
            category,
        )).fetchone()[0]

    pending = (
        total
        -
        called
    )


    db.close()


    body = """

    <section class="client-dashboard">
        <div class="cobra-hero" aria-hidden="true"></div>

        <div class="hero-copy">
            <h1 class="hero-title">
                Client <span class="accent">Follow-Up</span>
            </h1>

            <p class="hero-subtitle">
                Track which clients have already been called.
            </p>
        </div>

        <div class="stats-grid">
            <div class="stat-card total-card">
                <div class="stat-icon">👥</div>
                <div>
                    <div class="stat-label">Total Clients</div>
                    <div class="stat-number">{{ total }}</div>
                </div>
            </div>

            <div class="stat-card called-card">
                <div class="stat-icon">☎</div>
                <div>
                    <div class="stat-label">Called</div>
                    <div class="stat-number">{{ called }}</div>
                </div>
            </div>

            <div class="stat-card pending-card">
                <div class="stat-icon">◷</div>
                <div>
                    <div class="stat-label">Not Called</div>
                    <div class="stat-number">{{ pending }}</div>
                </div>
            </div>
        </div>

        <div class="category-tabs">
            {% for cat in ["All", "New", "Prospect", "Projects", "PT Commerce", "Restaurant", "Integrations", "GN"] %}
            <a
                href="{{ url_for('clients', category=cat) }}"
                class="category-chip {% if request.args.get('category', 'All') == cat %}active{% endif %}"
            >
                {{ cat }}
            </a>
            {% endfor %}
        </div>

        <div class="work-grid">
            <div class="card pro-panel">
                <h3 class="panel-title">
                    <span class="panel-icon">+</span>
                    Add Client
                </h3>

                <form
                    method="POST"
                    action="{{ url_for('add_client') }}"
                    class="row add-form"
                >
                    <input
                        name="code"
                        placeholder="Client code"
                        required
                    >

                    <input
                        name="name"
                        placeholder="Company name"
                        required
                    >

                    <input
                        name="phone"
                        placeholder="Phone number"
                    >

                    <button class="primary-blue full-width-btn" type="submit">
                        ＋ Add Client
                    </button>
                </form>
            </div>

            <div class="card pro-panel">
                <h3 class="panel-title">
                    <span class="panel-icon">⇧</span>
                    Import Clients
                </h3>

                <form
                    method="POST"
                    action="{{ url_for('import_clients', category=request.args.get('category', 'All')) }}"
                    enctype="multipart/form-data"
                    class="import-form"
                >
                    <input
                        type="file"
                        name="file"
                        accept=".csv"
                        required
                    >

                    <button class="primary-green" type="submit">
                        ⇧ Import CSV
                    </button>
                </form>

                <p class="muted small import-help">
                    CSV columns: <b>code</b> and <b>name</b>.<br>
                    It also accepts: codigo / nombre.
                </p>
            </div>
        </div>

        <div class="control-strip">
            <form method="GET" class="toolbar search-toolbar">
                <input
                    type="hidden"
                    name="category"
                    value="{{ request.args.get('category', 'All') }}"
                >

                <input
                    name="search"
                    value="{{ search }}"
                    placeholder="⌕  Search client..."
                >

                <select name="status">
                    <option value="all" {% if status == "all" %}selected{% endif %}>
                        All Status
                    </option>

                    <option value="pending" {% if status == "pending" %}selected{% endif %}>
                        Not Called
                    </option>

                    <option value="called" {% if status == "called" %}selected{% endif %}>
                        Called
                    </option>
                </select>

                <button class="primary-blue" type="submit">
                    ⌕ Search
                </button>
            </form>

            <div>
                <div class="bulk-actions">
                    <button
                        form="bulkForm"
                        type="submit"
                        name="action"
                        value="called"
                        class="success"
                    >
                        ✓ Mark Called
                    </button>

                    <button
                        form="bulkForm"
                        type="submit"
                        name="action"
                        value="pending"
                        class="danger"
                    >
                        ✕ Mark Not Called
                    </button>
                </div>

                <div class="muted small bulk-help">
                    Select one or multiple clients.
                </div>
            </div>
        </div>

        <form
            id="bulkForm"
            method="POST"
            action="{{ url_for('bulk_update') }}"
        >
            <input
                type="hidden"
                name="category"
                value="{{ request.args.get('category', 'All') }}"
            >

            <div class="table-wrapper results-panel">
                <table>
                    <thead>
                        <tr>
                            <th>
                                <input
                                    type="checkbox"
                                    onclick="selectAll(this)"
                                >
                            </th>
                            <th>Code</th>
                            <th>Company</th>
                            <th>Phone</th>
                            <th>Status</th>
                            <th>Called At</th>
                            <th>Quick Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {% for client in clients %}
                        <tr>
                            <td>
                                <input
                                    type="checkbox"
                                    class="client-checkbox"
                                    name="ids"
                                    value="{{ client['id'] }}"
                                >
                            </td>

                            <td>{{ client["code"] }}</td>

                            <td>{{ client["name"] }}</td>

                            <td>{{ client["phone"] or "" }}</td>

                            <td>
                                {% if client["called"] %}
                                    <span class="status yes">CALLED</span>
                                {% else %}
                                    <span class="status no">NOT CALLED</span>
                                {% endif %}
                            </td>

                            <td class="called-at-cell">
                                {% if client["called"] and client["called_at"] %}
                                    {{ client["called_at"][8:10] }}/{{ client["called_at"][5:7] }}/{{ client["called_at"][0:4] }}
                                    ·
                                    {{ client["called_at"][11:16] }}
                                {% else %}
                                    —
                                {% endif %}
                            </td>

                            <td>
                                <button
                                    class="secondary quick-button"
                                    type="submit"
                                    formaction="{{ url_for('toggle_client', client_id=client['id'], category=request.args.get('category', 'All')) }}"
                                    formmethod="POST"
                                >
                                    {% if client["called"] %}
                                        Mark NO
                                    {% else %}
                                        Mark YES
                                    {% endif %}
                                </button>
                            </td>
                        </tr>

                        {% else %}
                        <tr>
                            <td colspan="7" class="empty-state">
                                No clients found.
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </form>
    </section>

    """


    return render_page(

        "Client Follow-Up",

        body,

        clients=rows,

        total=total,

        called=called,

        pending=pending,

        search=search,

        status=status

    )


# =========================================================
# ADD CLIENT
# =========================================================

@app.route(
    "/clients/add",
    methods=["POST"]
)
@login_required
def add_client():

    code = request.form.get(
        "code",
        ""
    ).strip()

    name = request.form.get(
        "name",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()


    if not code or not name:

        flash(
            "Code and company name are required."
        )

        return redirect(
            url_for("clients")
        )


    db = get_db()


    try:

        db.execute("""

            INSERT INTO clients
            (
                code,
                name,
                phone
            )        


            VALUES
            (
                ?,
                ?,
                ?
            )


        """,
            (
                code,
                name,
                phone
            ))

        db.commit()

        flash(
            "Client added successfully."
        )


    except sqlite3.IntegrityError:

        flash(
            "That client code already exists."
        )


    db.close()


    return redirect(
        url_for("clients")
    )


# =========================================================
# IMPORT CSV
# =========================================================

@app.route(
    "/clients/import",
    methods=["POST"]
)
@login_required
def import_clients():
    category = request.args.get(
        "category",
        "New"
    ).strip()

    allowed_import_categories = {
        "New",
        "Prospect",
        "Projects",
        "PT Commerce",
        "Restaurant",
        "Integrations",
        "GN"
    }

    if category == "All":
        category = "New"

    if category not in allowed_import_categories:
        category = "New"


    uploaded = request.files.get(
        "file"
    )


    if not uploaded:

        flash(
            "Select a CSV file."
        )

        return redirect(
            url_for("clients", category=category)
        )


    raw = uploaded.read()


    try:

        text = raw.decode(
            "utf-8-sig"
        )

    except UnicodeDecodeError:

        text = raw.decode(
            "latin-1"
        )


    try:

        dialect = csv.Sniffer().sniff(
            text[:3000],
            delimiters=",;\t"
        )

    except csv.Error:

        dialect = csv.excel


    reader = csv.DictReader(
        io.StringIO(text),
        dialect=dialect
    )


    if not reader.fieldnames:

        flash(
            "CSV has no headers."
        )

        return redirect(
            url_for("clients", category=category)
        )


    headers = {

        h.strip().lower(): h

        for h in reader.fieldnames

        if h

    }


    code_column = (

        headers.get("code")

        or

        headers.get("codigo")

        or

        headers.get("código")

    )


    name_column = (

        headers.get("name")

        or

        headers.get("nombre")

        or

        headers.get("empresa")

        or

        headers.get("cliente")

or
headers.get("client")
    )

    phone_column = (
        headers.get("phone")

        or

        headers.get("telefono")

        or

        headers.get("teléfono")

        or

    headers.get("telefono principal")
    or
    headers.get("number")
    )


    if not code_column or not name_column:

        flash(
            "CSV needs code/name or codigo/nombre columns."
        )

        return redirect(
            url_for("clients", category=category)
        )


    db = get_db()


    added = 0

    updated = 0

    skipped = 0


    for row in reader:


        code = (
            row.get(
                code_column
            )
            or ""
        ).strip()


        name = (
            row.get(
                name_column
            )
            or ""
        ).strip()

        phone = ((row.get(phone_column) if phone_column else "") or "").strip()



        if not code or not name:

            skipped += 1

            continue


        existing = db.execute("""

            SELECT *

            FROM clients

            WHERE code = ?

        """,
        (
            code,
        )).fetchone()


        if existing:

            if (
                existing["name"] != name
                or (existing["phone"] or "") != phone
                or (existing["category"] or "New") != category
            ):

                db.execute("""
                    UPDATE clients

                    SET
                        name = ?,
                        phone = ?,
                        category = ?,
                        updated_at = CURRENT_TIMESTAMP

                    WHERE code = ?
                """,
                (
                    name,
                    phone,
                    category,
                    code
                ))

                updated += 1

            else:
                skipped += 1

        else:

            db.execute("""
                INSERT INTO clients
                (
                    code,
                    name,
                    phone,
                    category
                )

                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?
                )
            """,
            (
                code,
                name,
                phone,
                category
            ))

            added += 1


    db.commit()

    db.close()


    flash(

        f"Import finished: "

        f"{added} added, "

        f"{updated} updated, "

        f"{skipped} unchanged."

    )


    return redirect(
        url_for("clients", category=category)
    )


# =========================================================
# BULK UPDATE
# =========================================================

@app.route(
    "/clients/bulk",
    methods=["POST"]
)
@login_required
def bulk_update():

    bulk_category = request.form.get("category", "All")

    ids = request.form.getlist(
        "ids"
    )

    action = request.form.get(
        "action"
    )


    if not ids:

        flash(
            "Select at least one client."
        )

        return redirect(
            url_for("clients", category=bulk_category)
        )


    clean_ids = [

        int(x)

        for x in ids

        if x.isdigit()

    ]


    if action == "called":

        value = 1

    else:

        value = 0


    placeholders = ",".join(

        "?"

        for x in clean_ids

    )


    db = get_db()


    db.execute(

        f"""

        UPDATE clients

        SET
            called = ?,

            called_at =
            CASE
                WHEN ? = 1
                THEN datetime('now', 'localtime')
                ELSE NULL
             END,

            updated_at =
            CURRENT_TIMESTAMP

        WHERE id IN
        (
            {placeholders}
        )

        """,

        [
            value,
            value,
            *clean_ids
        ]

    )


    db.commit()

    db.close()


    flash(

        f"{len(clean_ids)} client(s) updated."

    )


    return redirect(
        url_for("clients", category=bulk_category)
    )


# =========================================================
# QUICK TOGGLE
# =========================================================

@app.route(
    "/clients/<int:client_id>/toggle",
    methods=["POST"]
)
@login_required
def toggle_client(
    client_id
):

    toggle_category = (
        request.form.get("category")
        or request.args.get("category")
        or "All"
    )

    db = get_db()


    client = db.execute("""

        SELECT called

        FROM clients

        WHERE id = ?

    """,
    (
        client_id,
    )).fetchone()


    if client:

        new_value = (

            0

            if client["called"]

            else 1

        )


        db.execute("""

            UPDATE clients

            SET
                called = ?,

                called_at =
                CASE
                    WHEN ? = 1
                    THEN datetime('now', 'localtime')
                    ELSE NULL
                 END,

                updated_at =
                CURRENT_TIMESTAMP

            WHERE id = ?

        """,
        (
            new_value,
            new_value,
            client_id
        ))


        db.commit()


        db.close()


        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
             return "", 204

        return redirect(
        url_for("clients", category=toggle_category)
        )
# =========================================================

# NO_REFRESH_AFTER_REQUEST_START
@app.after_request
def add_no_refresh_script(response):
    if response.mimetype == "text/html":
        html = response.get_data(as_text=True)
        tag = '<script src="/static/no_refresh.js"></script>'
        if tag not in html and "</body>" in html:
            html = html.replace("</body>", tag + "</body>", 1)
            response.set_data(html)
    return response
# NO_REFRESH_AFTER_REQUEST_END

# START SERVER
# =========================================================



# ============================================================
# ANDROID REST API
# Shared backend for Web + Native Android application
# ============================================================

from flask import jsonify


API_CATEGORIES = {
    "New",
    "Prospect",
    "Projects",
    "PT Commerce",
    "Restaurant",
    "Integrations",
    "GN",
}


def api_auth_required():
    auth = request.authorization

    if (
        auth
        and auth.username in USERS
        and USERS.get(auth.username) == auth.password
    ):
        return None

    response = jsonify({
        "ok": False,
        "error": "Unauthorized"
    })

    response.status_code = 401
    response.headers["WWW-Authenticate"] = (
        'Basic realm="Client Follow-Up API"'
    )

    return response


def api_normalize_category(category):
    category = (category or "New").strip()

    if category == "All":
        return "New"

    if category not in API_CATEGORIES:
        return "New"

    return category


def api_fetch_clients(
    category="All",
    search="",
    status="all"
):
    conditions = []
    values = []

    if category and category != "All":
        conditions.append("category = ?")
        values.append(category)

    if search:
        conditions.append("""
            (
                code LIKE ?
                OR name LIKE ?
                OR phone LIKE ?
            )
        """)

        term = "%" + search + "%"

        values.extend([
            term,
            term,
            term
        ])

    if status == "called":
        conditions.append("called = 1")

    elif status in (
        "pending",
        "not_called",
        "not called"
    ):
        conditions.append("called = 0")

    sql = """
        SELECT *
        FROM clients
    """

    if conditions:
        sql += (
            " WHERE "
            + " AND ".join(conditions)
        )

    sql += """
        ORDER BY
        name COLLATE NOCASE
    """

    db = get_db()

    rows = db.execute(
        sql,
        values
    ).fetchall()

    result = [
        dict(row)
        for row in rows
    ]

    db.close()

    return result


@app.route(
    "/api/health",
    methods=["GET"]
)
def api_health():
    return jsonify({
        "ok": True,
        "app": "Client Follow-Up",
        "api": "online"
    })


@app.route(
    "/api/login",
    methods=["POST"]
)
def api_login():
    data = request.get_json(
        silent=True
    ) or {}

    username = str(
        data.get("username", "")
    ).strip()

    password = str(
        data.get("password", "")
    )

    if (
        username in USERS
        and USERS.get(username) == password
    ):
        return jsonify({
            "ok": True,
            "username": username
        })

    return jsonify({
        "ok": False,
        "error": "Invalid username or password"
    }), 401


@app.route(
    "/api/clients",
    methods=["GET"]
)
def api_clients():
    denied = api_auth_required()

    if denied:
        return denied

    category = request.args.get(
        "category",
        "All"
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    status = request.args.get(
        "status",
        "all"
    ).strip().lower()

    clients = api_fetch_clients(
        category,
        search,
        status
    )

    return jsonify({
        "ok": True,
        "count": len(clients),
        "clients": clients
    })


@app.route(
    "/api/stats",
    methods=["GET"]
)
def api_stats():
    denied = api_auth_required()

    if denied:
        return denied

    category = request.args.get(
        "category",
        "All"
    )

    db = get_db()

    if category and category != "All":
        total = db.execute("""
            SELECT COUNT(*)
            FROM clients
            WHERE category = ?
        """,
        (
            category,
        )).fetchone()[0]

        called = db.execute("""
            SELECT COUNT(*)
            FROM clients
            WHERE category = ?
            AND called = 1
        """,
        (
            category,
        )).fetchone()[0]

    else:
        total = db.execute("""
            SELECT COUNT(*)
            FROM clients
        """).fetchone()[0]

        called = db.execute("""
            SELECT COUNT(*)
            FROM clients
            WHERE called = 1
        """).fetchone()[0]

    db.close()

    return jsonify({
        "ok": True,
        "total": total,
        "called": called,
        "not_called": total - called
    })


@app.route(
    "/api/sync",
    methods=["GET"]
)
def api_sync():
    denied = api_auth_required()

    if denied:
        return denied

    category = request.args.get(
        "category",
        "All"
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    status = request.args.get(
        "status",
        "all"
    ).strip().lower()

    clients = api_fetch_clients(
        category,
        search,
        status
    )

    total = len(clients)

    called = sum(
        1
        for client in clients
        if client.get("called")
    )

    return jsonify({
        "ok": True,
        "total": total,
        "called": called,
        "not_called": total - called,
        "clients": clients
    })


@app.route(
    "/api/clients/add",
    methods=["POST"]
)
def api_add_client():
    denied = api_auth_required()

    if denied:
        return denied

    data = request.get_json(
        silent=True
    ) or {}

    code = str(
        data.get("code", "")
    ).strip()

    name = str(
        data.get("name", "")
    ).strip()

    phone = str(
        data.get("phone", "")
    ).strip()

    category = api_normalize_category(
        data.get("category", "New")
    )

    if not code or not name:
        return jsonify({
            "ok": False,
            "error": "Client code and company name are required."
        }), 400

    db = get_db()

    try:
        db.execute("""
            INSERT INTO clients
            (
                code,
                name,
                phone,
                category
            )

            VALUES
            (
                ?,
                ?,
                ?,
                ?
            )
        """,
        (
            code,
            name,
            phone,
            category
        ))

        db.commit()

    except sqlite3.IntegrityError:
        db.close()

        return jsonify({
            "ok": False,
            "error": "That client code already exists."
        }), 409

    client = db.execute("""
        SELECT *
        FROM clients
        WHERE code = ?
    """,
    (
        code,
    )).fetchone()

    result = dict(client)

    db.close()

    return jsonify({
        "ok": True,
        "client": result
    }), 201


@app.route(
    "/api/clients/<int:client_id>/toggle",
    methods=["POST"]
)
def api_toggle_client(client_id):
    denied = api_auth_required()

    if denied:
        return denied

    db = get_db()

    client = db.execute("""
        SELECT called
        FROM clients
        WHERE id = ?
    """,
    (
        client_id,
    )).fetchone()

    if not client:
        db.close()

        return jsonify({
            "ok": False,
            "error": "Client not found."
        }), 404

    new_value = (
        0
        if client["called"]
        else 1
    )

    db.execute("""
        UPDATE clients

        SET
            called = ?,

            called_at =
            CASE
                WHEN ? = 1
                THEN datetime(
                    'now',
                    'localtime'
                )
                ELSE NULL
            END,

            updated_at =
            CURRENT_TIMESTAMP

        WHERE id = ?
    """,
    (
        new_value,
        new_value,
        client_id
    ))

    db.commit()

    updated = db.execute("""
        SELECT *
        FROM clients
        WHERE id = ?
    """,
    (
        client_id,
    )).fetchone()

    result = dict(updated)

    db.close()

    return jsonify({
        "ok": True,
        "client": result
    })


@app.route(
    "/api/clients/<int:client_id>/status",
    methods=["POST"]
)
def api_set_client_status(client_id):
    denied = api_auth_required()

    if denied:
        return denied

    data = request.get_json(
        silent=True
    ) or {}

    called = 1 if bool(
        data.get("called")
    ) else 0

    db = get_db()

    existing = db.execute("""
        SELECT id
        FROM clients
        WHERE id = ?
    """,
    (
        client_id,
    )).fetchone()

    if not existing:
        db.close()

        return jsonify({
            "ok": False,
            "error": "Client not found."
        }), 404

    db.execute("""
        UPDATE clients

        SET
            called = ?,

            called_at =
            CASE
                WHEN ? = 1
                THEN datetime(
                    'now',
                    'localtime'
                )
                ELSE NULL
            END,

            updated_at =
            CURRENT_TIMESTAMP

        WHERE id = ?
    """,
    (
        called,
        called,
        client_id
    ))

    db.commit()

    updated = db.execute("""
        SELECT *
        FROM clients
        WHERE id = ?
    """,
    (
        client_id,
    )).fetchone()

    result = dict(updated)

    db.close()

    return jsonify({
        "ok": True,
        "client": result
    })


@app.route(
    "/api/clients/bulk",
    methods=["POST"]
)
def api_bulk_clients():
    denied = api_auth_required()

    if denied:
        return denied

    data = request.get_json(
        silent=True
    ) or {}

    ids = data.get(
        "ids",
        []
    )

    action = str(
        data.get("action", "")
    ).strip().lower()

    clean_ids = []

    for value in ids:
        try:
            clean_ids.append(
                int(value)
            )
        except (
            TypeError,
            ValueError
        ):
            pass

    if not clean_ids:
        return jsonify({
            "ok": False,
            "error": "Select at least one client."
        }), 400

    value = (
        1
        if action == "called"
        else 0
    )

    placeholders = ",".join(
        "?"
        for _ in clean_ids
    )

    db = get_db()

    db.execute(
        f"""
        UPDATE clients

        SET
            called = ?,

            called_at =
            CASE
                WHEN ? = 1
                THEN datetime(
                    'now',
                    'localtime'
                )
                ELSE NULL
            END,

            updated_at =
            CURRENT_TIMESTAMP

        WHERE id IN ({placeholders})
        """,
        [
            value,
            value,
            *clean_ids
        ]
    )

    db.commit()
    db.close()

    return jsonify({
        "ok": True,
        "updated": len(clean_ids),
        "called": bool(value)
    })


@app.route(
    "/api/clients/import",
    methods=["POST"]
)
def api_import_clients():
    denied = api_auth_required()

    if denied:
        return denied

    import csv
    import io

    category = api_normalize_category(
        request.form.get(
            "category",
            "New"
        )
    )

    uploaded = request.files.get(
        "file"
    )

    if not uploaded:
        return jsonify({
            "ok": False,
            "error": "Select a CSV file."
        }), 400

    raw = uploaded.read()

    try:
        text = raw.decode(
            "utf-8-sig"
        )

    except UnicodeDecodeError:
        text = raw.decode(
            "latin-1"
        )

    try:
        dialect = csv.Sniffer().sniff(
            text[:3000],
            delimiters=",;\t"
        )

    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(
        io.StringIO(text),
        dialect=dialect
    )

    if not reader.fieldnames:
        return jsonify({
            "ok": False,
            "error": "CSV has no headers."
        }), 400

    headers = {
        h.strip().lower(): h
        for h in reader.fieldnames
        if h
    }

    code_column = (
        headers.get("code")
        or headers.get("codigo")
        or headers.get("código")
    )

    name_column = (
        headers.get("name")
        or headers.get("nombre")
        or headers.get("empresa")
        or headers.get("cliente")
        or headers.get("client")
    )

    phone_column = (
        headers.get("phone")
        or headers.get("telefono")
        or headers.get("teléfono")
        or headers.get("telefono principal")
        or headers.get("number")
    )

    if (
        not code_column
        or not name_column
    ):
        return jsonify({
            "ok": False,
            "error": (
                "CSV needs code/name "
                "or codigo/nombre columns."
            )
        }), 400

    db = get_db()

    added = 0
    updated = 0
    skipped = 0

    for row in reader:
        code = (
            row.get(
                code_column
            ) or ""
        ).strip()

        name = (
            row.get(
                name_column
            ) or ""
        ).strip()

        phone = (
            (
                row.get(
                    phone_column
                )
                if phone_column
                else ""
            )
            or ""
        ).strip()

        if not code or not name:
            skipped += 1
            continue

        existing = db.execute("""
            SELECT *
            FROM clients
            WHERE code = ?
        """,
        (
            code,
        )).fetchone()

        if existing:
            if (
                existing["name"] != name
                or (
                    existing["phone"]
                    or ""
                ) != phone
                or (
                    existing["category"]
                    or "New"
                ) != category
            ):
                db.execute("""
                    UPDATE clients

                    SET
                        name = ?,
                        phone = ?,
                        category = ?,
                        updated_at =
                        CURRENT_TIMESTAMP

                    WHERE code = ?
                """,
                (
                    name,
                    phone,
                    category,
                    code
                ))

                updated += 1

            else:
                skipped += 1

        else:
            db.execute("""
                INSERT INTO clients
                (
                    code,
                    name,
                    phone,
                    category
                )

                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?
                )
            """,
            (
                code,
                name,
                phone,
                category
            ))

            added += 1

    db.commit()
    db.close()

    return jsonify({
        "ok": True,
        "added": added,
        "updated": updated,
        "unchanged": skipped,
        "category": category
    })

# ============================================================
# END ANDROID REST API
# ============================================================



if __name__ == "__main__":

    init_db()

    print("")
    print(
        "===================================="
    )
    print(
        "       CLIENT FOLLOW-UP LOCAL"
    )
    print(
        "===================================="
    )
    print("")
    print(
        "http://127.0.0.1:5000"
    )
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

