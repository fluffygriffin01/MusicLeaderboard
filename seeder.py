import controller
import threading
import time
import random
from faker import Faker

#Simulate number of users interacting
THREADS_AMOUNT = 4
SIMULATION_DURATION = 20 #runtime in seconds
fake = Faker()

def generate_artist():
    name = fake.name()
    email = fake.email()

    return {"name": name, "email": email,}

def seed_artists(count): #return how many artists succesfully added in leaderboard
    added_amount = 0
    for _ in range(count):
        artist_info = generate_artist()
        added_artist = controller.add_artist(artist_info['name'], artist_info['email'])
        if added_artist == True:
            added_amount += 1
    return added_amount

def simulate_app_traffic(duration):
    time_simulating = 0
    while time_simulating < duration:
        artist = None
        try:
            artist = random.choice(controller.get_top_artists(random.randint(100, 200)))
        except IndexError:
            artist = None
        rng = random.random()

        if artist is not None:
            if rng > 0.8:
                controller.remove_artist(artist[0])
            elif rng > 0.6:
                controller.unfollow_artist(artist[0])
            elif rng > 0.4:
                controller.follow_artist(artist[0])
        else:
            artist_info = generate_artist()
            controller.add_artist(artist_info['name'], artist_info['email'])

        delay = random.uniform(0.01, 1) #delay to mimic real timing.
        time.sleep(delay)
        time_simulating += delay

def main():
    print(f'Simulating app traffic...')
    seed_artists(1) # add minimum of 1 artist to leaderboard.
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