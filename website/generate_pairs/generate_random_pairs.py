import random
from dataclasses import dataclass


@dataclass(eq=False)
class Person:
    name: str
    email: str

    def __repr__(self):
        return f'({self.name}, {self.email})'


def generate_random_pairs(random_people: list) -> list:
    '''This function takes an array of objects, mapped with name and email,
     outputs randomly generated pairs of these objects.'''

    if not isinstance(random_people, list):
        raise TypeError
    draw_pool = random_people.copy()
    draw_results = []

    for person in random_people:
        print(person)
        if is_alone_in_pool := draw_pool == [person]:
            print('return')
            return generate_random_pairs(random_people)

        chosen_person = random.choice(draw_pool)

        while someone_drew_himself := chosen_person == person:
            chosen_person = random.choice(draw_pool)

        draw_pool.remove(chosen_person)
        draw_results.append([person, chosen_person])

    return draw_results
