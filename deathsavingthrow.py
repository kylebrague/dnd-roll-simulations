from enum import Enum
from random import randint

class DeathSavingThrowResult(Enum):
    SUCCESS = 1
    FAILURE = -1
    CRITICAL_SUCCESS = 100
    CRITICAL_FAILURE = -2


def death_saving_throw() -> DeathSavingThrowResult:
    # Simulate a death saving throw
    roll = randint(1, 20)
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

