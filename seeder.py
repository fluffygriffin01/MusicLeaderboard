from faker import Faker

fake = Faker()

def generate_artist():
    name = fake.name()
    email = fake.email()
    return {"name": name, "email": email}