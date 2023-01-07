# Initialize the database
import sqlite3
from datetime import datetime

#Create database
"""conn = sqlite3.connect("bookings.db")

conn.execute(
    "CREATE TABLE IF NOT EXISTS bookings (booking_ref TEXT, check_in_date DATETIME, check_out_date datetime, num_rooms INTEGER, num_guests INTEGER)"
)
conn.execute(
    "CREATE TABLE IF NOT EXISTS guesthouse (id INTEGER PRIMARY KEY, name TEXT, location TEXT, description TEXT)"
)
conn.execute(
    "INSERT INTO guesthouse VALUES (1, 'Sunny Seaside Inn', 'Seaside Town', 'A cozy and affordable guesthouse by the sea.')"
)

conn.commit()
conn.close()
"""
# Insert a booking into the database
def insert_booking(booking):
    # Connect to the database
    conn = sqlite3.connect("bookings.db")

    # Insert the booking
    conn.execute(
        "INSERT INTO bookings (booking_ref, check_in_date, check_out_date, num_rooms, num_guests) VALUES (?, ?, ?, ?, ?)",
        (booking["tg_id"], booking["check_in_date"], booking["check_out_date"], int(booking["num_rooms"]), 0),
    )

    # Save (commit) the changes
    conn.commit()

    # Close the connection
    conn.close()

# Find bookings in the database
def find_bookings(query):
    # Connect to the database
    conn = sqlite3.connect("bookings.db")
    date_time1 = datetime.strptime(query["check_out_date"]+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    date_time2 = datetime.strptime(query["check_in_date"]+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    # Find bookings
    cursor = conn.execute(
        "SELECT * FROM bookings WHERE check_in_date <= ? AND check_out_date >= ?", (date_time1, date_time2)
    )

    # Fetch the results
    bookings = cursor.fetchall()

    # Close the connection
    conn.close()

    return bookings

# Find unbookings in the database
def find_unbookings(query):
    # Connect to the database
    conn = sqlite3.connect("bookings.db")
    # Find bookings
    date_time1 = datetime.strptime(query["check_out_date"]+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    date_time2 = datetime.strptime(query["check_in_date"]+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    cursor = conn.execute(
        "SELECT * FROM bookings WHERE (check_in_date > ?) or (check_out_date < ?) ", (date_time1,date_time2)
    )

    # Fetch the results
    bookings = cursor.fetchall()

    # Close the connection
    conn.close()

    return bookings

# Find tek unbookings in the database
def find_tek_unbookings(query):
    # Connect to the database
    conn = sqlite3.connect("bookings.db")
    # Find bookings
    date_time1 = datetime.strptime(query["check_out_date"]+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    date_time2 = datetime.strptime(query["check_in_date"]+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    cursor = conn.execute(
        "SELECT * FROM bookings WHERE ((check_in_date > ? and check_in_date > ?) or (check_out_date < ? and check_out_date < ?)) and num_rooms == ?", (date_time1, date_time2, date_time1, date_time2, query["num_rooms"])
    )

    # Fetch the results
    bookings = cursor.fetchall()

    # Close the connection
    conn.close()

    return (len(bookings) > 0)

# Delete a booking from the database
def delete_booking(booking_ref):
    # Connect to the database
    conn = sqlite3.connect("bookings.db")

    # Delete the booking
    conn.execute("DELETE FROM bookings WHERE booking_ref = ?", (booking_ref,))

    # Save (commit) the changes
    conn.commit()

    # Close the connection
    conn.close()

# About hotel
def hotel_about():
    conn = sqlite3.connect("bookings.db")

    data = conn.execute("SELECT * FROM guesthouse")
    data = data.fetchall()

    # Close the connection
    conn.close()

    return data[0]

# /insert_booking({"check_in_date":"2022-12-23","check_out_date":"2022-12-23","num_rooms":"9","tg_id":"123345"})
