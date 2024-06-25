# isedc
Simple Python script to test ISE Data Connect feature.
Script does not require Java or Oracle client to be installed.
Script does not validate ISE certificate, so no need to import the certificate.
Script uses python-oracledb Thin Mode which has some limitations. Please see more here:
https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_a.html

To connect to your ISE instance, set the environment variables:
    export ISEDC_USER=dataconnect
    export ISEDC_PASSWORD='12Characters_or_more' 
    export ISE_SMNT=1.2.3.4

Options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        SQL query to execute, enclosed in quotes.
  -t, --table           Output results in table format (default).
  -j, --json            Output results in JSON format.

Examples (the query is not case sensitive):
    isedc.py -q 'select * from node_list' # Get all entries from NODE_LIST view in table format
    isedc.py -q 'select * from NETWORK_DEVICE_GROUPS' -t # Get all entries from NETWORK_DEVICE_GROUPS view in table format
    isedc.py -q 'SELECT * FROM ENDPOINTS_DATA' -j # Get all entries from ENDPOINTS_DATA view in JSON format
    
