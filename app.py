from flask import Flask, request, redirect, session
from supabase import create_client
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = "Sakura6788"

# ====================================
# Supabase接続
# ====================================

url = "https://xcjgbrzqxkgoiynjsdhc.supabase.co"

key = "ここに公開可能なキー"

supabase = create_client(url, key)

# ====================================
# 判定基準
# ====================================

standards = {
    "防食下地":75,
    "下塗1":60,
    "増し塗1":60,
    "増し塗2":60,
    "下塗2":60,
    "中塗り":30,
    "上塗り":25
}

# ====================================
# ユーザー
# ====================================

users = {
    "敦司":"6788",
    "furui":"6788",
    "tsuchiya":"6788",
    "akashi":"6788",
    "kawano":"6788"
}

# ====================================
# 橋データ
# ====================================

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

# ====================================
# ログイン
# ====================================

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

    <h1>橋梁膜厚管理</h1>

    <form method="POST">

    ID<br>
    <input name="id"><br><br>

    PASSWORD<br>
    <input type="password" name="pw"><br><br>

    <button type="submit">ログイン</button>

    </form>

    """

# ====================================
# ホーム
# ====================================

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

    site_options = ""

    for site in bridges:

        site_options += f"<option>{site}</option>"

    bridge_options = ""

    for site in bridges:

        for bridge in bridges[site]:

            bridge_options += f"<option>{bridge}</option>"

    lot_options = ""

    for i in range(1,51):

        lot_options += f"<option>{i}</option>"

    point_options = ""

    for i in range(1,26):

        point_options += f"<option>{i}</option>"

    return f"""

    <h1>橋梁膜厚管理</h1>

    <form method="POST">

    現場名<br>

    <select name="site">

    {site_options}

    </select>

    <br><br>

    橋名<br>

    <select name="bridge">

    {bridge_options}

    </select>

    <br><br>

    箇所<br>

    <select name="place">

    <option>上部工</option>
    <option>下部工</option>
    <option>上部工内面</option>
    <option>下部工内面</option>

    </select>

    <br><br>

    部位<br>

    <select name="part">

    <option>一般部</option>
    <option>増し塗り部</option>
    <option>一種部</option>

    </select>

    <br><br>

    ロット<br>

    <select name="lot">

    {lot_options}

    </select>

    <br><br>

    測点<br>

    <select name="point">

    {point_options}

    </select>

    <br><br>

    工程<br>

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

    <br><br>

    膜厚<br>

    <input type="number" name="thickness">

    <br><br>

    <button type="submit">保存</button>

    </form>

    <br><br>

    <a href="/list">入力情報一覧</a>

    """

# ====================================
# 一覧
# ====================================

@app.route("/list")
def list_page():

    response = supabase.table("data").select("*").execute()

    df = pd.DataFrame(response.data)

    html = "<h1>入力情報一覧</h1>"

    if len(df) == 0:

        return html + "データなし"

    for site in df["site"].unique():

        html += f"<h2>{site}</h2>"

        site_df = df[df["site"] == site]

        for bridge in site_df["bridge"].unique():

            html += f"""

            <a href='/bridge/{bridge}'>

            {bridge}

            </a><br><br>

            """

    return html

# ====================================
# 橋詳細
# ====================================

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

        html += f"<h2>{part}</h2>"

        part_df = df[df["part"] == part]

        if len(part_df) == 0:

            continue

        lots = sorted(part_df["lot"].unique())

        for lot in lots:

            html += f"<h3>{lot}ロット</h3>"

            lot_df = part_df[part_df["lot"] == lot]

            html += """

            <table border="1" cellpadding="10">

            <tr>

            <th>測点</th>
            <th>工程</th>
            <th>膜厚</th>
            <th>増加量</th>
            <th>判定</th>

            </tr>

            """

            previous = None

            for i,row in lot_df.iterrows():

                thickness = int(row["thickness"])

                increase = "-"
                result = "-"

                if previous is not None:

                    diff = thickness - previous

                    increase = f"+{diff}"

                    standard = standards.get(
                        row["process"],
                        0
                    )

                    if diff >= standard:

                        result = "○"

                    else:

                        result = "✕"

                previous = thickness

                html += f"""

                <tr>

                <td>{row["point"]}</td>
                <td>{row["process"]}</td>
                <td>{thickness}</td>
                <td>{increase}</td>
                <td>{result}</td>

                </tr>

                """

            html += "</table><br>"

    return html

# ====================================
# 起動
# ====================================

if __name__ == "__main__":
    app.run(debug=True)
