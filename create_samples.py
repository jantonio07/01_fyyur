from app import Venue, Artist, Show, db

art1 = Artist(
    name = "Guns N Petals RJJ",
    city = "San Francisco",
    state = "CA",
    phone = "326-123-5000",
    genres = "Rock n Roll",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    facebook_link = "https://www.facebook.com/GunsNPetals",
    website = "https://www.gunsnpetalsband.com",
    seeking_venue = True,
    seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!"
)

art2 = Artist(
    name = "Matt Quevedito",
    city = "New York",
    state = "NY",
    phone = "300-400-5000",
    genres = "Jazz",
    image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    facebook_link = "https://www.facebook.com/mattquevedo923251523",
)

art3 = Artist(
    name = "The Wild Sax Band GG",
    city = "San Francisco",
    state = "CA",
    phone = "432-325-5432",
    genres = "Jazz,Classical",
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
)


db.session.add_all([art1, art2, art3])
db.session.commit()

venue1 = Venue(
    name = "The Musical HHop",
    city = "San Francisco",
    state = "CA",
    address = "1015 Folsom Street",
    phone = "123-123-1234",
    genres = "Jazz,Reggae,Swing,Classical,Folk",
    image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    facebook_link = "https://www.facebook.com/TheMusicalHop",
    website = "https://www.themusicalhop.com",
    seeking_talent = True,
    seeking_description = "We are on the lookout for a local artist to play every two weeks. Please call us."
)

venue2 = Venue(
    name = "The Dueling Pianos Bar OO",
    city = "New York",
    state = "NY",
    address = "335 Delancey Street",
    phone = "914-003-1132",
    genres = "Classical,R&B,Hip-Hop",
    image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    facebook_link = "https://www.facebook.com/theduelingpianos",
    website = "https://www.theduelingpianos.com",
)

venue3 = Venue(
    name = "Park Circle Live Music & Coffee",
    city = "San Francisco",
    state = "CA",
    address = "34 Whiskey Moore Ave",
    phone = "415-000-1234",
    genres = "Rock n Roll,Jazz,Classical,Folk",
    image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    facebook_link = "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    website = "https://www.parksquarelivemusicandcoffee.com",
)

db.session.add_all([venue1, venue2, venue3])
db.session.commit()

show_data = [{
"venue_id": 1,
"venue_name": "The Musical Hop",
"artist_id": 1,
"artist_name": "Guns N Petals",
"artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
"start_time": "2019-05-21T21:30:00.000Z"
}, {
"venue_id": 3,
"venue_name": "Park Square Live Music & Coffee",
"artist_id": 2,
"artist_name": "Matt Quevedo",
"artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
"start_time": "2019-06-15T23:00:00.000Z"
}, {
"venue_id": 3,
"venue_name": "Park Square Live Music & Coffee",
"artist_id": 3,
"artist_name": "The Wild Sax Band",
"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
"start_time": "2035-04-01T20:00:00.000Z"
}, {
"venue_id": 3,
"venue_name": "Park Square Live Music & Coffee",
"artist_id": 3,
"artist_name": "The Wild Sax Band",
"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
"start_time": "2035-04-08T20:00:00.000Z"
}, {
"venue_id": 3,
"venue_name": "Park Square Live Music & Coffee",
"artist_id": 3,
"artist_name": "The Wild Sax Band",
"artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
"start_time": "2035-04-15T20:00:00.000Z"
}]

shows_list = []
for show in show_data:
    s = Show(
        artist_id = show["artist_id"],
        venue_id = show["venue_id"],
        start_time = show["start_time"],
        artist_image_link = show["artist_image_link"]
    )
    shows_list.append(s)

db.session.add_all(shows_list)
db.session.commit()
