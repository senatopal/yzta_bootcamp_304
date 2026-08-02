# Volti Projesi — Çalıştırma Kılavuzu

Bu kılavuz; backend (FastAPI), veritabanı (PostgreSQL) ve arayüz (Reflex) bileşenlerinin yerel ortamda nasıl kurulacağını ve
çalıştırılacağını adım adım açıklamaktadır.

---

## 📋 Gereksinimler

- Python 3.10 veya daha yeni bir sürüm
- Çalışan bir PostgreSQL sunucusu
- `pip`
- Reflex
- Google AI Studio üzerinden oluşturulmuş bir Gemini API anahtarı
---

## 1. Kurulum ve Bağımlılıklar

Projenin bağımlılıklarını yüklemek için terminalde proje ana dizinindeyken aşağıdaki komutu çalıştırın:

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

*Not: PostgreSQL bağlantısı için `psycopg2-binary` kütüphanesi gereklidir. Bu kütüphane otomatik olarak yüklenecektir.*

---

## 2. PostgreSQL Veritabanı Yapılandırması ve Veri Yükleme

Volti projesi artık tümüyle PostgreSQL kullanmaktadır. Veritabanı bağlantı bilgilerini yapılandırmak için iki yöntem mevcuttur:

### A. `.env` Dosyası ile Yapılandırma (Önerilen)

`backend/` klasörünün altında `.env` adında bir dosya oluşturun ve PostgreSQL bağlantı bilgilerinizi buraya yazın:

```env
VOLTI_DB_HOST=localhost
VOLTI_DB_PORT=5432
VOLTI_DB_NAME=volti_db
VOLTI_DB_USER=postgres
VOLTI_DB_PASS=sifreniz_buraya

GEMINI_API_KEY=google_ai_studio_api_key_buraya
GEMINI_MODEL=gemini-3.6-flash
```
*Not: GEMINI_API_KEY değişkeninin karşısına Google AI Studio üzerinden oluşturulan API anahtarı yazılmalıdır. API anahtarının başına veya sonuna boşluk eklenmemeli ve anahtar tırnak içine alınmamalıdır.

*Örnek: GEMINI_API_KEY=AIzaSy...


Hem backend sunucusu hem de veritabanı yükleme script'i bu dosyayı otomatik olarak okuyacaktır.

### B. Ortam Değişkenleri (Environment Variables - Alternatif)

Eğer `.env` dosyası kullanmak istemiyorsanız, terminalinizde şu komutları çalıştırarak ortam değişkenlerini el ile tanımlayabilirsiniz:

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

### C. Şemaları ve Örnek Verileri Yükleme

Örnek Parquet verilerini PostgreSQL veritabanına aktarmak için:

1. PostgreSQL üzerinde `volti_db` adında boş bir veritabanı oluşturun (Tablolar backend başlatıldığında SQLAlchemy tarafından otomatik olarak oluşturulacaktır. Dilerseniz `Sprint 2/veritabani/schema.sql` dosyasını manuel de çalıştırabilirsiniz).
2. Proje kök dizinindeyken aşağıdaki komutla verileri aktarın:
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

Backend üzerinde geliştirilen tüketim geçmişi, yapay zeka koçu, anomali tespiti ve makine öğrenmesi tahmin modellerinin düzgün çalıştığını test etmek için aşağıdaki komutları çalıştırabilirsiniz:

```bash
# Tüketim geçmişi API testleri
python backend/test_consumption.py

# Makine öğrenmesi ve baseline tahmin testleri
python backend/test_forecast.py

# Karbon ayak izi, yük kaydırma ve anomali tespiti testleri
python backend/test_insights.py

# Yapay zeka koçu (LLM Grounding Context) testleri
python backend/test_coach.py
```

Test araçları, geçici SQLite test veritabanları oluşturarak tüm uçları izole şekilde test eder ve işlem bitiminde bu dosyaları otomatik temizler.


---

## 5. Arayüzü Çalıştırma — Reflex

Backend çalışmaya devam ederken ikinci bir terminal açın.

Proje kök dizininden:

```bash
cd frontend
reflex run

#Arayüz aşağıdaki adreste açılacaktı:
http://localhost:3001/

#Yapay zekâ koçunun çalışabilmesi için backend sunucusunun açık olması ve 
#backend/.env dosyasında geçerli bir GEMINI_API_KEY bulunması gerekir.
```

## Önerilen hızlı çalıştırma özeti
```markdown
## Hızlı Başlangıç

### Terminal 1 — Backend

```bash
cd backend
python -m uvicorn main:app --reload --port 8000

### Terminal 2 — Frontend
cd frontend
reflex run

URL: http://localhost:3000/