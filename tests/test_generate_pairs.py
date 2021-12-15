import unittest
from website.generate_pairs.generate_random_pairs import Person, generate_random_pairs


class GenerateRandomPairsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.first_person = Person('user1', 'first@testmail.com')
        self.second_person = Person('user2', 'second@testmail.com')
        self.third_person = Person('user3', 'third@testmail.com')
        self.pool = [self.first_person, self.second_person, self.third_person]
        self.draw = generate_random_pairs(self.pool)

    def tearDown(self) -> None:
        pass

    def test_generate_pairs(self):
        self.assertIsNotNone(self.draw)

    def test_call_single_person(self):
        pool = [self.first_person]
        with self.assertRaises(RecursionError):
            generate_random_pairs(pool)

    def test_somebody_draw_himself(self):
        for first_person, second_person in self.draw:
            self.assertNotEqual(first_person.name, second_person.name)
