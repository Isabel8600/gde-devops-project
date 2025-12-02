# ----------------------------------------------------------------------------------
# STAGE 1: Build Image (Alap image)
# Egy vékony (slim) Python image-t használunk alapként a kisebb méret érdekében
FROM python:3.11-slim as base

# Beállítjuk a konténerben használandó környezeti változókat
# A PORT-ot a python kód is használja (8080)
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Beállítjuk a munka könyvtárat, ahova a forráskódot másoljuk
WORKDIR /app

# ----------------------------------------------------------------------------------
# STAGE 2: Függőségek Telepítése
# A függőségek fájlját másoljuk be ELŐSZÖR (ez kihasználja a Docker rétegezést)
COPY requirements.txt .

# Telepítjük a Python függőségeket a requirements.txt alapján
# A --no-cache-dir flag csökkenti a végső image méretét
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------------------
# STAGE 3: Alkalmazás Kódjának Másolása
# Az alkalmazás többi fájlját (app.py, test_app.py, stb.) bemásoljuk a munka könyvtárba
COPY . .

# ----------------------------------------------------------------------------------
# STAGE 4: Konténer Konfigurálása
# Deklaráljuk, hogy a konténer a 8080-as porton figyel (EXPOSE nem nyit portot, csak dokumentál)
EXPOSE ${PORT}

# Meghatározzuk az alap parancsot, ami elindul, amikor a konténer fut
# A Gunicorn egy robusztusabb web szerver, mint a Flask beépített szervere
# Telepítéskor a Flask-kal együtt települ, ha a requirements.txt-be beírjuk (Flask függősége)
# A 'app:app' azt jelenti: app.py modul, app nevű Flask példány
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
#CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
# HA A GUNICORN HIÁNYZIK, EZT HASZNÁLD:
# CMD ["python", "app.py"]
# ----------------------------------------------------------------------------------