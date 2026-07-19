## Takım İsmi
Voltra

# Ürün İle İlgili Bilgiler

## Takım Elemanları
- Merve Günsay: Product Owner (ayrıca Frontend – UX/UI katkısı)
- Senanur Topal: Scrum Master (ayrıca Backend geliştirmeye katkı)
- Yasemin Koçbıyık: Team Member / ML & Model Geliştirici
- Reyyan Temel: Team Member / Veri & Backend Geliştirici
- Betül İrem Yardımcı: Team Member / Arayüz & LLM Entegrasyon

## Ürün İsmi
--Volti--

## Ürün Açıklaması
- Volti; bir hanenin veya küçük işletmenin elektrik tüketimini geçmiş akıllı sayaç verisinden öğrenip tahmin eden, dinamik (zamana bağlı) tarifeye göre "neyi ne zaman çalıştırırsan ne kadar tasarruf edersin" diye hesaplayan ve bu önerileri sade, gündelik dille anlatan yapay zekâ destekli bir enerji tasarruf koçudur. Kullanıcının hem elektrik faturasını hem karbon ayak izini düşürmesine somut ve kişiselleştirilmiş önerilerle yardımcı olur. Volti'yi bir veri analizi çalışmasından ayıran şey karar/aksiyon katmanıdır: sadece "tüketimin şöyle" demez, "şimdi ne yapmalısın" der.

## Ürün Özellikleri

- **Tüketim Tahmini** 
— Hane bazında geçmiş veriden öğrenip gelecek dönem elektrik tüketimini öngörür; "bu ay ne kadar harcayacağım?" sorusunu yanıtlar.

- **Dinamik Tarife & Maliyet Analizi** 
— Zamana bağlı tarifeye göre günlük/aylık maliyeti hesaplar, günün en pahalı ve en ucuz saatlerini net biçimde gösterir.

- **Akıllı Yük Kaydırma Önerileri** 
— "Çamaşırı 02:00'de çalıştır, ~X tasarruf et" tarzında, doğrudan uygulanabilir somut aksiyonlar sunar.

- **Anomali & İsraf Uyarısı** 
— Olağandışı yüksek tüketimi yakalar; olası arıza veya boşa harcamayı kullanıcı fark etmeden önce bildirir.

- **Sade Dilli Yapay Zekâ Koçu** 
— Teknik sonuçları herkesin anlayacağı gündelik dile çevirir; yalnızca gerçek verilere dayanır, sayı uydurmaz (grounding).

- **Tasarruf & Karbon Etkisi** 
— Kazancı hem **£ (sterlin)** hem **kg CO₂** olarak gösterir; para tasarrufunu çevresel katkıyla birlikte sunar.

- **Tek Ekran Panel** 
— Tüketim grafiği, öneriler ve koç mesajını tek bir sade arayüzde toplar.

- **Kişiselleştirilmiş Deneyim** 
— Her hane kendi tüketim geçmişine ve profiline göre öneri alır; genel tavsiyeler değil, sana özel içgörüler.

> **Not:** Veri seti Londra'ya ait olduğundan tüm maliyet/tasarruf hesapları **sterlin (£/pence)** cinsindendir (veri setindeki dinamik tarife pence/kWh olarak verilir).

## Hedef Kitle

 **Dinamik Tarifeli Haneler** 
 — Zamana bağlı (Time-of-Use) tarife kullanan ve elektriğin saate göre ucuzlayıp pahalandığını fırsata çevirmek isteyen evler. *(Birincil kitle)*

**Maliyet-Duyarlı Küçük İşletmeler** 
— Kafe, atölye, ofis gibi elektrik gideri yüksek ama enerji uzmanı olmayan işletmeler; faturasını düşürecek net öneriler arar.

**Prosumer Kullanıcılar** 
— Çatı güneş paneli veya elektrikli aracı olan, üretim-tüketim dengesini ve şarj/kullanım zamanlamasını optimize etmek isteyen ileri kullanıcılar.

**Sürdürülebilirlik-Duyarlı Bireyler** 
— Tasarrufu yalnızca para olarak değil, karbon ayak izini azaltma fırsatı olarak da gören çevre bilincine sahip kullanıcılar.

**Dijitale Yatkın Bireyler (18–65)** 
— Bir panel/uygulama üzerinden önerileri takip edip uygulayabilen, teknolojiyle rahat kullanıcılar.

## Product Backlog URL
Ürünün tüm kullanıcı hikâyeleri, öncelikleri (Must/Should/Could) ve puanlarıyla birlikte Trello panomuzda takip edilmektedir:

 https://trello.com/b/Fn8EetTL/volti-proje-geli%C5%9Ftime

> Puanlama: Sprint 1 keşif ve planlama sprintiydi (fikir seçimi, araştırma ve backlog oluşturma). Geliştirme iki sprint'e planlanmıştır — Sprint 2 ≈ 42 puan (veri hazırlığı + tahmin modeli + tarife maliyeti + arayüz iskeleti) ve Sprint 3 ≈ 47 puan (yük kaydırma + LLM koç + gerçek veri entegrasyonu + teslim). Model eğitilirken arayüz iskeleti örnek veriyle paralel kurulduğu için iki sprint dengelidir; Sprint 3'teki Should işleri (anomali, karbon, testler) kapasiteye göre esnektir — önce MVP garanti altına alınır, ekstralar zaman kalırsa eklenir.

---

# Sprint 1

- **Sprint Notu:** Sprint 1 keşif ve karar odaklıydı; hedef, "yeterli veriye sahip, AI entegrasyonu yapılabilir ve 1 ayda (3 sprintte) bitebilir" bir proje seçmekti. Bu hedefe ulaşıldı ve proje **Volti** olarak kesinleşti.

- **Backlog düzeni ve Story seçimleri:** Backlog, ilk yapılacak story'lere göre önceliklendirilmiştir (MoSCoW). Sprint başına tahmin edilen toplam puanı geçmeyecek şekilde sıradan seçimler yapılır; her story'nin puanı, sprint toplam puanının yarısından az tutulur. Story'ler yapılacak işlere (task) bölünür. 

- **Daily Scrum**: Daily Scrum toplantıları slack üzerinden yapılmıştır. Daily Scrum toplantısı görsel kanıtları ve özetleri için: https://github.com/senatopal/yzta_bootcamp_304/tree/52efb3fff4fdad0ca1da9ce5d502d9e7db85f6ad/Sprint%201 

- **Sprint board update:** Sprint 1 süreci slack ve notiondan takip edilmiştir. Slackteki görseller Sprint 1 başlığında Scrum_ olarak yüklenmiştir. Çalışmalarımız ve görevlerimiz notionda bulunuyor:

https://fortunate-infinity-26e.notion.site/GENEL-3897fe6d9df780458100d3ac3d4b7dc6?source=copy_link

Sprint Board Ekran Görüntüleri:

<img width="1920" height="931" alt="Sprint 1 Board" src="https://github.com/user-attachments/assets/f771f1ff-857e-413b-9c73-4f905c7f88da" />

<img width="1920" height="924" alt="Sprint 1 Board 1 1" src="https://github.com/user-attachments/assets/404fe78c-c596-4469-833c-ad690921dc1a" />

<img width="1920" height="922" alt="Sprint 1 Board 2" src="https://github.com/user-attachments/assets/7f10f025-c36c-41fc-ad5b-216e392b99e3" />

<img width="1920" height="923" alt="Sprint 1 Board Trello" src="https://github.com/user-attachments/assets/50381348-bbc8-4d7e-b74f-4560f9c6220f" />

Bundan sonraki görev takibi Trello ağırlıklı ilerleyecektir.

 

- **Ürün Durumu:** Ürün Sprint 1 sonunda "tanımlanmış ve planlanmış" aşamasındadır. Proje fikri kesinleşti, veri kaynağı (Londra akıllı sayaç seti) belirlenip erişilebilirliği doğrulandı, roller ve ürün kimliği belgelendi, backlog oluşturuldu ve repo iskeleti kuruldu. Çalışan bir yazılım çıktısı Sprint 2'de üretilecektir; bu, keşif odaklı ilk sprint için beklenen bir durumdur. 

- **Sprint Review:**
  Alınan kararlar: Üç aday fikirden, veri uygunluğu ve AI entegrasyonu kriterleriyle Volti seçildi. Veri kaynağı olarak Londra akıllı sayaç seti doğrulandı. Teknik geliştirmenin (veri temizleme + baseline tahmin) Sprint 2'de başlamasına karar verildi. Proje 3 sprintlik olduğu için geliştirme Sprint 2–3'e sıkıştırıldı; canlı fiyat entegrasyonu gibi özellikler "stretch" olarak işaretlendi.
  Sprint Review katılımcıları: Merve Günsay, Senanur Topal, Yasemin Koçbıyık, Reyyan Temel, Betül İrem Yardımcı.

- **Sprint Retrospective:**
  - Fikre karar vermek beklenenden uzun sürdü; veri uygunluğu ilk toplantılarda daha erken kontrol edilmeli.
  - Görev dağılımı fikrin geç karar verilmesinden dolayı sürecin sonuna doğru netleşti.
  - Ekibin yeniden takımlaştırılmasından dolayı doğan zaman kaybı daha çok göz önünde bulundurulabilinir.
 

  Projemizi geliştirdikçe, ürünümüzden görüntüler ve bilgiler ekleyeceğiz.
  


# Sprint 2

- **Sprint Notu:** Sprint 2, ilk gerçek geliştirme sprintiydi. Hedef; veriyi kullanılabilir hale getirmek, tahmin modelinin temelini atmak ve arayüz iskeletini paralel kurmaktı. Ayrıca ürünün yönünü sağlamlaştırmak için hedef kitle & UX analizi tamamlandı.

- **Backlog Dağıtma Mantığı:** İşler MoSCoW önceliğine ve beceriye göre dağıtıldı. Veri hattı ve veritabanı Veri/Backend geliştiricide (Reyyan), tahmin modeli ML geliştiricide (Yasemin), arayüz iskeleti arayüz geliştiricide (Betül), persona/UX analizi ve dokümantasyon PO'da (Merve); süreç ve backend desteği Scrum Master'da (Senanur). Model eğitilirken arayüz iskeleti örnek veriyle paralel kuruldu, böylece zaman daha efektif değerlendirildi.

- **Daily Scrum:** Daily scrum'lar Slack, huddle ve whatsapp üzerinden yürütüldü; notlar ve projenin görsel ilerleyişi Notion'da 'Daily Scrum' başlığı altında tutuluyor. Her kişi kendi adına açılmış sayfalara çelaışmalarını eklediler.
  
  🔗 **Daily Scrum & İlerleme Notları (Notion):** https://fortunate-infinity-26e.notion.site/GENEL-3897fe6d9df780458100d3ac3d4b7dc6?source=copy_link
  
  🔗 **Ekip toplantı notları ve görselleri (Slack-huddle-whatsapp):** https://fortunate-infinity-26e.notion.site/EK-P-TOPLANTISI-NOTLARI-3977fe6d9df780c688efc822f4dd11dc?source=copy_link

- **Sprint Board Update:** Görevler Trello'da "Product Backlog → Sprint 2 → Sprint 3 → Stretch → Done" akışında takip ediliyor. Sprint 2'de veri temizleme tamamlandı, arayüz iskeleti temel düzeyde oluşturuldu, persona analizi tamamlandı. (Kişiler kendi kolaylıklarına göre de kartlar eklediler.)
  
  🔗 **Sprint Board (Trello):** https://trello.com/b/Fn8EetTL
  
Sprint Board Ekran Görüntüleri
  <img width="1920" height="882" alt="Volti Proje Geliştime _ Trello ve diğer 7 sayfa - Kişisel - Microsoft​ Edge 19 07 2026 21_00_58" src="https://github.com/user-attachments/assets/a88d5228-9cbe-484a-87a1-f34a4410c86e" />

  <img width="1444" height="866" alt="Volti Proje Geliştime _ Trello ve diğer 9 sayfa - Kişisel - Microsoft​ Edge 19 07 2026 22_22_44" src="https://github.com/user-attachments/assets/0b10a0ee-3c0d-4bad-a12b-41f7b1d449ff" />



- **Ürün Durumu:** Sprint 2 sonunda üründeki gelişmeler:
  Repomuzda ürünün gelişim aşamalarını eklenen dosyalarda yakından takip edebilirsiniz. Bulması daha kolay olsun diye limkleri aşağıda eklendi:

  - Veri hazırlığı: https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/Sprint%202/veri_hazirligi)
  - Veritabanı tasarımı ve kurulumu: https://github.com/senatopal/yzta_bootcamp_304/blob/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/database_design_report.md
  - Backend / API: https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/backend
  - Veri seti (parquet): https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/dataset
  - Arayüz iskeleti (dashboard): https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/dashboard/lib

  **Arayüz Tasarımı (Mockup — geliştirme sürüyor):**

  > Aşağıdaki ekran görüntüleri mevcut tasarım taslağıdır (mockup). Arayüz, Sprint 3'te gerçek veriyle çalışan sürüme dönüştürülecek ve geri bildirimlere göre değişebilir.

  <img width="2618" height="942" alt="image (16)" src="https://github.com/user-attachments/assets/8335a4d1-c272-4e21-9dc0-9e4dea579240" />

  <img width="2652" height="976" alt="image (17)" src="https://github.com/user-attachments/assets/82c00c9e-476d-4f82-a78e-b67077ff6d24" />

  <img width="2622" height="912" alt="image (18)" src="https://github.com/user-attachments/assets/d9cfdee3-464d-47ea-984b-07e69d5830c7" />

  <img width="1472" height="1006" alt="WhatsApp Image 2026-07-12 at 18 20 24 (1)" src="https://github.com/user-attachments/assets/e10c6b1c-cba8-4786-b6f2-08c771701800" />



- **Sprint Review:**
  Tamamlananlar: veri temizleme + birleştirme, veritabanı tasarımı, backend ilk sürümü, arayüz iskeleti, hedef kitle & UX analizi ve ekran tasarımları. Alınan kararlar: tahmin modelinin backend'e entegrasyonu ve gerçek verinin panele bağlanması Sprint 3'e planlandı; video/sunum da Sprint 3'e alındı.

- **Sprint Retrospective:**
  - **İyi giden:** Model hazırlığı ile arayüz iskeleti paralel yürüdü; kimse birbirini beklemedi. Veri hattı ve veritabanı zamanında tamamlandı.
  - **Geliştirilecek:** Model çıktısı ile arayüzün beklediği veri formatı baştan netleştirilmeli (Sprint 3'te entegrasyonu hızlandırmak için).
  - **Aksiyon (Sprint 3):** Önce gerçek veri–panel entegrasyonunu bitirip MVP'yi garantiye almak; anomali, karbon ve canlı fiyat gibi Should/Could işlerini kapasiteye göre eklemek.

---

# Sprint 3

**Planlanan hedef:** Yük kaydırma önerisi + anomali tespiti + grounding'li LLM koç katmanı + tüketim/öneri paneli (dashboard) + karbon etkisi + çalışan demo ve sunum.

---

# Teknik Bilgiler

- **Veri Seti:** [Smart Meters in London](https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london) — 5.566 hane, yarım-saatlik tüketim + hava durumu + dinamik (Time-of-Use) tarife (pence/kWh).


