from random import choice


class RandomPerson:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


def generate_random_pairs(random_people) -> list:
    draw_pool = random_people[:]
    draw_results = []

    for person in random_people:
        if draw_pool == [person]:
            return generate_random_pairs(random_people)

        chosen_person = choice(draw_pool)

        while chosen_person == person:
            chosen_person = choice(draw_pool)

        draw_pool.remove(chosen_person)
        draw_results.append([person, chosen_person])

    return draw_results
