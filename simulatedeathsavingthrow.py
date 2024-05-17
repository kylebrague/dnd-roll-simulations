"""calculates death saving throws for D&D 5e characters"""

import sys

from character import Character
from party import Party
from utils import create_logging_function


def multicharacter_simulation(n=1000, num_characters=4, enable_logging=False):
    log = create_logging_function(enable_logging)

    all_results: list[Party] = []
    for i in range(n):
        party = Party(
            [
                Character(f"Character-{i}-{j}", enable_logging=enable_logging)
                for j in range(num_characters)
            ]
        )
        for pc in party:
            pc.down()
        counter = 0
        while not party.is_wiped:
            counter += 1
            if counter > 6:
                print("Too many iterations. Breaking.")
                print(i, [pc.get_status() for pc in party])
                raise Exception("Too many iterations.")
            log(
                f"Party is not wiped. {[pc.name for pc in party if pc.is_alive or pc.is_downed]} characters not dead."
            )
            for pc in party:
                log(pc)
                if pc.is_downed and pc.death_saving_throw_state.in_progress:
                    log(pc.roll_death_saving_throw())
                if pc.is_alive or party.is_wiped:
                    break

            if any((pc.is_alive for pc in party)):
                log(
                    f"Party saved! {[pc.name for pc in party if pc.is_alive]} characters are alive."
                )
                break
            if party.is_wiped:
                log(
                    f"Party wiped! {[pc.name for pc in party if pc.is_dead]} characters are dead."
                )
                break
        all_results.append(party)
    wiped_parties = [party for party in all_results if party.is_wiped]
    saved_parties = [party for party in all_results if not party.is_wiped]

    average_characters_alive = sum(
        (x.count_not_dead_characters() for x in saved_parties)
    ) / len(saved_parties)
    print(f"WIPED: {(len(wiped_parties) / n) * 100}%")
    print(f"SAVED: {(len(saved_parties) / n) * 100}%")
    print(f"Averaged {average_characters_alive} characters alive per saved party.")


p_stabilize_by_round = [0.05, 0.0475, 0.168, 0.197625, 0.132]
p_die_by_round = [0.0, 0.0425, 0.1145, 0.139875, 0.108]

if __name__ == "__main__":
    argtypes = [int, int, bool]
    args = sys.argv[1:]
    typed_args = [argtypes[i](args[i]) for i in range(len(args))]
    multicharacter_simulation(*typed_args)
