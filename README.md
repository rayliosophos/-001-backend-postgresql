# 📋 BackEnd (FastAPI) and PostgreSQL

![Python](/doc/badges/python.svg)
![FastAPI](/doc/badges/FastAPI.svg)
![Pytest](/doc/badges/pytest.svg)
![Postgres](/doc/badges/postgres.svg)
![JWT](/doc/badges/JWT-black.svg)
![Docker](/doc/badges/docker.svg)
![Swagger](/doc/badges/swagger.svg)
![Nginx](/doc/badges/nginx.svg)
![Red Hat](/doc/badges/redhat.svg)
![GitLab](/doc/badges/gitlab.svg)
![SonarQube](/doc/badges/SonarQube-black.svg)

---

## ⚙️ Installation

```bash
pip install "fastapi[standard]"
```

## 📋 Project Management

| NO | Task | Dev By | D.Start | D.End | Status |
| - | - | - | - | - | - | 
| 1 | System architecture and security design | Saray | 01/01/26 | ... | ✅ |

## 🔬 Technologies:

| # | Technology | Active |
| - | - | - |
| 1 | [FastAPI](https://fastapi.tiangolo.com) | ✅ |
| 2 | [PostgreSQL](https://www.postgresql.org) | ✅ |
| 2 | [Docker](https://www.docker.com) | ✅ |
| 2 | [Redhat](https://www.redhat.com) | ✅ |
| 2 | [Nginx](https://nginx.org) | ✅ |
| 3 | `LDAP` | ✅ |
| 3 | `Pytest` | ✅ |
| 5 | `JWT` | ✅ |
| 12 | `Audit` | ✅ |
| 13 | `Log` | ✅ |
| 14 | `Rate Limit` | ✅ |

## 📋 List Rest API

| # | URL | Type | Description | Active |
| - | - | - | - | - |
| 1 | 127.0.0.1:8080/api/v1/authorization/token | `POST` | Login | ✅ |

## 🔬 Scan Sonarqube

## 🐳 Deploy Docker Backend

```bash
docker compose -f docker\docker-compose.yml up -d
docker exec -it postgres psql -U tday -d postgres
CREATE DATABASE backend_db
ALTER DATABASE backend_db OWNER TO tday;
```

## 🏆 Interface