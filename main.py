
import constants
import time
from datetime import datetime,timedelta

test_case = [
    {
        'employee_code': "A02-0001",
        'log_records':[
            {
                "day":"Monday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("17:30", "%H:%M"),
                "overtime_out":time.strptime("20:30", "%H:%M")
            },
            {
                "day":"Tuesday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("17:03", "%H:%M"),
                "overtime_out":time.strptime("18:30", "%H:%M")
            },
            {
                "day":"Wednesday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("00:00", "%H:%M"),
                "overtime_out":time.strptime("00:00", "%H:%M")
            },
            {
                "day":"Thursday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":True,
                "overtime_in":time.strptime("00:00", "%H:%M"),
                "overtime_out":time.strptime("00:00", "%H:%M")
            },
            {
                "day":"Friday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("00:00", "%H:%M"),
                "overtime_out":time.strptime("00:00", "%H:%M")
            }
        ]
    },
    {
        'employee_code': "A02-0003",
        'log_records':[
            {
                "day":"Monday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("17:30", "%H:%M"),
                "overtime_out":time.strptime("20:30", "%H:%M")
            },
            {
                "day":"Tuesday",
                "time_in":time.strptime("13:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("17:30", "%H:%M"),
                "overtime_out":time.strptime("18:30", "%H:%M")
            },
            {
                "day":"Wednesday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("00:00", "%H:%M"),
                "overtime_out":time.strptime("00:00", "%H:%M")
            },
            {
                "day":"Thursday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":True,
                "overtime_in":time.strptime("00:00", "%H:%M"),
                "overtime_out":time.strptime("00:00", "%H:%M")
            },
            {
                "day":"Friday",
                "time_in":time.strptime("08:00", "%H:%M"),
                "time_out":time.strptime("17:01", "%H:%M"),
                "is_holiday":False,
                "overtime_in":time.strptime("00:00", "%H:%M"),
                "overtime_out":time.strptime("00:00", "%H:%M")
            }
        ]
    },
]

# The main function or the entry point of the program
def main():
    employees = read_employee_file()
        # while True:
        # employee_code = input("Enter employee code:")
    employee_code = "A02-0001"
    employee = get_employee_record(employees,employee_code)
    
    print_employee_details(employee)
    # log_records = get_input_log_times(employee["name"])
    log_records = test_case[0]["log_records"]
    # coverage_date = input("Enter the coverage date for this payroll:")
    coverage_date = ";"
    payroll = calc_payroll(log_records,coverage_date,employee)
    
    print_payroll_details(payroll)
    save_to_dtr(employee_code,log_records)



# Calculates the employee's payroll for the week
# @param log_records - the inputs for an employee, the time-in and out, overtime, and if holiday
# @param coverage_date - date covered for the payroll
# @param employee - dictionary containing the employee details
# @returns the calculated payroll with all the details
def calc_payroll(log_records,coverage_date,employee):
    payroll = {
        "coverage": coverage_date,
        "total_work_hrs":0.0,
        "overtime_hrs":0.0,
        "total_overtime_hrs":0.0,
        "regular_inc":0.0,
        "overtime_inc":0.0,
        "gross_inc":0.0,
        "deductions":{
            "tax":0.0,
            "sss":0.0,
        },
        "net_inc":0.0
    }

    for record in log_records:
        td_record = convert_to_td(record)

        late_hrs = calc_late_hrs(td_record["time_in"],record["time_in"].tm_hour)
        under_time_hrs = calc_under_time(td_record["time_out"])
        day_work_hrs = calc_daily_work_hrs(td_record,late_hrs,under_time_hrs)
        overtime_hrs = calc_overtime_hrs(td_record["overtime_out"],td_record["overtime_in"])
        payroll["overtime_hrs"] += overtime_hrs
        payroll["total_work_hrs"] += day_work_hrs
        payroll["regular_inc"] += calc_daily_regular_inc(day_work_hrs,employee["salary_level"],record["is_holiday"])
        payroll["overtime_inc"] += calc_day_overtime_inc(overtime_hrs,employee["salary_level"],record["is_holiday"])
    
    payroll["gross_inc"] = calc_wgsi(payroll["regular_inc"], payroll["overtime_inc"])
    payroll["deductions"]["tax"] = calc_tax(payroll["gross_inc"])
    payroll["deductions"]["sss"] = calc_gsis(employee["salary_level"])
    payroll["net_inc"] = calc_wnsi(payroll["gross_inc"],payroll["deductions"])

    return payroll



# Gets the employee with the matched employee code from a given list
# @param employees - list of employee dictionary
# @param employee_code - the code of the employee to look for
# @returns an employee dictionary if found else the program quits
def get_employee_record(employees,employee_code):

    for employee in employees:  
        if employee["code"] == employee_code:
            employee["salary_rate"] = get_salary_rate(employee["salary_level"])
            return employee
    else:
        print("Cannot find employee. Quitting...")
        quit()



# Reads the employee.txt file and stores it to a list 
# @returns a list of employees dictionary
def read_employee_file():
    employees = []
    employees_file_name = "employee.txt"
    try:
        file = open(employees_file_name, 'r')
        for each in file:
            line = each.strip('\n').split(',')
            employees.append({
                "name":line[0],
                "code":line[1],
                "salary_level":int(line[2])
            })
        file.close()
    except:
        # If employee.txt doesn't exist, the program quits
        print("Employee file does not exist or cannot read the file. ")
        print("Quitting...")
        quit()
    return employees



# Saves the log_records of an employee to the file "dtr.txt"
# @param employee_code - the code of the employee for which the details to be saved
# @param log_records - the inputs of the user (time-ins and outs, overtimes, is_holiday)
def save_to_dtr(employee_code,log_records):
    dtr_file_name = "dtr.txt"
    found = False
    # try:
    file = open(dtr_file_name,'r+')
    for line in file:
        val_array = line.split(',')
        if val_array[0] == employee_code:
            found = True
            break

    arr = []
    for record in log_records:
        # what the code below does is that it turns it to a 24-hour time string like 00:00, 23:33
        arr.append(str(record["time_in"].tm_hour).zfill(2) + ":"+ str(record["time_in"].tm_min).zfill(2))
        arr.append(str(record["time_out"].tm_hour).zfill(2) + ":"+ str(record["time_out"].tm_min).zfill(2))
        arr.append(str(record["overtime_in"].tm_hour).zfill(2) + ":"+ str(record["overtime_in"].tm_min).zfill(2))
        arr.append(str(record["overtime_out"].tm_hour).zfill(2) + ":"+ str(record["overtime_in"].tm_min).zfill(2))
    string = ""
    if not found:
        # we have to write a new line for the employee since it doesn't have its own line
        string += "\n" + employee_code 
    string += ","
    string += ",".join(arr) # now we can get something like A02-005,00:00,23:33
    file.write(string)
    file.close()



# Gets inputs (time-ins and outs, overtime-ins and outs, is_holiday) from a user
# @param employee_name - the name of the employee
# @returns a list of  dictionary of the inputs of user 
def get_input_log_times(employee_name):
    log_records = []
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    for day in days:
        log_record = {}
        
        log_record["time_in"] = ask_time(employee_name,day,"time","in",None)
        log_record["time_out"] = ask_time(employee_name,day,"time","out",log_record["time_in"])
        
        log_record["is_holiday"] = ask_if_holiday(day)

        log_record["overtime_in"] = ask_time(employee_name,day,"overtime","in",None)
        log_record["overtime_out"] = ask_time(employee_name,day,"overtime","out",log_record["overtime_in"])
        
        log_record["day"] = day

        log_records.append(log_record)
    return log_records



# Asks for a time 
# @param employee_name - the name of the employee
# @param day - like Monday, Tuesday and etc..
# @param type - "time" or "overtime"
# @param in_our_out - if the input time is a time out or a time in
# @param time_in - null if the type is a time out else the previously inputted time
# @returns the validated time 
def ask_time(employee_name,day,type,in_or_out,time_in):
    time = input("Enter %s %s of %s for %s:" %(type,in_or_out,employee_name,day))
    time = validate_time(time,type,in_or_out,time_in)
    return time



# Validates the time
# @param time - the inputted time
# @param type - "time" or "overtime"
# @param in_our_out - if the input time is a time out or a time in
# @param time_in - null if the type is a time out else the previously inputted time
# @returns the validated time 
def validate_time(time,type,in_or_out,time_in):
    while True:
        try:
            time = parse_time(time)
            if time.tm_hour == 0 and time.tm_min !=0:
                raise Exception("Error: Input 00:00 for an employee that is not present")
            if type == "overtime":
                if in_or_out == "in" and time.tm_hour < 17 and time.tm_hour != 0:
                    raise Exception("Error: Not a valid time for overtime in ")
            if time_in != None:
                time_out_td = timedelta(hours=time.tm_hour, minutes=time.tm_min)
                time_in_td = timedelta(hours=time_in.tm_hour, minutes=time_in.tm_min)
                if time_out_td < time_in_td:
                    raise Exception("Error: Time out cannot be greater than the time in")
            return time
        except Exception as e:
            print(e)
            time = input("Input again:")




# Parses the time string 
# @param input_time - the inputted time 
# @returns a time struct if valid or raises an exception
def parse_time(input_time):
    try:
        parsed_time = time.strptime(input_time, "%H:%M")
        return parsed_time
    except:
        raise Exception("Error: Invalid time")



# Asks the user if the day is holidiay. It converts the Yes or No of the user to True or False 
# @param day - "Monday","Tuesday" and etc.
# @returns True if it is False if not
def ask_if_holiday(day):
    is_holiday = ""
    while ((is_holiday != "YES") and  (is_holiday != "NO")):
        is_holiday = input("Is %s a holiday?" %(day))
        is_holiday = is_holiday.upper()
    return True if is_holiday == "YES" else False




# Calculates the number of hours the employee was late
# @param time_in - the time in of the employee of type timedelta
# @param in_hr - the time in hour of the employee 
# returns the late hours
def calc_late_hrs(time_in,in_hr):
    late_hrs = 0.0
    work_start_td = timedelta(hours=constants.WORK["start"].tm_hour,minutes=constants.WORK["start"].tm_min)
    if (not(time_in <= work_start_td)):
        diff = time_in - work_start_td
        late_hrs = convert_to_hrs(diff.seconds)
        if(in_hr >= 13):
            late_hrs = late_hrs - 1 # subtract 1 hour since we factor break time
    return late_hrs



# Calculates the number of hours the the employee lack for a day
# @param time_out - the time out of the employee of type timedelta
# returns the undertime hours
def calc_under_time(time_out):
    req_time_out = timedelta(hours=constants.WORK["end"].tm_hour, minutes=constants.WORK["end"].tm_min)
    if time_out >= req_time_out:
        return 0.0
    else:
        diff = req_time_out - time_out
        return convert_to_hrs(diff.seconds)



# Calculates the number of hours the employee worked for a day
# @param record - a dictionary containing the input times of type timedelta
# @param late  - late hours
# @param undertime - undertime hours
# @returns the calculated hours
def calc_daily_work_hrs(record, late, undertime):
    work_hours = constants.REQUIRED_WORK_HOURS
    if is_employee_absent(record["time_in"], record["time_out"]):
        work_hours = 0
    return work_hours - (late + undertime)



# Calculates the overtime hours for the day
# @param overtime_out - when the employee logged out for overtime of type timedelta 
# @param overtime_in - when the employee logged in for overtime of type timedelta
# @returns the calculated hours 
def calc_overtime_hrs(overtime_out, overtime_in):
    overtime = constants.OVERTIME
    ot_start_td = timedelta(hours=overtime["start"].tm_hour, minutes=overtime["end"].tm_min)
    ot_end_td = timedelta(hours=overtime["end"].tm_hour, minutes=overtime["end"].tm_min)
    if overtime_in == overtime_out == constants.NULL_TIME:
        return 0
    if overtime_in < ot_start_td:
        overtime_in = (ot_start_td - overtime_in) + overtime_in # overtime must start at 17:30
    if overtime_out > ot_end_td:
        overtime_out = overtime_out - ot_end_td # overtime must end at 20:30
    overtime = overtime_out - overtime_in
    return convert_to_hrs(overtime.seconds)



# Calculates the income accumulated from the overtime for a day 
# @param overtime_hrs - the overtime hours 
# @param employee_level - the employee's salary level either 1,2 or 3
# @param is_holiday - if the day was a holiday or not
# @returns the day overtime income
def calc_day_overtime_inc(overtime_hrs,employee_level,is_holiday):
    return calc_hrly_overtime_rate(employee_level,is_holiday) * overtime_hrs



# Calculates the income for the day 
# @param daily_work_hrs - the hours worked for the day 
# @param salary_level - the employee's salary level either 1,2 or 3
# @param is_holiday - if the day was a holiday or not
# @returns the income for the day
def calc_daily_regular_inc(daily_work_hrs,salary_level,is_holiday):
    hourly_rate = calc_hrly_rate(salary_level,is_holiday)
    regular_inc = hourly_rate * daily_work_hrs
    return regular_inc



# Calculates the Weekly Gross Salary Income (WGSI)
# @param regular_inc - the regular income 
# @param overtime_inc - the overtime income
# @returns the calculated wgsi
def calc_wgsi(regular_inc,overtime_inc):
    return regular_inc + overtime_inc



# Calculates the Weekly Net Salary Income (WNSI)
# @param wgsi - the Weekly Gross Salary Income (WGSI)
# @param deductions - the tax and sss of type dictionary
# @returns the calculated wnsi
def calc_wnsi(wgsi,deductions):
    return (wgsi-(deductions["tax"]+deductions["sss"])) + constants.ALLOWANCE



# Calculates the tax to be deducted from the WGSI
# @param wgsi - the Weekly Gross Salary Income (WGSI)
# @returns the calculated tax amount
def calc_tax(wgsi):
    return wgsi * constants.TAX_PERCENTAGE
    


# Calculates the gsis/sss to be deducted from the WGSI
# @param salary_level - the employee's salary level either 1,2 or 3
# @returns the gsis/sss amount
def calc_gsis(salary_level):
    return constants.GSIS_DEDUCTIONS[str(salary_level)] * get_salary_rate(salary_level)



# Calculates the hourly rate of the employee
# @param salary_level - the employee's salary level either 1,2 or 3
# @param is_holiday - if the day was a holiday or not
# @returns the hourly rate
def calc_hrly_rate(salary_level, is_holiday):
    rate = get_salary_rate(salary_level) / 8
    if is_holiday:
        rate *= 1.1  
    return rate



# Calculates the hourly rate when an employee overtimes
# @param salary_level - the employee's salary level either 1,2 or 3
# @param is_holiday - if the day was a holiday or not
# @returns the hourly overtime rate
def calc_hrly_overtime_rate(salary_level,is_holiday):
    return calc_hrly_rate(salary_level,is_holiday) * 1.1



# Gets the salary rate of an employee 
# @param salary_level - the employee's salary level either 1,2 or 3
# @returns the salary rate    
def get_salary_rate(salary_level):
    return constants.SALARY_RATES[str(salary_level)]



# Checks if the employee is absent or not
# @param time_in - the time in of the employee of type timedelta
# @param time_in - the time out of the employee of type timedelta
# @returns the True if the employee was absent else False
def is_employee_absent(time_in,time_out):
    absent_time = timedelta(hours=0, minutes=0)
    if absent_time == time_in == time_out:
        return True
    else:
        return False



# Converts seconds to hours
# @param seconds - the seconds to convert
# @returns hours 
def convert_to_hrs(seconds):
    return seconds/60/60



# Prints all the payroll details
# @param payroll - a dictionary returned by calc_payroll
def print_payroll_details(payroll):
    currency = constants.CURRENCY
    print("Date Covered: %s" %(payroll["coverage"]))
    print("Total Number of Work Hours: %.1f" %(payroll["total_work_hrs"]))
    print("Overtime hours: %.1f" %(payroll["overtime_hrs"]))
    print("Regular Income: %s %.2f" %(currency,payroll["regular_inc"]))
    print("Overtime Income: %s %.2f" %(currency,payroll["overtime_inc"]))
    print("Gross Income: %s %.2f" %(currency,payroll["gross_inc"]))        
    print("Deductions:")
    print("* Tax: %s %.2f" %(currency,payroll["deductions"]["tax"]))
    print("* SSS: %s %.2f" %(currency,payroll["deductions"]["sss"]))
    print("Net Income: %s %.2f" %(currency,payroll["net_inc"]))



# Prints all the employee details
# @param employee - a dictionary returned by get_employee_record
def print_employee_details(employee):
    print("==================================================")
    print("Employee Name: %s" %(employee["name"]))
    print("Employee Code: %s" %(employee["code"]))
    print("Salary Level: Level %d" %(employee["salary_level"]))
    print("Salary Rate: %s %.2f/day" %(constants.CURRENCY,employee["salary_rate"]))
    print("==================================================")



# Converts a dictionary of struct time to a dictionary of timedelta
# @param record - the dictionary of struct time
# @returns a dictionary of timedelta 
def convert_to_td(record):
    return {
        "time_out": timedelta(hours=record["time_out"].tm_hour, minutes=record["time_out"].tm_min),
        "time_in": timedelta(hours=record["time_in"].tm_hour, minutes=record["time_in"].tm_min),
        "overtime_in": timedelta(hours=record["overtime_in"].tm_hour, minutes=record["overtime_in"].tm_min),
        "overtime_out": timedelta(hours=record["overtime_out"].tm_hour, minutes=record["overtime_out"].tm_min)
    }



main()
