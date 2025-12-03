# MusicLeaderboard
A Redis database that stores and ranks information for a music listening app.

## Virtual Environment (Recommended):
python -m venv .venv  
.venv/Scripts/activate      (To activate venv)  
deactivate                  (To deactivate venv)  

## Setup:
pip install -r requirements.txt  
docker run --name music-app-redis-instance -p 6379:6379 -d redis  

## Execution:
python app.py

## In Postman:
GET     http://localhost:6000/api/artist_leaderboard/10  
POST    http://localhost:6000/api/artist_leaderboard/create  
PUT     http://localhost:6000/api/artist_leaderboard/update  
DELETE  http://localhost:6000/api/artist_leaderboard/delete  

## Example format:
{
    "name": "Bobby Stevens",
    "score": 412
}