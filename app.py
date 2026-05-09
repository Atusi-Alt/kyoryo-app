from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

html = """

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
    font-size:34px;
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
    margin-top:18px;
    margin-bottom:8px;
    font-size:18px;
    font-weight:bold;
}

input, select{
    width:100%;
    padding:14px;
    border-radius:10px;
    border:1px solid #ccc;
    font-size:18px;
    box-sizing:border-box;
}

button{
    width:100%;
    margin-top:30px;
    padding:16px;
    border:none;
    border-radius:12px;
    background:#1f3c88;
    color:white;
    font-size:24px;
    font-weight:bold;
}

.success{
    background:#d4edda;
    color:#155724;
    padding:15px;
    border-radius:10px;
    margin-bottom:20px;
    text-align:center;
    font-size:18px;
    font-weight:bold;
}

.link{
    display:block;
    margin-top:25px;
    text-align:center;
    background:#dfe7ff;
    padding:15px;
    border-radius:12px;
    text-decoration:none;
    color:#1f3c88;
    font-size:20px;
    font-weight:bold;
}

</style>

<script>

const bridges = {

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

};

function updateBridge(){

    let site = document.getElementById("site").value;

    let bridge = document.getElementById("bridge");

    bridge.innerHTML = "";

    for(let i=0;i<bridges[site].length;i++){

        let option = document.createElement("option");

        option.text = bridges[site][i];

        option.value = bridges[site][i];

        bridge.add(option);

    }

}

function updateProcess(){

    let section = document.getElementById("section").value;

    let process = document.getElementById("process");

    process.innerHTML = "";

    let list = [];

    if(section == "一種部"){

        list = [
        "素地調整完了",
        "防食下地",
        "下塗1",
        "下塗2",
        "増し塗1",
        "増し塗2",
        "中塗り",
        "上塗り"
        ];

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
        ];

    }

    for(let i=0;i<list.length;i++){

        let option = document.createElement("option");

        option.text = list[i];

        option.value = list[i];

        process.add(option);

    }

}

function init(){

    updateBridge();

    updateProcess();

}

</script>

</head>

<body onload="init()">

<div class="header">
橋梁膜厚管理システム
</div>

<div class="container">

{{message|safe}}

<form method="POST">

<label>現場名</label>

<select id="site" name="site" onchange="updateBridge()">

<option>ミカドR6-1</option>
<option>ミカドR6-2</option>

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
<option>一種部</option>

</select>

<label>部位</label>

<select id="section" name="section" onchange="updateProcess()">

<option>一般部</option>
<option>増し塗部</option>
<option>一種部</option>

</select>

<label>ロット番号</label>
<input name="lot" required>

<label>工程</label>

<select id="process" name="process">

</select>

<label>膜厚（μm）</label>
<input name="thickness" required>

<button type="submit">
保存
</button>

</form>

<a class="link" href="/list">
入力データ一覧
</a>

</div>

</body>

</html>

"""

@app.route("/", methods=["GET","POST"])

def home():

    message = ""

    if request.method == "POST":

        bridge = request.form["bridge"]

        file_name = bridge + ".xlsx"

        data = {
            "現場名":[request.form["site"]],
            "橋名":[bridge],
            "箇所":[request.form["place"]],
            "部位":[request.form["section"]],
            "ロット番号":[request.form["lot"]],
            "工程":[request.form["process"]],
            "膜厚":[request.form["thickness"]]
        }

        df = pd.DataFrame(data)

        if os.path.exists(file_name):

            old = pd.read_excel(file_name)

            df = pd.concat([old, df], ignore_index=True)

        df.to_excel(file_name, index=False)

        message = "<div class='success'>入力完了！</div>"

    return render_template_string(html, message=message)

@app.route("/list")

def list_data():

    files = [f for f in os.listdir() if f.endswith(".xlsx")]

    text = ""

    for file in files:

        text += f"<li>{file}</li>"

    return f"""

    <html>

    <head>

    <meta charset='UTF-8'>

    <style>

    body{{
        background:#eef2f7;
        font-family:Arial;
        padding:30px;
    }}

    .box{{
        background:white;
        padding:30px;
        border-radius:20px;
    }}

    li{{
        font-size:22px;
        margin-bottom:10px;
    }}

    a{{
        display:inline-block;
        margin-bottom:20px;
        background:#1f3c88;
        color:white;
        padding:12px 20px;
        border-radius:10px;
        text-decoration:none;
        font-weight:bold;
    }}

    </style>

    </head>

    <body>

    <div class='box'>

    <a href='/'>
    戻る
    </a>

    <h1>保存ファイル一覧</h1>

    <ul>

    {text}

    </ul>

    </div>

    </body>

    </html>

    """

app.run(host="0.0.0.0", port=5000)