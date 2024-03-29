# import pytest 
# import sys 
# import os 
# from backend.debatebot_api import app 

# def test_index_route():
#     """
#     GIVEN a Flask application
#     WHEN the '/' page is requested (GET)
#     THEN check the response is valid
#     """
#     with app.test_client() as client:
#         response = client.get('/')
#         assert response.status_code == 200
#         assert b'<!DOCTYPE html>' in response.data  
        
# def test_dummy_wrong_path():
#     """
#     GIVEN a Flask application
#     WHEN the '/wrong_path' page is requested (GET)
#     THEN check the response is valid
#     """
#     with app.test_client() as client:
#         response = client.get('/wrong_path')
#         assert response.status_code == 404
        
        
