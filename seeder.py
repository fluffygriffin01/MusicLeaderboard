# import controller
# import threading
# import time
# import random
# from faker import Faker

# #Simulate number of users interacting
# THREADS_AMOUNT = 4
# SIMULATION_DURATION = 20 #runtime in seconds
# fake = Faker()

# def generate_artist():
#     name = fake.name()
#     email = fake.email()

#     return {"name": name, "email": email,}

# def seed_artists(count): #return how many artists succesfully added in leaderboard
#     added_amount = 0
#     for _ in range(count):
#         artist_info = generate_artist()
#         added_artist = controller.add_artist(artist_info['name'], artist_info['email'])
#         if added_artist == True:
#             added_amount += 1
#     return added_amount

# def simulate_app_traffic(duration):
#     time_simulating = 0
#     while time_simulating < duration:
#         artist = None
#         try:
#             artist = random.choice(controller.get_top_artists(random.randint(100, 200)))
#         except IndexError:
#             artist = None
#         rng = random.random()

#         if artist is not None:
#             if rng > 0.8:
#                 controller.remove_artist(artist[0])
#             elif rng > 0.6:
#                 controller.unfollow_artist(artist[0])
#             elif rng > 0.4:
#                 controller.follow_artist(artist[0])
#         else:
#             artist_info = generate_artist()
#             controller.add_artist(artist_info['name'], artist_info['email'])

#         delay = random.uniform(0.01, 1) #delay to mimic real timing.
#         time.sleep(delay)
#         time_simulating += delay

# def main():
#     print(f'Simulating app traffic...')
#     seed_artists(1) # add minimum of 1 artist to leaderboard.
#     threads = []  
#     for _ in range(THREADS_AMOUNT):
#         thread = threading.Thread(target=simulate_app_traffic, kwargs={"duration": SIMULATION_DURATION})
#         threads.append(thread)
#         thread.start()

#     for t in threads:
#         t.join()

#     print('Finished simulating traffic')

# if __name__ == "__main__":
#     main()


import controller
import threading
import time
import random
from faker import Faker
import requests   # NEW  using actual API requests


API_BASE = "http://localhost:6000"

def api_create_artist(name, email):
    return requests.post(
        f"{API_BASE}/api/artist/create",
        json={"name": name, "email": email}
    )

def api_follow_artist(name):
    return requests.put(
        f"{API_BASE}/api/artist/follow",
        json={"name": name}
    )

def api_unfollow_artist(name):
    return requests.put(
        f"{API_BASE}/api/artist/unfollow",
        json={"name": name}
    )

def api_delete_artist(name):
    return requests.delete(
        f"{API_BASE}/api/artist/delete",
        json={"name": name}
    )

def api_get_top_artists(size):
    return requests.get(
        f"{API_BASE}/api/artist/leaderboard",
        json={"size": size}
    )



#Simulate number of users interacting
THREADS_AMOUNT = 4
SIMULATION_DURATION = 20 #runtime in seconds
fake = Faker()


def generate_artist():
    """Generate random artist data"""
    name = fake.name()
    email = fake.email()

    return {"name": name, "email": email}


def seed_artists(count):
    """Seed initial artists — now using API calls"""
    added_amount = 0
    for _ in range(count):
        artist_info = generate_artist()

    

        # NEW — API CALL
        res = api_create_artist(artist_info['name'], artist_info['email'])
        if res.status_code == 200:
            added_amount += 1

    return added_amount


def simulate_app_traffic(duration):
    """Simulates random follow/unfollow/delete/user creation events using API requests"""
    time_simulating = 0

    while time_simulating < duration:
        artist = None

       
        # NEW: calling API to get leaderboard
        size = random.randint(1, 50)
        leaderboard_res = api_get_top_artists(size)
        
        if leaderboard_res.status_code == 200:
            try:
                leaderboard_data = leaderboard_res.json()
                if isinstance(leaderboard_data, list) and len(leaderboard_data) > 0:
                    # Artist names come as ["Artist Name", score]
                    artist = random.choice(leaderboard_data)
            except:
                artist = None
        else:
            artist = None

        rng = random.random()

        if artist is not None:
            artist_name = artist[0]  

            if rng > 0.95:
                # OLD — controller.remove_artist(artist_name)
                api_delete_artist(artist_name) 
        

            elif rng > 0.6:
                # OLD — controller.unfollow_artist(artist_name)
                api_follow_artist(artist_name)

            elif rng > 0.3:
                # OLD — controller.follow_artist(artist_name)
                api_unfollow_artist(artist_name)

        else:
            artist_info = generate_artist()

            # OLD — controller.add_artist(artist_info['name'], artist_info['email'])
            api_create_artist(artist_info['name'], artist_info['email'])

        # Delay to mimic natural traffic patterns
        delay = random.uniform(0.01, 1)
        time.sleep(delay)
        time_simulating += delay


def main():
    print(f'Simulating app traffic...')

    # Seed minimum 1 artist
    seed_artists(15)

    threads = []
    for _ in range(THREADS_AMOUNT):
        thread = threading.Thread(target=simulate_app_traffic, kwargs={"duration": SIMULATION_DURATION})
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    print('Finished simulating traffic')


if __name__ == "__main__":
    main()
