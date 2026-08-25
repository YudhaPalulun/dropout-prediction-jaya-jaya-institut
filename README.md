# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

### Latar Belakang Bisnis

Jaya Jaya Institut merupakan institusi pendidikan yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak siswa yang tidak menyelesaikan pendidikannya alias dropout. Jumlah dropout yang tinggi ini menjadi masalah besar bagi institusi, sehingga Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang berpotensi dropout agar dapat diberikan bimbingan khusus.

### Permasalahan Bisnis

1. Faktor-faktor apa saja yang paling memengaruhi status seorang siswa (Dropout, Enrolled, atau Graduate)?
2. Bagaimana membangun model prediksi yang dapat mendeteksi siswa berisiko dropout sedini mungkin?
3. Bagaimana cara memonitor faktor-faktor performa siswa secara berkelanjutan melalui sebuah dashboard?

### Cakupan Proyek

1. Eksplorasi dan pemahaman dataset performa siswa (`data.csv`), didokumentasikan pada `notebook.ipynb` (analisis univariat, bivariat, dan visualisasi).
2. Data preparation dan pembangunan model machine learning untuk memprediksi status siswa.
3. Evaluasi model menggunakan metrik accuracy, precision, recall, dan confusion matrix.
4. Pembuatan business dashboard menggunakan Metabase untuk memonitor faktor-faktor performa siswa.
5. Pengembangan prototype aplikasi prediksi menggunakan Streamlit dan deployment ke Streamlit Community Cloud.
6. Penarikan kesimpulan dan penyusunan rekomendasi action items bagi institusi.

### Persiapan

**Sumber data**: Dataset yang digunakan dalam proyek ini adalah [Dataset Performa Siswa](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv), sesuai dengan instruksi submission proyek ini.

**Setup virtual environment & install dependencies:**

Proyek ini dikembangkan menggunakan **Python 3.10.11**. Disarankan menggunakan versi yang sama atau kompatibel untuk menghindari perbedaan perilaku program.

1. Buat virtual environment Python:
   ```bash
   python -m venv venv
   ```
2. Aktifkan virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies yang dibutuhkan untuk menjalankan prototype aplikasi:
   ```bash
   pip install -r requirements.txt
   ```
   `requirements.txt` sengaja hanya berisi library inti (pandas, scikit-learn, joblib, streamlit) agar proses deployment ke Streamlit Community Cloud lebih ringan dan stabil.

**Menjalankan notebook (EDA & modeling):**

Untuk membuka dan menjalankan ulang `notebook.ipynb` secara lokal, install tambahan library berikut:
```bash
pip install matplotlib seaborn jupyter ipykernel
```
Lalu buka `notebook.ipynb` menggunakan Jupyter Notebook, JupyterLab, atau VS Code (dengan ekstensi Jupyter), dan jalankan seluruh cell (Run All) untuk melihat proses eksplorasi data, pembuatan model, dan evaluasinya secara lengkap. Model hasil training akan tersimpan otomatis ke folder `model/`.

**Menjalankan prototype Streamlit secara lokal:**

```bash
streamlit run app.py
```
Aplikasi akan terbuka di browser pada `http://localhost:8501`.

**Setup environment untuk dashboard (Docker + Metabase):**

1. Pastikan Docker Desktop sudah terinstall dan berjalan.
2. Jalankan `docker compose up -d` di root folder proyek untuk menyalakan PostgreSQL dan Metabase.
3. Masukkan data siswa ke database dengan menjalankan script pemuatan data yang disediakan.
4. Buka Metabase di browser melalui `http://localhost:3001` (port disesuaikan dengan `docker-compose.yml`).
5. Login menggunakan kredensial berikut:
   - **Email**: `yudhapalulun211@gmail.com`
   - **Password**: `spaykupang211`

---

## Business Dashboard

Dashboard **Student Performance Dashboard - Jaya Jaya Institut** menampilkan visualisasi faktor-faktor penting yang memengaruhi status siswa, di antaranya:

1. Distribusi status siswa (Dropout / Enrolled / Graduate)
2. Status siswa berdasarkan performa akademik semester 1 & 2
3. Status siswa berdasarkan status pembayaran uang kuliah
4. Status siswa berdasarkan kepemilikan beasiswa
5. Status siswa berdasarkan usia saat mendaftar

Dashboard dapat diakses melalui Metabase lokal setelah mengikuti langkah-langkah pada bagian Persiapan di atas. File `metabase.db.mv.db` yang disertakan dalam repository ini adalah hasil ekspor database internal Metabase yang sudah berisi seluruh chart dan dashboard.

---

## Machine Learning Solution

Model yang dibangun adalah **Random Forest Classifier** untuk memprediksi status siswa (Dropout / Enrolled / Graduate) berdasarkan data akademik, finansial, dan demografis. Model mencapai **akurasi ~75%** pada data uji, dengan performa terbaik dalam mendeteksi kelas Dropout dan Graduate.

**Fitur paling berpengaruh** terhadap prediksi:
1. Jumlah mata kuliah yang lulus di semester 1 & 2
2. Nilai rata-rata semester 1 & 2
3. Status pembayaran uang kuliah
4. Usia saat mendaftar
5. Nilai masuk (admission grade)

Model ini di-deploy dalam bentuk prototype aplikasi menggunakan **Streamlit**, di mana pengguna (staf akademik) dapat memasukkan data seorang siswa dan langsung mendapatkan prediksi status beserta probabilitasnya.

**Link prototype (Streamlit Community Cloud):**
https://dropout-prediction-jaya-jaya-institut-4ghauvjuemiyktrbshbpse.streamlit.app/

---

## Conclusion

Berdasarkan analisis data dan pemodelan yang telah dilakukan, ditemukan empat faktor utama yang memengaruhi risiko dropout mahasiswa Jaya Jaya Institut:

1. **Performa akademik semester 1 & 2** — jumlah mata kuliah yang lulus dan nilai rata-rata adalah prediktor terkuat risiko dropout.
2. **Status pembayaran uang kuliah** — siswa yang menunggak memiliki risiko dropout yang jauh lebih tinggi.
3. **Kepemilikan beasiswa** — siswa penerima beasiswa memiliki kemungkinan dropout yang jauh lebih rendah.
4. **Usia saat mendaftar** — siswa yang mendaftar di usia lebih tua sedikit lebih berisiko dropout.

Model Random Forest yang dibangun mampu memprediksi status siswa dengan akurasi ~75%, dan telah tersedia dalam bentuk prototype aplikasi yang dapat digunakan oleh staf akademik untuk deteksi dini siswa berisiko dropout.

### Rekomendasi Action Items

1. **Sistem peringatan dini akademik** — pantau mahasiswa dengan jumlah mata kuliah lulus rendah di semester 1, berikan bimbingan/tutoring tambahan sebelum semester 2 berjalan.
2. **Bantuan finansial proaktif** — identifikasi mahasiswa yang menunggak uang kuliah dan tawarkan opsi cicilan atau bantuan finansial sebelum mereka memutuskan dropout.
3. **Perluas program beasiswa** — mengingat penerima beasiswa jauh lebih kecil risikonya untuk dropout, pertimbangkan memperluas cakupan beasiswa terutama untuk mahasiswa dengan performa akademik awal yang lemah.
4. **Gunakan model prediksi secara rutin** — jalankan prediksi risiko dropout setiap akhir semester menggunakan prototype Streamlit untuk menandai mahasiswa yang perlu intervensi khusus dari pihak akademik.
