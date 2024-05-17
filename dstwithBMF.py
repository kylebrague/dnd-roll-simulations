"""Currently incorect, need to fix the code to get the correct output
"""

from scipy.stats import binom

def probability_of_stabilizing_with_automatic_revival():
    p_success = 0.5
    p_failure = 0.4  # Adjusted for non-critical failures (rolling 2 to 9)
    p_critical_failure = 0.05  # Rolling a 1, counts as two failures
    p_revival = 0.05  # Rolling a 20

    # Probability of at least one revival in up to 2 rolls
    p_stabilize = 1 - ((1 - p_revival) ** 2)

    
    # If no revival first 2 rolls, calculate the stabilizing sequences
    # # Calculate for death in 2
    # probability_of_death_within_2_rolls = 1 - (p_critical_failure * p_failure) ** 2 - (p_critical_failure ** 2)
    # Calculate for 3 successes straight
    p_stabilize += (p_success ** 3) * ((1 - p_revival) ** 3) * ((1 - p_critical_failure) ** 3)

    # Calculate for 1 failure, then 3 successes
    for i in range(3):
        p_stabilize += binom.pmf(1, 4, p_failure) * (p_success ** 3) * \
                       ((1 - p_revival) ** 4) * ((1 - p_critical_failure) ** 4)

    # Calculate for 2 failures, then 3 successes, without hitting critical failures
    for i in range(6):
        p_stabilize += binom.pmf(2, 5, p_failure) * (p_success ** 3) * \
                       ((1 - p_revival) ** 5) * ((1 - p_critical_failure) ** 5)

    # Account for sequences where a critical failure occurs and doesn't immediately end the scenario
    # Only scenarios with 0 or 1 initial failures can proceed after one critical failure
    # After one critical failure and 0 initial failures
    p_stabilize += p_critical_failure * ((1 - p_revival) ** 1) * \
                   ((1 - p_critical_failure) ** 1) * (p_success ** 3)

    # After one critical failure and 1 initial failure
    p_stabilize += binom.pmf(1, 2, p_failure) * p_critical_failure * \
                   ((1 - p_revival) ** 2) * ((1 - p_critical_failure) ** 2) * (p_success ** 3)

    return p_stabilize

print(probability_of_stabilizing_with_automatic_revival())