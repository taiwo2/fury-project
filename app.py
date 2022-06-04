#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(220))
    seeking_description = db.Column(db.String(300))

  # def __repr__(self):
  #   return f'<Venue {self.id} {self.name}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
  

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    address = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue_id'), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist_id'), nullable=True)
    artist_name = db.Column(db.Integer, db.ForeignKey('artist_name'), nullable=True)
    artist_image_link = db.Column(db.Integer, db.ForeignKey('artist_image_link'), nullable=True)
    start_time = db.Column(db.String(120))
    

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  return render_template('pages/venues.html', areas=Venue.query.order_by('id').all());

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data = list(filter(lambda d: d['id'] == venue_id, [Venue]))[0]
  return render_template('pages/show_venue.html', venue=Venue.query.order_by('id').all())

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  error = False
  form = VenueForm()
  try:
    if form.validate_on_submit():
      name = form.name.data
      phone = form.phone.data 
      image_link = form.image_link.data 
      facebook_link = form.facebook_link.data 
      website_link = form.website_link.data 
      genres = form.genres.data 
      seeking_description = form.seeking_description.data
    db.session.add()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash("An error occured. Venue could not be listed.")
    return redirect(url_for('shows'))
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  form = VenueForm()
  try:
    name = form.name.data
    data = Venue.query.get(venue_id)
    data.name = name
    db.session.commit()

  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=Artist.query.order_by('id').all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = list(filter(lambda d: d['id'] == artist_id, [Artist]))[0]
  return render_template('pages/show_artist.html', artist=Artist.query.order_by('id').all())

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  error = False
  form = ArtistForm()
  try:
    if form.validate_on_submit():
      name = form.name.data
    db.session.add()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('forms/edit_artist.html', form=form, artist=Artist.query.order_by('id').all())

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):


  return redirect(url_for('show_artist', artist_id=Artist.query.order_by('id').all()))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  error = False
  form = VenueForm()
  try:
    if form.validate_on_submit():
      name = form.name.data
    db.session.add()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('forms/edit_venue.html', form=form, venue=Venue.query.all())

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  return redirect(url_for('show_venue', venue_id=Venue.query.order_by('id').all()))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  form = ArtistForm()
  try:
    if form.validate_on_submit():
      name = form.name.data
      phone = form.phone.data 
      state = form.state.data 
      city = form.city.data 
      image_link = form.image_link.data 
      facebook_link = form.facebook_link.data 
      website_link = form.website_link.data 
      genres = form.genres.data 
      seeking_description = form.seeking_description.data
    db.session.add()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  # called upon submitting the new artist listing form
  if error:
    flash("on unsuccessful db insert, flash an error instead.")
    return redirect(url_for('artists'))
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/shows')
def shows():
  # displays list of shows at /shows
  return render_template('pages/shows.html', shows=Show.query.order_by('id').all())

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  form = ShowForm()
  try:
    if form.validate_on_submit():
      venue_id = form.venue_id.data
      artist_id = form.artist_id.data 
      start_time = form.start_time.data 
    db.session.add()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  # on successful db insert, flash success
  if error: 
    flash("on successful db insert, flash success")
    return redirect(url_for('artists'))
    flash('Show was successfully listed!')
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
