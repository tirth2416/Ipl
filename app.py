from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("players.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home page (search players)
@app.route("/")
def index():

    search = request.args.get("search")

    conn = get_db()

    if search:
        players = conn.execute(
            "SELECT * FROM players WHERE name LIKE ?",
            ('%' + search + '%',)
        ).fetchall()
    else:
        players = conn.execute("SELECT * FROM players").fetchall()

    return render_template("index.html", players=players)


# Player profile page
@app.route("/player/<int:id>", methods=["GET", "POST"])
def player(id):

    conn = get_db()

    player = conn.execute(
        "SELECT * FROM players WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        new_price = int(request.form["price"])

        if new_price > player["price"]:

            conn.execute(
                "UPDATE players SET price=? WHERE id=?",
                (new_price, id)
            )

            conn.commit()

        return redirect(f"/player/{id}")

    return render_template("player.html", player=player)


# Auction board page
@app.route("/auction")
def auction():

    conn = get_db()

    players = conn.execute(
        "SELECT * FROM players ORDER BY price DESC"
    ).fetchall()

    return render_template("auction.html", players=players)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)