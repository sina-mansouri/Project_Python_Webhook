# Project Python Webhook — Webhook to Database

A Flask-based webhook receiver, secured with HTTP Basic Auth, intended to accept incoming data via POST and store it in a **PostgreSQL** database.

---

## 🚀 Features

- Flask app served via Gunicorn (4 workers)
- HTTP Basic Auth protecting the `/webhook` POST endpoint
- PostgreSQL integration via `psycopg2`
- CSV-to-database import helper (`save_to_db`) — see [Known Issues](#-known-issues--notes)
- Configuration entirely via environment variables (`.env`)

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Framework:** Flask + Gunicorn
- **Database:** PostgreSQL (via `psycopg2-binary`)
- **Containerization:** Docker & Docker Compose

---

## 📦 Getting Started

### Prerequisites

- Docker and Docker Compose
- A reachable PostgreSQL database

### Installation & Running

1. **Clone the repository:**

```bash
git clone https://github.com/sina-mansouri/Project_Python_Webhook.git
cd Project_Python_Webhook
```

2. **Create your environment file:**

```bash
cp .env.example .env
```

Then fill in `.env` with your real values (see [Configuration](#-configuration) below).

3. **Build and start:**

```bash
docker compose up -d --build
```

The webhook listens on port `5000` inside the container. No host port is published by default — see [Known Issues](#-known-issues--notes) if you need to reach it from outside the Docker network.

---

## 🔌 API Endpoints

| Method | Endpoint   | Auth                                              | Description                                                        |
|--------|------------|-----------------------------------------------------|------------------------------------------------------------------------|
| GET    | `/webhook` | none                                                | Simple health-check / confirmation message                            |
| POST   | `/webhook` | Basic Auth (`USERNAME_WEBHOOK` / `PASSWORD_WEBHOOK`) | Intended entry point to receive data and store it in PostgreSQL        |

---

## ⚙️ Configuration

Set via a `.env` file (copied from `.env.example`) — already wired up correctly in both `docker-compose.yaml` (`env_file: ./.env`) and `app/webhook_code.py` (via `python-dotenv` + `os.environ`):

| Variable              | Description                                          |
|------------------------|--------------------------------------------------------|
| `USERNAME_WEBHOOK`     | Basic Auth username required to call `POST /webhook`  |
| `PASSWORD_WEBHOOK`     | Basic Auth password required to call `POST /webhook`  |
| `HOST_DATABASE`        | PostgreSQL host                                       |
| `PORT_DATABASE`        | PostgreSQL port                                       |
| `DATABASE`             | PostgreSQL database name                              |
| `USER_DATABASE`        | PostgreSQL user                                       |
| `PASSWORD_DATABASE`    | PostgreSQL password                                   |

✅ This project already does credential handling correctly — all 7 values are read from the environment via `os.environ`, and once `.gitignore` is added, `.env` stays out of git while only the placeholder `.env.example` is tracked.

---

## 🛑 Stopping

```bash
docker compose down
```

---

## 📂 Project Structure

```
Project_Python_Webhook/
├── app/
│   ├── __init__.py
│   └── webhook_code.py     # Flask app: GET/POST /webhook, DB import helper
├── docker/
│   └── docker-entrypoint.sh
├── persistent/              # Runtime data volume (created at runtime; not tracked in git)
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🐞 Known Issues / Notes

- **`POST /webhook` doesn't actually save anything yet.** The file-upload handling and the call to `save_to_db()` are commented out in `app/webhook_code.py` — the endpoint currently just prints `"OK"` and returns a success message ("*Datei gespeichert und in die Datenbank importiert*") even though nothing was received or stored. Anyone calling this endpoint today gets a false-positive success response.
- **`save_to_db()` uses placeholder column/field names** (`TEST1`, `TEST2`, `Test3`), and there's no SQL schema or migration anywhere in the repo to create the `webhook` table. This function needs both a real table definition and real column names before it can be used.
- **No port is published** in `docker-compose.yaml`. Add a `ports:` mapping (e.g. `"5000:5000"`) under the `python-app` service if you need to reach the webhook from outside the Docker network.
- **`Dockerfile` copies the `app/` folder twice** (`COPY app /code/app/` and `ADD app /code/`) — likely leftover from an earlier layout. Only the first copy is actually used by the current Gunicorn command (`app.webhook_code:app`), so the second `ADD` line can probably be removed.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details. Since this looks like it connects to an internal database/workflow, feel free to swap this for a different license (or drop it) if that fits better.

---

## 👤 Author

**Sina Mansouri**
GitHub: [@sina-mansouri](https://github.com/sina-mansouri)
