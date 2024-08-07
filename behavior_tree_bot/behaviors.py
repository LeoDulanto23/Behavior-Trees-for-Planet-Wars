import sys
import math

sys.path.insert(0, '../')
from planet_wars import issue_order

def distance_from(pointA, pointB):
    return math.sqrt(pow(pointA[0] - pointB[0], 2) + pow(pointA[1] - pointB[1], 2))

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def attack_planets(state):
    if len(state.my_planets()) == 0:
        return False

    weak_planet = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)
    weak_ship = weak_planet.num_ships

    closest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    planet_distance = distance_from([weak_planet.x, weak_planet.y],[closest_planet.x, closest_planet.y])

    for planet in state.my_planets():
        distance_temp = state.distance(planet.ID, weak_planet.ID)
        if distance_temp < planet_distance and planet.num_ships > (weak_ship + 3):
            closest_planet = planet
            planet_distance = distance_temp
    return issue_order(state, closest_planet.ID, weak_planet.ID, weak_ship + 3)

def attack_further_planets(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda planet: planet.num_ships))
    planets_choices = [planet for planet in state.not_my_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    planets_choices.sort(key=lambda planet: planet.num_ships)

    target = iter(planets_choices) 

    try:
        my_planet = next(my_planets)
        target = next(target)
        while True:
            required_ships = target.num_ships + 1

            if target in state.enemy_planets(): required_ships = target.num_ships + \ state.distance(my_planet.ID, target.ID) * target.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return False


