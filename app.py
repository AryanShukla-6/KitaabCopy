
import streamlit as st
import pandas as pd

st.set_page_config(page_title="KitaabCopy", page_icon="📚", layout="centered")

LEVEL_WEIGHT = {"Beginner": 1, "Intermediate": 2, "Expert": 3}
LEVELS = ["Beginner", "Intermediate", "Expert"]

@st.cache_data
def load_data():
    return pd.read_csv("books.csv")

df = load_data()

st.title("📚 KitaabCopy")
st.caption("An explainable technical-book recommender built around what you actually want to learn.")

c1, c2, c3 = st.columns(3)
with c1:
    subject = st.selectbox("Subject", sorted(df["subject"].unique()))
with c2:
    level = st.selectbox("Level", LEVELS)
with c3:
    genre = st.selectbox("Style", ["Practical", "Theoretical"])

if st.button("Recommend Top 3", type="primary", use_container_width=True):
    candidates = df[df["subject"].str.lower() == subject.lower()].copy()

    if candidates.empty:
        st.warning("No exact subject match in the current MVP dataset.")
    else:
        target = LEVEL_WEIGHT[level]
        candidates["level_score"] = candidates["level"].map(LEVEL_WEIGHT).apply(lambda x: max(0, 1 - abs(x-target)*0.45))
        candidates["genre_score"] = (candidates["genre"] == genre).astype(float)
        candidates["rating_score"] = candidates["rating"] / 5.0

        # Explainable ranking: user fit matters more than popularity.
        candidates["score"] = (
            0.50 * candidates["genre_score"] +
            0.35 * candidates["level_score"] +
            0.15 * candidates["rating_score"]
        )

        top = candidates.sort_values(["score","rating"], ascending=False).head(3)

        for i, (_, row) in enumerate(top.iterrows(), 1):
            st.subheader(f"{i}. {row['title']}")
            st.write(f"**Author:** {row['author']}  ·  **Rating:** {row['rating']}/5")
            st.write(f"**Level:** {row['level']}  ·  **Style:** {row['genre']}")
            st.write(row["description"])
            reasons = []
            if row["genre"] == genre: reasons.append(f"matches your {genre.lower()} preference")
            if row["level"] == level: reasons.append(f"matches your {level.lower()} level")
            else: reasons.append(f"close to your {level.lower()} level")
            st.caption("Why recommended: " + "; ".join(reasons) + ".")
            st.divider()

st.info("MVP uses a small curated technical-book catalog and an explainable ranking function. The architecture is designed to swap in a larger dataset later.")
