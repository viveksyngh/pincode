import os
import re
import csv
from datetime import datetime
from elasticsearch_utils import create_index_only, create_index_bulk
from constants import (FILE_PATH, INDEX_NAME, DOCUMENT_TYPE)


def read_csv_and_prepare_elastic_search_data():
	"""Returns list of row from an excel in format of elatic bulk query."""
	try:
		pincode_list = []
		csv_file = open(FILE_PATH, 'rb')
	except IOError, e:
		print "CSV File is not present at given location."
	else:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for i, row in enumerate(csv_reader):
			if i == 0:
				continue
		
			pincode = {
				"_index": INDEX_NAME,
				"_type": DOCUMENT_TYPE,
				"_id": i,
				"_source": {
					"officename": re.sub('[^a-zA-Z0-9-_*.]', '', row[0]),
					"pincode": re.sub('[^a-zA-Z0-9-_*.]', '', row[1]), 
					"officetype": re.sub('[^a-zA-Z0-9-_*.]', '', row[2]),
					"deliverystatus": re.sub('[^a-zA-Z0-9-_*.]', '', row[3]),
					"divison": re.sub('[^a-zA-Z0-9-_*.]', '', row[4]),
					"region": re.sub('[^a-zA-Z0-9-_*.]', '', row[5]),
					"circle": re.sub('[^a-zA-Z0-9-_*.]', '', row[6]),
					"taluk": re.sub('[^a-zA-Z0-9-_*.]', '', row[7]),
					"district": re.sub('[^a-zA-Z0-9-_*.]', '', row[8]),
					"state": re.sub('[^a-zA-Z0-9-_*.]', '', row[9]),
					"timestamp": datetime.now()
					}
			}
			pincode_list.append(pincode)
	return pincode_list


def load_data_in_elastic():
	"""Dumping data in bulk to elasticsearch in chunk of 5000."""
	pincode_data = read_csv_and_prepare_elastic_search_data()
	print len(pincode_data)
	for i in range(0, len(pincode_data), 5000):
		try:
			create_index_bulk(pincode_data[i : i + 5000])
		except Exception, e:
			print str(e)
	os.remove(FILE_PATH)

load_data_in_elastic()