"""Search over runbooks that knows old runbooks never die.

Plain TF-IDF retrieval returns whichever document matches the words best, and old runbooks
often match best, because they were written longer and more repetitively. This adds two rules:
superseded documents are dropped, and documents past their review date are flagged.
Standard library only.
"""
import json
import math
import re
import sys
from collections import Counter

TODAY = "2026-11-02"


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def build_index(docs):
    df = Counter()
    for d in docs:
        df.update(set(tokens(d["title"] + " " + d["text"])))
    n = len(docs)
    idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
    vecs = {}
    for d in docs:
        tf = Counter(tokens(d["title"] + " " + d["text"]))
        vecs[d["id"]] = {t: c * idf[t] for t, c in tf.items()}
    return idf, vecs


def cosine(a, b):
    dot = sum(a[t] * b.get(t, 0) for t in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def search(docs, query, fresh=True, k=3):
    idf, vecs = build_index(docs)
    q = {t: c * idf.get(t, 1.0) for t, c in Counter(tokens(query)).items()}
    superseded = {s for d in docs for s in d.get("supersedes", [])}
    results = []
    for d in docs:
        if fresh and d["id"] in superseded:
            continue
        score = cosine(q, vecs[d["id"]])
        note = ""
        if fresh and d.get("review_by", "9999") < TODAY:
            note = f"past review date ({d['review_by']}): verify before use"
        results.append((score, d["id"], d["title"], note))
    return sorted(results, reverse=True)[:k]


def main(path, query):
    with open(path, encoding="utf-8") as fh:
        docs = json.load(fh)
    for label, fresh in (("Plain search", False), ("Freshness-aware", True)):
        print(f"{label}: '{query}'")
        for score, did, title, note in search(docs, query, fresh):
            print(f"  {score:.2f}  {did:<8} {title}" + (f"  [{note}]" if note else ""))
        print()


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0] if a else "examples/runbooks.json", a[1] if len(a) > 1 else "how do I pause a delivery that is already sending")
