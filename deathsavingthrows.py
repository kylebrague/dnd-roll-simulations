"""calculates death saving throws for D&D 5e characters"""

import random
from enum import Enum
import sys




class DeathSavingThrowResult(Enum):
    SUCCESS = 1
    FAILURE = -1
    CRITICAL_SUCCESS = 100
    CRITICAL_FAILURE = -2


def death_saving_throw() -> DeathSavingThrowResult:
    # Simulate a death saving throw
    roll = random.randint(1, 20)
    if roll == 1:
        return -2  # Two failures
    if roll == 20:
        return 100  # Automatic success and wake up
    if roll < 10:
        return -1  # One failure
    return 1  # One success


class DeathSavingThrowState():
    def __init__(self):
        self.in_progress = False
        self.successes = 0
        self.failures = 0

    def reset(self):
        self.in_progress = False
        self.successes = 0
        self.failures = 0



def simulate_death_saves(enable_logging=True):
    state = DeathSavingThrowState()

    def custom_print(x):
        return print(x) if enable_logging else None

    while state.successes < 3 and state.failures < 3:
        outcome = death_saving_throw()

        if outcome == 100:
            custom_print(f"Rolled a 20! The character wakes up with 1 HP.")
            return {"result": "REVIVED", "notes": "WAKE UP"}

        if outcome > 0:
            state.successes += outcome
            custom_print(f"Success! Total successes: {state.successes}")
        else:
            state.failures -= (
                outcome  # outcome is negative, so we subtract to add to failures
            )
            custom_print(f"Failure! Total failures: {state.failures}")

        # Check for stabilization or death
        if state.successes >= 3:
            custom_print("The character has stabilized but remains unconscious.")
            return {"result": "REVIVED", "notes": "UNCONCIOUS"}
        elif state.failures >= 3:
            custom_print("The character has died.")
            return {"result": "KILLED", "notes": "DEAD"}


class Character:
    """Represents a character in a role-playing game."""

    def __init__(self, name, is_downed=False, is_alive=True, enable_logging: bool = False):
        self.name = name
        self.is_downed = is_downed
        self.is_alive = is_alive
        self.logging = enable_logging
        self.death_saving_throw_state = DeathSavingThrowState()

    def log(self, x):
        return print(x) if self.logging else None
    
    def roll_death_saving_throw(self):
        default_dict = {"name": self.name, "successes": self.death_saving_throw_state.successes, "failures": self.death_saving_throw_state.failures}
        self.log(f"{self.name} is rolling a death saving throw.")
        if not self.is_downed:
            self.log(f"{self.name} is not downed. Ignoring roll.")
            return {**default_dict, "result": "ERROR", "notes": "Character is not downed."}
        self.death_saving_throw_state.in_progress = True
        roll_result = death_saving_throw()
        if roll_result == 100:
            self.revive()
            self.death_saving_throw_state.reset()
            self.log(f"{self.name} rolled a 20! The character wakes up with 1 HP.")
            return {**default_dict,"result": "REVIVED", "notes": "WAKE UP"}
        if roll_result > 0:
            self.log(f"{self.name} added {roll_result} to successes.")
            self.death_saving_throw_state.successes += roll_result
            if self.death_saving_throw_state.successes >= 3:
                self.revive()
                self.death_saving_throw_state.reset()
                self.log(f"{self.name} has stabilized but remains unconscious.")
                return {**default_dict,"result": "REVIVED", "notes": "UNCONCIOUS"}
            return {
                **default_dict,
                "result": "SUCCESS",
                "notes": f"Rolled a {roll_result}.",
            }
        self.log(f"{self.name} added {roll_result} to failures.")
        self.death_saving_throw_state.failures -= roll_result
        if self.death_saving_throw_state.failures >= 3:
            self.kill()
            self.death_saving_throw_state.reset()
            self.log(f"{self.name} has died.")
            return {**default_dict, "result": "KILLED", "notes": "DEAD"}
        return {
            **default_dict,
            "result": "FAILURE",
            "notes": f"Rolled a {roll_result}.",
        }
      
    def get_is_dead(self):
        if self.is_alive:
            return False
        if self.is_downed:
            return False
        return True
    
    is_dead:bool = property(get_is_dead)

    def down(self):
        self.log(f"{self.name} is down.")
        self.death_saving_throw_state.in_progress = True
        self.is_downed = True
        self.is_alive = False

    def revive(self):
        self.log(f"{self.name} is revived.")
        self.is_downed = False
        self.is_alive = True

    def kill(self):
        self.log(f"{self.name} is kill.")
        self.is_downed = False
        self.is_alive = False

    def get_status(self):
        return {"alive": self.is_alive, "downed": self.is_downed, "dead": self.is_dead}

    def __str__(self):
        return f"{self.name} is {'alive' if self.is_alive else 'downed' if self.is_downed else 'dead'}."


class Party:
    def __init__(self, characters: list[Character]):
        self.characters = characters
        self.all_downed_or_dead = self.get_all_downed_or_dead()

    def __len__(self):
        return len(self.characters)

    def count_not_dead_characters(self):
        return [not pc.is_dead for pc in self].count(True)

    def get_is_wiped(self):
        return all((pc.is_dead for pc in self))
    
    def get_all_downed_or_dead(self):
        return all((pc.is_downed or not pc.is_alive for pc in self))
    is_wiped: bool = property(get_is_wiped)

    def __iter__(self):
        return iter(self.characters)


def single_character_simulation(n=1000):
    death_saves_results_map = {
        "REVIVED": 0,
        "KILLED": 0,
    }
    for i in range(n):
        pc = Character("Character1", is_downed=True)
        while pc.is_downed:
            pc.roll_death_saving_throw()
        if pc.is_alive:
            death_saves_results_map["REVIVED"] += 1
        else:
            death_saves_results_map["KILLED"] += 1
    print(death_saves_results_map)
    print(f"Revived: {(death_saves_results_map['REVIVED'] / n)*100}%")
    print(f"Killed: {(death_saves_results_map['KILLED'] / n)*100}%")


def mean(numbers):
    return sum(numbers) / len(numbers)


def multicharacter_simulation(n=1000, num_characters=4, enable_logging=False):
    def log(x):
        return print(x) if enable_logging else None
    party_save_results = {
        "SAVED": 0,
        "WIPED": 0,
    }
    all_results:list[Party] = []
    for i in range(n):
        party = Party(
            [Character(f"Character-{i}-{j}", enable_logging=enable_logging) for j in range(num_characters)]
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
            log(f"Party is not wiped. {[pc.name for pc in party if pc.is_alive or pc.is_downed]} characters not dead.")
            for pc in party:
                log(pc)
                if pc.is_alive:
                    log(pc.name + " is alive.")
                    break
                if pc.is_downed and pc.death_saving_throw_state.in_progress:
                    log(pc.roll_death_saving_throw())
                if pc.is_alive:
                    log(pc.name + " is alive.")
                    break
                if(party.is_wiped):
                    break
            if any((pc.is_alive for pc in party)):
                log(f"Party saved! {[pc.name for pc in party if pc.is_alive]} characters are alive.")
                break
            if party.is_wiped:
                log(f"Party wiped! {[pc.name for pc in party if pc.is_dead]} characters are dead.")
                break
        all_results.append(party)
        if party.is_wiped:
            party_save_results["WIPED"] += 1
        else:
            party_save_results["SAVED"] += 1
    
    average_characters_alive = sum([x.count_not_dead_characters() for x in all_results if not x.is_wiped])/party_save_results['SAVED']
    print(f"WIPED: {(party_save_results['WIPED'] / n) * 100}%")
    print(f"SAVED: {(party_save_results['SAVED'] / n) * 100}%")
    print(
        f"Averaged {average_characters_alive} characters alive per saved party."
    )


if __name__ == "__main__":
    argtypes = [int, int, bool]
    args = sys.argv[1:]
    typed_args = [argtypes[i](args[i]) for i in range(len(args))]
    multicharacter_simulation(*typed_args)
