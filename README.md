# MojiFlix — Movie Ticket Booking System

MojiFlix is a web-based movie ticket booking system built with Flask and SQLite.
It enables users to browse available movies, submit booking details, select seats with real-time availability checks, and receive a detailed booking summary.
The application includes an integrated pricing model, dynamic seat mapping, and database-driven record management.

---

# Tech Stack

*Frontend*: HTML5, CSS3, Bootstrap
*Backend*: Flask (Python), Jinja2
*Database*: SQLite
*Deployment*: Render (or any Flask-supported hosting)

---

#Features
*Movie Selection*

- Displays available movies with posters and titles

- Direct navigation to the booking form for each movie

*Ticket Booking*

- Customer details, movie selection, date, time, and number of persons

- Server-side validation for booking information

- Automatic creation of a booking record in the database

- Seat Selection

- Interactive seat layout rendered through Jinja2

- Real-time detection of previously booked seats for the same show

- Seat categories defined based on row:

    - Platinum: Rows A–D

    - Gold: Rows E–M

    - Silver: Rows N–Z

*Pricing Model*

- Platinum seats: ₹700

- Gold seats: ₹500

- Silver seats: ₹300

Total cost calculated automatically based on selected seats

*Booking Management*

- List of all bookings with customer and screening details

- Individual booking details with seat information

- Option to clear all bookings from the database

- All records stored persistently in SQLite

---

# Future Improvements

- PDF ticket generation

- Real-time seat locking to avoid concurrent conflicts

- Movie descriptions, trailers, and metadata

- Enhanced interface using modern UI frameworks

- Search and filter options for bookings
