import secrets
import string
import unittest


class TestSecrets(unittest.TestCase):
    def test_choice(self):
        colors = ['Red', 'Green', 'Blue']
        print(secrets.choice(colors))

    def test_token_bytes(self):
        print(secrets.token_bytes())

    def test_token_hex(self):
        print(secrets.token_hex())

    def test_token_urlsafe(self):
        print(secrets.token_urlsafe())

    def test_temp_password(self):
        num_of_characters = 10
        char_pool = string.ascii_letters + string.digits + '+-?/!@'
        temp_password = ''.join(secrets.choice(char_pool) for i in range(num_of_characters))
        print(temp_password)

    def test_perm_password(self):
        num_of_characters = 10
        char_pool = string.ascii_letters + string.digits + '+-?/!@'

        while True:
            password = ''.join(secrets.choice(char_pool) for i in range(num_of_characters))
            if any(c.isupper() for c in password) and any(c.isdigit() for c in password):
                break

        print(password)

    def test_unique_url(self):
        url = 'http://www.example.com?reset=' + secrets.token_urlsafe(15)
        print(url)

    if __name__ == '__main__':
        unittest.main()
