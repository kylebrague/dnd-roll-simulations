from deathsavingthrow import DeathSavingThrowState, death_saving_throw
from utils import create_logging_function


class Character:
    """Represents a character in a role-playing game."""

    def __init__(
        self, name, is_downed=False, is_alive=True, enable_logging: bool = False
    ):
        self.name = name
        self.is_downed = is_downed
        self.is_alive = is_alive
        self.enable_logging = enable_logging
        self.death_saving_throw_state = DeathSavingThrowState()
        self.log = create_logging_function(self.enable_logging)
    

    def roll_death_saving_throw(self):
        default_dict = {
            "name": self.name,
            "successes": self.death_saving_throw_state.successes,
            "failures": self.death_saving_throw_state.failures,
        }
        self.log(f"{self.name} is rolling a death saving throw.")
        if not self.is_downed:
            self.log(f"{self.name} is not downed. Ignoring roll.")
            return {
                **default_dict,
                "result": "ERROR",
                "notes": "Character is not downed.",
            }
        self.death_saving_throw_state.in_progress = True
        roll_result = death_saving_throw()
        if roll_result == 100:
            self.revive()
            self.death_saving_throw_state.reset()
            self.log(f"{self.name} rolled a 20! The character wakes up with 1 HP.")
            return {**default_dict, "result": "REVIVED", "notes": "WAKE UP"}
        if roll_result > 0:
            self.log(f"{self.name} added {roll_result} to successes.")
            self.death_saving_throw_state.successes += roll_result
            if self.death_saving_throw_state.successes >= 3:
                self.revive()
                self.death_saving_throw_state.reset()
                self.log(f"{self.name} has stabilized but remains unconscious.")
                return {**default_dict, "result": "REVIVED", "notes": "UNCONCIOUS"}
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

    is_dead: bool = property(get_is_dead)

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
