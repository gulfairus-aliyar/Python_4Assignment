from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from parsing import get_paragraphs

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///.db"
db = SQLAlchemy(app)


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coin_name = db.Column(db.String, unique=True, nullable=False)
    paragraphs = db.relationship("Paragraph", backref='coin', lazy=True)


class Paragraph(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coin_id = db.Column(db.Integer, db.ForeignKey("coin.id"), nullable=False)
    text = db.Column(db.String)


@app.route("/coin", methods=["GET", "POST"])
def coin():
    if request.method == "GET":
        return render_template("index.html", paragraphs="")
    else:
        coin_name = request.form["coin"].lower()
        coin = Coin.query.filter_by(coin_name=coin_name).first()
        if not coin:
            coin = Coin(coin_name=coin_name)
            db.session.add(coin)
            db.session.flush()
            db.session.refresh(coin)
            paragraphs = get_paragraphs(coin_name)
            for p in paragraphs:
                paragraph = Paragraph(coin_id=coin.id, text=p)
                db.session.add(paragraph)
            db.session.commit()
            coin = Coin.query.filter_by(coin_name=coin_name).first()
        paragraphs = [p.text for p in coin.paragraphs]

        return render_template("index.html", coin=coin_name, paragraphs=paragraphs)


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run(host="0.0.0.0", port=5000)
