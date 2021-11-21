from random import choice
import json
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    email: str

    def __repr__(self):
        return f'({self.name}, {self.email})'


def _generate_random_pairs(random_people) -> list:
    draw_pool = random_people.copy()
    draw_results = []

    for person in random_people:
        is_alone_in_pool = draw_pool == [person]
        if is_alone_in_pool:
            return _generate_random_pairs(random_people)

        chosen_person = choice(draw_pool)
        someone_drew_himself = chosen_person == person

        while someone_drew_himself:
            chosen_person = choice(draw_pool)
            someone_drew_himself = chosen_person == person

        draw_pool.remove(chosen_person)
        draw_results.append([person, chosen_person])

    return draw_results


def generate_random_pairs(random_person_pool):
    random_pairs = _generate_random_pairs(random_person_pool)
    pairs_list = []

    for [person_one, person_two] in random_pairs:
        pairs_list.append([f'{person_one.name}, {person_one.email}', f'{person_two.name}, {person_two.email}'])

    return json.dumps(pairs_list)
