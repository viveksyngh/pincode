#!/bin/bash
wget "https://data.gov.in/sites/default/files/all_india_pin_code.csv"
python pincode/populate_data.py
python manage.py runserver 0.0.0.0:8000

