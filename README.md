# 🎁 Rubrics

![PyPI pyversions](https://img.shields.io/badge/python-3.11-blue)
![License: MIT](https://img.shields.io/github/license/eli64s/readme-ai?color=blueviolet)

---

## 🔗 Quick Links
* [Overview](#-overview)
* [Getting Started](#-getting-started)
* [License](#-license)

---

## 🔭 Overview
***Stack***

FastApi, PostgresSQL, ElasticSearch

---
## 👩‍💻 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

- *Python version 3.11 or higher*
- *Package manager poetry or Docker*

---
### 🚀 Running *RubricsApi*

Using `docker`

```bash
docker compose -f docker-compose-dev.yaml up -d
```

### 📝 Documentation

API documentation will be available after running
[openapi](http://localhost:8000/docs) at http://localhost:8000/docs

---

### 🧪 Tests

Execute the test suite using the command below.

```bash
 docker compose -f docker-compose-tests.yaml up -d &&
 docker compose -f docker-compose-tests.yaml run --rm backend_test sh -c 'pytest'
```

---

## 📄 License

[MIT](https://github.com/eli64s/readme-ai/blob/main/LICENSE)

---
