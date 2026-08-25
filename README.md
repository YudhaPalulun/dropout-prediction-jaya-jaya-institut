# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

### Latar Belakang Bisnis

Jaya Jaya Institut merupakan institusi pendidikan yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak siswa yang tidak menyelesaikan pendidikannya alias dropout. Jumlah dropout yang tinggi ini menjadi masalah besar bagi institusi, sehingga Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang berpotensi dropout agar dapat diberikan bimbingan khusus.

### Permasalahan Bisnis

1. Faktor-faktor apa saja yang paling memengaruhi apakah seorang siswa akan Dropout atau berhasil Graduate?
2. Bagaimana membangun model prediksi yang dapat mendeteksi siswa berisiko dropout sedini mungkin?
3. Bagaimana cara memonitor faktor-faktor performa siswa secara berkelanjutan melalui sebuah dashboard?

### Cakupan Proyek

1. Eksplorasi dan pemahaman dataset performa siswa (`data.csv`), didokumentasikan pada `notebook.ipynb` (analisis univariat, bivariat, dan visualisasi).
2. Data preparation, termasuk penentuan target pemodelan: hanya siswa berstatus **Dropout** dan **Graduate** yang digunakan untuk training (siswa **Enrolled** disisihkan ke `enrolled_students.csv` untuk keperluan prediksi di masa mendatang, karena status akhir mereka belum diketahui).
3. Pembangunan model klasifikasi biner (Dropout vs Graduate) dan evaluasinya menggunakan metrik accuracy, precision, recall, dan confusion matrix.
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
Lalu buka `notebook.ipynb` menggunakan Jupyter Notebook, JupyterLab, atau VS Code (dengan ekstensi Jupyter), dan jalankan seluruh cell (Run All). Notebook ini akan menghasilkan `enrolled_students.csv` (data siswa yang statusnya belum final) dan menyimpan model hasil training ke folder `model/`.

**Menjalankan prototype Streamlit secara lokal:**

```bash
streamlit run app.py
```
Aplikasi akan terbuka di browser pada `http://localhost:8501`.

**Setup environment untuk dashboard (Docker + Metabase):**

Proyek ini menggunakan **Docker Compose** untuk menjalankan PostgreSQL (menyimpan data siswa) dan **Metabase versi 0.63.14.2** (business dashboard). Berkas `docker-compose.yml` sudah disertakan dalam repository ini.

1. Pastikan Docker Desktop sudah terinstall dan berjalan.
2. Jalankan perintah berikut di root folder proyek ini:
   ```bash
   docker compose up -d
   ```
   Ini akan menyalakan PostgreSQL dan Metabase versi 0.63.14.2 sesuai yang tertulis di `docker-compose.yml`.
3. Masukkan data siswa ke database dengan menjalankan:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary
   python load_data.py
   ```
4. Buka Metabase di browser melalui `http://localhost:3000`.
5. **Untuk melihat dashboard yang sudah jadi** (bukan setup dari nol), salin file `metabase.db.mv.db` yang disertakan dalam repository ini ke dalam container, lalu restart container:
   ```bash
   docker cp metabase.db.mv.db metabase:/metabase.db/metabase.db.mv.db
   docker restart metabase
   ```
6. Setelah container selesai restart (±30 detik), buka kembali `http://localhost:3000` dan login menggunakan kredensial berikut:
   - **Email**: `yudhapalulun211@gmail.com`
   - **Password**: `spaykupang211`
7. Dashboard **"Student Performance Dashboard - Jaya Jaya Institut"** dapat ditemukan di koleksi **"Dropout Dashboard"**.

---

## Business Dashboard

Dashboard **Student Performance Dashboard - Jaya Jaya Institut** menampilkan visualisasi faktor-faktor penting yang memengaruhi status siswa (Dropout/Graduate), di antaranya:

1. **Status Overview** — proporsi keseluruhan siswa Dropout vs Graduate (pie chart).
2. **Status by Mata Kuliah Semester 1** — distribusi status berdasarkan jumlah mata kuliah yang lulus.
3. **Status by Tuition Fees** — status siswa berdasarkan kelunasan pembayaran uang kuliah.
4. **Status by Scholarship** — status siswa berdasarkan kepemilikan beasiswa.
5. **Status by Age Group** — status siswa berdasarkan kelompok usia saat mendaftar.
6. **Status by Gender** — status siswa berdasarkan gender.
7. **Status by Marital Status** — status siswa berdasarkan status pernikahan.
8. **Status by Debtor** — status siswa berdasarkan ada/tidaknya tunggakan.

Dashboard dilengkapi filter interaktif (berdasarkan atribut demografis) sehingga pengguna dapat mengeksplorasi data dari berbagai sudut pandang, bukan sekadar tampilan statis.

Dashboard dapat diakses melalui Metabase lokal setelah mengikuti langkah-langkah pada bagian Persiapan di atas. File `metabase.db.mv.db` yang disertakan dalam repository ini adalah hasil ekspor database internal Metabase yang sudah berisi seluruh chart dan dashboard tersebut.

---

## Machine Learning Solution

Model yang dibangun adalah **Random Forest Classifier** untuk klasifikasi **biner**: memprediksi apakah seorang siswa akan **Dropout** atau **Graduate**, berdasarkan data akademik, finansial, dan demografis.

**Catatan metodologi penting:** Dataset asli memiliki 3 kategori status (Dropout, Enrolled, Graduate). Karena siswa berstatus **Enrolled** belum memiliki hasil akhir, mereka **tidak disertakan dalam proses training** — hanya 3.630 siswa berstatus Dropout/Graduate yang dipakai untuk melatih dan mengevaluasi model. Data 794 siswa Enrolled disisihkan ke `enrolled_students.csv` untuk simulasi prediksi di masa mendatang.

Model mencapai **akurasi 91.74%** pada data uji (726 siswa), dengan hasil classification report sebagai berikut:

| Kelas | Precision | Recall | F1-score | Support |
|---|---|---|---|---|
| Graduate | 0.92 | 0.95 | 0.93 | 442 |
| Dropout | 0.91 | 0.87 | 0.89 | 284 |

Angka ini identik dengan output yang dihasilkan pada `notebook.ipynb` bagian Evaluation.

**Fitur paling berpengaruh** terhadap prediksi:
1. Jumlah mata kuliah yang lulus di semester 1 & 2
2. Nilai rata-rata semester 1 & 2
3. Status pembayaran uang kuliah
4. Usia saat mendaftar
5. Kepemilikan beasiswa

Model ini di-deploy dalam bentuk prototype aplikasi menggunakan **Streamlit**, di mana pengguna (staf akademik) dapat memasukkan data seorang siswa dan langsung mendapatkan prediksi Dropout/Graduate beserta probabilitasnya.

**Link prototype (Streamlit Community Cloud):**
https://dropout-prediction-jaya-jaya-institut-4ghauvjuemiyktrbshbpse.streamlit.app/

---

## Conclusion

Berdasarkan analisis data dan pemodelan biner (Dropout vs Graduate) yang telah dilakukan, ditemukan tiga faktor utama yang memengaruhi risiko dropout mahasiswa Jaya Jaya Institut:

1. **Performa akademik semester 1 & 2** — jumlah mata kuliah yang lulus dan nilai rata-rata adalah prediktor terkuat risiko dropout.
2. **Status pembayaran uang kuliah** — siswa yang menunggak memiliki risiko dropout yang jauh lebih tinggi.
3. **Kepemilikan beasiswa** — siswa penerima beasiswa memiliki kemungkinan dropout yang jauh lebih rendah.

Dengan memfokuskan model hanya pada siswa yang status akhirnya sudah diketahui (Dropout/Graduate), model Random Forest yang dibangun mampu mencapai **akurasi 91.74%** (Graduate: precision 0.92, recall 0.95; Dropout: precision 0.91, recall 0.87) — jauh lebih valid dan tidak ambigu dibanding pendekatan klasifikasi 3 kelas sebelumnya. Model ini kini siap digunakan untuk mendeteksi risiko dropout pada 794 siswa yang masih berstatus Enrolled.

### Rekomendasi Action Items

1. **Sistem peringatan dini akademik** — pantau mahasiswa dengan jumlah mata kuliah lulus rendah di semester 1, berikan bimbingan/tutoring tambahan sebelum semester 2 berjalan.
2. **Bantuan finansial proaktif** — identifikasi mahasiswa yang menunggak uang kuliah dan tawarkan opsi cicilan atau bantuan finansial sebelum mereka memutuskan dropout.
3. **Perluas program beasiswa** — mengingat penerima beasiswa jauh lebih kecil risikonya untuk dropout, pertimbangkan memperluas cakupan beasiswa terutama untuk mahasiswa dengan performa akademik awal yang lemah.
4. **Terapkan model prediksi pada siswa Enrolled** — gunakan model dan prototype Streamlit untuk memprediksi risiko dropout pada 794 siswa yang masih aktif kuliah (`enrolled_students.csv`), sehingga intervensi akademik dapat dilakukan sebelum mereka benar-benar dropout.
