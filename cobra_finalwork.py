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
    --black: #010407;
    --black2: #031018;
    --panel: rgba(3, 16, 25, 0.86);
    --panel2: rgba(4, 21, 31, 0.92);
    --line: rgba(45, 157, 217, 0.60);
    --cyan: #37cfff;
    --blue: #1687ff;
    --green: #1df58a;
    --green2: #0ee777;
    --red: #ff4d5c;
    --text: #f7fbff;
    --muted2: #b5c6d8;
}

html {
    background: var(--black);
}

body {
    min-height: 100vh;
    color: var(--text);
    background:
        radial-gradient(circle at 83% 10%, rgba(0,255,120,.20), transparent 24%),
        radial-gradient(circle at 15% 84%, rgba(0,140,255,.12), transparent 27%),
        linear-gradient(180deg,#010509 0%,#041018 48%,#010509 100%) !important;
    overflow-x: hidden;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: -20;
    pointer-events: none;
    background-image: url("/static/cobra-reference.png");
    background-size: cover;
    background-position: center top;
    filter: blur(17px) saturate(1.35) contrast(1.12) brightness(.50);
    transform: scale(1.06);
    opacity: .28;
}

body::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: -19;
    pointer-events: none;
    background:
        linear-gradient(90deg,rgba(0,5,9,.78) 0%,rgba(0,5,9,.42) 45%,rgba(0,7,8,.23) 100%),
        linear-gradient(180deg,rgba(0,3,6,.18),rgba(0,5,9,.60) 62%,rgba(0,3,6,.90));
}

.topbar {
    position: relative;
    z-index: 50;
    padding: 11px clamp(18px, 4.5vw, 72px) !important;
    background: rgba(1,8,13,.84) !important;
    border-bottom: 1px solid rgba(35,175,232,.56) !important;
    box-shadow: 0 7px 26px rgba(0,0,0,.34), 0 0 22px rgba(0,153,255,.08);
    backdrop-filter: blur(18px) saturate(1.15);
    -webkit-backdrop-filter: blur(18px) saturate(1.15);
}

.brand {
    font-size: clamp(20px,2.1vw,31px) !important;
    font-weight: 850 !important;
    letter-spacing: -1px;
    color: #fff;
    text-shadow: 0 3px 18px rgba(0,0,0,.55);
}

.brand .brand-accent {
    color: var(--green);
    text-shadow: 0 0 18px rgba(29,245,138,.28);
}

.lab {
    padding: 7px 13px !important;
    border-radius: 10px !important;
    background: rgba(4,65,40,.52) !important;
    color: #a8ffd0 !important;
    border: 1px solid rgba(29,245,138,.95) !important;
    box-shadow: inset 0 0 15px rgba(29,245,138,.10),0 0 18px rgba(29,245,138,.16);
}

.topbar .secondary {
    background: rgba(7,20,34,.90) !important;
    border: 1px solid rgba(73,151,208,.60) !important;
    color: #fff !important;
    box-shadow: inset 0 0 18px rgba(22,135,255,.06),0 0 16px rgba(22,135,255,.08);
}

.container {
    max-width: 1540px !important;
    padding: 18px clamp(14px,4.5vw,72px) 50px !important;
}

.client-dashboard {
    position: relative;
    isolation: isolate;
    min-height: calc(100vh - 86px);
}

.client-dashboard::before {
    content: "";
    position: absolute;
    z-index: -4;
    top: -18px;
    left: -36px;
    right: -36px;
    height: 470px;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 78% 34%,rgba(0,255,111,.20),transparent 42%),
        radial-gradient(ellipse at 28% 26%,rgba(0,151,255,.08),transparent 34%);
}

.cobra-hero {
    position: absolute;
    z-index: -2;
    pointer-events: none;
    top: -78px;
    right: -42px;
    width: min(800px,54vw);
    height: 470px;
    overflow: hidden;
    opacity: .98;
    filter: saturate(1.22) contrast(1.08) brightness(.95);
    border-radius: 0 0 0 42px;
    mask-image: linear-gradient(90deg,transparent 0%,rgba(0,0,0,.36) 13%,#000 34%,#000 100%);
    -webkit-mask-image: linear-gradient(90deg,transparent 0%,rgba(0,0,0,.36) 13%,#000 34%,#000 100%);
}

.cobra-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("/static/cobra-reference.png");
    background-repeat: no-repeat;
    background-size: 1536px 1024px;
    background-position: right -10px top 0;
    transform: scale(1.08);
    transform-origin: right top;
}

.cobra-hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(90deg,#010509 0%,rgba(1,5,9,.56) 14%,rgba(1,5,9,.05) 38%,transparent 100%),
        linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(1,5,9,.28) 76%,#010509 100%);
}

.hero-copy {
    position: relative;
    z-index: 3;
    max-width: 800px;
    padding-top: 23px;
}

.hero-title {
    margin: 0;
    font-size: clamp(36px,4.9vw,65px);
    line-height: .98;
    font-weight: 900;
    letter-spacing: -2.4px;
    text-shadow: 0 4px 24px rgba(0,0,0,.62);
}

.hero-title .accent {
    color: var(--green);
    text-shadow: 0 0 23px rgba(29,245,138,.30);
}

.hero-subtitle {
    margin: 15px 0 20px;
    color: #d0dcec;
    font-size: clamp(15px,1.65vw,21px);
    font-weight: 650;
    text-shadow: 0 3px 12px rgba(0,0,0,.62);
}

.stats-grid {
    position: relative;
    z-index: 4;
    display: grid;
    grid-template-columns: repeat(3,minmax(0,1fr));
    gap: 18px;
    max-width: 920px;
    margin-top: 8px;
}

.stat-card {
    position: relative;
    min-height: 114px;
    padding: 17px 20px;
    border-radius: 16px;
    border: 1.5px solid rgba(64,146,204,.78);
    background: linear-gradient(145deg,rgba(7,29,48,.94),rgba(3,14,25,.86));
    box-shadow: 0 15px 35px rgba(0,0,0,.36),inset 0 1px 0 rgba(255,255,255,.06);
    backdrop-filter: blur(14px) saturate(1.18);
    -webkit-backdrop-filter: blur(14px) saturate(1.18);
    display: grid;
    grid-template-columns: 62px 1fr;
    align-items: center;
    gap: 16px;
    overflow: hidden;
}

.stat-card::after {
    content:"";
    position:absolute;
    inset:-40% 45% 35% -20%;
    transform:rotate(-18deg);
    background:linear-gradient(90deg,transparent,rgba(255,255,255,.10),transparent);
    pointer-events:none;
}

.total-card {
    border-color:#1b91ff;
    background:linear-gradient(145deg,rgba(7,37,72,.96),rgba(2,15,33,.90));
    box-shadow:0 0 26px rgba(20,136,255,.34),0 15px 35px rgba(0,0,0,.35),inset 0 0 22px rgba(20,136,255,.08);
}

.called-card {
    border-color:#25e58b;
    background:linear-gradient(145deg,rgba(3,72,43,.92),rgba(2,27,20,.90));
    box-shadow:0 0 26px rgba(29,245,138,.26),0 15px 35px rgba(0,0,0,.35),inset 0 0 22px rgba(29,245,138,.08);
}

.pending-card {
    border-color:#ff5264;
    background:linear-gradient(145deg,rgba(89,20,32,.94),rgba(34,8,17,.91));
    box-shadow:0 0 26px rgba(255,77,92,.25),0 15px 35px rgba(0,0,0,.35),inset 0 0 22px rgba(255,77,92,.07);
}

.stat-icon {
    width: 59px;
    height: 59px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 29px;
    border: 1px solid rgba(255,255,255,.10);
    background: linear-gradient(145deg,rgba(16,119,224,.62),rgba(6,57,116,.62));
    box-shadow: inset 0 0 18px rgba(255,255,255,.05),0 0 18px rgba(20,136,255,.20);
}
.called-card .stat-icon {background:linear-gradient(145deg,rgba(22,173,94,.70),rgba(5,83,48,.62));box-shadow:0 0 18px rgba(29,245,138,.20)}
.pending-card .stat-icon {background:linear-gradient(145deg,rgba(218,55,75,.72),rgba(112,22,38,.60));box-shadow:0 0 18px rgba(255,77,92,.20)}

.stat-label {color:#e0e9f3;font-size:15px;font-weight:650}
.stat-number {margin-top:5px;font-size:34px;line-height:1;font-weight:900}
.called-card .stat-number{color:#76ffb9}
.pending-card .stat-number{color:#ff9aa3}

.category-tabs {
    position: relative;
    z-index: 5;
    display:flex;
    gap:10px;
    overflow-x:auto;
    margin:18px 0 19px;
    padding:2px 2px 5px;
    scrollbar-width:none;
    white-space:nowrap;
}
.category-tabs::-webkit-scrollbar{display:none}

.category-chip {
    flex:0 0 auto;
    padding:10px 19px;
    border-radius:11px;
    border:1px solid rgba(68,144,199,.66);
    color:#e1ecf7;
    text-decoration:none;
    font-size:13px;
    font-weight:750;
    background:linear-gradient(180deg,rgba(8,31,50,.92),rgba(5,20,34,.90));
    box-shadow:inset 0 0 13px rgba(19,123,196,.04);
    transition:.18s ease;
}
.category-chip:hover{transform:translateY(-1px);border-color:#3dd5ff;box-shadow:0 0 15px rgba(55,207,255,.14)}
.category-chip.active{color:#fff;border-color:#27ef8e;background:linear-gradient(145deg,rgba(6,101,58,.95),rgba(6,54,38,.93));box-shadow:0 0 20px rgba(29,245,138,.28),inset 0 0 18px rgba(29,245,138,.08)}

.work-grid {
    position:relative;
    z-index:5;
    display:grid;
    grid-template-columns:1.08fr .92fr;
    gap:18px;
}

.pro-panel {
    position:relative;
    margin:0 !important;
    padding:18px 20px !important;
    border-radius:15px !important;
    border:1.25px solid rgba(42,205,192,.72) !important;
    background:linear-gradient(145deg,rgba(3,24,35,.91),rgba(3,15,25,.88)) !important;
    box-shadow:0 18px 38px rgba(0,0,0,.33),0 0 20px rgba(29,245,138,.08),inset 0 0 32px rgba(42,205,192,.025) !important;
    backdrop-filter:blur(16px) saturate(1.15);
    -webkit-backdrop-filter:blur(16px) saturate(1.15);
    overflow:hidden;
}
.pro-panel::before{
    content:"";
    position:absolute;
    top:0;left:4%;right:4%;height:1px;
    background:linear-gradient(90deg,transparent,rgba(29,245,138,.75),transparent);
    box-shadow:0 0 12px rgba(29,245,138,.35);
}

.panel-title {margin:0 0 16px;font-size:18px;font-weight:850;display:flex;align-items:center;gap:10px;color:#fff}
.panel-icon {width:31px;height:31px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(145deg,#24f59a,#0fa75f);color:#062414;font-weight:950;box-shadow:0 0 18px rgba(29,245,138,.28)}

.add-form {display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:11px !important}
.add-form .full-width-btn{grid-column:1/-1}

.import-form {display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:13px;align-items:stretch}
.import-help{margin:12px 0 0 !important;line-height:1.45;color:#c7d4e2 !important}

input,select {
    min-height:47px !important;
    border-radius:10px !important;
    border:1px solid rgba(67,146,202,.64) !important;
    background:linear-gradient(180deg,rgba(5,21,36,.95),rgba(3,14,24,.95)) !important;
    color:#f6fbff !important;
    box-shadow:inset 0 0 18px rgba(0,130,255,.025),0 0 0 1px rgba(255,255,255,.012);
}
input::placeholder{color:#a9bdd1 !important}
input:focus,select:focus{outline:none !important;border-color:#37cfff !important;box-shadow:0 0 0 2px rgba(55,207,255,.13),0 0 20px rgba(55,207,255,.10) !important}
input[type=file]{padding:8px 9px !important}

button,.button {border-radius:10px !important;font-weight:800 !important;letter-spacing:.1px}
.primary-blue {background:linear-gradient(180deg,#1d94ff 0%,#056ff1 100%) !important;border:1px solid #4ab3ff !important;color:#fff !important;box-shadow:0 0 24px rgba(22,135,255,.27),inset 0 1px 0 rgba(255,255,255,.22) !important}
.primary-green,.success {background:linear-gradient(180deg,#22e88a 0%,#0b9f5a 100%) !important;border:1px solid #58ffaf !important;color:#f4fff8 !important;box-shadow:0 0 23px rgba(29,245,138,.22),inset 0 1px 0 rgba(255,255,255,.18) !important}
.danger {background:linear-gradient(180deg,#df4052 0%,#9f1627 100%) !important;border:1px solid #ff6878 !important;color:#fff !important;box-shadow:0 0 23px rgba(255,77,92,.20),inset 0 1px 0 rgba(255,255,255,.14) !important}
button:hover,.button:hover{filter:brightness(1.08);transform:translateY(-1px)}

.control-strip {
    position:relative;
    z-index:5;
    display:grid;
    grid-template-columns:minmax(0,1.45fr) auto;
    gap:18px;
    align-items:center;
    margin:15px 0 10px;
}
.search-toolbar {display:grid !important;grid-template-columns:minmax(260px,1.45fr) minmax(160px,.62fr) 175px !important;gap:11px !important;margin:0 !important}
.bulk-actions{display:flex;gap:11px;justify-content:flex-end;align-items:center}
.bulk-actions button{min-width:150px}
.bulk-help{text-align:right;margin-top:4px;color:#c4d0dc !important}

.results-panel {
    position:relative;
    z-index:5;
    margin-top:0 !important;
    border-radius:14px !important;
    border:1.25px solid rgba(53,165,220,.58) !important;
    background:rgba(2,14,23,.88) !important;
    box-shadow:0 20px 45px rgba(0,0,0,.38),0 0 24px rgba(18,165,224,.07),inset 0 0 28px rgba(11,79,124,.03);
    backdrop-filter:blur(14px);
    -webkit-backdrop-filter:blur(14px);
    overflow:auto;
}

.results-panel table {background:transparent !important;min-width:930px !important}
.results-panel thead th {background:linear-gradient(180deg,rgba(8,35,55,.94),rgba(4,23,37,.94)) !important;color:#eff7ff !important;font-weight:850 !important;border-bottom:1px solid rgba(60,157,214,.42) !important}
.results-panel th,.results-panel td {padding:11px 13px !important;border-right:1px solid rgba(48,111,151,.19);border-bottom:1px solid rgba(48,111,151,.24) !important}
.results-panel tbody tr {background:rgba(3,17,27,.30);transition:.14s ease}
.results-panel tbody tr:nth-child(even){background:rgba(5,26,39,.30)}
.results-panel tbody tr:hover{background:rgba(10,49,67,.52);box-shadow:inset 3px 0 0 rgba(29,245,138,.55)}
.results-panel tbody tr:last-child td{border-bottom:none !important}

.status {min-width:86px;text-align:center;padding:5px 10px !important;border-radius:8px !important;font-size:11px !important;font-weight:900 !important;letter-spacing:.15px}
.status.yes {background:linear-gradient(180deg,rgba(14,155,77,.96),rgba(4,92,47,.96)) !important;color:#dfffee !important;border:1px solid rgba(50,255,144,.42);box-shadow:0 0 13px rgba(29,245,138,.15)}
.status.no {background:linear-gradient(180deg,rgba(207,39,58,.96),rgba(122,14,29,.96)) !important;color:#fff1f3 !important;border:1px solid rgba(255,86,102,.48);box-shadow:0 0 13px rgba(255,77,92,.14)}
.called-at-cell{white-space:nowrap;color:#dbe6f2}
.quick-button {min-width:105px;background:linear-gradient(180deg,rgba(32,79,119,.96),rgba(17,49,78,.96)) !important;border:1px solid rgba(88,158,210,.63) !important;color:#fff !important;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.empty-state{text-align:center;color:#a8bbcf;padding:30px !important}

.flash {position:relative;z-index:80;background:rgba(5,31,43,.93) !important;border:1px solid rgba(29,245,138,.47) !important;box-shadow:0 0 18px rgba(29,245,138,.08)}

@media (max-width:1100px){
    .cobra-hero{right:-155px;width:760px;opacity:.82}
    .stats-grid{max-width:780px}
    .work-grid{grid-template-columns:1fr}
    .control-strip{grid-template-columns:1fr}
    .bulk-actions{justify-content:flex-start}
    .bulk-help{text-align:left}
}

@media (max-width:780px){
    .container{padding:13px 11px 34px !important}
    .topbar{padding:10px 12px !important}
    .brand{font-size:18px !important}
    .topbar .actions{gap:6px}
    .topbar .button,.topbar .lab{padding:7px 9px !important;font-size:10px !important}
    .cobra-hero{top:-28px;right:-300px;width:650px;height:320px;opacity:.46}
    .hero-copy{padding-top:7px;padding-right:28px}
    .hero-title{font-size:31px}
    .hero-subtitle{font-size:13px;max-width:82%}
    .stats-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;max-width:none}
    .stat-card{min-height:92px;padding:10px 8px;grid-template-columns:1fr;gap:3px}
    .stat-icon{width:30px;height:30px;font-size:15px}
    .stat-label{font-size:9px}
    .stat-number{font-size:22px}
    .category-tabs{gap:6px;margin:10px 0 13px}
    .category-chip{padding:7px 10px;font-size:10px}
    .pro-panel{padding:14px !important}
    .panel-title{font-size:15px;margin-bottom:12px}
    .add-form,.import-form,.search-toolbar{grid-template-columns:1fr !important}
    .import-form .primary-green{width:100%}
    .control-strip{gap:10px;margin-top:12px}
    .bulk-actions{flex-wrap:wrap}
    .bulk-actions button{flex:1 1 140px;min-width:0}
    .results-panel{border-radius:10px !important}
    .results-panel table{min-width:840px !important}
    .results-panel th,.results-panel td{padding:9px 10px !important;font-size:11px}
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

