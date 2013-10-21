"""
All data parsers for particular TestLink information
"""
from datetime import datetime
API_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def format_date(date):
    """Format a date return from the API"""
    return datetime.strptime(date, API_DATE_FORMAT)
