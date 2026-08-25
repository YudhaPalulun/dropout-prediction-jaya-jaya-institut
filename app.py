import streamlit as st
import joblib
import json
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

st.set_page_config(page_title="Prediksi Dropout Mahasiswa - Jaya Jaya Institut", page_icon="🎓", layout="centered")

@st.cache_resource
def load_artifacts():
    model = joblib.load(os.path.join(MODEL_DIR, "model.joblib"))
    feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.joblib"))
    with open(os.path.join(MODEL_DIR, "defaults.json")) as f:
        defaults = json.load(f)
    return model, feature_columns, defaults

model, feature_columns, defaults = load_artifacts()

st.title("🎓 Prediksi Risiko Dropout Mahasiswa")
st.markdown(
    "Aplikasi ini membantu **Jaya Jaya Institut** memprediksi kemungkinan seorang mahasiswa akan "
    "**Dropout** atau berhasil **Graduate**, berdasarkan data akademik, finansial, dan demografis. "
    "Model dilatih khusus pada data mahasiswa yang statusnya sudah final (Dropout/Graduate); "
    "cocok digunakan untuk mahasiswa yang masih aktif kuliah guna deteksi dini risiko dropout. "
    "Isi data pada form di bawah, lalu klik **Prediksi**."
)

st.divider()
st.subheader("📊 Data Akademik Utama")

col1, col2 = st.columns(2)
with col1:
    cu1_approved = st.number_input(
        "Mata kuliah lulus - Semester 1",
        min_value=0, max_value=30,
        value=int(defaults["Curricular_units_1st_sem_approved"]["default"])
    )
    cu1_grade = st.number_input(
        "Rata-rata nilai - Semester 1",
        min_value=0.0, max_value=20.0,
        value=float(defaults["Curricular_units_1st_sem_grade"]["default"])
    )
    admission_grade = st.number_input(
        "Nilai masuk (Admission Grade)",
        min_value=0.0, max_value=200.0,
        value=float(defaults["Admission_grade"]["default"])
    )

with col2:
    cu2_approved = st.number_input(
        "Mata kuliah lulus - Semester 2",
        min_value=0, max_value=30,
        value=int(defaults["Curricular_units_2nd_sem_approved"]["default"])
    )
    cu2_grade = st.number_input(
        "Rata-rata nilai - Semester 2",
        min_value=0.0, max_value=20.0,
        value=float(defaults["Curricular_units_2nd_sem_grade"]["default"])
    )
    age = st.number_input(
        "Usia saat mendaftar",
        min_value=15, max_value=70,
        value=int(defaults["Age_at_enrollment"]["default"])
    )

st.subheader("💰 Data Finansial")
col3, col4, col5 = st.columns(3)
with col3:
    tuition_paid = st.selectbox("Uang kuliah lunas?", ["Ya", "Tidak"], index=0)
with col4:
    scholarship = st.selectbox("Penerima beasiswa?", ["Ya", "Tidak"], index=1)
with col5:
    debtor = st.selectbox("Memiliki tunggakan?", ["Tidak", "Ya"], index=0)

# Build the full feature row, starting from dataset medians for anything not shown above
input_data = {col: defaults[col]["default"] for col in feature_columns}
input_data["Curricular_units_1st_sem_approved"] = cu1_approved
input_data["Curricular_units_1st_sem_grade"] = cu1_grade
input_data["Curricular_units_2nd_sem_approved"] = cu2_approved
input_data["Curricular_units_2nd_sem_grade"] = cu2_grade
input_data["Admission_grade"] = admission_grade
input_data["Age_at_enrollment"] = age
input_data["Tuition_fees_up_to_date"] = 1 if tuition_paid == "Ya" else 0
input_data["Scholarship_holder"] = 1 if scholarship == "Ya" else 0
input_data["Debtor"] = 1 if debtor == "Ya" else 0

with st.expander("⚙️ Opsi lanjutan (fitur demografis & akademik lainnya)"):
    st.caption("Nilai default sudah diisi otomatis dari rata-rata dataset. Ubah jika perlu.")
    advanced_cols = [c for c in feature_columns if c not in [
        "Curricular_units_1st_sem_approved", "Curricular_units_1st_sem_grade",
        "Curricular_units_2nd_sem_approved", "Curricular_units_2nd_sem_grade",
        "Admission_grade", "Age_at_enrollment", "Tuition_fees_up_to_date",
        "Scholarship_holder", "Debtor"
    ]]
    n_cols = 3
    cols = st.columns(n_cols)
    for i, feat in enumerate(advanced_cols):
        info = defaults[feat]
        with cols[i % n_cols]:
            if info["is_int"]:
                val = st.number_input(feat, min_value=int(info["min"]), max_value=int(info["max"]),
                                       value=int(info["default"]), key=feat)
            else:
                val = st.number_input(feat, min_value=float(info["min"]), max_value=float(info["max"]),
                                       value=float(info["default"]), key=feat)
            input_data[feat] = val

st.divider()

if st.button("🔮 Prediksi Status Mahasiswa", type="primary", use_container_width=True):
    input_df = pd.DataFrame([input_data])[feature_columns]
    pred = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]  # index 0 = Graduate, index 1 = Dropout

    st.subheader("Hasil Prediksi")
    if pred == 1:
        st.error(f"⚠️ Prediksi: Berisiko **Dropout** (probabilitas {proba[1]*100:.1f}%)")
        st.info(
            "💡 **Rekomendasi:** Mahasiswa ini disarankan mendapat bimbingan akademik "
            "tambahan dan/atau bantuan finansial sesegera mungkin."
        )
    else:
        st.success(f"🎉 Prediksi: Kemungkinan **Graduate** (probabilitas {proba[0]*100:.1f}%)")

    proba_df = pd.DataFrame({
        "Status": ["Graduate", "Dropout"],
        "Probabilitas": [proba[0], proba[1]]
    })
    st.bar_chart(proba_df.set_index("Status"))

st.divider()
st.caption(
    "Model dilatih pada data mahasiswa berstatus final (Dropout/Graduate). "
    "Prototype ini dibuat untuk keperluan submission Proyek Akhir Dicoding - Belajar Penerapan Data Science."
)
