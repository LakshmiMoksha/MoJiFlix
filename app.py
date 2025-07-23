from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            movie TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            persons INTEGER NOT NULL,
            seats TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def index():
    movies = [
        {"title": "Devara", "image": "movie1.jpg"},
        {"title": "Pushpa 2", "image": "movie2.jpg"},
        {"title": "Guntur Kaaram", "image": "movie3.jpg"},
        {"title": "Salaar", "image": "movie4.jpg"},
        {"title": "HIT 3", "image": "movie5.jpg"}
    ]
    return render_template('index.html', movies=movies)

# Booking Form
@app.route('/book/<movie_name>')
def book_form(movie_name):
    return render_template('book.html', movie=movie_name)

# Handle Booking Form Submission
@app.route('/book', methods=['POST'])
def book_ticket():
    name = request.form['name']
    movie = request.form['movie']
    date = request.form['date']
    time = request.form['time']
    persons = request.form['persons']

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO bookings (name, movie, date, time, persons)
        VALUES (?, ?, ?, ?, ?)
    """, (name, movie, date, time, persons))
    booking_id = c.lastrowid
    conn.commit()
    conn.close()

    return redirect(url_for('select_seats', booking_id=booking_id))


# Show Seat Selection UI
@app.route('/seats')
def select_seats():
    booking_id = request.args.get('booking_id')

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT movie, date, time FROM bookings WHERE id = ?", (booking_id,))
    result = c.fetchone()

    if not result:
        return "Booking not found.", 404

    movie, date, time = result

    c.execute("""
        SELECT seats FROM bookings 
        WHERE movie = ? AND date = ? AND time = ? AND seats IS NOT NULL
    """, (movie, date, time))
    seat_rows = c.fetchall()
    conn.close()

    booked_seats = set()
    for row in seat_rows:
        if row[0]:
            booked_seats.update(row[0].split(','))

    return render_template('seats.html', booking_id=booking_id, booked_seats=booked_seats)

# Save Selected Seats
@app.route('/seats', methods=['POST'])
def save_seats():
    booking_id = request.form['booking_id']
    selected_seats = request.form['selected_seats']

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("UPDATE bookings SET seats = ? WHERE id = ?", (selected_seats, booking_id))
    conn.commit()

    c.execute("SELECT id, name, movie, date, time, persons, seats FROM bookings WHERE id = ?", (booking_id,))
    booking = c.fetchone()

    conn.close()

    total_price = calculate_price(selected_seats)

    return render_template('success.html', booking=booking, total_price=total_price)

# Pricing Logic
def calculate_price(seats):
    platinum = gold = silver = 0
    for seat in seats.split(','):
        seat = seat.strip().upper()
        if seat.startswith(('A', 'B', 'C', 'D')):
            platinum += 1
        elif seat.startswith(('E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M')):
            gold += 1
        elif seat.startswith(tuple("NOPQRSTUVWXYZ")):
            silver += 1
    return platinum * 700 + gold * 500 + silver * 300

# View All Bookings
@app.route('/view_bookings')
def view_bookings():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT id, name, movie, date, time, persons, seats FROM bookings")

    bookings = c.fetchall()
    conn.close()
    return render_template('view_bookings.html', bookings=bookings)

# Individual Booking
@app.route('/my_booking/<int:booking_id>')
def my_booking(booking_id):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT id, name, movie, date, time, persons, seats FROM bookings WHERE id = ?", (booking_id,))
    booking = c.fetchone()
    conn.close()
    return render_template('my_booking.html', booking=booking)

# Clear All Bookings
@app.route('/clear_bookings', methods=['POST'])
def clear_bookings():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("DELETE FROM bookings")
    conn.commit()
    conn.close()
    return redirect(url_for('view_bookings'))

if __name__ == '__main__':
    app.run(debug=True)
