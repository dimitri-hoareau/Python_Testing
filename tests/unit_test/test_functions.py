from http import server
from server import find_club_or_competition, find_club_or_competition_for_booking

def test_find_club_or_competion():
    list_club_or_contest = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'}, {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}, {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]
    key1 = 'email'
    key2 = 'john@simplylift.co'
    assert find_club_or_competition(list_club_or_contest, key1, key2) == {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'}


def test_find_club_or_competition_for_booking():
    list_club_or_contest = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'}, {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}, {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]
    key1 = 'name'
    key2 = 'Iron Temple'
    assert find_club_or_competition_for_booking(list_club_or_contest, key1, key2) == {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}

