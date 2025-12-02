import redis

client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_top_ten_artists():
    client.zadd('artist_leaderboard', {'Bob Bobson': 234})
    return client.zrevrange('artist_leaderboard', 0, 9, withscores=True)

def add_artist(name, score):
    client.zadd('artist_leaderboard', {name: score})


# pip install redis    
# pip install Flask
# docker run --name music-app-redis-instance -p 6379:6379 -d redis