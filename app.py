from flask import Flask, request, render_template_string, redirect, session
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = "Sakura6788"

users = {
    "敦司":"6788",
    "furui":"6788",
    "tsuchiya":"6788",
    "akashi":"6788",
    "kawano":"6788"
}

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
    box-shadow:0 0 15px rgba(0,0,0,0.1);
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
    font-size:18px;
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

.error{
    color:red;
    text-align:center;
    margin-top:15px;
}

</style>

</head>

<body>

<div class="box">

<h1>橋梁膜厚管理</h1>

<form method="POST">

<input name="id" placeholder="ID" required>

<input type="password" name="pw" placeholder="パスワード" required>

<button type="submit">
ログイン
</button>

</form>

{{error|safe}}

</div>

</body>

</html>

"""

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
    padding:0;
    background:#eef2f7;
    font-family:Arial;
}

.header{
    background:#1f3c88;
    color:white;
    text-align:center;
    padding:20px;
    font-size:32px;
    font-weight:bold;
}

.container{
    max-width:700px;
    margin:20px auto;
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 0 15px rgba(0,0,0,0.1);
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
    font-size:18px;
    box-sizing:border-box;
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

.success{
    background:#d4edda;
    color:#155724;
    padding:15px;
    margin-top:20px;
    border-radius:10px;
    text-align:center;
    font-weight:bold;
}

.user{
    text-align:right;
    font-weight:bold;
    color:#1f3c88;
    margin-bottom:20px;
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

function updateProcess(){

    const part = document.getElementById("part").value

    const process = document.getElementById("process")

    process.innerHTML = ""

    let list = []

    if(part == "一種部"){

        list = [
        "素地調整完了",
        "防食下地",
        "下塗1",
        "下塗2",
        "増し塗1",
        "増し塗2",
        "中塗り",
        "上塗り"
        ]

    }

    else{

        list = [
        "補修塗",
        "下塗1",
        "増し塗1",
        "増し塗2",
        "下塗2",
        "中塗り",
        "上塗り"
        ]

    }

    list.forEach(function(item){

        let option = document.createElement("option")

        option.text = item

        option.value = item

        process.add(option)

    })

}

function init(){

    updateBridge()
    updateProcess()

}

</script>

</head>

<body onload="init()">

<div class="header">
橋梁膜厚管理
</div>

<div class="container">

<div class="user">
ログイン中：{{user}}
</div>

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

<select id="part" name="part" onchange="updateProcess()">

<option>一般部</option>
<option>増し塗り部</option>
<option>一種部</option>

</select>

<label>ロット番号</label>
<input name="lot" required>

<label>工程</label>

<select id="process" name="process"></select>

<label>膜厚（μm）</label>
<input name="thickness" required>

<button type="submit">
保存
</button>

</form>

<a class="link" href="/list">
入力データ確認
</a>

{{message|safe}}

</div>

</body>

</html>

"""

@app.route("/", methods=["GET","POST"])
def login():

    error = ""

    if request.method == "POST":

        user_id = request.form["id"]
        user_pw = request.form["pw"]

        if user_id in users and users[user_id] == user_pw:

            session["login"] = True
            session["user"] = user_id

            return redirect("/home")

        else:

            error = "<div class='error'>ログイン失敗</div>"

    return render_template_string(login_html, error=error)

@app.route("/home", methods=["GET","POST"])
def home():

    if "login" not in session:
        return redirect("/")

    message = ""

    if request.method == "POST":

        bridge = request.form["bridge"]
        place = request.form["place"]
        part = request.form["part"]
        lot = request.form["lot"]

        file_name = f"{bridge}_{place}_{part}_{lot}.xlsx"

        if os.path.exists(file_name):

            df = pd.read_excel(file_name)

        else:

            df = pd.DataFrame(columns=[
                "No",
                "日時",
                "入力者",
                "現場名",
                "橋名",
                "箇所",
                "部位",
                "ロット番号",
                "工程",
                "膜厚"
            ])

        no = len(df) + 1

        new_row = {
            "No":no,
            "日時":datetime.now().strftime("%Y-%m-%d %H:%M"),
            "入力者":session["user"],
            "現場名":request.form["site"],
            "橋名":bridge,
            "箇所":place,
            "部位":part,
            "ロット番号":lot,
            "工程":request.form["process"],
            "膜厚":request.form["thickness"]
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.to_excel(file_name, index=False)

        message = "<div class='success'>保存完了</div>"

    return render_template_string(
        home_html,
        bridges=bridges,
        user=session["user"],
        message=message
    )

@app.route("/list")
def list_page():

    if "login" not in session:
        return redirect("/")

    files = [f for f in os.listdir() if f.endswith(".xlsx")]

    rows = ""

    for file in files:

        rows += f"""

        <tr>

        <td>
        <a href='/view/{file}'>
        {file}
        </a>
        </td>

        </tr>

        """

    return f"""

    <!DOCTYPE html>

    <html lang='ja'>

    <head>

    <meta charset='UTF-8'>

    <style>

    body{{
        background:#eef2f7;
        font-family:Arial;
        padding:20px;
    }}

    .box{{
        background:white;
        padding:20px;
        border-radius:20px;
    }}

    table{{
        width:100%;
        border-collapse:collapse;
    }}

    th,td{{
        border:1px solid #ccc;
        padding:12px;
        text-align:center;
    }}

    th{{
        background:#1f3c88;
        color:white;
    }}

    a{{
        text-decoration:none;
        color:#1f3c88;
        font-weight:bold;
    }}

    .back{{
        display:inline-block;
        margin-bottom:20px;
        background:#1f3c88;
        color:white;
        padding:12px 20px;
        border-radius:10px;
        text-decoration:none;
    }}

    </style>

    </head>

    <body>

    <div class='box'>

    <a class='back' href='/home'>
    戻る
    </a>

    <table>

    <tr>
    <th>保存ファイル</th>
    </tr>

    {rows}

    </table>

    </div>

    </body>

    </html>

    """

if __name__ == "__main__":
    app.run(debug=False)
