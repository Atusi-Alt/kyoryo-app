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

key = "sb_publishable_Z-nEPLmqRbLV_kWy_lW0GA_b7DC-EIn"

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
# ログイン
# =====================================

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        user_id = request.form["id"]
        password = request.form["pw"]

        if user_id in users and users[user_id] == password:

            session["login"] = True
            session["user"] = user_id

            return redirect("/home")

    return """

    <body style='
    margin:0;
    background:#0f172a;
    font-family:Arial;
    color:white;
    '>

    <div style='
    width:350px;
    margin:120px auto;
    background:#111827;
    padding:30px;
    border-radius:20px;
    box-shadow:0 0 20px #2563eb;
    '>

    <h1 style='
    text-align:center;
    color:#38bdf8;
    '>

    橋梁膜厚管理

    </h1>

    <form method="POST">

    <input name="id"
    placeholder="ID"
    style='
    width:100%;
    padding:14px;
    margin-top:15px;
    border:none;
    border-radius:10px;
    background:#1e293b;
    color:white;
    box-sizing:border-box;
    '>

    <input type="password"
    name="pw"
    placeholder="パスワード"
    style='
    width:100%;
    padding:14px;
    margin-top:15px;
    border:none;
    border-radius:10px;
    background:#1e293b;
    color:white;
    box-sizing:border-box;
    '>

    <button type="submit"
    style='
    width:100%;
    padding:14px;
    margin-top:20px;
    border:none;
    border-radius:10px;
    background:linear-gradient(
    90deg,
    #2563eb,
    #06b6d4
    );
    color:white;
    font-size:20px;
    font-weight:bold;
    '>

    ログイン

    </button>

    </form>

    </div>

    </body>

    """

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

    return render_template_string("""

    <!DOCTYPE html>

    <html lang="ja">

    <head>

    <meta charset="UTF-8">

    <style>

    body{
        margin:0;
        background:#0f172a;
        font-family:Arial;
        color:white;
    }

    .header{
        background:linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
        );
        padding:22px;
        text-align:center;
        font-size:34px;
        font-weight:bold;
        box-shadow:0 0 20px #0ea5e9;
    }

    .container{
        max-width:900px;
        margin:25px auto;
        padding:20px;
    }

    .card{
        background:#111827;
        border:1px solid #1e3a8a;
        border-radius:20px;
        padding:22px;
        box-shadow:0 0 18px rgba(37,99,235,0.4);
    }

    label{
        display:block;
        margin-top:15px;
        margin-bottom:8px;
        font-size:18px;
        font-weight:bold;
        color:#93c5fd;
    }

    input,select{
        width:100%;
        padding:14px;
        border:none;
        border-radius:12px;
        background:#1e293b;
        color:white;
        font-size:18px;
        box-sizing:border-box;
    }

    button{
        width:100%;
        padding:16px;
        margin-top:25px;
        border:none;
        border-radius:14px;
        background:linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
        );
        color:white;
        font-size:24px;
        font-weight:bold;
    }

    .link{
        display:block;
        background:#1e293b;
        color:#38bdf8;
        text-decoration:none;
        padding:16px;
        margin-top:15px;
        border-radius:14px;
        text-align:center;
        font-size:20px;
        font-weight:bold;
    }

    </style>

    <script>

    const bridges = {{bridges|safe}}

    function updateBridge(){

        const site =
        document.getElementById("site").value

        const bridge =
        document.getElementById("bridge")

        bridge.innerHTML = ""

        bridges[site].forEach(function(item){

            let option =
            document.createElement("option")

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

    <div class="card">

    <form method="POST">

    <label>現場名</label>

    <select id="site"
    name="site"
    onchange="updateBridge()">

    <option value="ミカドR6-1">
    ミカドR6-1
    </option>

    <option value="ミカドR6-2">
    ミカドR6-2
    </option>

    </select>

    <label>橋名</label>

    <select id="bridge" name="bridge">

    </select>

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

    </div>

    </body>

    </html>

    """, bridges=bridges)

# =====================================
# 起動
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
