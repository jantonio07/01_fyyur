#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler, error
from forms import *
from sqlalchemy import exc
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    phone = db.Column(db.String)
    genres = db.Column(db.String)
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)

    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
      return f'<Venue name={self.name}, city={self.city}, state={self.state}, address={self.address}>'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)
    phone = db.Column(db.String)
    genres = db.Column(db.String, nullable = False)
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)

    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
      return f'<Artist name={self.name}, city={self.city}, state={self.state}, genres={self.genres}>'

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key = True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable = False, server_default = db.func.now())
    artist_image_link = db.Column(db.String)

    def __repr__(self):
      return f'<artist_id={self.artist_id}, venue_id={self.venue_id}>'


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

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
  query = db.session.query(Venue.id, Venue.name, Venue.city, Venue.state).all()
  reg = {}
  for q in query:
    key = (q.city, q.state)
    if not key in reg:
      reg[key] = []
    reg[key].append({
      "id": str(q.id),
      "name": str(q.name)
    })
  data = [{"city": key[0], "state": key[1], "venues": reg[key]} for key in reg]
  # NOTE: num_upcoming_shows is not being used in pages/venues.html, so no need to include it, I guess
  return render_template('pages/venues.html', areas = data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  query = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()
  response = {
    "count": len(query),
    "data": [
      {
        "id": q.id,
        "name": q.name
      }
      for q in query
    ]
  }
  # NOTE: num_upcoming_shows is not being used in pages/search_venues.html, so no need to include it, I guess
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

def filter_shows_for_venues(shows):
  past_shows = []
  upcoming_shows = []
  for show in shows:
    artist_data = Artist.query.filter_by(id = show.artist_id).first()
    show_d = {
      "artist_id": show.artist_id,
      "artist_name": artist_data.name,
      "artist_image_link": artist_data.image_link,
      "start_time": show.start_time.strftime("%a, %d %b %Y %H:%M:%S +0000")
    }
    if show.start_time < datetime.now():
      past_shows.append(show_d)
    else:
      upcoming_shows.append(show_d)
  return past_shows, upcoming_shows

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  query = Venue.query.filter_by(id = venue_id).first()

  if query is None:
    return abort(404)

  past_shows, upcoming_shows = filter_shows_for_venues(query.shows)

  data = {
    "id": query.id,
    "name": query.name,
    "genres": query.genres.split(","),
    "address": query.address,
    "city": query.city,
    "state": query.state,
    "phone": query.phone,
    "website": query.website,
    "facebook_link": query.facebook_link,
    "seeking_talent": query.seeking_talent,
    "seeking_description": query.seeking_description,
    "image_link": query.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_venue.html', venue = data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error_message = None
  try:
    data = VenueForm(request.form)
    venue = Venue(
      name = data.name.data,
      city = data.city.data,
      state = data.state.data,
      address = data.address.data,
      phone = data.phone.data,
      genres = ','.join(data.genres.data),
      facebook_link = data.facebook_link.data,
      image_link = data.image_link.data,
      website = data.website_link.data,
      seeking_talent = data.seeking_talent.data,
      seeking_description = data.seeking_description.data
    )
    db.session.add(venue)
    db.session.commit()
  except exc.SQLAlchemyError as error:
    print(error)
    if error_message is None:
      error_message = "Something went wrong, please try again."
    db.session.rollback()
  finally:
    if error_message:
      flash(error_message, category="error")
      return create_venue_form()
    else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return redirect(url_for('show_venue', venue_id = venue.id))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except exc.SQLAlchemyError as excError:
    print(excError)
    error = str(excError.__dict__['orig'])
    print()
    print("JOGALLAR")
    print(error)
    print()
    db.session.rollback()
  finally:
    if error:
      return jsonify({"success": False, "error": error})
    else:
      return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  query = db.session.query(Artist.id, Artist.name).all()
  data = [{"id": q.id, "name": q.name} for q in query]
  return render_template('pages/artists.html', artists = data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  query = Artist.query.filter(Artist.name.ilike("%" + search_term + "%")).all()
  response = {
    "count": len(query),
    "data": [
      {
        "id": q.id,
        "name": q.name
      }
      for q in query
    ]
  }
  # NOTE: num_upcoming_shows is not being used in pages/search_artists.html, so no need to include it, I guess
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


def filter_shows_for_artists(shows):
  past_shows = []
  upcoming_shows = []
  for show in shows:
    venue_data = Venue.query.filter_by(id = show.venue_id).first()
    show_d = {
      "venue_id": show.venue_id,
      "venue_name": venue_data.name,
      "venue_image_link": venue_data.image_link,
      "start_time": show.start_time.strftime("%a, %d %b %Y %H:%M:%S +0000")
    }
    if show.start_time < datetime.now():
      past_shows.append(show_d)
    else:
      upcoming_shows.append(show_d)
  return past_shows, upcoming_shows

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  query = Artist.query.filter_by(id = artist_id).first()

  if query is None:
    return abort(404)

  past_shows, upcoming_shows = filter_shows_for_artists(query.shows)

  data = {
    "id": query.id,
    "name": query.name,
    "genres": query.genres.split(","),
    "city": query.city,
    "state": query.state,
    "phone": query.phone,
    "website": query.website,
    "facebook_link": query.facebook_link,
    "seeking_venue": query.seeking_venue,
    "seeking_description": query.seeking_description,
    "image_link": query.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  query = Artist.query.filter_by(id = artist_id).first()
  if query is None:
    return abort(404)
  form = ArtistForm(formdata = None, data = {
    'id': query.id,
    'name': query.name,
    'genres': query.genres.split(','),
    'city': query.city,
    'state': query.state,
    'phone': query.phone,
    'website': query.website,
    'facebook_link': query.facebook_link,
    'seeking_venue': query.seeking_venue,
    'seeking_description': query.seeking_description,
    'image_link': query.image_link
  })
  return render_template('forms/edit_artist.html', form=form, artist=query)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  query = Artist.query.filter_by(id=artist_id).first()
  if query is None:
      abort(404)
  form = ArtistForm(request.form)
  form.genres.data = ', '.join(form.genres.data)
  if "seeking_venue" in request.form:
      form.seeking_venue.data = True
  else:
      form.seeking_venue.data = False
  form.populate_obj(query)
  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  query = Venue.query.filter_by(id = venue_id).first()
  if query is None:
    return abort(404)
  form = VenueForm(formdata = None, data = {
    'id': query.id,
    'name': query.name,
    'genres': query.genres.split(','),
    "address": query.address,
    'city': query.city,
    'state': query.state,
    'phone': query.phone,
    'website': query.website,
    'facebook_link': query.facebook_link,
    'seeking_talent': query.seeking_talent,
    'seeking_description': query.seeking_description,
    'image_link': query.image_link
  })
  return render_template('forms/edit_venue.html', form = form, venue = query)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  query = Venue.query.filter_by(id=venue_id).first()
  if query is None:
        abort(404)
  form = VenueForm(request.form)
  form.genres.data = ', '.join(form.genres.data)
  form.populate_obj(query)
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error_message = None
  try:
    if "seeking_venue" in request.form:
      seeking_venue = True
    else:
      seeking_venue = False
    data = ArtistForm(request.form)
    artist = Artist(
      name = data.name.data,
      city = data.city.data,
      state = data.state.data,
      phone = data.phone.data,
      genres = ','.join(data.genres.data),
      facebook_link = data.facebook_link.data,
      image_link = data.image_link.data,
      website = data.website_link.data,
      seeking_venue = seeking_venue,
      seeking_description = data.seeking_description.data
    )
    db.session.add(artist)
    db.session.commit()
  except exc.SQLAlchemyError as error:
    print(error)
    if error_message is None:
      error_message = "Something went wrong, please try again."
    db.session.rollback()
  finally:
    if error_message:
      flash(error_message, category="error")
      return create_artist_form()
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return redirect(url_for('show_artist', artist_id = artist.id))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  query = db.session.query(Show, Artist, Venue).select_from(Show).join(Artist).join(Venue).all()
  data = [
    {
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.strftime("%a, %d %b %Y %H:%M:%S +0000")
    }
    for (show, artist, venue) in query
  ]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error_message = None
  try:
    data = ShowForm(request.form)
    show = Show(
      artist_id = data.artist_id.data,
      venue_id = data.venue_id.data,
      start_time = data.start_time.data
    )
    db.session.add(show)
    db.session.commit()
  except:
    if error_message is None:
      error_message = "Something went wrong, please try again."
    db.session.rollback()
  finally:
    if error_message:
      flash(error_message, category="error")
      return create_shows()
    else:
      flash('Show was successfully listed!')
      return redirect(url_for('shows'))

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
