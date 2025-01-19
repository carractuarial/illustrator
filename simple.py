if __name__ == '__main__':
    face_amount = 100000
    interest_rate = 0.01
    
    premium = 2000
    premium_load = premium * 0.06
    expense_charge = (120 + 12 * face_amount / 1000) / 12
    value_for_naar = premium - premium_load - expense_charge
    naar = face_amount / (1 + interest_rate)**(1/12) - value_for_naar
    coi = (naar / 1000) * 3.00 / 12
    value_for_interest = value_for_naar - coi
    interest = value_for_interest * ((1 + interest_rate)**(1/12)-1)
    end_value = value_for_interest + interest

    print(end_value)