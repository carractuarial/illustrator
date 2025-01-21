from math import ceil

def calculate_policy_year(policy_month: int) -> int:
    return ceil(policy_month/12)

def calculate_start_value(prior_end_value: float) -> float:
    return prior_end_value

def calculate_premium(policy_month: int, premium:float) -> float:
    """
    Calculates the premium to be paid for given month in policy year

    Parameters
    ----------
    policy_month: int
        An integer value greater than or equal to 1 corresponding to the applicable policy month
    premium: float
        The annualized illustrated premium

    Returns
    -------
    float
        premium if month in policy year is 1 else 0
    """
    return premium if (policy_month % 12 == 1) else 0

def calculate_premium_load(premium: float, rate: float) -> float:
    return premium * rate

def calculate_per_policy_fee(annual_rate: float) -> float:
    return annual_rate / 12

def calculate_per_unit_load(annual_rate: float, face_amount: float) -> float:
    return (annual_rate * face_amount / 1000) / 12

def calculate_value_for_naar(start_value: float, premium: float, premium_load: float, expense_charges: float) -> float:
    return start_value + premium - premium_load - expense_charges

def calculate_naar(face_amount: float, discount_rate: float, value_for_naar: float) -> float:
    return max(0, face_amount * discount_rate - max(0, value_for_naar))

def calculate_coi(naar: float, annual_rate: float) -> float:
    return (naar / 1000) * annual_rate / 12

def calculate_value_for_interest(value_for_naar: float, coi: float) -> float:
    return value_for_naar - coi

def calculate_interest(value_for_interest: float, annual_rate: float) -> float:
    return max(0, value_for_interest) * ((1 + annual_rate)**(1/12)- 1)

def calculate_end_value(value_for_interest: float, interest: float) -> float:
    return value_for_interest + interest