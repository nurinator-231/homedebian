# Home Debian Server

Köhnə kompüter üzərində qurulan şəxsi ev serveri layihəsi.
Məqsəd: ailə/dostlar üçün fayl paylaşma sistemi + Linux/Python öyrənmək.

## Server haqqında

- OS: Debian 13 (Trixie), amd64
- CPU: Intel Atom D525
- RAM: 4 GB DDR3
- Giriş: yalnız ev WiFi-si daxilində (hələlik internetə açıq deyil)

## Qovluqlar

- `docs/` — layihə qeydləri və dərs xülasələri
- `file-server/` — fayl paylaşma proqramının Python kodu (inkişafdadır)
- `configs/` — server konfiqurasiya nümunələri (parollar/tokenlər YOXDUR — əlavə etməzdən əvvəl təmizlənməlidir)
- `scripts/` — köməkçi skriptlər (backup və s.)

## Status

İlkin struktur. Fayl paylaşma proqramı hələ yazılır (Python-un `http.server` modulu ilə başlanılır, sonra Flask-a keçiləcək).
