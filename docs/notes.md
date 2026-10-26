# Home Server Layihəsi — Qeydlər

## Layihə haqqında

Debian 13 (Trixie) işləyən köhnə kompüter (Intel Atom D525, 4GB RAM) ailə/dostlar üçün fayl paylaşma serverinə çevrilir. Əsas məqsəd: Python, Linux və HTTP-ni real layihə üzərində öyrənmək — hazır kod kopyalamadan, addım-addım.

## Server məlumatları

- OS: Debian 13 (Trixie), amd64
- CPU: Intel Atom D525
- RAM: 4 GB DDR3
- Lokal IP: 192.168.1.102
- Gateway: 192.168.1.1
- İnterfeys: ens35
- Playit.gg tunnel: quraşdırılıb, systemd service kimi işləyir (playit.service)
- Minecraft (Paper 1.16.5, Java 16) — test layihəsi idi, hazırkı fokus deyil

## Fayl-paylaşma app tələbləri

- İstifadəçilər: ailə/dostlar, ortaq giriş (parolsuz)
- Funksiya: həm upload, həm download
- Giriş: yalnız ev WiFi-si daxilində (hələlik internetə açıq deyil)

## Öyrənmə mərhələləri

1. Python əsasları (bilinir)
2. Python fayl əməliyyatları (open, pathlib) — **hazırkı mərhələ**
3. HTTP anlayışları (IP, port, request/response, GET/POST)
4. http.server ilə sadə server (Flask-dan əvvəl)
5. LAN fayl-siyahı serveri (baxış/endirmə)
6. Upload funksiyası (POST)
7. Flask-a keçid
8. Home Server-in böyüməsi (silmə, backup, status və s.)

## Dərs 2: Python fayl əməliyyatları — qeydlər

### open() funksiyası və rejimlər

`open("fayl_adı", rejim)` — fayl ilə işləməyə başlamaq üçün istifadə olunur.

- `"w"` (write) — fayl yoxdursa yaradır; varsa **mövcud məzmunu silib yenidən yazır**
- `"r"` (read) — fayl mövcud olmalıdır, olmasa xəta verir
- `"a"` (append) — mövcud məzmunu saxlayır, **sonuna əlavə edir**

### "w" vs "a" fərqi

```python
f = open("test.txt", "w")
f.write("Birinci")
f.close()
# fayl: "Birinci"

f = open("test.txt", "w")   # "w" təmizləyir!
f.write("İkinci")
f.close()
# fayl: "İkinci"  (Birinci silindi)
```

```python
f = open("test.txt", "w")
f.write("Birinci")
f.close()

f = open("test.txt", "a")   # "a" saxlayır, əlavə edir
f.write("İkinci")
f.close()
# fayl: "BirinciİkinciBirinci"
```

`write()` özündən boşluq/yeni sətir əlavə etmir — lazımdırsa `\n` özün yazmalısan.

### with statement

Fayl açıb-bağlamağın təhlükəsiz üsulu:

```python
with open("salam.txt", "w") as fayl:
    fayl.write("Salam, bu mənim ilk faylımdır!")
```

`with` bloku bitən kimi (xəta olsa belə) faylı avtomatik bağlayır — `close()` yazmağa ehtiyac qalmır. Bu, Python-da fayllarla işin standart üsuludur.

## GitHub repo (homedebian) strukturu

```
homedebian/
├── README.md
├── docs/
│   └── notes.md
├── file-server/
├── configs/
└── scripts/
```

`configs/` qovluğuna real fayllar server açılanda SSH ilə köçürülüb əlavə ediləcək (playit.service və digər systemd konfiqurasiyaları) — gizli açar/token-lər təmizləndikdən sonra. Minecraft ilə bağlı fayllar hələlik əlavə edilmir.

## Növbəti addımlar

- Server açılanda: `configs/` üçün real fayl kopyalanması (scp və ya əl ilə), gizli məlumatların təmizlənməsi
- Dərsə davam: Python fayl əməliyyatları (pathlib, qovluqlar) → HTTP anlayışları
- `file-server/` qovluğuna kodu tədricən əlavə etmək

## GitHub-a yerləşdirmə — addım-addım bələdçi

### 1. README.md
Repo-nun "üz qabığı" — nə olduğunu, qovluqların nə mənaya gəldiyini izah edir.

### 2. Git quraşdırılıbmı, yoxla
```
git --version
```
Komputerində Git-in olub-olmadığını göstərir.

### 3. Git-ə özünü tanıt (bir dəfəlik)
```
git config --global user.name "Sənin adın"
git config --global user.email "sənin-emailin@example.com"
```
Hər commit-in kim tərəfindən edildiyini qeyd edir.

### 4. Repo-nu komputerinə klonla
```
git clone https://github.com/istifadəçi-adın/homedebian.git
```

### 5. Bu zip-in içindəkiləri həmin qovluğa çıxar (extract)
Zip-in içindəki bütün fayl/qovluqları klonlanmış `homedebian` qovluğunun içinə köçür (üzərinə yaz).

### 6. ⚠️ Təhlükəsizlik — configs əlavə etməzdən əvvəl
Real server config faylları (playit.service və s.) əlavə edəndə, içindəki gizli açar/token-ləri silib `***GİZLİ***` kimi yer tutucu ilə əvəz et. Yalnız bundan sonra `configs/`-a qoy.

### 7. Dəyişiklikləri bildir
```
git add .
```

### 8. Commit et
```
git commit -m "İlk struktur: docs, file-server, configs, scripts qovluqları"
```

### 9. GitHub-a göndər
```
git push
```

### Xülasə
```
Fayl yarat/dəyiş → git add . → git commit -m "izah" → git push → GitHub-da görünür
```
