# JodWai - Personal Finance & Mood Tracker App

A web application for tracking income, expenses, and personal mood using Streamlit and PostgreSQL.

---

## Key Features

- Record income and expenses with summaries over selected date ranges
- User account system (register and login)
- Mood tracking with Thai language Sentiment Analysis model
- Reports and trends of mood sentiments over time
- Shared expense tracking for trips (Han Tao!)

---

## Technology Stack

- Python 3.x
- Streamlit
- PostgreSQL (via Docker)
- psycopg2 (PostgreSQL connector)
- transformers (Thai Sentiment Analysis model)
- Docker and Docker Compose

---

## Installation and Usage

### 1. Prepare Docker and Database

- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Run the command to start PostgreSQL and pgAdmin containers:

```bash
docker-compose up -d
````

* Wait about 10 seconds to ensure the database is ready

---

### 2. Setup Python Environment and Install Dependencies

#### On macOS/Linux:

```bash
chmod +x run_setup.sh
./run_setup.sh
```

#### On Windows:

Run the batch script in Command Prompt or by double-clicking:

```bat
run_setup.bat
```

---

## Database

* `account` table for user information
* `expense` table for income and expense records
* `hantao_friend` table for tracking shared trip expenses
* `diary` table for mood journal entries with sentiment analysis

Tables are created automatically from the SQL scripts located in the `initdb` folder when the Docker containers start.

---

## Important Files

* `app.py` — Main Streamlit application code
* `docker-compose.yml` — Docker configuration for PostgreSQL and pgAdmin
* `initdb/init.sql` — SQL script to create database tables
* `requirements.txt` — Python dependencies
* `run_setup.sh` / `run_setup.bat` — Scripts to setup environment and install dependencies

---

## Notes

* Update the database connection settings in `app.py` if needed (host, port, user, password)
* Make sure the Docker ports specified in `docker-compose.yml` are available and accessible
* The app uses a Thai Sentiment Analysis model from HuggingFace: `poom-sci/WangchanBERTa-finetuned-sentiment`

---

## Contact

If you have any questions or issues, feel free to contact \[Your Email] or open an issue on GitHub.

---

Thank you for using JodWai! 🙏
