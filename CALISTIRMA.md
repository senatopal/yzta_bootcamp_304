# Volti Projesi — Çalıştırma Kılavuzu

Bu kılavuz, backend (FastAPI), veritabanı (PostgreSQL) ve arayüz (Streamlit) bileşenlerinin yerel ortamda nasıl kurulacağını ve çalıştırılacağını adım adım açıklamaktadır.

---

## 📋 Gereksinimler

- Python 3.9 veya daha yeni bir sürüm
- Çalışan bir PostgreSQL sunucusu (yerel veya uzak)
- `pip` (Python paket yöneticisi)

---

## 1. Kurulum ve Bağımlılıklar

Projenin bağımlılıklarını yüklemek için terminalde proje ana dizinindeyken aşağıdaki komutu çalıştırın:

```bash
pip install -r backend/requirements.txt
```

*Not: PostgreSQL bağlantısı için `psycopg2-binary` kütüphanesi gereklidir. Bu kütüphane otomatik olarak yüklenecektir.*

---

## 2. PostgreSQL Veritabanı Yapılandırması ve Veri Yükleme

Volti projesi artık tümüyle PostgreSQL kullanmaktadır. Veritabanını hazırlamak için şu adımları izleyin:

### A. Ortam Değişkenleri (Environment Variables)
Backend ve veri yükleme aracı, veritabanına bağlanmak için aşağıdaki ortam değişkenlerini okur. Kendi PostgreSQL bilgilerinize göre terminalinizde tanımlayabilirsiniz:

#### Windows (PowerShell):
```powershell
$env:VOLTI_DB_HOST="localhost"
$env:VOLTI_DB_PORT="5432"
$env:VOLTI_DB_NAME="volti_db"
$env:VOLTI_DB_USER="postgres"
$env:VOLTI_DB_PASS="sifreniz_buraya"
```

#### Linux / macOS / Git Bash:
```bash
export VOLTI_DB_HOST="localhost"
export VOLTI_DB_PORT="5432"
export VOLTI_DB_NAME="volti_db"
export VOLTI_DB_USER="postgres"
export VOLTI_DB_PASS="sifreniz_buraya"
```

### B. Şemaları ve Örnek Verileri Yükleme
Örnek Parquet verilerini PostgreSQL veritabanına aktarmak için:

1. PostgreSQL üzerinde `volti_db` adında boş bir veritabanı oluşturun.
2. `Sprint 2/veritabani/schema.sql` dosyasındaki tabloları veritabanınızda çalıştırarak tabloları oluşturun.
3. Aşağıdaki komutla verileri aktarın:
   ```bash
   python "Sprint 2/veritabani/load_data.py"
   ```

---

## 3. Backend Sunucusunu Başlatma (FastAPI)

Bağlantı ayarlarınızı yaptıktan sonra FastAPI uygulamasını başlatmak için:

```bash
cd backend
python main.py
```

Sunucu başarıyla başladığında tarayıcınızdan şu adreslere erişebilirsiniz:
- **API Dokümantasyonu (Swagger UI):** `http://localhost:8000/docs`
- **Alternatif Dokümantasyon (ReDoc):** `http://localhost:8000/redoc`

---

## 4. Backend Testlerini Çalıştırma

Geliştirilen tüketim geçmişi API'sinin (`/api/v1/consumption/history`) ve diğer servislerin düzgün çalıştığını test etmek için:

```bash
python backend/test_consumption.py
```

Test aracı, geçici bir test veritabanı oluşturarak tüm uçları test edecek ve işlem bitiminde temizleyecektir.

---

## 5. Arayüzü Çalıştırma (Streamlit)

Geliştirilen dashboard arayüzünü çalıştırmak için:

```bash
streamlit run dashboard/lib/app.py
```

Tarayıcınız otomatik olarak `http://localhost:8501` adresinde arayüzü açacaktır.
