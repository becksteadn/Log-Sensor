# Log-Sensor
Parse log file and send attempted logins to MySQL server

## Introduction

When I saw a huge amount of failed login attempts in my SSH logs, I wanted a way to get more information. I started out only mapping IPs using geolocation data and now the map is more interactive with links to Shodan and more statistics. This project is made up of a [server](https://github.com/becksteadn/Mapper-Server) and sensor, both of which use the same SQL database. I also created a self-contained version [here](https://github.com/becksteadn/Log-Mapper) though it is not maintained.

## Requirements
The MySQLdb Python module is required to connect to a MySQL server.

**Windows** platforms can install it from [here](https://sourceforge.net/projects/mysql-python/files/)

**Ubuntu** systems can install it with apt using `sudo apt-get install python-mysqldb`

**RPM** systems can install it with `yum install MySQL-python`

**Fedora** can install it with `dnf install python-mysql`

**macOS** can install it using [these steps](https://stackoverflow.com/questions/1448429/how-to-install-mysqldb-python-data-access-library-to-mysql-on-mac-os-x#1448476)

**Amazon Linux** can install it with `sudo yum install mysql-devel python-devel MySQL-python`

## Setup

### Database Creation

This is the same database as referenced in the [Mapper Server](https://github.com/becksteadn/Mapper-Server/blob/master/README.md#database-configuration) documentation.

### Sensor Configuration
Change the variables in `sensor_vars.py` to connect to a database.

**HOSTNAME** gives a name to the sensor. It does not need to be the machine's actual hostname. If it is left as None the default value will be 'Anonymous' in the database.

**DB_URL** is the FQDN or IP address of the database server.

**DB_USER** and **DB_PASSWD** are the credentials required to use the database.

**DB_TABLE** is the database the sensor will use.

**AUTH_FILE** is the file the sensor parses.

**LOG_SUCCESSES** does not log successful login attempts so that they are not mapped. If you wish to include successful logins, set this variable to anything except None and 0.

### Update Script Configuration

**LS_USER** user the script should run as.

**LS_LOC** location the sensor was installed at.


### Cron

Set a root crontab to run the sensor update.
```
sudo crontab -e
0 * * * * /opt/Log-Sensor/update.sh
```

Change the location from `/opt/` if you cloned it somewhere else.
