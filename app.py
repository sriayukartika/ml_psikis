from flask import Flask, render_template, request, redirect, url_for, session
from psikologi import prediksi_kategori

app = Flask(__name__)
app.secret_key = "kita_sehat"

pertanyaan = [
    "Bagaimana kondisi emosimu akhir-akhir ini?",
    "Apa yang paling sering kamu pikirkan belakangan?",
    "Hal apa yang paling membuatmu lelah secara mental?",
    "Apakah ada kejadian masa lalu yang masih membebani?",
    "Bagaimana perasaanmu tentang hubungan atau cinta?",
    "Apakah kamu sering merasa cemas atau overthinking?",
    "Apa yang paling kamu butuhkan saat ini?"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/intro", methods=["GET", "POST"])
def intro():
    if request.method == "POST":
        session["jawaban"] = []
        session["step"] = 0
        return redirect(url_for("pertanyaan_view"))
    return render_template("intro.html")

@app.route("/pertanyaan", methods=["GET", "POST"])
def pertanyaan_view():
    step = session.get("step", 0)

    if request.method == "POST":
        session["jawaban"].append(request.form["jawaban"])
        session["step"] = step + 1
        return redirect(url_for("pertanyaan_view"))

    if step >= len(pertanyaan):
        return redirect(url_for("hasil"))

    return render_template(
        "intro.html",
        mode="question",
        pertanyaan=pertanyaan[step],
        nomor=step + 1
    )

@app.route("/hasil")
def hasil():
    kategori, skor = prediksi_kategori(session["jawaban"])

    return render_template(
        "hasil.html",
        kategori=kategori,
        skor=skor
    )

if __name__ == "__main__":
    app.run(debug=True)
