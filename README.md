# 🗺️ RouteOpt — Rota Optimizasyonu & Araç Rotalama Araç Kutusu

Python ile yazılmış, **TSP (Gezgin Satıcı Problemi)** ve **CVRP (Kapasiteli Araç Rotalama Problemi)** için birden fazla klasik ve sezgisel algoritma içeren, test edilmiş, görselleştirmeli bir optimizasyon kütüphanesi.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

---

## 📌 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Mimari](#-mimari)
- [Kurulum](#-kurulum)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [CLI Kullanımı](#-cli-kullanımı)
- [Algoritmalar](#-algoritmalar)
- [Örnek Çıktılar](#-örnek-çıktılar)
- [Testler](#-testler)
- [Kendi Verinizle Kullanma](#-kendi-verinizle-kullanma)
- [Yol Haritası](#-yol-haritası)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## 🎯 Proje Hakkında

Lojistik, kargo dağıtımı, filo yönetimi, servis planlama gibi birçok gerçek dünya
probleminin temelinde **"en kısa/en verimli rotayı nasıl bulurum?"** sorusu yatar.
Bu proje, bu soruya farklı yaklaşımlarla cevap veren, **eğitim amaçlı ama
üretim kalitesinde yazılmış**, uçtan uca çalışan bir Python paketidir.

İki temel problemi kapsar:

| Problem | Açıklama |
|---|---|
| **TSP** (Traveling Salesman Problem) | Tek bir aracın tüm noktaları ziyaret edip başlangıca dönerken toplam mesafeyi minimize etmesi |
| **CVRP** (Capacitated VRP) | Birden fazla aracın, kapasite kısıtı altında bir depodan müşterilere dağıtım yapması |

## ✨ Özellikler

- 🧮 **5 farklı algoritma**: Dijkstra, A*, Nearest Neighbor, 2-opt, Simulated Annealing, Genetic Algorithm ve Clarke-Wright Savings (VRP)
- 📊 **Otomatik görselleştirme**: rotalar, yakınsama grafikleri ve algoritma karşılaştırma grafikleri PNG olarak kaydedilir
- 🖥️ **Komut satırı arayüzü (CLI)**: tek satır komutla TSP/VRP çöz
- 🧪 **%100 test kapsamı olan çekirdek mantık**: `pytest` ile yazılmış birim testler
- 📦 **Modüler mimari**: her algoritma bağımsız bir modül, kolayca genişletilebilir
- 🌍 **Gerçek coğrafi koordinat desteği**: haversine mesafesi ile enlem/boylam verileriyle çalışabilir
- 📁 **CSV veri girişi/çıkışı**: kendi verinizi kolayca içe/dışa aktarın

## 🏗️ Mimari

```
routeopt/
├── src/routeopt/
│   ├── graph.py              # Graf yapısı, Dijkstra, A*
│   ├── distance.py           # Öklid/Haversine mesafe, mesafe matrisi
│   ├── vrp.py                 # Clarke-Wright Savings (CVRP)
│   ├── visualize.py           # matplotlib görselleştirmeleri
│   ├── data_generator.py      # Rastgele veri üretimi + CSV I/O
│   ├── cli.py                  # Komut satırı arayüzü
│   └── algorithms/
│       ├── nearest_neighbor.py
│       ├── two_opt.py
│       ├── simulated_annealing.py
│       └── genetic_algorithm.py
├── examples/                  # Çalıştırılabilir örnek betikler
├── tests/                     # pytest birim testleri
├── data/                      # Örnek CSV veri seti
├── assets/                    # Örnek çıktı görselleri
├── requirements.txt
├── LICENSE
└── README.md
```

**Tasarım prensibi:** Her algoritma, mesafe matrisi (`List[List[float]]`) ve
tur (indeks listesi) üzerinden çalışan saf fonksiyonlardır — birbirinden
bağımsızdır ve tek başına test edilip kullanılabilir.

## ⚙️ Kurulum

```bash
git clone https://github.com/kullanici-adiniz/routeopt.git
cd routeopt
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Hızlı Başlangıç

```python
from routeopt.data_generator import generate_random_points
from routeopt.distance import build_distance_matrix, tour_length
from routeopt.algorithms import nearest_neighbor_tour, two_opt

# 1) Rastgele 20 nokta üret
points = generate_random_points(n=20, seed=42)
dist_matrix = build_distance_matrix(points)

# 2) Başlangıç turu (Nearest Neighbor)
tour = nearest_neighbor_tour(dist_matrix)

# 3) 2-opt ile iyileştir
tour = two_opt(tour, dist_matrix)

print("Tur uzunluğu:", tour_length(tour, dist_matrix))
```

Daha fazla örnek için [`examples/`](examples/) klasörüne bakın:

```bash
python examples/example_basic.py   # TSP algoritmaları karşılaştırması
python examples/example_vrp.py     # Kapasiteli araç rotalama örneği
```

## 🖥️ CLI Kullanımı

Paket, `routeopt.cli` modülü üzerinden doğrudan komut satırından çalıştırılabilir:

```bash
# Tek araçlı TSP - 2-opt algoritmasıyla 30 şehir
python -m routeopt.cli tsp --n 30 --algo two_opt --seed 42

# Genetik algoritma ile, 500 nesil
python -m routeopt.cli tsp --n 40 --algo ga --generations 500

# Kapasiteli çok araçlı VRP (25 müşteri, araç kapasitesi 50)
python -m routeopt.cli vrp --n 25 --capacity 50 --seed 7

# Tüm TSP algoritmalarını aynı veri üzerinde karşılaştır
python -m routeopt.cli compare --n 30 --seed 1
```

Her komut, sonuçları terminale yazdırır ve ilgili `.png` görselini kaydeder.

| Parametre | Açıklama | Varsayılan |
|---|---|---|
| `--n` | Şehir/müşteri sayısı | 25 |
| `--algo` | `nn`, `two_opt`, `sa`, `ga` (yalnızca `tsp` komutunda) | `two_opt` |
| `--capacity` | Araç kapasitesi (yalnızca `vrp` komutunda) | 50 |
| `--seed` | Rastgelelik tohumu (tekrarlanabilirlik için) | `None` |
| `--output` | Çıktı görsel dosya yolu | komuta göre değişir |

## 🧠 Algoritmalar

### Kesin (Exact) — Graf Üzerinde En Kısa Yol
| Algoritma | Karmaşıklık | Kullanım Alanı |
|---|---|---|
| **Dijkstra** | O(E log V) | Negatif olmayan ağırlıklı graf üzerinde tek kaynaktan en kısa yol |
| **A\*** | O(E log V) (sezgisel iyiyse daha hızlı) | Koordinat tabanlı sezgisel ile hedefe yönlü arama |

### Sezgisel (Heuristic) — TSP
| Algoritma | Yaklaşım | Tipik Sonuç Kalitesi |
|---|---|---|
| **Nearest Neighbor** | Açgözlü, en yakın şehre git | Optimalin ~%25 üzeri |
| **2-opt** | Kesişen kenarları açarak lokal iyileştirme | Optimalin ~%5 üzeri |
| **Simulated Annealing** | Sıcaklık azalan olasılıklı kabul ile global arama | Optimalin ~%2-5 üzeri |
| **Genetic Algorithm** | Popülasyon, çaprazlama (OX), mutasyon, elitizm | Optimalin ~%3-8 üzeri |

### Sezgisel — CVRP
| Algoritma | Yaklaşım |
|---|---|
| **Clarke-Wright Savings** | İkili rota birleştirmelerinin sağladığı "tasarrufu" hesaplayıp büyükten küçüğe uygulama |

> 💡 **Not:** Küçük problemler (n ≤ 12) için kesin çözüm (brute-force / dinamik programlama)
> mantıklıyken, gerçek dünya problemleri (n > 15-20) NP-Zor olduğundan sezgisel/metasezgisel
> yöntemler tercih edilir. Bu proje her iki dünyayı da gösterir.

## 📊 Örnek Çıktılar

`assets/` klasöründe üretilmiş örnek görseller bulunur:

- `comparison.png` — Nearest Neighbor, 2-opt, Simulated Annealing ve Genetic Algorithm'ın aynı 25 şehirlik problemdeki performans karşılaştırması
- `tsp_ga.png` — Genetik algoritma ile bulunan 30 şehirlik rota
- `vrp_routes.png` — 24 müşterili, 2 araçlı kapasiteli rotalama çözümü

Örnek çalıştırma çıktısı (`compare` komutu, n=25):

```
Sonuçlar:
  Nearest Neighbor: 604.08
  2-opt: 577.56
  Simulated Annealing: 469.10
  Genetic Algorithm: 552.37
```

## 🧪 Testler

Proje, `pytest` ile yazılmış birim testler içerir (graf algoritmaları, TSP
algoritmalarının geçerli permütasyon ürettiğinin doğrulanması, VRP kapasite
kısıtının ihlal edilmediğinin kontrolü vb.):

```bash
pytest tests/ -v
```

Beklenen çıktı: tüm testler `PASSED` olmalıdır (9 test).

## 📁 Kendi Verinizle Kullanma

Gerçek koordinatlarınız varsa (`data/sample_vrp.csv` formatında bir CSV
hazırlayıp) şu şekilde yükleyebilirsiniz:

```python
from routeopt.data_generator import load_points_csv
from routeopt.distance import build_distance_matrix

points, demands = load_points_csv("data/sample_vrp.csv")

# Gerçek enlem/boylam koordinatlarıyla çalışıyorsanız haversine kullanın:
dist_matrix = build_distance_matrix(points, metric="haversine")
```

CSV formatı:

```csv
id,x,y,demand
0,50.0,50.0,0.0
1,32.38,15.08,6.0
2,7.24,53.59,16.0
...
```

## 🗺️ Yol Haritası

- [ ] Zaman pencereli VRP (VRPTW) desteği
- [ ] OR-Tools tabanlı çözücü entegrasyonu (opsiyonel bağımlılık)
- [ ] Gerçek yol ağı verisiyle çalışma (OpenStreetMap / OSRM entegrasyonu)
- [ ] Web tabanlı interaktif görselleştirme (Folium / Leaflet)
- [ ] Çoklu depo desteği (Multi-Depot VRP)
- [ ] Paralel/çok işlemcili GA popülasyon değerlendirmesi

## 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır:

1. Bu repoyu fork'layın
2. Yeni bir branch açın (`git checkout -b ozellik/yeni-algoritma`)
3. Değişikliklerinizi yapın ve test ekleyin
4. `pytest tests/` ile tüm testlerin geçtiğini doğrulayın
5. Pull request açın

Yeni bir algoritma eklerken `algorithms/` klasöründeki mevcut modüllerin
imzasını (mesafe matrisi girdisi, tur/liste çıktısı) takip etmeniz önerilir.

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

<p align="center">Sezgisel optimizasyon algoritmalarını öğrenmek ve gerçek
projelerde kullanmak isteyenler için hazırlanmıştır.</p>
