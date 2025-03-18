import illustrator.data_functions as df
import illustrator.functions as functions

import abc
import argparse
import csv
import dataclasses
import os
import sqlite3


@dataclasses.dataclass
class Insured:
    gender: str
    risk_class: str
    issue_age: str


class SQLiteRateDatabase:

    def __init__(self, connection_path: str):
        self._connection = sqlite3.connect(connection_path)

    def import_csv(self, file_path: str):
        # convert file name to table name
        file_name = os.path.split(file_path)[-1]
        file_ext = os.path.splitext(file_path)[-1]
        table_name = file_name.removesuffix(file_ext)
        table_name = table_name.replace(" ", "_")

        # remove existing table if applicable
        sql = f"DROP TABLE IF EXISTS [{table_name}]"
        self._connection.execute(sql)

        # create table structure
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            fields_and_types = {}
            for field in reader.fieldnames:
                if field == 'Rate':
                    fields_and_types[field] = "float"
                elif field in ["Issue_Age", "Attained_Age", "Policy_Year"]:
                    fields_and_types[field] = "int"
                else:
                    fields_and_types[field] = "varchar"
            sql = f"CREATE TABLE [{table_name}] ({','.join([k + " " + v for k, v in fields_and_types.items()])})"
            self._connection.execute(sql)

            # add records to table
            total_fields = len(fields_and_types)
            placeholders = ['?'] * total_fields
            sql = f"INSERT INTO [{table_name}] ({','.join(reader.fieldnames)}) VALUES ({','.join(placeholders)})"
            for row in reader:
                self._connection.execute(sql, list(row.values()))
        self._connection.commit()

    def read_table_for_insured(self, insured: Insured, table_name: str, table_type: str, default: float) -> list[float]:
        # prepare default output
        output = [default for _ in range(120)]

        # build SQL statement
        # determine headers of table
        sql = f"SELECT * FROM [{table_name}] WHERE 1 = 0"
        cursor = self._connection.execute(sql)
        headers = [f[0] for f in cursor.description]

        # build WHERE clause
        where_clauses = []
        if "Issue_Age" in headers:
            where_clauses.append(f"Issue_Age = {insured.issue_age}")
        if "Gender" in headers:
            where_clauses.append(f"Gender = '{insured.gender}'")
        if "Risk_Class" in headers:
            where_clauses.append(f"Risk_Class = '{insured.risk_class}'")
        where = " WHERE " + \
            ' AND '.join(where_clauses) if where_clauses else ""

        # determine SELECT fields
        select_fields = []
        if table_type == 'Policy_Year':
            select_fields.append('Policy_Year')
        select_fields.append('Rate')

        sql = f"SELECT {','.join(select_fields)} FROM [{table_name}]{where}"

        # execute SQL statement
        cursor = self._connection.execute(sql)
        results = cursor.fetchall()

        # translate query results
        if table_type == 'Flat':
            output = [results[0][0] for _ in range(120)]
        elif table_type == 'Policy_Year':
            for row in results:
                output[row[0]-1] = row[1]
        else:
            raise

        # return final output
        return output


class Rates:

    def __init__(self,
                 premium_loads: list[float],
                 policy_fees: list[float],
                 per_units: list[float],
                 naar_discounts: list[float],
                 coi_rates: list[float],
                 interest_rates: list[float]):
        self._premium_loads = premium_loads
        self._policy_fees = policy_fees
        self._per_units = per_units
        self._naar_discounts = naar_discounts
        self._coi_rates = coi_rates
        self._interest_rates = interest_rates

    def premium_load(self, policy_year: int) -> float:
        return self._premium_loads[policy_year - 1]

    def policy_fee(self, policy_year: int) -> float:
        return self._policy_fees[policy_year - 1]

    def unit_load(self, policy_year: int) -> float:
        return self._per_units[policy_year - 1]

    def naar_discount(self, policy_year: int) -> float:
        return self._naar_discounts[policy_year - 1]

    def coi_rate(self, policy_year: int) -> float:
        return self._coi_rates[policy_year - 1]

    def interest_rate(self, policy_year: int) -> float:
        return self._interest_rates[policy_year - 1]


class BaseProduct(abc.ABC):

    @abc.abstractmethod
    def get_rates_for_insured(self, insured: Insured) -> Rates:
        pass

    @abc.abstractmethod
    def illustrate_from_issue(self, insured: Insured, face_amount: int, annual_premium: float, rates: Rates) -> float:
        pass


class Product(BaseProduct):

    def __init__(self):
        self.maturity_age = 121
        self._db_path = './data/data.db'

    def get_rates_for_insured(self, insured: Insured) -> Rates:
        db = SQLiteRateDatabase(self._db_path)
        premium_loads = db.read_table_for_insured(
            insured, 'premium_load', 'Flat', 0)
        policy_fees = db.read_table_for_insured(
            insured, 'policy_fee', 'Flat', 0)
        unit_loads = db.read_table_for_insured(
            insured, 'unit_load', 'Policy_Year', 0)
        naar_discounts = db.read_table_for_insured(
            insured, 'naar_discount', 'Flat', 1)
        coi_rates = db.read_table_for_insured(insured, 'coi', 'Policy_Year', 0)
        interest_rates = db.read_table_for_insured(
            insured, 'interest_rate', 'Flat', 0)

        rates = Rates(premium_loads, policy_fees, unit_loads,
                      naar_discounts, coi_rates, interest_rates)
        return rates

    def illustrate_from_issue(self, insured: Insured, face_amount: int, annual_premium: float, rates: Rates) -> float:
        projection_years = self.maturity_age - insured.issue_age
        end_value = 0
        for i in range(12*projection_years):
            policy_year = functions.calculate_policy_year(i+1)
            start_value = functions.calculate_start_value(end_value)
            premium = functions.calculate_premium(i+1, annual_premium)
            premium_load = functions.calculate_premium_load(
                premium, rates.premium_load(policy_year))
            expense_charge = functions.calculate_per_policy_fee(rates.policy_fee(
                policy_year)) + functions.calculate_per_unit_load(rates.unit_load(policy_year), face_amount)
            value_for_naar = functions.calculate_value_for_naar(
                start_value, premium, premium_load, expense_charge)
            naar = functions.calculate_naar(
                face_amount, rates.naar_discount(policy_year), value_for_naar)
            coi = functions.calculate_coi(naar, rates.coi_rate(policy_year))
            value_for_interest = functions.calculate_value_for_interest(
                value_for_naar, coi)
            interest = functions.calculate_interest(
                value_for_interest, rates.interest_rate(policy_year))
            end_value = functions.calculate_end_value(
                value_for_interest, interest)

        return end_value


class Policy:

    def __init__(self, insured: Insured, product: BaseProduct, face_amount: int):
        self.insured = insured
        self.product = product
        self.face_amount = face_amount
        self.rates = product.get_rates_for_insured(insured)

    def illustrate_from_issue(self, annual_premium: float):
        return self.product.illustrate_from_issue(self.insured, self.face_amount, annual_premium, self.rates)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arguments for simple.py")
    parser.add_argument("-g", "--gender", default="M", choices=[
                        "M", "F"], help="The gender for projection, default is M for male")
    parser.add_argument("-r", "--risk_class", default="NS", choices=[
                        "NS", "SM"], help="The risk class for the projection, default is NS")
    parser.add_argument("-i", "--issue_age", default=35, type=int, choices=range(
        18, 81), help="The issue age for the projection, default is 35")
    parser.add_argument("-f", "--face_amount", default=100000, type=int,
                        help="The face amount for the projection, default is 100,000")
    parser.add_argument("-p", "--premium", default=1255.03, type=float,
                        help="The annual premium for the projection, default is 1,255.03")
    args = parser.parse_args()

    insured = Insured(args.gender, args.risk_class, args.issue_age)
    policy = Policy(insured, Product(), args.face_amount)
    end_value = policy.illustrate_from_issue(args.premium)
    print(end_value)
