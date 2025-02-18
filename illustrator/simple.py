import argparse

import illustrator.data_functions as df
import illustrator.functions as functions

def at_issue_projection(gender: str, risk_class: str, issue_age: int, face_amount: int, annual_premium: float) -> float:
    """
    Account value rollforward for new policy

    Parameters
    ----------
    gender: str
        Gender for policy, "M" or "F"
    risk_class: str
        Risk class for policy, "NS" or "SM"
    issue_age: int
        Issue age for policy
    face_amount: int
        Policy face amount
    annual_premium: float
        Annual premium for projection

    Returns
    -------
    float
        Value at end of projection
    """
    maturity_age = 121
    projection_years = maturity_age - issue_age
    interest_rate = df.read_flat_csv('./data/interest_rate.csv')
    premium_load_rate = df.read_flat_csv('./data/premium_load.csv')
    annual_policy_fee = df.read_flat_csv('./data/policy_fee.csv')
    annual_unit_load = df.read_ia_py_csv('./data/unit_load.csv', issue_age)
    annual_coi_rate = df.read_gen_rc_ia_py_csv('./data/coi.csv', gender, risk_class, issue_age)
    naar_discount_rate = df.read_flat_csv('./data/naar_discount.csv', 1)

    end_value = 0
    for i in range(12*projection_years):
        policy_year = functions.calculate_policy_year(i+1)
        start_value = functions.calculate_start_value(end_value)
        premium = functions.calculate_premium(i+1, annual_premium)
        premium_load = functions.calculate_premium_load(premium, premium_load_rate[policy_year-1])
        expense_charge = functions.calculate_per_policy_fee(annual_policy_fee[policy_year-1]) + functions.calculate_per_unit_load(annual_unit_load[policy_year-1], face_amount)
        value_for_naar = functions.calculate_value_for_naar(start_value, premium, premium_load, expense_charge)
        naar = functions.calculate_naar(face_amount, naar_discount_rate[policy_year-1], value_for_naar)
        coi = functions.calculate_coi(naar, annual_coi_rate[policy_year-1])
        value_for_interest = functions.calculate_value_for_interest(value_for_naar, coi)
        interest = functions.calculate_interest(value_for_interest, interest_rate[policy_year-1])
        end_value = functions.calculate_end_value(value_for_interest, interest)

    return end_value

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arguments for simple.py")
    parser.add_argument("-g", "--gender", default="M", choices=["M","F"], help="The gender for projection, default is M for male")
    parser.add_argument("-r", "--risk_class", default="NS", choices=["NS","SM"], help="The risk class for the projection, default is NS")
    parser.add_argument("-i", "--issue_age", default=35, type=int, choices=range(18,81), help="The issue age for the projection, default is 35")
    parser.add_argument("-f", "--face_amount", default=100000, type=int, help="The face amount for the projection, default is 100,000")
    parser.add_argument("-p", "--premium", default=1255.03, type=float, help="The annual premium for the projection, default is 1,255.03")
    args = parser.parse_args()
    end_value = at_issue_projection(args.gender, args.risk_class, args.issue_age, args.face_amount, args.premium)
    print(end_value)