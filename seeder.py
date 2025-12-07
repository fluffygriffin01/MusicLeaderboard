import controller
import threading
import time
import random
from faker import Faker

fake = Faker()

def generate_artist():
    name = fake.name()
    email = fake.email()
    return {"name": name, "email": email}

def seed_artists(count):
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
        artist = random.choice(controller.get_top_artists(random.randint(100, 200)))

        if random.random() > 0.4:
            controller.follow_artist(artist[0])
        else:
            controller.unfollow_artist(artist[0])

        delay = random.uniform(0.01, 1)
        time.sleep(delay)
        time_simulating += delay

def main():
    print(f'Simulating app traffic...')
    seed_artists(100)
    threads = []  
    for _ in range(6):
        thread = threading.Thread(target=simulate_app_traffic, kwargs={"duration": 20})
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    print('Finished simulating traffic')

if __name__ == "__main__":
    main()