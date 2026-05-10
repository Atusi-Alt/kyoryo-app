# =====================================================
# 橋梁膜厚管理 Ultimate Edition
# 現場最強UI版
# =====================================================

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template_string
from flask import session

from supabase import create_client

from datetime import datetime

import json

# =====================================================
# APP
# =====================================================

app = Flask(__name__)

app.secret_key = "sakura"

# =====================================================
# SUPABASE
# =====================================================

url = "https://xcjgbrzqxkgoiynjsdhc.supabase.co"

key = "sb_publishable_Z-nEPLmqRbLV_kWy_lW0GA_b7DC-EIn"

supabase = create_client(url, key)

# =====================================================
# USER
# =====================================================

users = {

    "敦司":"6788",
    "furui":"6788",
    "tsuchiya":"6788",
    "akashi":"6788",
    "kawano":"6788"
}

# =====================================================
# MASTER
# =====================================================

sites = [

    "ミカドR6-1",
    "ミカドR6-2"
]

bridges = {

    "ミカドR6-1":[

        "I 1-286",
        "I 2-286",

        "I 1-287",
        "I 2-287",

        "I 1-288",
        "I 2-288",

        "I 1-289",
        "I 2-289",

        "I 1-290",
        "I 2-290",

        "I 1-291",
        "I 2-291",

        "I 1-292",
        "I 2-292",

        "I-287",
        "I-288",
        "I-289",
        "I-290",
        "I-291",
        "I-292"
    ],

    "ミカドR6-2":[

        "Ⅱ 1-144",
        "Ⅱ 2-144",
        "入-144",

        "Ⅱ 1-145",
        "Ⅱ 2-145",
        "入-145",

        "Ⅱ 1-146",
        "Ⅱ 2-146",
        "入-146",

        "Ⅱ-145",
        "Ⅱ-146",
        "Ⅱ-147"
    ]
}

places = [

    "上部工",
    "下部工",
    "上部工内面",
    "下部工内面"
]

parts = [

    "一般部",
    "増し塗り部",
    "一種部"
]

processes = [

    "素地調整",
    "防食下地",
    "下塗1",
    "増し塗1",
    "増し塗2",
    "下塗2",
    "中塗",
    "上塗",
    "補修塗"
]

# =====================================================
# 判定基準
# =====================================================

standards = {

    "防食下地":75,

    "下塗1":60,

    "増し塗1":60,

    "増し塗2":60,

    "下塗2":60,

    "中塗":30,

    "上塗":25
}

# =====================================================
# 部位別工程順
# =====================================================

part_process_orders = {

    "一般部":[

        "補修塗",
        "下塗1",
        "下塗2",
        "中塗",
        "上塗"
    ],

    "増し塗り部":[

        "補修塗",
        "下塗1",
        "増し塗1",
        "増し塗2",
        "下塗2",
        "中塗",
        "上塗"
    ],

    "一種部":[

        "素地調整",
        "防食下地",
        "下塗1",
        "増し塗1",
        "増し塗2",
        "下塗2",
        "中塗",
        "上塗"
    ]
}

# =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        user_id = request.form.get("id")

        password = request.form.get("pw")

        if user_id in users:

            if users[user_id] == password:

                session["login"] = True

                session["user"] = user_id

                return redirect("/")

    return """

<!DOCTYPE html>

<html>

<head>

<meta charset='UTF-8'>

<meta name='viewport'
content='width=device-width, initial-scale=1.0'>

<style>

body{

    margin:0;
    background:#0f172a;
    color:white;
    font-family:Arial;
}

.box{

    max-width:420px;
    margin:120px auto;
    background:#111827;
    border-radius:25px;
    padding:25px;
}

h1{

    text-align:center;
    color:#38bdf8;
}

input{

    width:100%;
    height:55px;
    margin-top:15px;
    padding:12px;
    border:none;
    border-radius:12px;
    background:#1e293b;
    color:white;
    font-size:18px;
    box-sizing:border-box;
}

button{

    width:100%;
    padding:15px;
    margin-top:20px;
    border:none;
    border-radius:14px;
    background:linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );
    color:white;
    font-size:20px;
    font-weight:bold;
}

</style>

</head>

<body>

<div class='box'>

<h1>橋梁膜厚管理</h1>

<form method='POST'>

<input
name='id'
placeholder='ID'>

<input
type='password'
name='pw'
placeholder='パスワード'>

<button type='submit'>

ログイン

</button>

</form>

</div>

</body>

</html>

"""

# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# =====================================================
# HOME
# =====================================================

@app.route("/", methods=["GET","POST"])
def home():

    if not session.get("login"):

        return redirect("/login")

    if request.method == "POST":

        data = {

            "datetime":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

            "user_name":
            session.get("user"),

            "site":
            request.form.get("site"),

            "bridge":
            request.form.get("bridge"),

            "place":
            request.form.get("place"),

            "part":
            request.form.get("part"),

            "lot":
            request.form.get("lot"),

            "point":
            request.form.get("point"),

            "process":
            request.form.get("process"),

            "thickness":
            request.form.get("thickness")
        }

        supabase.table("data").insert(
            data
        ).execute()

        return redirect("/")

    return render_template_string("""

<!DOCTYPE html>

<html>

<head>

<meta charset='UTF-8'>

<meta name='viewport'
content='width=device-width, initial-scale=1.0'>

<style>

body{

    margin:0;
    background:#0f172a;
    color:white;
    font-family:Arial;
}

.header{

    background:linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );

    padding:18px;

    text-align:center;

    font-size:24px;

    font-weight:bold;
}

.container{

    max-width:650px;

    margin:auto;

    padding:15px;
}

.card{

    background:#111827;

    border-radius:25px;

    padding:22px;
}

label{

    display:block;

    margin-top:16px;

    margin-bottom:6px;

    font-weight:bold;

    color:#93c5fd;
}

input,select{

    width:100%;

    height:55px;

    padding:12px;

    border:none;

    border-radius:12px;

    background:#1e293b;

    color:white;

    font-size:18px;

    box-sizing:border-box;
}

button{

    width:100%;

    padding:15px;

    margin-top:18px;

    border:none;

    border-radius:14px;

    background:linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );

    color:white;

    font-size:20px;

    font-weight:bold;
}

.sub{

    background:#1e293b;
}

</style>

</head>

<body>

<div class='header'>

橋梁膜厚管理

</div>

<div class='container'>

<div class='card'>

<form method='POST'>

<label>現場名</label>

<select
id='site'
name='site'
onchange='changeBridge()'>

<option>ミカドR6-1</option>
<option>ミカドR6-2</option>

</select>

<label>橋名</label>

<select
id='bridge'
name='bridge'>

</select>

<label>箇所</label>

<select name='place'>

<option>上部工</option>
<option>下部工</option>
<option>上部工内面</option>
<option>下部工内面</option>

</select>

<label>部位</label>

<select name='part'>

<option>一般部</option>
<option>増し塗り部</option>
<option>一種部</option>

</select>

<label>ロット</label>

<select name='lot'>

{% for i in range(1,51) %}

<option>{{i}}</option>

{% endfor %}

</select>

<label>測点</label>

<select name='point'>

{% for i in range(1,26) %}

<option>{{i}}</option>

{% endfor %}

</select>

<label>工程</label>

<select name='process'>

<option>素地調整</option>
<option>防食下地</option>
<option>下塗1</option>
<option>増し塗1</option>
<option>増し塗2</option>
<option>下塗2</option>
<option>中塗</option>
<option>上塗</option>
<option>補修塗</option>

</select>

<label>膜厚</label>

<input
type='number'
name='thickness'
required>

<button type='submit'>

保存

</button>

</form>

<a href='/list'>

<button class='sub'>

入力情報一覧

</button>

</a>

<a href='/logout'>

<button class='sub'>

ログアウト

</button>

</a>

</div>

</div>

<script>

const bridges = {{ bridges|safe }}

function changeBridge(){

    let site =
    document.getElementById(
        "site"
    ).value

    let bridgeSelect =
    document.getElementById(
        "bridge"
    )

    bridgeSelect.innerHTML = ""

    bridges[site].forEach(function(b){

        let option =
        document.createElement(
            "option"
        )

        option.value = b

        option.text = b

        bridgeSelect.appendChild(
            option
        )
    })
}

changeBridge()

</script>

</body>

</html>

""", bridges=json.dumps(bridges))

# =====================================================
# LIST
# =====================================================

@app.route("/list")
def list_page():

    if not session.get("login"):

        return redirect("/login")

    rows = supabase.table("data")\
        .select("*")\
        .order("id")\
        .execute().data

    html = ""

    bridge_names = []

    for row in rows:

        bridge = row.get("bridge")

        if bridge not in bridge_names:

            bridge_names.append(bridge)

    for bridge in bridge_names:

        html += f"""

<details class='bridge'>

<summary>

{bridge}

</summary>

"""

        bridge_rows = [

            x for x in rows
            if x.get("bridge") == bridge
        ]

        for lot in range(1,51):

            lot_rows = [

                x for x in bridge_rows
                if str(x.get("lot")) == str(lot)
            ]

            if not lot_rows:

                continue

            html += f"""

<details class='lot'>

<summary>

{lot}ロット

</summary>

"""

            point_names = []

            for row in lot_rows:

                point = row.get("point")

                if point not in point_names:

                    point_names.append(point)

            for point in point_names:

                point_rows = [

                    x for x in lot_rows
                    if x.get("point") == point
                ]

                html += f"""

<details class='point'>

<summary>

測点 {point}

</summary>

"""

                for part in parts:

                    part_rows = [

                        x for x in point_rows
                        if x.get("part") == part
                    ]

                    if not part_rows:

                        continue

                    html += f"""

<div class='part-title'>

{part}

</div>

"""

                    order = part_process_orders.get(
                        part,
                        []
                    )

                    sorted_rows = []

                    for process in order:

                        for row in part_rows:

                            if row.get("process") == process:

                                sorted_rows.append(row)

                    prev = 0

                    for index,row in enumerate(sorted_rows):

                        process = row.get("process")

                        thickness = int(
                            row.get("thickness",0)
                        )

                        difference = 0

                        if index != 0:

                            difference = (
                                thickness - prev
                            )

                        prev = thickness

                        result = "OK"

                        if process in standards:

                            if thickness < standards[process]:

                                result = "NG"

                        color = "#22c55e"

                        if result == "NG":

                            color = "#ef4444"

                        html += f"""

<div class='process-card'>

<div class='top'>

<div class='process-name'>

{process}

</div>

<div class='judge'
style='color:{color};'>

{result}

</div>

</div>

<div class='value'>

膜厚 {thickness}μ

</div>

<div class='difference'>

前層差 +{difference}μ

</div>

<div class='subdata'>

{row.get('place')}

・

{row.get('datetime')}

・

{row.get('user_name')}

</div>

<div class='btns'>

<a href='/edit/{row['id']}'>

<button class='edit'>

編集

</button>

</a>

<a href='/delete/{row['id']}'>

<button class='delete'>

削除

</button>

</a>

</div>

</div>

"""

                html += "</details>"

            html += "</details>"

        html += "</details>"

    return f"""

<!DOCTYPE html>

<html>

<head>

<meta charset='UTF-8'>

<meta name='viewport'
content='width=device-width, initial-scale=1.0'>

<style>

body{{

    margin:0;

    background:#d1d5db;

    font-family:Arial;

    padding:15px;
}}

.main-btn{{

    width:100%;

    padding:18px;

    border:none;

    border-radius:16px;

    background:linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );

    color:white;

    font-size:22px;

    font-weight:bold;

    margin-bottom:20px;
}}

.bridge{{

    background:white;

    border-radius:24px;

    margin-bottom:20px;

    padding:12px;
}}

.bridge summary{{

    font-size:42px;

    font-weight:bold;

    list-style:none;

    cursor:pointer;
}}

.lot{{

    margin-top:15px;
}}

.lot summary{{

    font-size:30px;

    font-weight:bold;

    cursor:pointer;
}}

.point{{

    margin-top:12px;

    background:#e5e7eb;

    border-radius:18px;

    padding:10px;
}}

.point summary{{

    font-size:24px;

    font-weight:bold;

    cursor:pointer;
}}

.part-title{{

    margin-top:15px;

    background:#1e3a8a;

    color:white;

    padding:15px;

    border-radius:14px;

    font-size:24px;

    font-weight:bold;
}}

.process-card{{

    background:white;

    border-radius:18px;

    padding:18px;

    margin-top:14px;

    box-shadow:0 0 10px rgba(
        0,0,0,0.1
    );
}}

.top{{

    display:flex;

    justify-content:space-between;

    align-items:center;
}}

.process-name{{

    font-size:28px;

    font-weight:bold;
}}

.judge{{

    font-size:26px;

    font-weight:bold;
}}

.value{{

    margin-top:15px;

    font-size:34px;

    font-weight:bold;
}}

.difference{{

    margin-top:8px;

    font-size:24px;

    color:#2563eb;

    font-weight:bold;
}}

.subdata{{

    margin-top:10px;

    color:#6b7280;

    font-size:15px;
}}

.btns{{

    display:flex;

    gap:10px;

    margin-top:15px;
}}

.edit{{

    flex:1;

    background:#2563eb;
}}

.delete{{

    flex:1;

    background:#dc2626;
}}

button{{

    width:100%;

    padding:12px;

    border:none;

    border-radius:12px;

    color:white;

    font-size:18px;

    font-weight:bold;
}}

</style>

</head>

<body>

<a href='/'>

<button class='main-btn'>

戻る

</button>

</a>

{html}

</body>

</html>

"""

# =====================================================
# EDIT
# =====================================================

@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id):

    row = supabase.table("data")\
        .select("*")\
        .eq("id", id)\
        .execute().data[0]

    if request.method == "POST":

        supabase.table("data").update({

            "process":
            request.form.get("process"),

            "thickness":
            request.form.get("thickness")

        }).eq("id", id).execute()

        return redirect("/list")

    return f"""

<!DOCTYPE html>

<html>

<head>

<meta charset='UTF-8'>

<style>

body{{

    margin:0;

    background:#0f172a;

    color:white;

    font-family:Arial;

    padding:20px;
}}

.card{{

    background:#111827;

    border-radius:20px;

    padding:20px;
}}

input,select{{

    width:100%;

    height:55px;

    margin-top:15px;

    padding:12px;

    border:none;

    border-radius:12px;

    background:#1e293b;

    color:white;

    box-sizing:border-box;
}}

button{{

    width:100%;

    padding:14px;

    margin-top:18px;

    border:none;

    border-radius:12px;

    background:#2563eb;

    color:white;

    font-size:18px;
}}

</style>

</head>

<body>

<div class='card'>

<h1>編集</h1>

<form method='POST'>

<select name='process'>

{''.join([

f"<option {'selected' if row['process']==x else ''}>{x}</option>"

for x in processes

])}

</select>

<input
type='number'
name='thickness'
value='{row['thickness']}'>

<button type='submit'>

更新

</button>

</form>

<a href='/list'>

<button>

戻る

</button>

</a>

</div>

</body>

</html>

"""

# =====================================================
# DELETE
# =====================================================

@app.route("/delete/<id>")
def delete(id):

    supabase.table("data")\
        .delete()\
        .eq("id", id)\
        .execute()

    return redirect("/list")

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)
