# isedc
A simple Python script to test the [ISE Data Connect](https://developer.cisco.com/docs/dataconnect/getting-started/) feature. 

This script does not require Java or an Oracle client installation and does not perform ISE certificate validation, so there is no need to import the certificate. 
It utilizes python-oracledb in Thin Mode, which has some limitations. For more information, please review [table](https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_a.html) here.

To connect to your ISE instance, set the environment variables:
```    
    export ISEDC_USER=dataconnect
    export ISEDC_PASSWORD='12Characters_or_more' 
    export ISE_SMNT=1.2.3.4
```

Options:
```
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        SQL query to execute, enclosed in quotes.
  -t, --table           Output results in table format (default).
  -j, --json            Output results in JSON format.
```
Examples (the query is not case sensitive):
```
    isedc.py -q 'select * from node_list' # Get all entries from NODE_LIST view in table format
    isedc.py -q 'select * from NETWORK_DEVICE_GROUPS' -t # Get all entries from NETWORK_DEVICE_GROUPS view in table format
    isedc.py -q 'SELECT * FROM ENDPOINTS_DATA' -j # Get all entries from ENDPOINTS_DATA view in JSON format
```    
