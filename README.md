# MusicLeaderboard
A Redis database that stores and ranks information for a music listening app.

## Virtual Environment (Recommended):
python -m venv .venv  
.venv/Scripts/activate                  (Activates venv)  

## Setup:
pip install -r requirements.txt  

## Execution:
docker run --name music-app-redis-instance -p 6379:6379 -d redis  
python app.py

## In Postman:
GET     http://localhost:6000/api/artist_leaderboard/10  
POST    http://localhost:6000/api/artist_leaderboard/create  
PUT     http://localhost:6000/api/artist_leaderboard/update  
DELETE  http://localhost:6000/api/artist_leaderboard/delete  

## Example PUT format:
{  
    "id": 1,  
    "name": "Alvin Smith",  
    "email": "alvinsmith@gmail.com",  
    "listeners": 3456,  
    "followers": 235,  
    "songs": 12,  
    "albums": 2  
}  

## Shutdown
ctrl + c                                (Stops the python app)  
deactivate                              (Deactivates venv)  
docker stop music-app-redis-instance    (Stop redis instance)  
docker rm music-app-redis-instance      (Removes redis instance)  