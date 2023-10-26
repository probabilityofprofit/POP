from numba import jit
from MonteCarlo import monteCarlo
import time
from BlackScholes import blackScholesPut
import numpy as np


def bsm_debit(sim_price, strikes, rate, time_fraction, sigma):
    P_short_puts = blackScholesPut(sim_price, strikes[0], rate, time_fraction, sigma)
    P_long_puts = blackScholesPut(sim_price, strikes[1], rate, time_fraction, sigma)

    credit = P_long_puts - P_short_puts
    debit = -credit

    return debit


def putDebitSpread(underlying, sigma, rate, trials, days_to_expiration,
                   closing_days_array, percentage_array, short_strike,
                   short_price, long_strike, long_price):

    # Data Verification
    if long_price <= short_price:
        raise ValueError("Long price cannot be less than or equal to Short price")

    if short_strike >= long_strike:
        raise ValueError("Short strike cannot be greater than or equal to Long strike")

    for closing_days in closing_days_array:
        if closing_days > days_to_expiration:
            raise ValueError("Closing days cannot be beyond Days To Expiration.")

    if len(closing_days_array) != len(percentage_array):
        raise ValueError("closing_days_array and percentage_array sizes must be equal.")

    # SIMULATION
    initial_debit = long_price - short_price  # Debit paid from opening trade
    initial_credit = -1 * initial_debit

    percentage_array = [x / 100 for x in percentage_array]
    max_profit = long_strike - short_strike - initial_debit
    min_profit = [max_profit * x for x in percentage_array]

    strikes = [short_strike, long_strike]

    # LISTS TO NUMPY ARRAYS CUZ NUMBA HATES LISTS
    strikes = np.array(strikes)
    closing_days_array = np.array(closing_days_array)
    min_profit = np.array(min_profit)

    try:
        pop, pop_error, avg_dtc, avg_dtc_error = monteCarlo(underlying, rate, sigma, days_to_expiration,
                                                                closing_days_array, trials,
                                                                initial_credit, min_profit, strikes, bsm_debit)
    except RuntimeError as err:
        print(err.args)

    response = "   ".join(f"{value:.2f}" for value in pop)

    return response
