
# This means that in the Gregorian calendar, the years 2000 and 2400 are leap years, while 1800, 1900, 2100, 2200, 2300 and 2500 are NOT leap years. Source

def is_leap(year):
    leap = False
    if year % 400 ==0:
        leap = True
    elif year % 100 ==0:
        leap = False
    elif year %4 ==0:
        leap = True
    return leap

year = int(input())
