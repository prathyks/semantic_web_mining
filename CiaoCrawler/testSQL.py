import pymysql
import SQLFunctions
import SQLConnect
import requests
import logging
from bs4 import BeautifulSoup
pymysql.install_as_MySQLdb()
import sys

from datetime import date
from dateutil.rrule import rrule, DAILY


cur = SQLFunctions.selectUserTable(conn)
SQLFunctions.getNextUser(cur)

