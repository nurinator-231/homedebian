# Fayl Paylaşma Serveri — başlanğıc versiya

## İşə salmaq

```
python3 server.py
```

Sonra evdəki istənilən cihazdan brauzerdə:

```
http://<server-in-lokal-IP-si>:8000
```

(məsələn `http://192.168.1.102:8000`)

## Nə edir

- `/` — mövcud faylların siyahısı + yükləmə forması
- `/download/<fayl adı>` — faylı endirir
- `/upload` — formadan göndərilən faylı `shared_files/` qovluğuna saxlayır

## Status

Bu, işləyən amma HƏLƏ İZAH OLUNMAMIŞ versiyadır. Dərslərdə bu kodun
hər hissəsi (`http.server`, `BaseHTTPRequestHandler`, request/response,
multipart/form-data və s.) addım-addım təhlil ediləcək ki, bu kodu
tam anlayasan və özün yaza biləcək səviyyəyə gələsən.

## Test edildi

- ✅ Fayl siyahısı göstərmə
- ✅ Fayl yükləmə (upload)
- ✅ Fayl endirmə (download)
