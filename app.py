# =====================================================
# 橋梁膜厚管理 完全版
# =====================================================

from flask import Flask, request, redirect, render_template_string, session
from supabase import create_client
from datetime import datetime
import io
import csv

app = Flask(__name__)

app.secret_key = "sakura6788"

# =====================================================
# Supabase
# =====================================================

url = "https://xcjgbrzqxkgoiynjsdhc.supabase.co"

key = "sb_publishable_Z-nEPLmqRbLV_kWy_lW0GA_b7DC-EIn"

supabase = create_client(url, key)

# =====================================================
# ログイン
# =====================================================

users = {
    "敦司":"6788",
    "furui":"6788",
    "tsuchiya":"6788",
    "akashi":"6788",
    "kawano":"6788"
}

# =====================================================
# データ
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

lots = [str(i) for i in range(1, 51)]

points = [str(i) for i in range(1, 26)]

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
<meta name='viewport' content='width=device-width, initial-scale=1.0'>

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
    border-radius:18px;
    padding:25px;
    border:1px solid #16325c;
}

h1{
    text-align:center;
    color:#38bdf8;
}

input{
    width:100%;
    height:48px;
    margin-top:15px;
    padding:10px;
    border:none;
    border-radius:10px;
    background:#1e293b;
    color:white;
    box-sizing:border-box;
    font-size:16px;
}

button{
    width:100%;
    padding:14px;
    margin-top:20px;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    font-size:18px;
    font-weight:bold;
}

</style>

</head>

<body>

<div class='login-box'>

<h1>橋梁膜厚管理</h1>

<form method='POST'>

<input name='id' placeholder='ID'>

<input type='password' name='pw' placeholder='パスワード'>

<button type='submit'>ログイン</button>

</form>

</div>

</body>
</html>

"""

# =====================================================
# HOME
# =====================================================

@app.route("/", methods=["GET","POST"])
def home():

    if not session.get("login"):
        return redirect("/login")

    if request.method == "POST":

        process = request.form.get("process")
        thickness = request.form.get("thickness")

        standard = standards.get(process, 0)

        result = "OK"

        if thickness:

            if int(thickness) < standard:
                result = "NG"

        data = {

            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),

            "user_name": session.get("user"),

            "site": request.form.get("site"),

            "bridge": request.form.get("bridge"),

            "place": request.form.get("place"),

            "part": request.form.get("part"),

            "lot": request.form.get("lot"),

            "point": request.form.get("point"),

            "process": process,

            "thickness": thickness,

            "result": result
        }

        supabase.table("data").insert(data).execute()

        return redirect("/")

    bridge_html = ""

    for bridge in bridges["ミカドR6-1"]:
        bridge_html += f"<option>{bridge}</option>"

    return f"""

<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>橋梁膜厚管理</title>

<style>

body{{
    margin:0;
    background:#020b22;
    font-family:Arial;
    color:white;
}}

.header{{
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    padding:16px;
    text-align:center;
    font-size:24px;
    font-weight:bold;
    box-shadow:0 0 18px #0ea5e9;
}}

.container{{
    max-width:600px;
    margin:10px auto;
    padding:10px;
}}

.card{{
    background:#081229;
    border:1px solid #16325c;
    border-radius:18px;
    padding:18px;
    box-shadow:0 0 15px rgba(37,99,235,0.35);
}}

label{{
    display:block;
    margin-top:12px;
    margin-bottom:6px;
    font-size:16px;
    font-weight:bold;
    color:#93c5fd;
}}

input,select{{
    width:100%;
    height:48px;
    padding:10px;
    border:none;
    border-radius:10px;
    background:#1e293b;
    color:white;
    font-size:16px;
    box-sizing:border-box;
}}

button{{
    width:100%;
    padding:14px;
    margin-top:18px;
    border:none;
    border-radius:14px;
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    font-size:18px;
    font-weight:bold;
}}

.subbtn{{
    background:#1e293b;
}}

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

<select name="site">

{''.join([f'<option>{x}</option>' for x in sites])}

</select>

<label>橋名</label>

<select name="bridge">

{bridge_html}

</select>

<label>箇所</label>

<select name="place">

{''.join([f'<option>{x}</option>' for x in places])}

</select>

<label>部位</label>

<select name="part">

{''.join([f'<option>{x}</option>' for x in parts])}

</select>

<label>ロット</label>

<select name="lot">

{''.join([f'<option>{x}</option>' for x in lots])}

</select>

<label>測点</label>

<select name="point">

{''.join([f'<option>{x}</option>' for x in points])}

</select>

<label>工程</label>

<select name="process">

{''.join([f'<option>{x}</option>' for x in processes])}

</select>

<label>膜厚</label>

<input type="number" name="thickness" required>

<button type="submit">
保存
</button>

</form>

<a href="/list">
<button class="subbtn">
入力情報一覧
</button>
</a>

<a href="/backup">
<button class="subbtn">
CSVバックアップ
</button>
</a>

</div>
</div>

</body>
</html>

"""

# =====================================================
# 一覧
# =====================================================

@app.route("/list")
def list_page():

    if not session.get("login"):
        return redirect("/login")

    rows = supabase.table("data").select("*").order("id").execute().data

    html = ""

    bridge_names = []

    for row in rows:

        bridge = row.get("bridge")

        if bridge not in bridge_names:
            bridge_names.append(bridge)

    for bridge in bridge_names:

        html += f"""

<div class='bridge-title'>
{bridge}
</div>

"""

        bridge_rows = [x for x in rows if x.get("bridge") == bridge]

        part_names = []

        for row in bridge_rows:

            part = row.get("part")

            if part not in part_names:
                part_names.append(part)

        for part in part_names:

            html += f"""

<div class='part-title'>
{part}
</div>

"""

            part_rows = [x for x in bridge_rows if x.get("part") == part]

            lot_names = []

            for row in part_rows:

                lot = row.get("lot")

                if lot not in lot_names:
                    lot_names.append(lot)

            for lot in lot_names:

                html += f"""

<div class='lot-title'>
{lot}ロット
</div>

<table>

<tr>
<th>ID</th>
<th>日時</th>
<th>箇所</th>
<th>工程</th>
<th>膜厚</th>
<th>判定</th>
</tr>

"""

                lot_rows = [x for x in part_rows if x.get("lot") == lot]

                for row in lot_rows:

                    result = row.get("result","")

                    color = "#22c55e"

                    if result == "NG":
                        color = "#ef4444"

                    html += f"""

<tr>

<td>{row.get('id','')}</td>

<td>{row.get('datetime','')}</td>

<td>{row.get('place','')}</td>

<td>{row.get('process','')}</td>

<td>{row.get('thickness','')}</td>

<td style='color:{color};font-weight:bold;'>

{result}

</td>

</tr>

"""

                html += "</table>"

    return f"""

<!DOCTYPE html>
<html>
<head>

<meta charset='UTF-8'>

<meta name='viewport' content='width=device-width, initial-scale=1.0'>

<style>

body{{
    margin:0;
    background:#d1d5db;
    font-family:Arial;
    padding:15px;
}}

.bridge-title{{
    font-size:26px;
    font-weight:bold;
    margin-top:20px;
    margin-bottom:15px;
}}

.part-title{{
    background:#1e3a8a;
    color:white;
    padding:15px;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
    margin-top:20px;
}}

.lot-title{{
    color:#1e3a8a;
    font-size:18px;
    font-weight:bold;
    margin-top:25px;
    margin-bottom:10px;
}}

table{{
    width:100%;
    border-collapse:collapse;
    margin-bottom:20px;
    background:white;
}}

th,td{{
    border:1px solid #d1d5db;
    padding:10px;
    text-align:center;
    font-size:14px;
}}

th{{
    background:#c7d2fe;
}}

button{{
    width:100%;
    padding:14px;
    margin-top:20px;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    font-size:18px;
    font-weight:bold;
}}

</style>

</head>

<body>

{html}

<a href="/">
<button>
戻る
</button>
</a>

</body>
</html>

"""

# =====================================================
# CSV
# =====================================================

@app.route("/backup")
def backup():

    if not session.get("login"):
        return redirect("/login")

    rows = supabase.table("data").select("*").execute().data

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "datetime",
        "site",
        "bridge",
        "place",
        "part",
        "lot",
        "point",
        "process",
        "thickness",
        "result"
    ])

    for row in rows:

        writer.writerow([
            row.get("datetime",""),
            row.get("site",""),
            row.get("bridge",""),
            row.get("place",""),
            row.get("part",""),
            row.get("lot",""),
            row.get("point",""),
            row.get("process",""),
            row.get("thickness",""),
            row.get("result","")
        ])

    return f"""

<!DOCTYPE html>
<html>
<head>

<meta charset='UTF-8'>

<style>

body{{
    background:#020b22;
    color:white;
    font-family:Arial;
    padding:20px;
}}

textarea{{
    width:100%;
    height:500px;
    background:#111827;
    color:#38bdf8;
    border:none;
    padding:10px;
}}

</style>

</head>

<body>

<h1>CSVバックアップ</h1>

<textarea>

{output.getvalue()}

</textarea>

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
# 起動
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
