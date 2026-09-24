from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

kategori_data = {
    "Masalah Cinta": [
        "patah hati",
        "kehilangan pasangan",
        "hubungan tidak sehat"
    ],
    "Move On": [
        "sulit melupakan",
        "terjebak masa lalu",
        "belum bisa ikhlas"
    ],
    "Trauma Emosional": [
        "takut hubungan",
        "pengalaman buruk",
        "takut disakiti lagi"
    ],
    "Stres & Overthinking": [
        "pikiran berlebihan",
        "cemas berlebih",
        "tidak tenang"
    ]
}

vectorizer = TfidfVectorizer()

def prediksi_kategori(jawaban_list):
    jawaban_text = " ".join(jawaban_list)

    corpus = []
    labels = []
    for kategori, contoh in kategori_data.items():
        for teks in contoh:
            corpus.append(teks)
            labels.append(kategori)

    tfidf = vectorizer.fit_transform(corpus + [jawaban_text])
    similarity = cosine_similarity(tfidf[-1], tfidf[:-1])

    skor = {}
    for i, label in enumerate(labels):
        skor[label] = skor.get(label, 0) + similarity[0][i]

    kategori_tertinggi = max(skor, key=skor.get)
    return kategori_tertinggi, skor
