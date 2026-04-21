# GreenCart 🛒

> Food waste is a growing crisis. In the United States alone, roughly 30-40% of the food supply is wasted every year, amounting to over 133 billion pounds, and 43% of that waste comes from households. Beyond the financial toll, food waste is one of the leading drivers of landfill methane emissions, which are 29 times more harmful than carbon dioxide. Many individuals, especially college students, busy parents, people shopping with food stamps, and those with dietary restrictions, struggle to understand the shelf life of items they purchase, leading to extra and avoidable expenses. Current solutions tend to focus on either sustainability or budgeting, but not both together. GreenCart brings these two goals into one app. By combining pantry tracking, grocery list planning, expiration monitoring, and food waste analytics, GreenCart helps users make smarter grocery decisions while reducing the environmental and financial impact of food waste. Users can track the remaining shelf life of items in their kitchen, receive reminders before food spoils, and get sustainability recommendations for items that are no longer safely edible. Shop smarter, waste less.

---

## Team Members
- Abigail Rillovick
- Danielle Chen
- Dreshta Boghra
- Nina Mayer
- Alyssa Haidar

---

## Project Links

| Description | Link |
|---|---|
| Phase 3 Design Document | [Link](https://docs.google.com/document/d/1NIn8ppfP6_rEYrqyM73gP4aREB2OysxTGKp-0EbvWcY/edit?usp=sharing) |
| GitHub Repository | [Link](https://github.com/arillovick/26S-Project-WIP) |
| Demo Video | [Link](https://youtu.be/RmgUepFQSus) |

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) with Python 3.11

Create a Python 3.11 environment and install dependencies:

```bash
conda create -n db-proj python=3.11
conda activate db-proj

cd api
pip install -r requirements.txt

cd ../app/src
pip install -r requirements.txt
```

---

## Setup Instructions

**1. Clone the repo**
```bash
git clone <repo-url>
cd <repo-folder>
```

**2. Create your `.env` file**

Copy the template and fill in your values:
```bash
cp api/.env.template api/.env
```

Open `api/.env` and set:
```
SECRET_KEY=<your-secret-key>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=green-cart
MYSQL_ROOT_PASSWORD=<your-password>
```

**3. Start the containers**
```bash
docker compose up -d
```

The app will be available at **http://localhost:8501** and the API at **http://localhost:4000**.

---

## Common Docker Commands

| Command | Description |
|---|---|
| `docker compose up -d` | Start all containers in the background |
| `docker compose down` | Stop and remove containers |
| `docker compose down db -v && docker compose up db -d` | Reset the database (re-runs all SQL files) |
| `docker compose restart` | Restart containers after a code bug |

> **Note:** The `.env` file is never committed to GitHub. Every team member must create their own locally.

> **Note:** When connecting to the database externally (e.g. DataGrip), use port **3200** — the DB is mapped to `localhost:3200`.

---

## Project Structure

```
├── app/              # Streamlit frontend
├── api/              # Flask REST API
├── database-files/   # SQL scripts to initialize the database
├── datasets/         # Raw datasets
└── docker-compose.yaml
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Flask REST API |
| Database | MySQL |
| Infrastructure | Docker |

---

## User Roles

| Role | Description |
|---|---|
| **Ashe** | Ashe is a busy college student who uses GreenCart to track his pantry, plan grocery lists with estimated budgets, and monitor his food waste by category. As a college student juggling classes and a busy schedule, it is easy to overspend on groceries and forget what is already in the fridge, leading to avoidable waste and unnecessary expenses. GreenCart helps him stay on budget, keep track of what he has, and receive reminders before food spoils so that nothing goes to waste. |
| **Bob** | Bob is a father of three and project manager who uses GreenCart to manage his household pantry across multiple storage locations, plan biweekly grocery runs, and track his family's spending by food category. With a busy work and family schedule, it is easy to lose track of what is in the freezer versus the fridge, make duplicate purchases, and go over budget without realizing it. GreenCart helps him stay organized, avoid unnecessary spending, and make sure his family is using what they buy before it expires. |
| **Janice** | Janice is a back-end engineer on GreenCart's platform team who manages the food item database, monitors audit logs for data corruption, and looks up individual user account states to diagnose support tickets. Without proper tooling, tracing when and why data changes is difficult and time consuming. GreenCart gives her full admin controls to keep the platform running smoothly, including the ability to add, update, and delete food items in the global database and view timestamped audit logs to trace any changes made across the system. |
| **Vector** | Vector is a community program coordinator at a local food bank who uses GreenCart to track food waste trends across SNAP recipients and food-insecure households. Without a single view of waste data, it is difficult to prove program impact to funders or identify where intervention is needed most. GreenCart gives him dashboards and analytics to identify where waste is highest, including week-over-week waste trends, spending by food category, and insights into which users are actively engaging with the app so he can follow up with those who have fallen off. |