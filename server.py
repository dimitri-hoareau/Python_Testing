import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def find_club_or_competition(list_of_club_or_contest , key1, key2 ):
    return [club for club in list_of_club_or_contest if club[key1] == key2][0]

def find_club_or_competition_for_booking(list_of_club_or_contest, key1, key2 ):
    return [c for c in list_of_club_or_contest if c[key1] == key2][0]

def places_deduction(club_points, places_required):
    return int(club_points) - places_required * 3


competitions = loadCompetitions()
clubs = loadClubs()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        try:
            club = find_club_or_competition(clubs, 'email', request.form['email'])
            # club = [club for club in clubs if club['email'] == request.form['email']][0]
        except IndexError:
            return "Sorry, that email wasn't found."
        return render_template('welcome.html',club=club,competitions=competitions)


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        # foundClub = [c for c in clubs if c['name'] == club][0]
        # foundCompetition = [c for c in competitions if c['name'] == competition][0]
        foundClub = find_club_or_competition_for_booking(clubs, 'name', club)
        foundCompetition = find_club_or_competition_for_booking(competitions, 'name', competition)

        now = datetime.now()
        date_time_now = now.strftime("%Y-%m-%d %H:%M:%S")
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition, date=date_time_now)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition = find_club_or_competition(competitions, 'name', request.form['competition'])
        club = find_club_or_competition(clubs, 'name', request.form['club'] )
        # competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        # club = [c for c in clubs if c['name'] == request.form['club']][0]
        point_club = club["points"]
        places_competition = competition["numberOfPlaces"]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        # club["points"] = int(club["points"]) - placesRequired * 3
        club["points"] = places_deduction(club["points"], placesRequired)
        if club["points"] >= 0:
            if placesRequired > 12:
                club["points"] = point_club
                competition["numberOfPlaces"] = places_competition
                flash("You can't redeem more than 12 points ! please try again")
                return render_template('welcome.html', club=club, competitions=competitions)

            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            club["points"] = point_club
            competition["numberOfPlaces"] = places_competition
            flash("You haven't enought points in your possession !! Please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route("/clubs")
    def list_clubs():
        return render_template(
            "clubs.html",
            clubs=clubs,
        )

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))


    return app

