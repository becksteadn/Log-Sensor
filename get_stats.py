#
# Parse log file and send attempted logins to a MySQL server
# Author: N. Beckstead, github.com/becksteadn
#
import MySQLdb
import re
import datetime
from sensor_vars import HOSTNAME
from sensor_vars import DB_URL
from sensor_vars import DB_USER
from sensor_vars import DB_PASSWD
from sensor_vars import DB_TABLE
from sensor_vars import AUTH_FILE
from sensor_vars import LOG_SUCESSES

#
# Pad numbers with 0s
#
def fill(data, length):
    return str(data).zfill(length)

#
# Connect to a MySQL server
#
def db_connect():
    db = MySQLdb.connect(DB_URL, DB_USER, DB_PASSWD, DB_TABLE)
    return db

#
# Generate SQL queries to insert records to database
#
def insert_attempt(cursor, hostname, ip_addr, timestamp, success_value):
    if ip_addr is None or timestamp is None:
        return

    base_columns = "INSERT INTO attempts ("
    base_values = " VALUES ("

    if hostname:
        base_columns += "host, "
        base_values += "'{}', ".format(hostname)

    base_columns += "ip, "
    base_values += "'{}', ".format(ip_addr)

    if success_value == 0 or success_value == 1:
        base_columns += "stamp, success)"
        base_values += "'{}', {});".format(timestamp, success_value)
    else:
        base_columns += "stamp)"
        base_values += "'{}');".format(timestamp)
    base_cmd = base_columns + base_values

    markers_cmd = "INSERT INTO markers (ip) VALUES ('{}');".format(ip_addr)

    print(base_cmd)
    print(markers_cmd)
    try:
        cursor.execute(base_cmd)
    except:
        pass
    try:
        cursor.execute(markers_cmd)
    except:
        pass


#
# Read log file and create an Attempt tuple with (ip, timestamp, success)
#
def get_attempts(filename, atm_list):
    with open(filename, 'r') as f:
        for line in f.readlines():
            atm_ip = None
            atm_stamp = None
            atm_success = None

# Check if line is generated from cron
            if "CRON" in line:
                continue

# Find IP address in line
            line_ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}',line)
            if len(line_ips) == 0:      # no ip found
                continue
            else:
                atm_ip = line_ips[0]

# Determine success based on keywords
            line_lower = line.lower()
            fail_keywords = ["fail", "invalid", "preauth"]
            if any(elm in line_lower for elm in fail_keywords):
                atm_success = 0
            elif "accept" in line_lower:
                if LOG_SUCESSES:
                    atm_success = 1
                else:
                    continue
            else:
                continue

# Convert timestamp to SQL compatible DATETIME form
            spline = line.split()
            year = datetime.datetime.now().year
            month = spline[0].upper()
            try:
                month = {
                'JAN' : 1,
                'FEB' : 2,
                'MAR' : 3,
                'APR' : 4,
                'MAY' : 5,
                'JUN' : 6,
                'JUL' : 7,
                'AUG' : 8,
                'SEP' : 9,
                'OCT' : 10,
                'NOV' : 11,
                'DEC' : 12
                }[month]
            except KeyError:
                print("[*] Error getting month for timestamp.")
                print(line)
                continue
            day = spline[1]
            time = spline[2].split(':')
            hour = time[0]
            minute = time[1]
            second = time[2]
            atm_stamp = "{}-{}-{} {}:{}:{}".format(
                fill(year, 4),
                fill(month, 2),
                fill(day, 2),
                fill(hour, 2),
                fill(minute, 2),
                fill(second, 2)
            )

# Necessary variables for DB insertion
            if atm_ip is None or atm_stamp is None:
                continue
            else:
                attempt = (atm_ip, atm_stamp, atm_success)
                attempts.append(attempt)


if __name__ == "__main__":
# Parse file for attempts
    attempts = list()
    get_attempts(AUTH_FILE, attempts)

# Start connection to database
    db = db_connect()
    cur = db.cursor()

    for atm in attempts:
        insert_attempt(cur, HOSTNAME, atm[0], atm[1], atm[2])

# Write changes and disconnect from server
    db.commit()
    db.close()
