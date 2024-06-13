import uuid
import unittest


class TestUUID(unittest.TestCase):
    def test_uuid4(self):
        uuid4 = uuid.uuid4()
        print('uuid4', uuid4)
        print('uuid4::hex', uuid4.hex)
        print('uuid4::urn', uuid4.urn)

    def test_uuid5(self):
        uuid5 = uuid.uuid5(uuid.NAMESPACE_DNS, 'example.com')
        print('uuid4', uuid5)
        print('uuid4::hex', uuid5.hex)
        print('uuid4::urn', uuid5.urn)

    if __name__ == '__main__':
        unittest.main()
