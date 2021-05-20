from random import choice
import json


class RandomPerson:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


def _generate_random_pairs(random_people) -> list:
    draw_pool = random_people.copy()
    draw_results = []

    for person in random_people:
        if draw_pool == [person]:
            return _generate_random_pairs(random_people)

        chosen_person = choice(draw_pool)

        while chosen_person == person:
            chosen_person = choice(draw_pool)

        draw_pool.remove(chosen_person)
        draw_results.append([person, chosen_person])

    return draw_results


def generate_random_pairs(random_person_pool):
    random_pairs = _generate_random_pairs(random_person_pool)
    pairs_list = []

    for [person_one, person_two] in random_pairs:
        pairs_list.append([f'{person_one.name}, {person_one.email}', f'{person_two.name}, {person_two.email}'])

    return json.dumps(pairs_list)
