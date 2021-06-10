import time
from datetime import timedelta

CURRENCY = "Php"

SALARY_RATES = {
    "1":380.00,
    "2":450.00,
    "3": 550.00
}

OVERTIME = {
    "start": time.strptime("17:30", "%H:%M"),
    "end": time.strptime("20:30", "%H:%M")
}

WORK = {
    "start": time.strptime("08:00", "%H:%M"),
    "end": time.strptime("17:00", "%H:%M"),
}

NULL_TIME = timedelta(hours=0, minutes=0)

ALLOWANCE = 500.00

REQUIRED_WORK_HOURS = 8

TAX_PERCENTAGE = 0.1

GSIS_DEDUCTIONS = {
    "1": 0.01,
    "2": 0.015,
    "3": 0.02
}