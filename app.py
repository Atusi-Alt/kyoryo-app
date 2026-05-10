# =====================================================
# 橋梁膜厚管理 完全版 安定版
# =====================================================

from flask import Flask, request, redirect, render_template_string, session
from supabase import create_client
from datetime import datetime
import json

app = Flask(__name__)

app.secret_key = "sakura"

# =====================================================
# SUPABASE
# =====================================================

url = "https://xcjgbrzqxkgoiynjsdhc.supabase.co"

key = "sb_publishable_Z-nEPLmqRbLV_kWy_lW0GA_b7DC-EIn"

supabase = create_client(url, key)

# =====================================================
# LOGIN USER
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

    "防食下地",
    "下塗1",
    "増し塗1",
    "増し塗2",
    "下塗2",
    "中塗",
    "上塗",
    "補修塗"
]

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
# LOGIN
# =====================================================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        user_id = request.form.get("id")
        password = request.form.get("pw")

        if user_id in users and users[user_id] == password:

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
    background:#020b22;
    font-family:Arial;
    color:white;
}

.login-box{
    max-width:400px;
    margin:120px auto;
    background:#081229;
    border-radius:20px;
    padding:25px;
}

input{
    width:100%;
    height:50px;
    margin-top:15px;
    padding:10px;
    border:none;
    border-radius:10px;
    background:#1e293b;
    color:white;
    box-sizing:border-box;
}

button{
    width:100%;
    padding:14px;
    margin-top:20px;
    border:none;
    border-radius:12px;
    background:#2563eb;
    color:white;
    font-size:18px;
    font-weight:bold;
}

h1{
    text-align:center;
}

</style>

</head>

<body>

<div class='login-box'>

<h1>橋梁膜厚管理</h1>

<form method='POST'>

<input name='id' placeholder='ID'>

<input type='password'
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
            datetime.now().strftime("%Y-%m-%d %H:%M"),

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

        supabase.table("data").insert(data).execute()

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
    background:#020b22;
    font-family:Arial;
    color:white;
}

.header{
    background:#2563eb;
    padding:18px;
    text-align:center;
    font-size:24px;
    font-weight:bold;
}

.container{
    max-width:650px;
    margin:auto;
    padding:10px;
}

.card{
    background:#081229;
    border-radius:20px;
    padding:20px;
}

label{
    display:block;
    margin-top:15px;
    margin-bottom:5px;
    font-weight:bold;
}

input,select{
    width:100%;
    height:52px;
    padding:10px;
    border:none;
    border-radius:10px;
    background:#1e293b;
    color:white;
    font-size:16px;
    box-sizing:border-box;
}

button{
    width:100%;
    padding:14px;
    margin-top:18px;
    border:none;
    border-radius:14px;
    background:#2563eb;
    color:white;
    font-size:18px;
    font-weight:bold;
}

.subbtn{
    background:#1e293b;
}

</style>

</head>

<body>

<div class="header">

橋梁膜厚管理

</div>

<div class="container">

<div class="card">

<form method="POST">

<label>現場名</label>

<select id="site"
name="site"
onchange="changeBridge()">

<option>ミカドR6-1</option>
<option>ミカドR6-2</option>

</select>

<label>橋名</label>

<select id="bridge" name="bridge"></select>

<label>箇所</label>

<select name="place">

<option>上部工</option>
<option>下部工</option>
<option>上部工内面</option>
<option>下部工内面</option>

</select>

<label>部位</label>

<select name="part">

<option>一般部</option>
<option>増し塗り部</option>
<option>一種部</option>

</select>

<label>ロット</label>

<select name="lot">

{% for i in range(1,51) %}

<option>{{i}}</option>

{% endfor %}

</select>

<label>測点</label>

<select name="point">

{% for i in range(1,26) %}

<option>{{i}}</option>

{% endfor %}

</select>

<label>工程</label>

<select name="process">

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

<input type="number"
name="thickness"
required>

<button type="submit">

保存

</button>

</form>

<a href="/list">

<button class="subbtn">

入力情報一覧

</button>

</a>

<a href="/logout">

<button class="subbtn">

ログアウト

</button>

</a>

</div>

</div>

<script>

const bridges = {{ bridges|safe }}

function changeBridge(){

    let site =
    document.getElementById("site").value

    let bridgeSelect =
    document.getElementById("bridge")

    bridgeSelect.innerHTML = ""

    bridges[site].forEach(function(bridge){

        let option =
        document.createElement("option")

        option.value = bridge

        option.text = bridge

        bridgeSelect.appendChild(option)

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

    process_order = {

        "防食下地":0,
        "下塗1":1,
        "増し塗1":2,
        "増し塗2":3,
        "下塗2":4,
        "中塗":5,
        "上塗":6,
        "補修塗":7
    }

    html = ""

    bridge_names = []

    for row in rows:

        bridge = row.get("bridge")

        if bridge not in bridge_names:
            bridge_names.append(bridge)

    for bridge in bridge_names:

        html += f"""

<h1 style='font-size:50px;'>

{bridge}

</h1>

"""

        bridge_rows = [

            x for x in rows
            if x.get("bridge") == bridge
        ]

        for part in parts:

            part_rows = [

                x for x in bridge_rows
                if x.get("part") == part
            ]

            if not part_rows:
                continue

            html += f"""

<h2 style='background:#1e3a8a;
color:white;
padding:18px;
border-radius:16px;'>

{part}

</h2>

"""

            lot_names = []

            for row in part_rows:

                lot = row.get("lot")

                if lot not in lot_names:
                    lot_names.append(lot)

            for lot in lot_names:

                html += f"""

<details>

<summary style='font-size:28px;
font-weight:bold;
margin-top:20px;'>

{lot}ロット

</summary>

<div style='overflow-x:auto;'>

<table style='width:100%;
min-width:1400px;
background:white;
border-collapse:collapse;
margin-top:10px;'>

<tr>

<th>測点</th>
<th>日時</th>
<th>入力者</th>
<th>箇所</th>
<th>工程</th>
<th>膜厚</th>
<th>前層差</th>
<th>判定</th>
<th>編集</th>
<th>削除</th>

</tr>

"""

                lot_rows = [

                    x for x in part_rows
                    if x.get("lot") == lot
                ]

                lot_rows.sort(
                    key=lambda x:
                    process_order.get(
                        x.get("process"),99
                    )
                )

                previous_thickness = 0

                for row in lot_rows:

                    process = row.get("process","")

                    thickness = int(
                        row.get("thickness",0)
                    )

                    standard = standards.get(process,0)

                    result = "OK"

                    if thickness < standard:
                        result = "NG"

                    difference = (
                        thickness -
                        previous_thickness
                    )

                    if process == "防食下地":
                        difference = 0

                    previous_thickness = thickness

                    color = "green"

                    if result == "NG":
                        color = "red"

                    html += f"""

<tr>

<td>{row.get('point','')}</td>

<td>{row.get('datetime','')}</td>

<td>{row.get('user_name','')}</td>

<td>{row.get('place','')}</td>

<td>{process}</td>

<td>{thickness}μ</td>

<td>{difference}μ</td>

<td style='color:{color};
font-weight:bold;'>

{result}

</td>

<td>

<a href='/edit/{row['id']}'>

<button>

編集

</button>

</a>

</td>

<td>

<a href='/delete/{row['id']}'>

<button style='background:red;'>

削除

</button>

</a>

</td>

</tr>

"""

                html += """

</table>

</div>

</details>

"""

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
    padding:15px;
    background:#d1d5db;
    font-family:Arial;
}}

th,td{{
    border:1px solid #ccc;
    padding:12px;
    text-align:center;
    white-space:nowrap;
}}

th{{
    background:#c7d2fe;
}}

button{{
    padding:10px 14px;
    border:none;
    border-radius:8px;
    background:#2563eb;
    color:white;
}}

.main-btn{{
    width:100%;
    padding:18px;
    margin-bottom:20px;
    font-size:20px;
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
    padding:20px;
    background:#020b22;
    color:white;
    font-family:Arial;
}}

.card{{
    background:#081229;
    padding:20px;
    border-radius:20px;
}}

input,select{{
    width:100%;
    height:50px;
    margin-top:15px;
    padding:10px;
    border:none;
    border-radius:10px;
    background:#1e293b;
    color:white;
    box-sizing:border-box;
}}

button{{
    width:100%;
    padding:14px;
    margin-top:20px;
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

<option {'selected' if row['process']=='防食下地' else ''}>
防食下地
</option>

<option {'selected' if row['process']=='下塗1' else ''}>
下塗1
</option>

<option {'selected' if row['process']=='増し塗1' else ''}>
増し塗1
</option>

<option {'selected' if row['process']=='増し塗2' else ''}>
増し塗2
</option>

<option {'selected' if row['process']=='下塗2' else ''}>
下塗2
</option>

<option {'selected' if row['process']=='中塗' else ''}>
中塗
</option>

<option {'selected' if row['process']=='上塗' else ''}>
上塗
</option>

<option {'selected' if row['process']=='補修塗' else ''}>
補修塗
</option>

</select>

<input type='number'
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
