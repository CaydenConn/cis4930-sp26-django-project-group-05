# Project 3: Web Development Project

## Description
This Django web application explores a dataset of movies sourced from IMDb, continuing the analysis begun in Projects 1 and 2. The app allows users to browse, search, and manage movie records through a full CRUD interface, view live weather data for Florida cities fetched from a public API, and explore an analytics dashboard with aggregated insights such as genre revenue breakdowns and budget-vs-gross comparisons.

## Application Features

| Page / View | Route | Description |
|---|---|---|
| **Homepage** | `/` | Dashboard showing total movie and genre counts, quick navigation links, and a "Recently Added" card listing the five newest movies. |
| **Movie List** | `/records/` | Paginated table (20 per page) of all movies displaying title, year, genre, rating, and score with links to edit or delete each entry. |
| **Movie Detail** | `/records/<id>/` | Full detail view for a single movie including director, writer, star, country, budget, gross, runtime, and computed profit. |
| **Add Movie** | `/records/add/` | Form to create a new movie record with validation (year range, score 0–10, genre foreign key selection). |
| **Edit Movie** | `/records/<id>/edit/` | Pre-populated form to update an existing movie's fields. |
| **Delete Movie** | `/records/<id>/delete/` | Confirmation page before permanently removing a movie from the database. |
| **Weather List** | `/weather/` | Paginated table of weather records for five Florida cities (Jacksonville, Miami, Orlando, Tampa, St. Petersburg) showing date, temperatures, UV index, and precipitation. |
| **Weather Detail** | `/weather/<id>/` | Single-record view with full weather details including sunrise, sunset, and rain totals. |
| **Fetch Weather Data** | `/fetch/` | Staff-only POST endpoint that triggers the `fetch_data` management command to pull fresh forecasts from the Open-Meteo API and store them in the database. |
| **Analytics Dashboard** | `/analytics/` | Data-driven dashboard built with Chart.js featuring: summary statistics (count, mean, min, max) for score, gross, and runtime; a pie chart of movies by MPAA rating; a bar chart of average gross revenue by genre (top 10); a scatter plot of budget vs. gross (top 100 movies); a table of average R-rated movie scores by year; and a table of average ROI by country (top 10). |

## Group Members and Contributions
### Cayden Conn: cbc22b
- 2.1
- 2.4
- README
### Nicholas Marciniak: nem22c
- 2.2
- 2.3
- README
### Judah Alter: jaa22h
- 2.4
- 2.6
### Ben Ashir Georges:bsg22a
- 2.5

### API Documentation:
https://open-meteo.com/en/docs

### Data Set:
https://www.kaggle.com/datasets/danielgrijalvas/movies

### Startup Instructions:
- Clone the repository `git clone {link}`
- Run a virtual environment
- `pip install -r requirements.txt`
- `python manage.py migrate`
- `python manage.py seed_data`
- `python manage.py fetch_data`
- `python manage.py runserver`
- Open the application at `http://127.0.0.1:8000/`

<img width="1881" height="880" alt="image" src="https://github.com/user-attachments/assets/e8ee9ff6-dd7b-422c-93bb-41fc95fc6188" />

<img width="1910" height="903" alt="image" src="https://github.com/user-attachments/assets/836a2fbe-a618-47d3-9d5f-d13785fab395" />

<img width="1909" height="892" alt="image" src="https://github.com/user-attachments/assets/7fe59a14-35d4-4bee-8385-df128bbb45e7" />
