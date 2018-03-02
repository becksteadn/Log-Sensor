# Log-Sensor
Parse log file and send attempted logins to MySQL server

## Requirements
The MySQLdb Python module is required to connect to a MySQL server.

**Windows** platforms can install it from [here](https://sourceforge.net/projects/mysql-python/files/)

**Ubuntu** systems can install it with apt using `sudo apt-get install python-mysqldb`

**RPM** systems can install it with `yum install MySQL-python`

**Fedora** can install it with `dnf install python-mysql`

**macOS** can install it using [these steps](https://stackoverflow.com/questions/1448429/how-to-install-mysqldb-python-data-access-library-to-mysql-on-mac-os-x#1448476)

## Setup

#### Database Creation

#### Sensor Configuration
Change the variables in `sensor_vars.py` to connect to a database.

**HOSTNAME** gives a name to the sensor. It does not need to be the machine's actual hostname. If it is left as None the default value will be 'Anonymous' in the database.

**DB_URL** is the FQDN or IP address of the database server.

**DB_USER** and **DB_PASSWD** are the credentials required to use the database.

**DB_TABLE** is the database the sensor will use.

**AUTH_FILE** is the file the sensor parses.

**LOG_SUCCESSES** does not log successful login attempts so that they are not mapped. If you wish to include successful logins, set this variable to anything except None and 0.

#### Cron
Set up a crontab with root to move the log file to the sensor's directory.
`sudo crontab -e`
`0 * * * * cp /var/log/auth.log /opt/Log-Sensor/`

Set a user crontab to run the sensor update.
`crontab -e`
`1 * * * * cd /opt/Log-Sensor/ && python get_stats.py`
