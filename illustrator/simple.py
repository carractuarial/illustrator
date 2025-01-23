import functions

if __name__ == '__main__':
    issue_age = 35
    maturity_age = 121
    projection_years = maturity_age - issue_age
    face_amount = 100000
    interest_rate = 0.03
    premium_load_rate = 0.06
    annual_policy_fee = 120
    annual_unit_load = [3.5 if year < 10 else 0 for year in range(projection_years)]
    annual_coi_rate = [0.15, 0.18, 0.29, 0.34, 0.4, 0.45, 0.51, 0.62, 0.7, 0.76,
                        0.83, 0.92, 1.04, 1.17, 1.31, 1.47, 1.63, 1.8, 2.02, 2.3,
                        2.64, 2.99, 3.32, 3.62, 3.92, 4.28, 4.74, 5.27, 5.88, 6.54,
                        7.25, 8.02, 8.86, 9.79, 10.88, 12.16, 13.69, 15.48, 17.55, 19.89,
                        22.48, 25.32, 28.46, 31.99, 36.04, 40.76, 46.15, 52.27, 59.31, 67.48,
                        76.96, 87.87, 100.29, 114.02, 128.76, 144.17, 159.79, 175.3, 190.25, 203.94,
                        218.45, 235.54, 253.92, 273.64, 294.31, 315.52, 336.99, 358.54, 379.81, 400.44,
                        420.09, 438.4, 455.01, 469.56, 481.7, 491.07, 497.31, 500, 500, 500,
                        500, 500, 500, 500, 500, 500]
    naar_discount_rate = 1.01**(-1/12)

    annual_premium = 1255.03
    end_value = 0
    policy_year = 0

    for i in range(12*projection_years):
        policy_year = functions.calculate_policy_year(i+1)
        start_value = functions.calculate_start_value(end_value)
        premium = functions.calculate_premium(i+1, annual_premium)
        premium_load = functions.calculate_premium_load(premium, premium_load_rate)
        expense_charge = functions.calculate_per_policy_fee(annual_policy_fee) + functions.calculate_per_unit_load(annual_unit_load[policy_year-1], face_amount)
        value_for_naar = functions.calculate_value_for_naar(start_value, premium, premium_load, expense_charge)
        naar = functions.calculate_naar(face_amount, naar_discount_rate, value_for_naar)
        coi = functions.calculate_coi(naar, annual_coi_rate[policy_year-1])
        value_for_interest = functions.calculate_value_for_interest(value_for_naar, coi)
        interest = functions.calculate_interest(value_for_interest, interest_rate)
        end_value = functions.calculate_end_value(value_for_interest, interest)

    print(end_value)