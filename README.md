# Illustrator

## Purpose
Universal life illustration engine for new business.

## Usage

### Default
Run simple.py in the terminal / Powershell as a module from the parent directory

```
...> python -m illustrator.simple
132184.0426761172
```

Alternatively, run objects.py in the terminal / Powershell as a module from the parent directory
```
...> python -m illustrator.objects
132184.0426761172
```

Using objects.py requires preparing a SQLite database 'data.db' in './data/' first. Run the following commands:
```
>>> import illustrator.objects as iobj
>>> db = iobj.SQLiteRateDatabase('./data/data.db')
>>> db.import_csv('./data/coi.csv')
>>> db.import_csv('./data/interest_rate.csv')
>>> db.import_csv('./data/naar_discount.csv')
>>> db.import_csv('./data/policy_fee.csv')
>>> db.import_csv('./data/premium_load.csv')
>>> db.import_csv('./data/unit_load.csv')
>>> exit()
``` 

### Command-line arguments
Command-line arguments have been included to facilitate quick execution of different cases. 
* -g, --gender 
  * description: The gender for projection
  * options: M, F
  * default: M
* -r, --risk_class {NS, SM}
  * description: The risk class for projection
  * options: NS, SM
  * default: NS
* -i, --issue_age {18, ..., 80}
  * description: The issue age for projection
  * options: 18, 19, ..., 80
  * default: 35
* -f, --face_amount
  * description: The face amount for projection
  * default: 100,000
* -p, --premium
  * description: The annual premium for projection
  * default: 1,255.03

To use the arguments include the flag and input value. To explicitly run a male, non-smoker, age 35, 100k policy with a premium of 1,255.03 we would use the following command:

```
...> python -m illustrator.simple -g M -r NS -i 35 -f 100000 -p 1255.03
132184.0426761172
```

This can be done using illustrator.simple OR illustrator.objects.

## Tests
Make sure the included tests successfully execute. Run the following code from the parent directory. The actual run-time may differ on your machine.

```
...> python -m unittest
...............
-----------------------------------------------
Ran 15 tests in 0.026s

OK
```