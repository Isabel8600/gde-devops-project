# gde-devops-project
Együd Izabella K4QQHB beadandója GDE DEVOPS tárgyból


🛠️ GDE B-DEVOPS Beadandó Projekt

Ez a projekt a GDE B-DEVOPS tárgy keretében készült, bemutatva egy egyszerű Python alapú webalkalmazás konténerizálását és a GitLab CI/CD pipeline használatát a Continuous Integration (CI) folyamat megvalósítására.

1. Alkalmazás (app.py)

Programnyelv: Python (Flask web framework)

Lényeg:
Az alkalmazás egy rendkívül egyszerű HTTP szerver, amely a 8080-as porton figyel. Két végpontot definiál:
    /: Alapvető információkat ad vissza JSON formátumban.
    /status: Ez a fő végpont, amely egy HTTP 200 (OK) státuszkóddal válaszol, és tartalmazza a feladat által kért, szabadon választott egyedi üzenetet (GDE B-DEVOPS beadandó KÉSZ).

Unit Test (test_app.py)
A projekt tartalmaz egy darab unit tesztet, amely a Flask beépített tesztkliensét használja. A teszt ellenőrzi, hogy a /status végpont:
    Sikeresen válaszol-e (HTTP 200).
    Tartalmazza-e a meghatározott üzenetet.

2. Dockerfile és Konténerizálás
A Dockerfile felelős a Python kód futtatható Docker image-gé alakításáért.

A Dockerfile lényegi lépései:
    FROM python:3.11-slim: Egy minimalista Python image-et használ alapként, ami csökkenti a végső image méretét.
    WORKDIR /app: Beállítja a munkakönyvtárat a konténer belsejében.
    COPY requirements.txt . / RUN pip install -r requirements.txt: Először bemásolja a függőségek listáját, majd telepíti azokat (Flask, gunicorn). Ez optimalizálja a Docker cache-elését.
    COPY . .: Bemásolja az összes többi kódfájlt (app.py, test_app.py, stb.).
    EXPOSE 8080: Dokumentálja, hogy a konténer a 8080-as porton figyel.
    CMD ["gunicorn", ...]: A gunicorn nevű robusztus webkiszolgálót használja az alkalmazás elindításához a 8080-as porton.

Helyi Build és Futtatás

A Docker image helyi környezetben (ahol futó Docker Daemon/Docker Desktop van) a következő parancsokkal állítható elő és indítható el:

1. Image Előállítása (Build)

Létrehozza a "devops-app" nevű image-et, 1.0 taggel, a jelenlegi könyvtárban lévő Dockerfile alapján.
docker build -t devops-app:1.0 .


2. Konténer Futtatása (Run)

Elindítja az image-et a háttérben (-d)
Átirányítja a konténer 8080-as portját (-p) a helyi gép 8080-as portjára.
Nevezi a konténert "devops-container"-nek.
docker run -d -p 8080:8080 --name devops-container devops-app:1.0


3. Tesztelés (Curl)

curl http://localhost:8080/status


3. CI Pipeline (Continuous Integration)
A CI folyamat a .gitlab-ci.yml fájlban van definiálva, és automatikusan lefut minden kódváltozás (push) esetén.

Stage-ek (Szakaszok)
A pipeline két fő szakaszra van osztva, amelyek csak a megelőző szakasz sikeres befejezése után futnak le:

test --> unit_test_job --> Telepíti a függőségeket, futtatja a unit teszteket (python3 test_app.py). --> Unit-test sikeres futtatása
test --> unit_test_job --> Létrehoz egy test_report.txt nevű fájlt. --> Egy szabadon választható artifact kiadása
build_image --> build_and_push_image --> Belép a GitLab Registry-be, elkészíti a Docker image-et, majd feltölti azt a publikus registrybe. --> Docker image előállítása és feltöltése

A build_and_push_image job logikája
    Login: Bejelentkezés a GitLab Image Registry-be a beépített CI változókkal ($CI_REGISTRY_USER, $CI_REGISTRY_PASSWORD)
    Build: docker build -t $IMAGE_TAG . parancs kiadása a Dockerfile alapján.
    Push: docker push $IMAGE_TAG parancs, amivel a frissen előállított image felkerül a nyilvános GitLab Registrybe (pl. registry.gitlab.com/felhasználó/projekt:SHA).