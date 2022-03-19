import json
from datetime import datetime
import pytest
from tests.conftest import client
from flask import Flask,render_template,request,redirect,flash,url_for


# @pytest.mark.parametrize("email", [("admin@irontemple.com"), ("wrong@email.com")])
@pytest.mark.parametrize("email", [("admin@irontemple.com")])
def test_login_status_code_ok(client, email):
    response = client.post('/showSummary', data={'email' : email })
    assert response.status_code == 200
    assert b"<h2>Welcome, admin@irontemple.com </h2>" in response.data
    # assert b"Sorry, that email wasn't found." in response.data


def test_login_status_code_ok(client):
    email = "admin@irontemple.com"
    response = client.post('/showSummary', data={'email' : email })
    assert response.status_code == 200

def test_login_wrong_email(client):
    email = "wrong@email.com"
    response = client.post('/showSummary', data={'email' : email })
    assert response.status_code == 200 and b"Sorry, that email wasn't found." in response.data


def test_purshase_more_place_than_club_possess_OK(client):
    '''
    test when a club try to book a competition with enought points
    '''

    club = {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}
    request_data = {"club": "Iron Temple","competition": "Spring Festival","places": "3"}
    places_left = club["points"] = int(club["points"]) - int(request_data["places"])
    response = client.post('/purchasePlaces', data=request_data)
    assert b"<li>Great-booking complete!</li>" in response.data

def test_purshase_more_place_than_club_possess_failed(client):
    '''
    test when a club try to book a competition with not enought points
    '''

    club = {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}
    request_data = {"club": "Iron Temple","competition": "Spring Festival","places": "5"}
    places_left = club["points"] = int(club["points"]) - int(request_data["places"])
    response = client.post('/purchasePlaces', data=request_data)
    print(response.data)
    assert b"<li>You haven&#39;t enought points in your possession !! Please try again</li>" in response.data

def test_purshase_places_deduction_ok(client):
    club = {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}
    request_data = {"club": "Iron Temple","competition": "Spring Festival","places": "3"}
    places_left = club["points"] = int(club["points"]) - int(request_data["places"])
    response = client.post('/purchasePlaces', data=request_data)
    assert b"Points available: " + bytes(str(places_left),'UTF-8') in response.data


def test_try_to_book_more_than_12_ok(client):
    '''
    test when a club try to book a less than 12 places
    '''

    request_data = {"club": "Simply Lift","competition": "Fall Classic","places": "11"}
    response = client.post('/purchasePlaces', data=request_data)
    assert b"<li>Great-booking complete!</li>" in response.data 

def test_try_to_book_more_than_12_ok(client):

    '''
    test when a club try to book a more than 12 places
    '''
    request_data = {"club": "Simply Lift","competition": "Fall Classic","places": "13"}
    response = client.post('/purchasePlaces', data=request_data)
    print(response.data)
    assert b"<li>You can&#39;t redeem more than 12 points ! please try again</li>" in response.data 


def test_try_to_book_past_competition_ok(client):
    foundClub = {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}
    foundCompetition = {'name': 'Fall Classic', 'date': '2023-10-22 13:30:00', 'numberOfPlaces': '13'}

    now = datetime.now()
    date_time_now = now.strftime("%Y-%m-%d %H:%M:%S")

    response_data = "<h3>This competition is still open</h3>"
    
    if foundCompetition['date'] < date_time_now:
        response_data = "<h3>Sorry, this competition is already closed</h3>"

    # response = client.get('/book/Spring Festival/Iron Temple')
    response = client.get('/book/' + foundCompetition['name'] + '/' + foundClub['name'])

    assert bytes(str(response_data),'UTF-8') in response.data





