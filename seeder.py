from faker import Faker
import controller

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