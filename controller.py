import redis

client = redis.Redis(host='localhost', port=6379, decode_responses=True)


def get_top_artists(size):
    return client.zrevrange('artist_leaderboard_followers', 0, size - 1, withscores=True)

def get_artist_by_id(id):
    return client.hgetall(f"artist:{id}")

def get_artist_by_name(name):
    if client.exists(f'name_to_artist_key:{name}') == False:
        return {}
    artist_key = client.hget(f'name_to_artist_key:{name}', 'artist_key')
    artist_data = client.hgetall(artist_key)
    artist_data['id'] = int(artist_key.replace("artist:", ""))
    return artist_data

def add_artist(name, email):
    if client.exists(f'name_to_artist_key:{name}') == True:
        return False
    artist_id = client.incr('next_artist_id')
    artist_key = f'artist:{artist_id}'
    artist_data = {
    'name': name,
    'email': email,
    'listeners': 0,
    'followers': 0,
    'songs': 0,
    'albums': 0
    }
    added_to_artists = client.hset(artist_key, mapping=artist_data) > 0
    added_to_leaderboard = client.zadd('artist_leaderboard_followers', {name: 0}, nx=True) > 0
    added_to_lookup = client.hset(f'name_to_artist_key:{name}', 'artist_key', f'artist:{artist_id}') > 0
    return added_to_artists and added_to_leaderboard and added_to_lookup
    
def update_artist(id, name, email, listeners, followers, songs, albums):
    if client.exists(f'artist:{id}') == False:
        return False
    artist_key = f'artist:{id}'
    old_name = client.hget(artist_key, 'name')
    artist_data = {
    'name': name,
    'email': email,
    'listeners': listeners,
    'followers': followers,
    'songs': songs,
    'albums': albums
    }
    updated_in_artists = client.hset(artist_key, mapping=artist_data) == 0
    removed_from_leaderboard = client.zrem('artist_leaderboard_followers', old_name) > 0
    updated_in_leaderboard = client.zadd('artist_leaderboard_followers', {name: followers}, ch=True) > 0
    removed_from_lookup = client.delete(f'name_to_artist_key:{old_name}') > 0
    updated_in_lookup = client.hset(f'name_to_artist_key:{name}', 'artist_key', artist_key) > 0
    return updated_in_artists and removed_from_leaderboard and updated_in_leaderboard and removed_from_lookup and updated_in_lookup

def follow_artist(name):
    if client.exists(f'name_to_artist_key:{name}') == False:
        return
    client.zincrby('artist_leaderboard_followers', 1, name)

def unfollow_artist(name):
    if client.exists(f'name_to_artist_key:{name}') == False:
        return
    client.zincrby('artist_leaderboard_followers', -1, name)

def remove_artist(name):
    if client.exists(f'name_to_artist_key:{name}') == False:
        return False
    artist_key = client.hget(f'name_to_artist_key:{name}', 'artist_key')
    removed_from_artists = client.delete(artist_key) > 0
    removed_from_leaderboard = client.zrem('artist_leaderboard_followers', name) > 0
    removed_from_lookup = client.delete(f'name_to_artist_key:{name}') > 0
    return removed_from_artists and removed_from_leaderboard and removed_from_lookup