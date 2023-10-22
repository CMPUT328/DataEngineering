# Elo Ranking Methodology

The present study aims to estimate the strength of teams participating in tournaments, and subsequently the strength of the tournaments themselves, using the well-established Elo ranking system. The methodology employed in processing, transforming, and analyzing the gameplay data is outlined below.

## 1. Data Retrieval

- Initial data was sourced from `tournaments.json`.
  - `teams`: Two team IDs participating in the game.
  - `winner`: ID of the winning team.
  - `league`: ID of the league under which the game was played.
  - `tournament`: ID of the tournament.
  - `section`: Section (e.g., "Group A") of the game.
  - `startDate`: Start date of the game.

## 2. Elo Rating for Teams

- Each team received an Elo rating based on game performance.
  - Initial rating for all teams: 1000
  - Expected outcome was calculated for both teams.
  - Ratings were updated post-game.
  - K-factor values varied based on league and section.

## 3. Tournament Strength Calculation

- Tournament strength was calculated by averaging the Elo ratings of all participating teams.

## 4. Elo Rating Based on Tournament Strength

- Elo ranking was re-initiated with the tournament strength metric.
  - Teams initialized with scores from their tournament history.
  - Expected outcome recalculated for each game.
  - K-factor values varied based on tournament and section.

## 5. Global Rankings

- A global power ranking order was established from the Elo ratings.
  - Ranking was exported on a table on Amplify.

## 7. Tournament rankings and Team Rankings

- The routnament rankings and team rankings are derived from the global ranking in React.

  
In conclusion, this methodology offered a comprehensive analysis of team and tournament strengths, giving stakeholders an all-encompassing ranking system that encapsulates the multifaceted nature of competitive gameplay.

