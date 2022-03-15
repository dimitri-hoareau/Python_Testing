import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = 'something_special'

    def loadClubs():
        with open('clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs


    def loadCompetitions():
        with open('competitions.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions


    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
        except IndexError:
            return "Sorry, that email wasn't found."
        return render_template('welcome.html',club=club,competitions=competitions)


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]

        now = datetime.now()
        date_time_now = now.strftime("%Y-%m-%d %H:%M:%S")
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition, date=date_time_now)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        print(request.form)
        point_club = club["points"]
        places_competition = competition["numberOfPlaces"]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club["points"] = int(club["points"]) - placesRequired
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

