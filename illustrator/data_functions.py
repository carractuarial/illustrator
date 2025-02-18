import csv

def read_flat_csv(path: str, default: float = 0.0) -> list[float]:
    """
    Retrieve rate from csv assuming "Flat" rate structure

    Parameters
    ----------
    path: str
        Path to the csv
    default: float
        Optional parameter for default return value if file empty

    Returns
    -------
    list[float]
        Rates by policy year (index 0 = year 1); all values of list should be identical
    """
    rate = default
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rate = float(row["Rate"])
            break
    rates = [rate for _ in range(120)]
    return rates

def read_ia_py_csv(path: str, issue_age: int, default: float = 0.0) -> list[float]:
    rates = [default for _ in range(120)]
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Issue_Age'] == str(issue_age):
                policy_year = int(row['Policy_Year'])
                rate = float(row["Rate"])
                rates[policy_year-1] = rate
    return rates

def read_gen_rc_ia_py_csv(path: str, gender: str, risk_class: str, issue_age: int, default: float = 0.0) -> list[float]:
    rates = [default for _ in range(120)]
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Gender'] == gender and row['Risk_Class'] == risk_class and row['Issue_Age'] == str(issue_age):
                policy_year = int(row['Policy_Year'])
                rate = float(row["Rate"])
                rates[policy_year-1] = rate
    return rates