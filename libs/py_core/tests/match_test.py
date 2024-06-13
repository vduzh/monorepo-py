import unittest


class TestMatch(unittest.TestCase):
    def test_match(self):
        code = 200
        match code:
            case 100:
                self.assertTrue(code == 100)
            case 200:
                self.assertTrue(code == 200)
            case _:
                self.assertTrue(False)

    def test_match_template(self):
        code = 200
        match code:
            case 100:
                self.assertTrue(code == 100)
            case 200 | 201:
                self.assertTrue(code == 200 or code == 201)
            case _:
                self.assertTrue(False)

    def test_match_template_with_if(self):
        lang_orig = "En"
        lang = lang_orig.lower()

        value = None
        match lang:
            case "en" | "us" if lang == lang_orig:
                value = "En"
            case "en" | "us":
                value = "en"
            case _:
                pass

        self.assertEqual(value, "en")

    def test_match_template_with_if_sample(self):
        age = 20
        match age:
            case age if age < 18:
                self.assertTrue(False)
            case age if age >= 18:
                self.assertTrue(True)
            case _:
                self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
