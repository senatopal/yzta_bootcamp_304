
<img width="1536" height="572" alt="yazılı volti logo" src="https://github.com/user-attachments/assets/d9a6d709-ce5a-42a3-8b4b-196774f1e9ac" />


## Takım İsmi
VOLTRA

# Ürün İle İlgili Bilgiler

### Takım Rolleri

| İsim | Rol | İletişim |
|---|---|---|
| Merve Günsay | Product Owner & Frontend (UX/UI) | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/merve-gunsay/) |
| Senanur Topal | Scrum Master & Backend | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/senanur-topal-77ab7b254/) |
| Yasemin Koçbıyık | ML & Model Geliştirici | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/yasemin-kocbiyik/) |
| Reyyan Temel | Veri & Backend Geliştirici | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/reyyan-temel-845258219/) |
| Betül İrem Yardımcı | Frontend & LLM Entegrasyon | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/bet%C3%BCl-irem-yard%C4%B1mc%C4%B1-aa17a2217/) |


## Ürün İsmi
**Volti**

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
— Teknik sonuçları herkesin anlayacağı gündelik dile çevirir; yalnızca gerçek verilere dayanır, sayı uydurmaz.

- **Tasarruf & Karbon Etkisi** 
— Kazancı hem **£ (sterlin)** hem **kg CO₂** olarak gösterir; para tasarrufunu çevresel katkıyla birlikte sunar.

- **Tek Ekran Panel** 
— Tüketim grafiği, öneriler ve koç mesajını tek bir sade arayüzde toplar.

- **Kişiselleştirilmiş Deneyim** 
— Her profil kendi tüketim geçmişine ve planlarına göre öneri alır; genel tavsiyeler değil, kişiye özel içgörüler.

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
  Repomuzda ürünün gelişim aşamalarını eklenen dosyalarda yakından takip edebilirsiniz. Bulması daha kolay olsun diye linkleri aşağıda eklendi:

  - [Veri hazırlığı](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/Sprint%202/veri_hazirligi)
  - [Veritabanı tasarımı ve kurulumu](https://github.com/senatopal/yzta_bootcamp_304/blob/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/database_design_report.md)
  - [Backend / API](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/backend)
  - [Veri seti (parquet)](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/dataset)
  - [Arayüz iskeleti (dashboard)](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/dashboard/lib)
    
  **Arayüz Tasarımı (Mockup geliştirme sürüyor):**

  > Aşağıdaki ekran görüntüleri mevcut tasarım taslağıdır (mockup). Arayüz, Sprint 3'te gerçek veriyle çalışan sürüme dönüştürülecek ve geri bildirimlere göre değişebilir.

  <img width="2618" height="942" alt="image (16)" src="https://github.com/user-attachments/assets/8335a4d1-c272-4e21-9dc0-9e4dea579240" />

  <img width="2652" height="976" alt="image (17)" src="https://github.com/user-attachments/assets/82c00c9e-476d-4f82-a78e-b67077ff6d24" />

  <img width="2622" height="912" alt="image (18)" src="https://github.com/user-attachments/assets/d9cfdee3-464d-47ea-984b-07e69d5830c7" />

  <img width="1472" height="1006" alt="WhatsApp Image 2026-07-12 at 18 20 24 (1)" src="https://github.com/user-attachments/assets/e10c6b1c-cba8-4786-b6f2-08c771701800" />



- **Sprint Review:**
  Tamamlananlar: veri temizleme + birleştirme, veritabanı tasarımı, backend ilk sürümü, arayüz iskeleti, hedef kitle & UX analizi ve ekran tasarımları.
  Alınan kararlar: tahmin modelinin backend'e entegrasyonu ve gerçek verinin panele bağlanması Sprint 3'e planlandı; video/sunum da Sprint 3'e alındı.
  Sprint Review katılımcıları: Merve Günsay, Senanur Topal, Yasemin Koçbıyık, Reyyan Temel, Betül İrem Yardımcı.


- **Sprint Retrospective:**
  - **İyi giden:** Model hazırlığı ile arayüz iskeleti paralel yürüdü; kimse birbirini beklemedi. Veri hattı ve veritabanı zamanında tamamlandı.
  - **Geliştirilecek:** Model çıktısı ile arayüzün beklediği veri formatı baştan netleştirilmeli (Sprint 3'te entegrasyonu hızlandırmak için).
  - **Aksiyon (Sprint 3):** Önce gerçek veri–panel entegrasyonunu bitirip MVP'yi garantiye almak; anomali, karbon ve canlı fiyat gibi Should/Could işlerini kapasiteye göre eklemek.

---

# Sprint 3

- **Sprint Notu:** Sprint 3, ürünün son kullanıcıya gösterilecek hale getirildiği sprint oldu. Hedef; Sprint 2'de kurulan tahmin modeli ve arayüz iskeletini gerçek veriyle birleştirmek, yük kaydırma önerisi ve anomali tespitini panele bağlamak, LLM tabanlı koç katmanını grounding'li şekilde devreye almak ve ürünü pazarlama/SEO açısından son haline getirmekti.

- **Backlog Dağıtma Mantığı: Sprint 3'te öncelik, ürünü son haline getirip canlıya almaktı. İşler yine beceriye göre dağıtıldı: arayüz tamamlanması Betül'de; veri setinin genişletilmesi, temizlenmesi ve modele aktarılması Reyyan ve Yasemin'de; ürünün canlıya alınma çalışmaları Senanur'da yürütüldü. Arayüz testi, sprintin kapanışı için tanıtım videosu ve README dokümantasyonu Merve tarafından hazırlandı. Ürünün tamamlanması için yapılması gerekilen ve yeni planlanan görevler zaman kısıtı göz önünde bulundurularak sıralandı ve trelloda öncelik takibi sağlanarak ilerlendi.
 
- **Daily Scrum:** Daily scrum'lar Slack, huddle ve WhatsApp üzerinden yürütüldü; notlar ve projenin görsel ilerleyişi Notion'da 'Daily Scrum' başlığı altında tutulmaya devam edildi.

  🔗 **Daily Scrum & İlerleme Notları (Notion):** https://fortunate-infinity-26e.notion.site/GENEL-3897fe6d9df780458100d3ac3d4b7dc6?source=copy_link
  🔗 **Ekip toplantı notları ve görselleri (Slack-huddle-whatsapp):** https://app.notion.com/p/EK-P-TOPLANTISI-NOTLARI-3977fe6d9df780c688efc822f4dd11dc?source=copy_link

- **Sprint Board Update:** Görevler Trello'da "Product Backlog → Sprint 2 → Sprint 3 → Done" akışında takip edilmeye devam edildi. Sprint 3'te gerçek veri–panel entegrasyonu, yük kaydırma önerisi, anomali tespiti ve LLM koç katmanı tamamlandı. Arayüz tasarımı revizeleri ayrı kartta takip edildi. Öncelik sırasında en üstte gelen görevlerin tamamlanmasına özen gösterildi, kalan zamanda yeşil etiketli planlamalar değerlendirildi.

  🔗 **Sprint Board (Trello):** https://trello.com/invite/b/6a4a912914a9f05fbfc01f49/ATTI0db497b4a727e1df105d043d01a7b763620E97A8/volti-proje-gelistime

  Sprint Board Ekran Görüntüleri
  
 <img width="1920" height="1020" alt="Volti Proje Geliştime _ Trello ve diğer 9 sayfa - Kişisel - Microsoft​ Edge 28 07 2026 22_29_14" src="https://github.com/user-attachments/assets/3b27cd74-341a-40b5-b6e7-68e79bc141ab" /> 

<img width="1881" height="905" alt="Ekran görüntüsü_29-7-2026_20470_trello com" src="https://github.com/user-attachments/assets/0fbb0db1-2ff0-41bd-955e-3dca8644bdbd" />

<img width="1894" height="910" alt="Ekran görüntüsü_29-7-2026_205147_trello com" src="https://github.com/user-attachments/assets/a4beacdb-833c-460c-97f9-663edf97abc5" />


<img width="1901" height="899" alt="trello" src="https://github.com/user-attachments/assets/f5ec5ce3-2d5f-49fd-9a3a-cc2510518a6c" />


**Ürün Durumu:** Sprint 3 sonunda üründeki gelişmeler: Web sitemiz Home - Dashboard - How It Works - About sayfalarından oluşmaktadır. Aşağıda her bir sayfanın görseli mevcuttur.

**Home**
<img width="1763" height="1664" alt="image" src="https://github.com/user-attachments/assets/3dd8b1f6-d908-4061-8182-4d736c78ac89" />


**Dashboard_1**
<img width="1026" height="455" alt="Ekran görüntüsü_2-8-2026_22429_www canva com" src="https://github.com/user-attachments/assets/c52bc6c1-18ad-445c-8b9f-c32f219264ee" />

**Dashboard_2**
<img width="1280" height="721" alt="WhatsApp Image 2026-08-01 at 21 44 23" src="https://github.com/user-attachments/assets/362e6474-14c1-4dba-b61f-d6bd01840fd9" />

**Dashboard_3**
 <img width="1280" height="720" alt="WhatsApp Image 2026-08-01 at 21 50 27 (1)" src="https://github.com/user-attachments/assets/75ec8998-ff2f-49cc-bf04-1228dd1f1dfd" />

**Dashboard_4**
<img width="1280" height="727" alt="WhatsApp Image 2026-08-01 at 21 50 46 (1)" src="https://github.com/user-attachments/assets/2f695ca7-105a-4e01-9a33-31f9345c2442" />

**Dashboard_5**
<img width="1280" height="725" alt="WhatsApp Image 2026-08-01 at 21 51 16 (1)" src="https://github.com/user-attachments/assets/61334618-d283-41a7-a79a-bdad3c9f73f6" />

**Dashboard_6**
<img width="1280" height="468" alt="WhatsApp Image 2026-08-01 at 21 53 00 (1)" src="https://github.com/user-attachments/assets/78e31556-a6c5-4458-b0b3-3d6262678b33" />

**Dashboard_7**
<img width="1280" height="725" alt="WhatsApp Image 2026-08-01 at 21 53 19 (1)" src="https://github.com/user-attachments/assets/29a35732-a255-43e9-874f-5b682006ca12" />

**How It Works**
<img width="1763" height="2447" alt="image" src="https://github.com/user-attachments/assets/b6928018-dc41-45ef-b39b-756c34477f05" />

**About**
<img width="1763" height="2007" alt="image" src="https://github.com/user-attachments/assets/45f17e37-7127-4f3a-be94-c6abd527e220" />



- **Ana Sayfa** — Hero bölümü, "Why Volti?" fayda kartları (Save money / Take one clear action / Use greener energy), 3 adımlı "How It Works" özeti ve gerçek dashboard önizlemesi (Best action today kartı + Hourly energy breakdown grafiği) eklendi.
  - **How It Works Sayfası** — Kullanıcı odaklı, 3 adımlık detaylı anlatım (Connect → Analyse → Act) ve "Built for homes and small businesses" bölümü ile güncellendi.
  - **Dashboard** — Tüketim tahmini, kişiselleştirilmiş öneriler (Personalised recommendations), anomali tespiti (Consumption anomalies), saatlik tüketim dağılımı (Hourly energy breakdown), 24 saatlik tahmin (Next 24-hour forecast) ve tüketim geçmişi (Consumption history) grafiklerini içeren, gerçek veriyle çalışan tam işlevsel panel tamamlandı. Planlanan kullnaıcı dostu AI featuresi eklendi. Kullanımın kolaylaşması ve dashboardların daha kolay anlaşılması için Quick Tour eklendi.

  _

  🔗 **Repo / kod linkleri:** Buradaki linkler ve daha fazlası repomuzda public bir şekilde bulunmakta. İncelerken kolaylık sağlanması için bazı linkleri aşağıda sıraladık:
  
  - [Veri hazırlığı](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/Sprint%202/veri_hazirligi)
  - [ML Modeli](https://github.com/senatopal/yzta_bootcamp_304/tree/dce39bb02211cb5fc92cabd0716c238f1371d84e/src)
  - [Veritabanı tasarımı ve kurulumu](https://github.com/senatopal/yzta_bootcamp_304/blob/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/database_design_report.md)
  - [Backend / API](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/backend)
  - [Veri seti (parquet)](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/dataset)
  - [Arayüz iskeleti (dashboard)](https://github.com/senatopal/yzta_bootcamp_304/tree/0cf46afef680cf4bc4bd82e91a6374983ae7c5f6/dashboard/lib)

- **Sprint Review:**
  Tamamlananlar: Ürünümüzün web sitesi tamamlandı. Web sitesi kullanıcı odaklı analiz edilerek yeniden düzenlendi.Gerçek veri–panel entegrasyonu, anomali tespiti, LLM koç katmanı görevleri tamamlandı. Ürünümüzün canlıya alma çalışmaları yapıldı. Araştırmalarımız sonucu 15 dakikalık sürelerle ürünün canlıda kalmasını sağlayan araç denendi fakat kısıtlı süresi nedeniyle kullanım açısında işe yaramadı.
  Alınan Kararlar: Ürünü sürekli bir biçimde canlıda tutmak için ücretsiz bir araç bulunamadı. Bootcamp sürecinde ücretli araçların kullanımı önerilmediği için ücretli araç kullanılmamasına karar verildi. Ürünün bütün detaylarıyla incelenebilmesi için bütün web sayfalarının README'ye eklenmesine karar verildi.
  İlerleyen süreçlerde kullanıcı açıısndan daha efektif bir biçimde ürünü kullanabilmesi için ürünün mobil versiyonu çalışmaları yapılabilinir diye konuşuldu.
  Sprint Review katılımcıları: Merve Günsay, Senanur Topal, Yasemin Koçbıyık, Reyyan Temel, Betül İrem Yardımcı.

- **Sprint Retrospective:**
  - **İyi giden:** Voltra ekip üyeleri sürece daha geç başlamalarına rağmen, her bir ekip üyesi almış olduğu sorumluluğu hiçbir zorluk çıkarmadan yerine getirmiştir. Bu süreçte ekip içerinde sık iletişimde kalarak, haftada en az iki ün ekip toplantısı yaparak süreci planlanan şekilde ilerletebildik. Bootcamp sürecinde hem öğrenip hem de birbirimize öğrettiğimiz süreç sonucunda istediğimiz ürünü çıkarabildik.
  - **Geliştirilecek:** Hedef kitlemizin ürünümüzü daha kolay benimsemesi ve daha kolay kullanabilmesi için mobil çalışması da yapmayı düşünüyoruz.
  - **Aksiyon (sonraki adımlar):** Hedef kitle analizlerinin sonucunda web sitemizi oluştururken aynı zamanda rakiplerimizi de daha yakından tanıma fırsatı elde ettik. İlerleyen sürçlerde bu araştırmaları daha da derinleştirerek bizi rakiplerden daha çok öne geçirecek özellikler kazandırmaya çalışacağız ürünümüze. Data setini kullandığımız Londra haneleri dışında, daha başka marketler arayışı içerinde bulunmayı da planlarımız arasına dahil ettik.

---

# Teknik Bilgiler

- **Veri Seti:** [Smart Meters in London](https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london) — 5.566 hane, yarım-saatlik tüketim + hava durumu + dinamik (Time-of-Use) tarife (pence/kWh).


