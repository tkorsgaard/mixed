import datetime
import hashlib

from stdnum.exceptions import *
from stdnum.util import clean

from datetime import date
#from dateutil.rrule import rrule, DAILY

def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def checksum(number):
    """Calculate the checksum. Note that the checksum isn't actually used
    any more. Valid numbers used to have a checksum of 0."""
    weights = (4, 3, 2, 7, 6, 5, 4, 3, 2, 1)
    return sum(w * int(n) for w, n in zip(weights, number)) % 11


def get_birth_date(number):
    """Split the date parts from the number and return the birth date."""
    day = int(number[0:2])
    month = int(number[2:4])
    year = int(number[4:6])
    if number[6] in '5678' and year >= 58:
        year += 1800
    elif number[6] in '0123' or (number[6] in '49' and year >= 37):
        year += 1900
    else:
        year += 2000
    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise InvalidComponent()


def validate(number):
    """Check if the number provided is a valid CPR number. This checks the
    length, formatting, embedded date and check digit."""
    #number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 10:
        raise InvalidLength()
    # check if birth date is valid
    get_birth_date(number)
    # TODO: check that the birth date is not in the future
    return number


def is_valid(number):
    """Check if the number provided is a valid CPR number. This checks the
    length, formatting, embedded date and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join((number[:6], number[6:]))

d = date(2009, 5, 30)
delta = datetime.timedelta(days=1)
while d <= date(2010, 5, 30):
    #print d.strftime("%Y-%m-%d")
    dnew = d.strftime("%d%m%y")
    for digits in range ("0000", "9999"):
        print dnew + digits
    d += delta

#i = 1000000000
#while (i<3200000000):
#    if validate(str(i)):
#        print i + " hash: " + hashlib.sha256(i)
#    #print str(i) + " hash: " + hashlib.sha256(str(i)).hexdigest()
#    i = i + 1