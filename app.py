from flask import Flask, request, render_template_string, redirect, session
import pandas as pd
import os

app = Flask(__name__)

app.secret_key = "Sakura6788"

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

{error}

</div>

</body>

</html>

"""

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

.success{
    background:#d4edda;
    color:#155724;
    padding:15px;
    margin-top:20px;
    border-radius:10px;
    text-align:center;
    font-weight:bold;
}

</style>

</head>

<body>

<div class="header">
橋梁膜厚管理
</div>

<div class="container">

<form method="POST">

<label>現場名</label>
<input name="site" required>

<label>橋名</label>
<select name="bridge">

<option>I 1-286</option>
<option>I 2-286</option>
<option>I 1-287</option>
<option>I 2-287</option>
<option>I-287</option>

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
<input name="section">

<label>ロット番号</label>
<input name="lot">

<label>工程</label>
<select name="process">

<option>素地調整完了</option>
<option>防食下地</option>
<option>下塗1</option>
<option>下塗2</option>
<option>増し塗1</option>
<option>増し塗2</option>
<option>中塗り</option>
<option>上塗り</option>

</select>

<label>膜厚</label>
<input name="thickness">

<button type="submit">
保存
</button>

</form>

{message}

</div>

</body>

</html>

"""

@app.route("/", methods=["GET","POST"])
def login():

    error = ""

    if request.method == "POST":

        if request.form["id"] == "admin" and request.form["pw"] == "Sakura6788":

            session["login"] = True

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

if __name__ == "__main__":
    app.run(debug=False)
