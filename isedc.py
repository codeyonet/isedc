#!/usr/bin/env python3
"""

Show Cisco ISE Oracle Database data.

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        SQL query to execute, enclosed in quotes.
  -t, --table           Output results in table format (default).
  -j, --json            Output results in JSON format.

Script does not rely on Java or Oracle client.
Script does not validate ISE certificate, so no need to import the certificate.

Examples (the query is not case sensitive):
    isedc.py -q 'select * from node_list' # Get all entries from NODE_LIST view in table format
    isedc.py -q 'select * from NETWORK_DEVICE_GROUPS' -t # Get all entries from NETWORK_DEVICE_GROUPS view in table format
    isedc.py -q 'SELECT * FROM ENDPOINTS_DATA' -j # Get all entries from ENDPOINTS_DATA view in JSON format
  
Set the environment variables:
    export ISEDC_USER=dataconnect
    export ISEDC_PASSWORD='12Characters_or_more' 
    export ISE_SMNT=1.2.3.4
    
"""
__author__ = "codeyo.net"
__email__ = "codeyonet@gmail.com"
__license__ = "MIT - https://mit-license.org/"

import oracledb
import traceback
import ssl
import sys
from prettytable import PrettyTable
import json
import datetime
import argparse
import os

# Set up the argument parser
parser = argparse.ArgumentParser(description="Execute SQL queries on an Oracle database.")
parser.add_argument('-q', '--query', type=str, help='SQL query to execute, enclosed in quotes.')
parser.add_argument('-t', '--table', action='store_true', help='Output results in table format (default).')
parser.add_argument('-j', '--json', action='store_true', help='Output results in JSON format.')

# Parse arguments
args = parser.parse_args()

# Check if a query was provided, if not, print help and exit
if not args.query:
    parser.print_help()
    sys.exit(1)

sql_query = args.query
output_json = args.json

conn = None
cursor = None

# Helper function to serialize datetime objects
def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()  # Convert datetime to ISO 8601 string
    raise TypeError(f"Type {type(obj)} not serializable")

def handle_encoding_errors(cursor, name, default_type, size, precision, scale):
    if name == "PROBE_DATA":
        return cursor.var(str, size, arraysize=cursor.arraysize, encoding_errors="replace")
    return None

try:
    # Connection parameters
    user = os.getenv('ISEDC_USER', 'admin')  # Fallback to 'admin' if not set
    password = os.getenv('ISEDC_PASSWORD', 'default_password')  # Fallback to 'default_password' if not set
    ip_ise = os.getenv('ISE_SMNT', 'default_ip')  # Fallback to 'default_ip' if not set
    port_ise = "2484"  # Data Connect port on ISE
    service_name = "cpm10"  # Data Connect service name on ISE

    # Create an Easy Connect Plus string
    dsn = f"tcps://{ip_ise}:{port_ise}/{service_name}"

    # Create an SSL context that does not verify certificates
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Connect to the database
    conn = oracledb.connect(user=user, password=password, dsn=dsn, ssl_context=ctx)

    cursor = conn.cursor()

    # Set the output type handler on the cursor
    cursor.outputtypehandler = handle_encoding_errors

    # Execute the SQL query passed as a command-line argument
    cursor.execute(sql_query)
    output = cursor.fetchall()

    # Modify the output section based on the output format argument
    if output_json:
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in output]
        print(json.dumps(results, indent=4, default=datetime_serializer))
    else:
        print("\nResults:")
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]  # Set column headers
        for row in output:
            processed_row = [col.decode('utf-8', errors='replace') if isinstance(col, bytes) else col for col in row]
            table.add_row(processed_row)
        print(table)

except Exception as e:
    print('An exception occurred: {}'.format(e))
    traceback.print_exc()

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
