# simple-app

Aplikasi Flask dengan database SQLite untuk praktikum Jenkins dan Docker.
Endpoint `/` menyimpan kunjungan ke database dan menampilkan jumlah kunjungan.
Endpoint `/health` menampilkan status aplikasi.

## Persiapan

1. Upload seluruh file paket ini ke root repository GitHub, termasuk `.dockerignore`.
2. Di Jenkinsfile, ganti `GANTI_USERNAME_DOCKERHUB` dengan username Docker Hub.
3. Buat repository Docker Hub `simple-app` di akun tersebut.
4. Buat Docker Hub access token dengan izin Read dan Write.
5. Di Jenkins, tambahkan Global credential bertipe Username with password:
   - Username: username Docker Hub.
   - Password: access token Docker Hub.
   - ID: `dockerhub-credentials`.
6. Buat pipeline dengan Definition `Pipeline script from SCM`, SCM `Git`, URL
   repository kamu, branch `*/main`, dan Script Path `Jenkinsfile`.
7. Jalankan Docker Desktop sebelum Build Now. Jenkins Windows harus memiliki
   akses ke Docker CLI dan Docker Engine. Keberhasilan `docker version` di
   PowerShell pengguna belum menjamin akun layanan Jenkins memiliki akses.

Jangan upload token atau password ke GitHub.

## Menjalankan aplikasi setelah build berhasil

Jalankan di PowerShell. Ganti `USERNAME_DOCKERHUB` dengan username kamu:

```powershell
docker volume create simple_app_data
docker run -d --name simple-app -p 5000:5000 -v simple_app_data:/data USERNAME_DOCKERHUB/simple-app:latest
```

Buka http://localhost:5000 dan refresh untuk menambah kunjungan. Volume menyimpan
database walaupun container dihapus. Pipeline membangun dan push image;
menjalankan container dilakukan secara manual dengan perintah di atas.

Jika port 5000 digunakan aplikasi lain, ganti `-p 5000:5000` menjadi
`-p 5001:5000` dan buka http://localhost:5001.

Untuk mengganti container setelah image diperbarui, hapus container lama dengan
`docker rm -f simple-app`, pull image terbaru, lalu jalankan kembali perintah run.
Volume database tetap dipakai.
