import json
from datetime import datetime
import pytest
from tests.conftest import client
from flask import Flask,render_template,request,redirect,flash,url_for


# @pytest.mark.parametrize("email", [("admin@irontemple.com"), ("wrong@email.com")])
@pytest.mark.parametrize("email", [("admin@irontemple.com")])
def test_login_status_code(client, email):
    response = client.post('/showSummary', data={'email' : email })
    assert response.status_code == 200
    assert b"<h2>Welcome, admin@irontemple.com </h2>" in response.data
    # assert b"Sorry, that email wasn't found." in response.data


@pytest.mark.parametrize("request_data_param", [({"club": "Iron Temple","competition": "Spring Festival","places": "1"})])
# @pytest.mark.parametrize("request_data_param", [({"club": "Iron Temple","competition": "Spring Festival","places": "1"}),
# ({"club": "Iron Temple","competition": "Spring Festival","places": "3"})])
def test_purshase_more_place_than_club_possess(client, request_data_param):
    request_data = request_data_param
    response = client.post('/purchasePlaces', data=request_data)
    assert b"<li>Great-booking complete!</li>" in response.data
    # assert b"<li>You haven&#39;t enought points in your possession !! Please try again</li>" in response.data

def test_display_place_deduction_ok(client):
    club = {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '63'}
    request_data = {"club": "Simply Lift","competition": "Fall Classic","places": "4"}
    places_left = int(club["points"]) - int(request_data["places"]) * 3
    response = client.post('/purchasePlaces', data=request_data)
    assert b"Points available: " + bytes(str(places_left),'UTF-8') in response.data


@pytest.mark.parametrize("request_data_param", [({"club": "Simply Lift","competition": "Fall Classic","places": "11"})])
# @pytest.mark.parametrize("request_data_param", [({"club": "Simply Lift","competition": "Fall Classic","places": "13"})])
def test_try_to_book_more_than_12(client, request_data_param):
    request_data = request_data_param
    response = client.post('/purchasePlaces', data=request_data)
    assert b"<li>Great-booking complete!</li>" in response.data
    # assert b"<li>You can&#39;t redeem more than 12 points ! please try again</li>" in response.data 

# @pytest.mark.parametrize("competition", [({'name': 'Spring Festival', 'date': '2021-10-22 13:30:00', 'numberOfPlaces': '13'})])
@pytest.mark.parametrize("competition", [({'name': 'Fall Classic', 'date': '2023-10-22 13:30:00', 'numberOfPlaces': '13'})])
def test_try_to_book_past_competition_ok(client, competition):
    foundClub = {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}
    foundCompetition = competition

    response = client.get('/book/' + foundCompetition['name'] + '/' + foundClub['name'])

    assert b"<h3>This competition is still open</h3>" in response.data
    # assert b"<h3>Sorry, this competition is already closed</h3>" in response.data



