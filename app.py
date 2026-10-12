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


</style>

</head>


<body>


<div class="topbar">

    <div class="brand">

        Client Follow-Up

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

    <h1>
        Client Follow-Up
    </h1>

    <p class="muted">

        Track which clients
        have already been called.

    </p>


    <div class="grid">

        <div class="card">

            <div class="muted">
                Total Clients
            </div>

            <div class="number">

                {{ total }}

            </div>

        </div>


        <div class="card">

            <div class="muted">
                Called
            </div>

            <div class="number green">

                {{ called }}

            </div>

        </div>


        <div class="card">

            <div class="muted">
                Not Called
            </div>

            <div class="number red">

                {{ pending }}

            </div>

        </div>

    </div>



    <div style="
    display:flex;
    gap:6px;
    overflow-x:auto;
    margin-top:12px;
    margin-bottom:8px;
    padding-bottom:3px;
    white-space:nowrap;
">

    {% for cat in ["All", "New", "Prospect", "Projects", "PT Commerce", "Restaurant", "Integrations", "GN"] %}

    <a
        href="{{ url_for('clients', category=cat) }}"
        style="
            padding:7px 12px;
            border-radius:7px;
            text-decoration:none;
            font-size:12px;
            font-weight:600;
            background:
            {% if request.args.get('category', 'All') == cat %}
                #2563eb
            {% else %}
                #13243a
            {% endif %};
            color:white;
            flex-shrink:0;
        "
    >
        {{ cat }}
    </a>

    {% endfor %}

</div>

<div
    class="card"
    style="margin-top:15px;"
    >





        <h3>
            Add Client
        </h3>


        <form
        method="POST"
        action="{{ url_for('add_client') }}"
        class="row"
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


            <button>

                Add

            </button>

        </form>

    </div>



    <div
    class="card"
    style="margin-top:15px;"
    >

        <h3>
            Import Clients
        </h3>


        <form
        method="POST"
        action="{{ url_for('import_clients', category=request.args.get('category', 'All')) }}"
        enctype="multipart/form-data"
        class="actions"
        >

            <input
            type="file"
            name="file"
            accept=".csv"
            required
            style="max-width:500px;"
            >


            <button>

                Import CSV

            </button>

        </form>


        <p class="muted small">

            CSV columns:

            <b>code</b>

            and

            <b>name</b>

            <br><br>

            It also accepts:

            codigo / nombre.

        </p>

    </div>



    <form
    method="GET"
    class="toolbar"
    >

        <input
        name="search"
        value="{{ search }}"
        placeholder="Search client..."
        >


        <select name="status">

            <option
            value="all"
            {% if status == "all" %}
            selected
            {% endif %}
            >

                All

            </option>


            <option
            value="pending"
            {% if status == "pending" %}
            selected
            {% endif %}
            >

                Not Called

            </option>


            <option
            value="called"
            {% if status == "called" %}
            selected
            {% endif %}
            >

                Called

            </option>

        </select>


        <button>

            Search

        </button>

    </form>



    <form
    method="POST"
    action="{{ url_for('bulk_update') }}"
    >
<input
type="hidden"
name="category"
value="{{ category }}"
>



        <div
        class="actions"
        style="margin-bottom:10px;"
        >

            <button
            name="action"
            value="called"
            class="success"
            >

                ✓ Mark Called

            </button>


            <button
            name="action"
            value="pending"
            class="danger"
            >

                ✕ Mark Not Called

            </button>


            <span class="muted small">

                Select one or multiple clients.

            </span>

        </div>



        <div class="table-wrapper">


        <table>


        <thead>

        <tr>

            <th>

                <input
                type="checkbox"
                onclick="selectAll(this)"
                >

            </th>


            <th>
                Code
            </th>


            <th>
                Company
            </th>

            <th>
                Phone
            </th>


            <th>
                Status
            </th>


            <th>
                Quick Action
            </th>

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


            <td>

                {{ client["code"] }}

            </td>


            <td>

                {{ client["name"] }}

            </td>


            <td>
                {{ client["phone"] or "" }}
            </td>


            <td>


                {% if client["called"] %}

                <span class="status yes">

                    CALLED

                </span>



                {% if client["called_at"] %}
                <div class="call-time">
{{ client["called_at"][8:10] }}/{{ client["called_at"][5:7] }}/{{ client["called_at"][0:4] }} · {{ client["called_at"][11:16] }}
</div>
{% endif %}


                {% else %}

                <span class="status no">

                    NOT CALLED

                </span>

                {% endif %}


            </td>


            <td>

                <button
                class="secondary"
                formaction="{{ url_for(
                    'toggle_client',
                    client_id=client['id'],
                    category=category
                ) }}"
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

            <td colspan="5">

                No clients found.

            </td>

        </tr>


        {% endfor %}


        </tbody>


        </table>


        </div>


    </form>





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

