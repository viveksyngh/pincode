from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from pincode.elasticsearch_utils import search_query
from pincode.constants import (ELASTIC_FIELD_NAMES, 
							   VALID_SEARCH_KEYS,
							   INDEX_NAME,
							   DOCUMENT_TYPE)

# Create your views here.


class Search(View):

	def get(self, request):
		request_params = request.GET
		is_valid = self.validate_keys(request_params)
		
		if not is_valid:
			return JsonResponse({"messgae": "Invalid filter key"}, status=400)

		if 'q' in request_params and request_params.get('q'):
			query = self.get_multi_match_query(request_params.get('q'))
		else:
			query = self.get_match_query(request_params)
		print query
		result = search_query(INDEX_NAME, DOCUMENT_TYPE, query)
		return JsonResponse({"message": "Success", "result": result}, 
							status=200)
		
	def validate_keys(self, request_params):
		"""Validates request parameters of API."""
		for key in request_params.keys():
			if key not in VALID_SEARCH_KEYS:
				return False
		return True

	def get_multi_match_query(self, query_string):
		"""Returns elastic query for matching on multiple field."""
		query = {
		  "query": {
		    "multi_match" : {
		      "query":  query_string, 
		      "fields":  ELASTIC_FIELD_NAMES
		    }
		  }
		}
		return query

	def get_match_query(self, request_params):
		"""Returns elastic query for matching on indivisual fields"""
		query = {
			"query" : {
				"bool" : {
					"filter": []
				}	
			}
		}
		for key, value in request_params.items():
			if value:
				query["query"]["bool"]["filter"].\
					append({"match": {str(key): str(value)}})
		return query
