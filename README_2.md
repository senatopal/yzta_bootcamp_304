# **Takım İsmi**
Voltra

# Ürün İle İlgili Bilgiler

## Takım Elemanları
- Merve Günsay: Product Owner (ayrıca Frontend – UX/UI katkısı)
- Senanur Topal: Scrum Master (ayrıca Backend geliştirmeye katkı)
- Yasemin Koçbıyık: Team Member / ML & Model Geliştirici
- Reyyan Temel: Team Member / Veri & Backend Geliştirici
- Betül İrem: Team Member / Arayüz & LLM Entegrasyon (Yardımcı)

## Ürün İsmi
--Volti--

## Ürün Açıklaması
- Volti; bir hanenin veya küçük işletmenin elektrik tüketimini geçmiş akıllı sayaç verisinden öğrenip tahmin eden, dinamik (zamana bağlı) tarifeye göre "neyi ne zaman çalıştırırsan ne kadar tasarruf edersin" diye hesaplayan ve bu önerileri sade, gündelik dille anlatan yapay zekâ destekli bir enerji tasarruf koçudur. Kullanıcının hem elektrik faturasını hem karbon ayak izini düşürmesine somut ve kişiselleştirilmiş önerilerle yardımcı olur. Volti'yi bir veri analizi çalışmasından ayıran şey karar/aksiyon katmanıdır: sadece "tüketimin şöyle" demez, "şimdi ne yapmalısın" der.

## Ürün Özellikleri
- Hane bazında gelecek dönem elektrik tüketimi tahmini
- Dinamik tarifeye göre günlük/aylık maliyet ve en pahalı/ucuz saatlerin gösterimi
- "Neyi ne zaman çalıştır" tarzı somut yük kaydırma önerileri
- Olağandışı tüketim (anomali/israf) uyarısı
- Sonuçları sade dille anlatan LLM tabanlı tasarruf koçu (veriye dayalı, uydurma yok)
- Tasarrufun hem £ (sterlin) hem kg CO₂ (karbon etkisi) olarak gösterimi
- Tüketim grafiği + öneriler + koç metnini tek ekranda toplayan panel

> **Not:** Veri seti Londra'ya ait olduğundan tüm maliyet/tasarruf hesapları **sterlin (£/pence)** cinsindendir (veri setindeki dinamik tarife pence/kWh olarak verilir).

## Hedef Kitle
- Zamana bağlı (dinamik) tarifeli elektrik kullanan haneler
- Faturasını düşürmek isteyen küçük işletmeler
- Çatı güneşi / elektrikli araç sahibi "prosumer" kullanıcılar
- Sürdürülebilirlik-duyarlı, enerji tasarrufuna önem veren kullanıcılar
- 18 – 65 yaş arası, dijital araçları kullanabilen bireyler

## Product Backlog URL
[Miro Backlog Board](https://miro.com/app/board/BOARD-ID/)  *(ekip Miro board bağlantınızı buraya ekleyin)*

**Product Backlog (özet):** Öncelik MoSCoW (Must/Should/Could), puanlar Fibonacci story-point'tir. Proje **3 sprint**ten oluşur; Sprint 1 keşif/planlama sprintiydi (bugün tamamlandı), geliştirme Sprint 2–3'e planlanmıştır.

| Epik | Kullanıcı Hikayesi | Öncelik | Puan | Sprint |
|---|---|---|---|---|
| Veri & Altyapı | Londra akıllı sayaç verisini indirip temizlemek | Must | 5 | 2 |
| Veri & Altyapı | Tüketim + hava + tarife verilerini birleştirmek | Must | 3 | 2 |
| Tahmin | Gelecek tüketim tahminini görmek | Must | 8 | 2 |
| Tahmin | Modeli bir baseline ile kıyaslamak | Must | 3 | 2 |
| Tarife & Optimizasyon | Dinamik tarifeye göre günlük/aylık maliyeti görmek | Must | 5 | 2 |
| Tarife & Optimizasyon | Neyi ne zaman çalıştırınca ne kadar tasarruf edileceğini görmek | Must | 8 | 3 |
| Anomali | Olağandışı yüksek tüketim uyarısı almak | Should | 5 | 3 |
| LLM Koç | Önerileri sade dille açıklayan koç metni görmek | Must | 5 | 3 |
| LLM Koç | Koçun uydurma sayı vermemesi (grounding) | Must | 3 | 3 |
| Arayüz | Tüketim ve önerileri bir panelde görmek | Must | 8 | 3 |
| Karbon | Tasarrufun karbon etkisini görmek | Should | 3 | 3 |
| Sunum | Çalışan demo ve sunum hazırlamak | Must | 5 | 3 |
| Stretch | Canlı elektrik fiyatına göre öneri almak | Could | 8 | Stretch |

> Sprint 2 ≈ 24 puan (veri + tahmin + tarife maliyeti). Sprint 3, ürünü tamamlayan sprinttir; içindeki **Should/Could** işleri (anomali, karbon, canlı fiyat) kapasiteye göre esnektir.

---

# Sprint 1

- **Sprint Notu:** Sprint 1 keşif ve karar odaklıydı; hedef, "yeterli veriye sahip, AI entegrasyonu yapılabilir ve 1 ayda (3 sprintte) bitebilir" bir proje seçmekti. Bu hedefe ulaşıldı ve proje **Volti** olarak kesinleşti.

- **Backlog düzeni ve Story seçimleri:** Backlog, ilk yapılacak story'lere göre önceliklendirilmiştir (MoSCoW). Sprint başına tahmin edilen toplam puanı geçmeyecek şekilde sıradan seçimler yapılır; her story'nin puanı, sprint toplam puanının yarısından az tutulur. Story'ler yapılacak işlere (task) bölünür. (Board'da mavi item'lar story'leri, kırmızı item'lar task'leri temsil eder.)

- **Daily Scrum:** Sprint 1 boyunca ekip toplantıları yapılmış ve kararlar not edilmiştir. Sprint 2'den itibaren daily scrum'ların zamansal esneklik için Slack/Discord üzerinden sürdürülmesine karar verilmiştir. Sprint 1 toplantı notları:
  - **Toplantı 1 — Tanışma:** Ekip ilk kez bir araya geldi; COP31 temalı fikirler konuşuldu.
  - **Toplantı 2 — Ekip Tanışması:** Ekibin tamamı toplandı; COP31 alanında olası projeler değerlendirildi.
  - **Toplantı 3 — Fikir Üretimi:** Üç fikir tartışıldı (fabrika sürdürülebilirlik skoru / karbon yutakları kapasitesi / doğal-kentsel ekosistem dengesi); karar verilmedi, form dolduruldu.
  - **Toplantı 4 — Derinleştirme:** Üç fikir derinlemesine incelendi, ilham veren firmalar araştırıldı.
  - **Toplantı 5 — Pazar Araştırması:** Benzer şirketler ve fikirler araştırılıp ekip içinde paylaşıldı.
  - **Toplantı 6 — Veri İncelemesi:** Mevcut verinin yetersiz olduğu ve 1 ayda daha fazla veriye ulaşılamayacağı görüldü; herkesin veri uygunluğunu gözeten en az bir fikirle gelmesi kararlaştırıldı.
  - **Toplantı 7 — Proje Kararı:** Teslim tarihi ve veri uygunluğu göz önünde tutularak enerji tasarrufu projesi (Volti) seçildi.

- **Sprint board update:** Sprint 1 ağırlıklı olarak keşif/karar sürecini içerdiğinden çoğu madde "Bitti" durumundadır. *(Board ekran görüntüleri buraya eklenecek.)*

  | İş | Durum |
  |---|---|
  | Ekip kurulumu ve tanışma | ✅ Bitti |
  | Fikir üretimi (3 aday fikir) | ✅ Bitti |
  | Pazar/rakip araştırması | ✅ Bitti |
  | Veri setlerinin incelenmesi ve uygunluk kararı | ✅ Bitti |
  | Proje fikrinin kesinleştirilmesi | ✅ Bitti |
  | Ürün ve roller belgeleme (bu README) | ✅ Bitti |
  | Product Backlog oluşturma | ✅ Bitti |
  | Repo + geliştirme ortamı kurulumu | 🔄 Devam Eden |
  | Londra veri setinin indirilip temizlenmesi | 📋 Yapılacak (Sprint 2) |

- **Ürün Durumu:** Ürün Sprint 1 sonunda "tanımlanmış ve planlanmış" aşamasındadır. Proje fikri kesinleşti, veri kaynağı (Londra akıllı sayaç seti) belirlenip erişilebilirliği doğrulandı, roller ve ürün kimliği belgelendi, backlog oluşturuldu ve repo iskeleti kuruldu. Çalışan bir yazılım çıktısı Sprint 2'de üretilecektir; bu, keşif odaklı ilk sprint için beklenen bir durumdur. *(Ürün ekran görüntüleri Sprint 2'den itibaren eklenecek.)*

- **Sprint Review:**
  Alınan kararlar: Üç aday fikirden, veri uygunluğu ve AI entegrasyonu kriterleriyle Volti seçildi. Veri kaynağı olarak Londra akıllı sayaç seti doğrulandı. Teknik geliştirmenin (veri temizleme + baseline tahmin) Sprint 2'de başlamasına karar verildi. Proje 3 sprintlik olduğu için geliştirme Sprint 2–3'e sıkıştırıldı; canlı fiyat entegrasyonu gibi özellikler "stretch" olarak işaretlendi.
  Sprint Review katılımcıları: Merve Günsay, Senanur Topal, Yasemin Koçbıyık, Reyyan Temel, Betül İrem.

- **Sprint Retrospective:**
  - Fikre karar vermek beklenenden uzun sürdü; veri uygunluğu ilk toplantılarda daha erken kontrol edilmeli.
  - Görev dağılımı sürecin sonuna doğru netleşti; rollerin sprint başında yazılı sabitlenmesine karar verildi.
  - Tahmin puanları gözden geçirilmeli; sprint planlamada developer'ların geri bildirim verdiğine emin olunmalı.
  - Yalnızca 2 geliştirme sprinti kaldığı için, Sprint 2'nin 1. haftası sonunda en küçük çalışan sürümü (temiz veri + baseline tahmin) hedeflemek; gösterişli katmanları sona bırakmak.

---

# Sprint 2
*(Bu sprint henüz başlamadı — tamamlandığında board güncellemeleri, ürün durumu, review ve retrospective buraya eklenecek.)*

**Planlanan hedef:** Temizlenmiş veri + baseline'a karşı ölçülmüş ilk tüketim tahmin modeli + tarife maliyet simülasyonunun ilk sürümü.

---

# Sprint 3
*(Bu sprint henüz başlamadı — projenin son sprinti.)*

**Planlanan hedef:** Yük kaydırma önerisi + anomali tespiti + grounding'li LLM koç katmanı + tüketim/öneri paneli (dashboard) + karbon etkisi + çalışan demo ve sunum.

---

# Teknik Bilgiler

- **Veri Seti:** [Smart Meters in London](https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london) — 5.566 hane, yarım-saatlik tüketim + hava durumu + dinamik (Time-of-Use) tarife (pence/kWh).
- **Teknoloji Yığını:** Python 3.11 · pandas/numpy · LightGBM & Prophet (tahmin) · scikit-learn (anomali) · FastAPI · Streamlit · Anthropic/OpenAI API (LLM koç).
- **Kurulum:**
  ```bash
  git clone https://github.com/<kullanici>/volti.git
  cd volti
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env      # LLM API anahtarınızı girin
  streamlit run app/streamlit_app.py
  ```

---

<p align="center"><b>Voltra</b> · <i>Enerjini boşa harcama — Volti doğru saati fısıldasın. ⚡</i></p>
