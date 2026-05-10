from flask import Flask, request, render_template_string, redirect, session
from supabase import create_client
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = "Sakura6788"

# =====================================
# Supabase
# =====================================

url = "https://xcjgbrzqxkgoiynjsdhc.supabase.co"

key = "ここに公開可能なキー"

supabase = create_client(url, key)

# =====================================
# 判定基準
# =====================================

standards = {

    "防食下地":75,
    "下塗1":60,
    "増し塗1":60,
    "増し塗2":60,
    "下塗2":60,
    "中塗り":30,
    "上塗り":25

}

# =====================================
# ユーザー
# =====================================

users = {

    "敦司":"6788",
    "furui":"6788",
    "tsuchiya":"6788",
    "akashi":"6788",
    "kawano":"6788"

}

# =====================================
# 橋データ
# =====================================

bridges = {

    "ミカドR6-1":[
        "I 1-286",
        "I 2-286",
        "I 1-287",
        "I 2-287",
        "I 1-290",
        "I 2-290",
        "I 1-291",
        "I 2-291",
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

# =====================================
# ログイン画面
# =====================================

login_html = """

<!DOCTYPE html>

<html lang="ja">

<head>

<meta charset="UTF-8">

<title>ログイン</title>

<style>

body{
    background:#eef2f7;
    font-family:Arial;
}

.box{
    width:350px;
    margin:120px auto;
    background:white;
    padding:30px;
    border-radius:20px;
}

h1{
    text-align:center;
    color:#1f3c88;
}

input{
    width:100%;
    padding:14px;
    margin-top:15px;
    border-radius:10px;
    border:1px solid #ccc;
    box-sizing:border-box;
}

button{
    width:100%;
    padding:14px;
    margin-top:20px;
    border:none;
    border-radius:10px;
    background:#1f3c88;
    color:white;
    font-size:20px;
    font-weight:bold;
}

</style>

</head>

<body>

<div class="box">

<h1>橋梁膜厚管理</h1>

<form method="POST">

<input name="id" placeholder="ID">

<input type="password" name="pw" placeholder="パスワード">

<button type="submit">
ログイン
</button>

</form>

</div>

</body>

</html>

"""

# =====================================
# ホーム画面
# =====================================

home_html = """

<!DOCTYPE html>

<html lang="ja">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>橋梁膜厚管理</title>

<style>

body{
    margin:0;
    background:#eef2f7;
    font-family:Arial;
}

.header{
    background:#1f3c88;
    color:white;
    text-align:center;
    padding:20px;
    font-size:30px;
    font-weight:bold;
}

.container{
    max-width:700px;
    margin:20px auto;
    background:white;
    padding:25px;
    border-radius:20px;
}

label{
    display:block;
    margin-top:15px;
    font-weight:bold;
}

input,select{
    width:100%;
    padding:12px;
    margin-top:5px;
    border-radius:10px;
    border:1px solid #ccc;
    box-sizing:border-box;
    font-size:18px;
}

button{
    width:100%;
    padding:15px;
    margin-top:25px;
    border:none;
    border-radius:10px;
    background:#1f3c88;
    color:white;
    font-size:22px;
    font-weight:bold;
}

.link{
    display:block;
    text-align:center;
    margin-top:20px;
    background:#dfe7ff;
    padding:14px;
    border-radius:10px;
    text-decoration:none;
    color:#1f3c88;
    font-weight:bold;
}

.ok{
    color:green;
    font-weight:bold;
}

.ng{
    color:red;
    font-weight:bold;
}

</style>

<script>

const bridges = {{bridges|safe}}

function updateBridge(){

    const site = document.getElementById("site").value

    const bridge = document.getElementById("bridge")

    bridge.innerHTML = ""

    bridges[site].forEach(function(item){

        let option = document.createElement("option")

        option.text = item

        option.value = item

        bridge.add(option)

    })

}

function init(){

    updateBridge()

}

</script>

</head>

<body onload="init()">

<div class="header">
橋梁膜厚管理
</div>

<div class="container">

<form method="POST">

<label>現場名</label>

<select id="site" name="site" onchange="updateBridge()">

<option value="ミカドR6-1">ミカドR6-1</option>
<option value="ミカドR6-2">ミカドR6-2</option>

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

"""

for i in range(1,51):

    home_html += f"<option>{i}</option>"

home_html += """

</select>

<label>測点</label>

<select name="point">

"""

for i in range(1,26):

    home_html += f"<option>{i}</option>"

home_html += """

</select>

<label>工程</label>

<select name="process">

<option>防食下地</option>
<option>補修塗</option>
<option>下塗1</option>
<option>増し塗1</option>
<option>増し塗2</option>
<option>下塗2</option>
<option>中塗り</option>
<option>上塗り</option>

</select>

<label>膜厚</label>

<input type="number" name="thickness">

<button type="submit">

保存

</button>

</form>

<a class="link" href="/list">

入力情報一覧

</a>

</div>

</body>

</html>

"""

# =====================================
# ログイン
# =====================================

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        user_id = request.form["id"]
        user_pw = request.form["pw"]

        if user_id in users and users[user_id] == user_pw:

            session["login"] = True
            session["user"] = user_id

            return redirect("/home")

    return render_template_string(login_html)

# =====================================
# ホーム
# =====================================

@app.route("/home", methods=["GET","POST"])
def home():

    if "login" not in session:

        return redirect("/")

    if request.method == "POST":

        japan_time = (
            datetime.now() + timedelta(hours=9)
        ).strftime("%Y-%m-%d %H:%M")

        supabase.table("data").insert({

            "datetime": japan_time,
            "user_name": session["user"],
            "site": request.form["site"],
            "bridge": request.form["bridge"],
            "place": request.form["place"],
            "part": request.form["part"],
            "lot": request.form["lot"],
            "point": request.form["point"],
            "process": request.form["process"],
            "thickness": request.form["thickness"]

        }).execute()

    return render_template_string(
        home_html,
        bridges=bridges
    )

# =====================================
# 一覧
# =====================================

@app.route("/list")
def list_page():

    response = supabase.table("data").select("*").execute()

    df = pd.DataFrame(response.data)

    html = ""

    if len(df) == 0:

        html = "<h1>データなし</h1>"

    else:

        sites = df["site"].unique()

        for site in sites:

            html += f"""

            <h2 style='
            background:#1f3c88;
            color:white;
            padding:15px;
            border-radius:10px;
            '>

            {site}

            </h2>

            """

            site_df = df[df["site"] == site]

            for bridge in site_df["bridge"].unique():

                html += f"""

                <a href="/bridge/{bridge}"
                style='
                display:block;
                background:white;
                padding:15px;
                margin-top:10px;
                border-radius:10px;
                text-decoration:none;
                font-size:22px;
                font-weight:bold;
                color:#1f3c88;
                '>

                {bridge}

                </a>

                """

    return f"""

    <body style='
    background:#eef2f7;
    font-family:Arial;
    padding:20px;
    '>

    <a href='/home'
    style='
    display:inline-block;
    background:#1f3c88;
    color:white;
    padding:12px 20px;
    border-radius:10px;
    text-decoration:none;
    margin-bottom:20px;
    '>

    戻る

    </a>

    <h1>入力情報一覧</h1>

    {html}

    </body>

    """

# =====================================
# 橋詳細
# =====================================

@app.route("/bridge/<bridge>")
def bridge_page(bridge):

    response = (
        supabase
        .table("data")
        .select("*")
        .eq("bridge", bridge)
        .execute()
    )

    df = pd.DataFrame(response.data)

    html = f"<h1>{bridge}</h1>"

    if len(df) == 0:

        return html + "データなし"

    parts = ["一般部","増し塗り部","一種部"]

    for part in parts:

        html += f"""

        <h2 style='
        background:#1f3c88;
        color:white;
        padding:15px;
        border-radius:10px;
        '>

        {part}

        </h2>

        """

        part_df = df[df["part"] == part]

        if len(part_df) == 0:

            continue

        lots = sorted(part_df["lot"].unique())

        for lot in lots:

            html += f"""

            <details style='margin-bottom:20px;'>

            <summary style='
            font-size:24px;
            font-weight:bold;
            cursor:pointer;
            '>

            {lot}ロット

            </summary>

            <table style='
            width:100%;
            border-collapse:collapse;
            background:white;
            margin-top:15px;
            '>

            <tr style='background:#dfe7ff;'>

            <th>測点</th>
            <th>工程</th>
            <th>膜厚</th>
            <th>増加量</th>
            <th>判定</th>

            </tr>

            """

            lot_df = part_df[part_df["lot"] == lot]

            previous = None

            for i,row in lot_df.iterrows():

                thickness = int(row["thickness"])

                increase = "-"

                result = "-"

                color = "black"

                if previous is not None:

                    diff = thickness - previous

                    increase = f"+{diff}"

                    standard = standards.get(
                        row["process"],
                        0
                    )

                    if diff >= standard:

                        result = "○"

                        color = "green"

                    else:

                        result = "✕"

                        color = "red"

                previous = thickness

                html += f"""

                <tr>

                <td style='padding:10px;border:1px solid #ccc;'>

                {row["point"]}

                </td>

                <td style='padding:10px;border:1px solid #ccc;'>

                {row["process"]}

                </td>

                <td style='padding:10px;border:1px solid #ccc;'>

                {thickness}μ

                </td>

                <td style='padding:10px;border:1px solid #ccc;'>

                {increase}

                </td>

                <td style='
                padding:10px;
                border:1px solid #ccc;
                color:{color};
                font-weight:bold;
                '>

                {result}

                </td>

                </tr>

                """

            html += "</table></details>"

    return f"""

    <body style='
    background:#eef2f7;
    font-family:Arial;
    padding:20px;
    '>

    <a href='/list'
    style='
    display:inline-block;
    background:#1f3c88;
    color:white;
    padding:12px 20px;
    border-radius:10px;
    text-decoration:none;
    margin-bottom:20px;
    '>

    戻る

    </a>

    {html}

    </body>

    """

# =====================================
# 起動
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
