from flask import Flask, request, render_template_string, redirect, session, send_file
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = "Sakura6788"

# =====================================
# DB作成
# =====================================

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS data (

id INTEGER PRIMARY KEY AUTOINCREMENT,

datetime TEXT,
user TEXT,
site TEXT,
bridge TEXT,
place TEXT,
part TEXT,
lot TEXT,
point TEXT,
process TEXT,
thickness TEXT

)

""")

conn.commit()
conn.close()

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

<label>ロット番号</label>

<select name="lot">

<option>1</option>
<option>2</option>
<option>3</option>
<option>4</option>
<option>5</option>
<option>6</option>
<option>7</option>
<option>8</option>
<option>9</option>
<option>10</option>

<option>11</option>
<option>12</option>
<option>13</option>
<option>14</option>
<option>15</option>
<option>16</option>
<option>17</option>
<option>18</option>
<option>19</option>
<option>20</option>

<option>21</option>
<option>22</option>
<option>23</option>
<option>24</option>
<option>25</option>
<option>26</option>
<option>27</option>
<option>28</option>
<option>29</option>
<option>30</option>

<option>31</option>
<option>32</option>
<option>33</option>
<option>34</option>
<option>35</option>
<option>36</option>
<option>37</option>
<option>38</option>
<option>39</option>
<option>40</option>

<option>41</option>
<option>42</option>
<option>43</option>
<option>44</option>
<option>45</option>
<option>46</option>
<option>47</option>
<option>48</option>
<option>49</option>
<option>50</option>

</select>

<label>測点</label>

<select name="point">

<option>1</option>
<option>2</option>
<option>3</option>
<option>4</option>
<option>5</option>
<option>6</option>
<option>7</option>
<option>8</option>
<option>9</option>
<option>10</option>

<option>11</option>
<option>12</option>
<option>13</option>
<option>14</option>
<option>15</option>
<option>16</option>
<option>17</option>
<option>18</option>
<option>19</option>
<option>20</option>

<option>21</option>
<option>22</option>
<option>23</option>
<option>24</option>
<option>25</option>

</select>

<label>工程</label>

<select name="process">

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

<a class="link" href="/backup">
バックアップ
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

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        japan_time = (
            datetime.now() + timedelta(hours=9)
        ).strftime("%Y-%m-%d %H:%M")

        cursor.execute("""

        INSERT INTO data (

        datetime,
        user,
        site,
        bridge,
        place,
        part,
        lot,
        point,
        process,
        thickness

        )

        VALUES (?,?,?,?,?,?,?,?,?,?)

        """, (

        japan_time,
        session["user"],
        request.form["site"],
        request.form["bridge"],
        request.form["place"],
        request.form["part"],
        request.form["lot"],
        request.form["point"],
        request.form["process"],
        request.form["thickness"]

        ))

        conn.commit()
        conn.close()

    return render_template_string(
        home_html,
        bridges=bridges
    )

# =====================================
# 一覧
# =====================================

@app.route("/list")
def list_page():

    conn = sqlite3.connect("database.db")

    df = pd.read_sql_query("""

    SELECT DISTINCT
    site,
    bridge

    FROM data

    ORDER BY
    site,
    bridge

    """, conn)

    conn.close()

    html = ""

    sites = df["site"].unique()

    for site in sites:

        html += f"""

        <h2 style='
        background:#1f3c88;
        color:white;
        padding:15px;
        border-radius:10px;
        margin-top:30px;
        '>

        {site}

        </h2>

        <table style='
        width:100%;
        border-collapse:collapse;
        margin-bottom:30px;
        '>

        <tr>

        <th style='
        background:#dfe7ff;
        padding:15px;
        border:1px solid #ccc;
        '>

        橋一覧

        </th>

        </tr>

        """

        site_df = df[df["site"] == site]

        for i,row in site_df.iterrows():

            html += f"""

            <tr>

            <td style='
            border:1px solid #ccc;
            padding:15px;
            text-align:center;
            '>

            <a href="/bridge/{row['bridge']}"
            style='
            text-decoration:none;
            color:#1f3c88;
            font-weight:bold;
            font-size:22px;
            '>

            {row['bridge']}

            </a>

            </td>

            </tr>

            """

        html += "</table>"

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

    .back{{
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

    <a class='back' href='/home'>
    戻る
    </a>

    {html}

    </div>

    </body>

    </html>

    """

# =====================================
# 橋詳細
# =====================================

@app.route("/bridge/<bridge>")
def bridge_page(bridge):

    conn = sqlite3.connect("database.db")

    query = f"""

    SELECT *

    FROM data

    WHERE bridge='{bridge}'

    ORDER BY
    part,
    CAST(lot as INTEGER),
    CAST(point as INTEGER)

    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    html = ""

    parts = ["一般部","増し塗り部","一種部"]

    for part in parts:

        html += f"""

        <h2 style='background:#1f3c88;color:white;padding:15px;border-radius:10px;'>
        {part}
        </h2>

        """

        part_df = df[df["part"] == part]

        lots = part_df["lot"].unique()

        for lot in lots:

            lot_df = part_df[part_df["lot"] == lot]

            html += f"""

            <details style='margin-bottom:20px;'>

            <summary style='
            font-size:24px;
            font-weight:bold;
            color:#1f3c88;
            cursor:pointer;
            '>

            {lot}ロット

            </summary>

            <table style='width:100%;border-collapse:collapse;margin-top:15px;margin-bottom:30px;'>

            <tr style='background:#dfe7ff;'>

            <th>測点</th>
            <th>日時</th>
            <th>入力者</th>
            <th>箇所</th>
            <th>工程</th>
            <th>膜厚</th>
            <th>削除</th>

            </tr>

            """

            for i,row in lot_df.iterrows():

                html += f"""

                <tr>

                <td>{row['point']}</td>
                <td>{row['datetime']}</td>
                <td>{row['user']}</td>
                <td>{row['place']}</td>
                <td>{row['process']}</td>
                <td>{row['thickness']}</td>

                <td>

                <a href="/delete/{row['id']}"
                style="
                color:red;
                font-weight:bold;
                text-decoration:none;
                ">

                削除

                </a>

                </td>

                </tr>

                """

            html += """

            </table>

            </details>

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

    table,th,td{{
        border:1px solid #ccc;
    }}

    th,td{{
        padding:10px;
        text-align:center;
    }}

    .back{{
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

    <a class='back' href='/list'>
    戻る
    </a>

    <h1>
    {bridge}
    </h1>

    {html}

    </div>

    </body>

    </html>

    """

# =====================================
# 削除
# =====================================

@app.route("/delete/<id>")
def delete(id):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(f"""

    DELETE FROM data

    WHERE id={id}

    """)

    conn.commit()
    conn.close()

    return redirect("/list")

# =====================================
# バックアップ
# =====================================

@app.route("/backup")
def backup():

    return send_file(
        "database.db",
        as_attachment=True
    )

# =====================================
# 起動
# =====================================

if __name__ == "__main__":
    app.run(debug=False)
