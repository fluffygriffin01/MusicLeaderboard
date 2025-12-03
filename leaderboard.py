import redis

client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_top_artists(size):
    return client.zrevrange('artist_leaderboard', 0, size - 1, withscores=True)

def add_artist(name, score):
    return client.zadd('artist_leaderboard', {name: score}, nx=True)
    
def update_artist(name, score):
    return client.zadd('artist_leaderboard', {name: score}, xx=True, ch=True)

def remove_artist(name):
    return client.zrem('artist_leaderboard', name)