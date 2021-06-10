
# import constants
# from datetime import timedelta
# import time

# test_case = [
#     {
#         'employee_code': "A02-0001",
#         'log_records':[
#             {
#                 "day":"Monday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("17:30", "%H:%M"),
#                 "overtime_out":time.strptime("20:30", "%H:%M")
#             },
#             {
#                 "day":"Tuesday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("17:03", "%H:%M"),
#                 "overtime_out":time.strptime("18:30", "%H:%M")
#             },
#             {
#                 "day":"Wednesday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("00:00", "%H:%M"),
#                 "overtime_out":time.strptime("00:00", "%H:%M")
#             },
#             {
#                 "day":"Thursday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":True,
#                 "overtime_in":time.strptime("00:00", "%H:%M"),
#                 "overtime_out":time.strptime("00:00", "%H:%M")
#             },
#             {
#                 "day":"Friday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("00:00", "%H:%M"),
#                 "overtime_out":time.strptime("00:00", "%H:%M")
#             }
#         ]
#     },
#     {
#         'employee_code': "A02-0003",
#         'log_records':[
#             {
#                 "day":"Monday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("17:30", "%H:%M"),
#                 "overtime_out":time.strptime("20:30", "%H:%M")
#             },
#             {
#                 "day":"Tuesday",
#                 "time_in":time.strptime("13:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("17:30", "%H:%M"),
#                 "overtime_out":time.strptime("18:30", "%H:%M")
#             },
#             {
#                 "day":"Wednesday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("00:00", "%H:%M"),
#                 "overtime_out":time.strptime("00:00", "%H:%M")
#             },
#             {
#                 "day":"Thursday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":True,
#                 "overtime_in":time.strptime("00:00", "%H:%M"),
#                 "overtime_out":time.strptime("00:00", "%H:%M")
#             },
#             {
#                 "day":"Friday",
#                 "time_in":time.strptime("08:00", "%H:%M"),
#                 "time_out":time.strptime("17:01", "%H:%M"),
#                 "is_holiday":False,
#                 "overtime_in":time.strptime("00:00", "%H:%M"),
#                 "overtime_out":time.strptime("00:00", "%H:%M")
#             }
#         ]
#     },
# ]

# def main():
#     employees = read_employee_file()
#     for case in test_case:
#         employee = get_employee_record(case["employee_code"])
#         if employee == None:
#             print("Cannot find employee. Quitting...")
#             quit()
#         employee["salary_rate"] = get_salary_rate(employee["salary_level"])
#         print_employee_details(employee)
#         # log_records 
#         payroll = calc_payroll(case["log_records"],"lala",employee)
#         print_payroll_details(payroll)
#     # #a.
#     # employee_code = input("Enter employee code:")
#     # #b.
#     # employee = get_employee_record(employee_code)
#     # if(employee == None):
#     #     print("Cannot find employee. Quitting...")
#     #     quit()

#     # print_employee_details(employee)
#     # #c.d.e.f.g.
#     # log_records = get_input_log_times(employee["name"])
#     # #h.
#     # coverage_date = input("Enter the coverage date for this payroll:")
#     # #i.
#     # calc_payroll(log_records,coverage_date)



# def calc_payroll(log_records,coverage_date,employee):
#     payroll = {
#         "coverage": coverage_date,
#         "total_work_hrs":0.0,
#         "overtime_hrs":0.0,
#         "total_overtime_hrs":0.0,
#         "regular_inc":0.0,
#         "overtime_inc":0.0,
#         "gross_inc":0.0,
#         "deductions":{
#             "tax":0.0,
#             "sss":0.0,
#         },
#         "net_inc":0.0
#     }

#     for record in log_records:
#         td_record = convert_to_td(record)

#         late_hrs = calc_late_hrs(td_record["time_in"],record["time_in"].tm_hour)
#         under_time_hrs = calc_under_time(td_record["time_out"])
#         day_work_hrs = calc_daily_work_hrs(td_record,late_hrs,under_time_hrs,record["is_holiday"])
#         overtime_hrs = calc_overtime_hrs(td_record["overtime_out"],td_record["overtime_in"])
#         payroll["overtime_hrs"] += overtime_hrs
#         payroll["total_work_hrs"] += day_work_hrs
#         payroll["regular_inc"] += calc_daily_regular_inc(day_work_hrs,employee["salary_level"],record["is_holiday"])
#         payroll["overtime_inc"] += calc_day_overtime_inc(overtime_hrs,employee["salary_level"])
    
#     payroll["gross_inc"] = calc_wgsi(payroll["regular_inc"], payroll["overtime_inc"])
#     payroll["deductions"]["tax"] = calc_tax(payroll["gross_inc"])
#     payroll["deductions"]["sss"] = calc_gsis(employee["salary_level"])
#     payroll["net_inc"] = calc_wnsi(payroll["gross_inc"],payroll["deductions"])

#     return payroll







# # params:
# #   employee_code
# # returns:
# #   employee dict if found else None

# def get_employee_record(employee_code):
#     employees_file_name = "employee.txt"
#     file = open(employees_file_name, 'r')
#     for each in file:
#         line = each.strip('\n').split(',')
#         if(line[1] == employee_code):
#             file.close()
#             return {
#                 "name":line[0],
#                 "code":line[1],
#                 "salary_level":int(line[2])
#             }
#     file.close()
#     return None



# def read_employee_file():
#     employees = []
#     employees_file_name = "employee.txt"
#     file = open(employees_file_name, 'r')
#     for each in file:
#         line = each.strip('\n').split(',')
#         employees.append({
#             "name":line[0],
#             "code":line[1],
#             "salary_level":int(line[2])
#         })
#     file.close()
#     return employees

# # params:
# #   employee_name
# # returns:
# #   a list/array of log_times 

# def get_input_log_times(employee_name):
#     log_records = []
#     days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
#     for day in days:
#         log_record = {}
#         log_record["day"] = day
        
#         log_record["time_in"] = parse_time(input("Enter time in of %s for %s:" %(employee_name,day)))
#         log_record["time_out"] = parse_time(input("Enter time out of %s for %s:" %(employee_name,day)))
        
#         log_record["is_holiday"] = ask_if_holiday(day)
        
#         log_record["overtime_in"] = parse_time(input("Enter overtime time in of %s for %s:" %(employee_name,day)))
#         log_record["overtime_out"] = parse_time(input("Enter overtime out of %s for %s:" %(employee_name,day)))
        
#         log_records.append(log_record)

#     print(log_records)
#     return log_records


# # params;
# #   day  
# # returns:
# #   True or False
# def ask_if_holiday(day):
#     is_holiday = ""
#     while ((is_holiday != "YES") and  (is_holiday != "NO")):
#         is_holiday = input("Is %s a holiday?" %(day))
#         is_holiday = is_holiday.upper()
#     return True if is_holiday == "YES" else False

# # params:
# #   time -> input time
# # returns:
# #   the parsed valid time

# def parse_time(input_time):
#     while True:
#         try:
#             struct_time = time.strptime(input_time, "%H:%M")
#             break
#         except:
#             input_time = input("Inputted time cannot be parsed. Input again:")
#     # return {
#     #     "hh": struct_time.tm_hour, # int
#     #     "mm": struct_time.tm_min, # int
#     #     "hhmm": str(struct_time.tm_hour) + ":" + str(struct_time.tm_min) 
#     # }  
#     return struct_time




# # main computations


# def calc_late_hrs(time_in,in_hr):
#     late_hrs = 0.0
#     work_start_td = timedelta(hours=constants.WORK["start"].tm_hour,minutes=constants.WORK["start"].tm_min)
#     if (not(time_in <= work_start_td)):
#         diff = time_in - work_start_td
#         late_hrs = convert_to_hrs(diff.seconds)
#         if(in_hr >= 13):
#             late_hrs = late_hrs - 1 # subtract 1 hour since we factor break time
#     return late_hrs


# def calc_under_time(time_out):
#     req_time_out = timedelta(hours=constants.WORK["end"].tm_hour, minutes=constants.WORK["end"].tm_min)
#     if time_out >= req_time_out:
#         return 0.0
#     else:
#         diff = req_time_out - time_out
#         return convert_to_hrs(diff.seconds)


# def calc_daily_work_hrs(record, late, undertime,is_holiday):
#     work_hours = constants.REQUIRED_WORK_HOURS
#     if is_holiday:
#         return 0 # holidays not counted in the paper
#     if is_employee_absent(record["time_in"], record["time_out"]):
#         work_hours = 0
#     return work_hours - (late + undertime)


# def calc_overtime_hrs(overtime_out, overtime_in):
#     overtime = constants.OVERTIME
#     ot_start_td = timedelta(hours=overtime["start"].tm_hour, minutes=overtime["end"].tm_min)
#     ot_end_td = timedelta(hours=overtime["end"].tm_hour, minutes=overtime["end"].tm_min)
#     if overtime_in == overtime_out == constants.NULL_TIME:
#         return 0
#     if overtime_in < ot_start_td:
#         overtime_in = (ot_start_td - overtime_in) + overtime_in # overtime must start at 17:30
#     if overtime_out > ot_end_td:
#         overtime_out = overtime_out - ot_end_td # overtime must end at 20:30
#     overtime = overtime_out - overtime_in
#     return convert_to_hrs(overtime.seconds)


# def calc_day_overtime_inc(overtime_hrs,employee_level):
#     return calc_hrly_overtime_rate(employee_level) * overtime_hrs


# def calc_daily_regular_inc(daily_work_hrs,salary_level,is_holiday):
#     hourly_rate = calc_hrly_rate(salary_level)
#     hourly_rate *= daily_work_hrs
#     if is_holiday:
#         hourly_rate *= 1.1
#     return hourly_rate


# def calc_wgsi(regular_inc,overtime):
#     return regular_inc + overtime


# def calc_wnsi(wgsi,deductions):
#     return (wgsi-(deductions["tax"]+deductions["sss"])) + constants.ALLOWANCE


# def calc_tax(weekly_gross_inc):
#     return weekly_gross_inc * constants.TAX_PERCENTAGE
    

# def calc_gsis(salary_level):
#     return constants.GSIS_DEDUCTIONS[str(salary_level)] * get_salary_rate(salary_level)

# # end of main computations




# def calc_hrly_rate(salary_level):
#     return get_salary_rate(salary_level) / 8


# def calc_hrly_overtime_rate(salary_level):
#     return calc_hrly_rate(salary_level) * 1.1

    
# def get_salary_rate(salary_level):
#     return constants.SALARY_RATES[str(salary_level)]


# def is_employee_absent(time_in,time_out):
#     absent_time = timedelta(hours=0, minutes=0)
#     if absent_time == time_in == time_out:
#         return True
#     else:
#         return False


# def convert_to_hrs(seconds):
#     return seconds/60/60


# def print_payroll_details(payroll):
#     currency = constants.CURRENCY
#     print("Date Covered: %s" %(payroll["coverage"]))
#     print("Total Number of Work Hours: %.1f" %(payroll["total_work_hrs"]))
#     print("Overtime hours: %.1f" %(payroll["overtime_hrs"]))
#     print("Regular Income: %s %.2f" %(currency,payroll["regular_inc"]))
#     print("Overtime Income: %s %.2f" %(currency,payroll["overtime_inc"]))
#     print("Gross Income: %s %.2f" %(currency,payroll["gross_inc"]))        
#     print("Deductions:")
#     print("* Tax: %s %.2f" %(currency,payroll["deductions"]["tax"]))
#     print("* SSS: %s %.2f" %(currency,payroll["deductions"]["sss"]))
#     print("Net Income: %s %.2f" %(currency,payroll["net_inc"]))


# def print_employee_details(employee):
#     print("==================================================")
#     print("Employee Name: %s" %(employee["name"]))
#     print("Employee Code: %s" %(employee["code"]))
#     print("Salary Level: Level %d" %(employee["salary_level"]))
#     print("Salary Rate: %s %.2f/day" %(constants.CURRENCY,employee["salary_rate"]))
#     print("==================================================")


# def convert_to_td(record):
#     return {
#         "time_out": timedelta(hours=record["time_out"].tm_hour, minutes=record["time_out"].tm_min),
#         "time_in": timedelta(hours=record["time_in"].tm_hour, minutes=record["time_in"].tm_min),
#         "overtime_in": timedelta(hours=record["overtime_in"].tm_hour, minutes=record["overtime_in"].tm_min),
#         "overtime_out": timedelta(hours=record["overtime_out"].tm_hour, minutes=record["overtime_out"].tm_min)
#     }


# main()
