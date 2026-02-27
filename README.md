# Soccerway Web Scraping – Match Results Dataset
## Project Overview

This project focuses on web scraping match results from Soccerway to build a structured dataset containing historical soccer match outcomes.

The resulting dataset is designed to support data analysis and machine learning models, particularly for predicting match outcomes (Home Win, Draw, Away Win) without relying on goal counts.

## Objective

* Extract historical match results from Soccerway.
* Clean and structure the data into a machine-learning-ready dataset.
* Store the dataset in CSV format for further analysis and modeling.

## Dataset Structure

The final dataset `(futve_season_results,csv)` is structured as follows:

| season     | competition | phase     | round     | match_id  | match_date               | match_date_local          | home_team | away_team | home_score | away_score | result | source_url |
|------------|------------|-----------|-----------|-----------|--------------------------|---------------------------|-----------|-----------|------------|------------|--------|------------|
| 2002-2003  | Liga FUTVE | Apertura  | Jornada 1 | 67ZAeFqH  | 2002-08-04T20:30:00+00:00 | 2002-08-04T16:30:00-04:00  | Caracas   | Mineros   | 4          | 1          | H      | https://ve.soccerway.com/venezuela/liga-futve-2002-2003/resultados/ |

## Target Variable
The main target variable for machine learning purposes is:
```
result:
- H → Home Win
- D → Draw
- A → Away Win
```

## Ethical Considerations

* This project is for educational and research purposes only.
* Respect Soccerway’s `robots.txt`.
* Avoid sending excessive requests (use rate limiting).