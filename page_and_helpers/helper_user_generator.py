from faker import Faker


class TestData:
    def __init__(self):
        self.fake = Faker()

    def get_admin(self):
        admin = {
            'username': 'aramis_ris',
            'email': 'aramisov2018@yandex.ru',
            'password': 'samp1337A'
        }
        return admin

    def get_fake_person(self):
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        fake_person = {
            'username': username,
            'password': password,
            'email': email
        }
        return fake_person
