#!/bin/bash
wget "https://data.gov.in/sites/default/files/all_india_pin_code.csv"
python pincode/populate_data.py
exec uwsgi --ini app.ini

