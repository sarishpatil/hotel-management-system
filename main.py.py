import os
import random
import mysql.connector


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "") 

TOTAL_ROOM_CAPACITY = {
    "Single": 5,
    "Double": 3,
    "Suite": 2
}

ROOM_PRICES = {
    "Single": 100,
    "Double": 150,
    "Suite": 250
}


def connect_db(include_db=True):
    kwargs = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD
    }
    if include_db:
        kwargs["database"] = "hotel"
    return mysql.connector.connect(**kwargs)


def setup_database():
    # Connect to MySQL server without specifying database to create 'hotel' safely first
    conn = connect_db(include_db=False)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS hotel")
    conn.close()

    # Connect directly to the 'hotel' database to initialize table
    conn = connect_db(include_db=True)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT PRIMARY KEY,
        customer_name VARCHAR(100),
        room_type VARCHAR(50),
        nights INT,
        total_cost FLOAT,
        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()


def get_available_rooms():
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT room_type, COUNT(*) FROM bookings GROUP BY room_type")
    booked_counts = dict(cursor.fetchall())
    conn.close()

    available = {}
    for room, capacity in TOTAL_ROOM_CAPACITY.items():
        booked = booked_counts.get(room, 0)
        available[room] = capacity - booked
    return available


def generate_booking_id():
    return random.randint(10000, 99999)


def get_price(room_type, nights):
    return ROOM_PRICES.get(room_type, 0) * nights


def pause():
    while True:
        choice = input("\nType 'B' to go back to the main menu: ").strip().lower()
        if choice == 'b':
            break
        print("Invalid input. Please type 'B'.")


def print_line():
    print("-" * 60)


# ----------------- Main Booking Logic ------------------

def book_room():
    print_line()
    print("HOTEL BOOKING SYSTEM")
    print_line()

    available_rooms = get_available_rooms()

    name = input("Enter your full name: ").strip()
    room_type = input("Room Type (Single/Double/Suite): ").strip().title()

    if room_type not in ROOM_PRICES:
        print("Invalid room type selected.")
        pause()
        return

    if available_rooms.get(room_type, 0) <= 0:
        print(f"Sorry, no {room_type} rooms available.")
        pause()
        return

    try:
        nights = int(input("Number of nights: "))
        if nights <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid positive number.")
        pause()
        return

    booking_id = generate_booking_id()
    total_cost = get_price(room_type, nights)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO bookings (booking_id, customer_name, room_type, nights, total_cost)
    VALUES (%s, %s, %s, %s, %s)
    """, (booking_id, name, room_type, nights, total_cost))
    conn.commit()
    conn.close()

    print("\nBooking Confirmed!")
    print(f"Booking ID: {booking_id}")
    print(f"Name: {name}")
    print(f"Room Type: {room_type}")
    print(f"Nights: {nights}")
    print(f"Total Cost: ${total_cost}")
    pause()


def view_all_bookings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()

    print_line()
    print("ALL BOOKINGS")
    print_line()

    if not bookings:
        print("No bookings found.")
    else:
        for b in bookings:
            print(f"ID: {b[0]} | Name: {b[1]} | Room: {b[2]} | Nights: {b[3]} | Total: ${b[4]} | Date: {b[5]}")
    pause()


def search_booking():
    try:
        booking_id = int(input("Enter Booking ID to search: "))
    except ValueError:
        print("Invalid input.")
        pause()
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
    booking = cursor.fetchone()
    conn.close()

    print_line()
    print("BOOKING DETAILS")
    print_line()

    if booking:
        print(f"ID: {booking[0]}\nName: {booking[1]}\nRoom: {booking[2]}\nNights: {booking[3]}\nTotal: ${booking[4]}\nDate: {booking[5]}")
    else:
        print("No booking found with that ID.")
    pause()


def delete_booking():
    try:
        booking_id = int(input("Enter Booking ID to delete: "))
    except ValueError:
        print("Invalid input.")
        pause()
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT room_type FROM bookings WHERE booking_id = %s", (booking_id,))
    result = cursor.fetchone()

    if not result:
        print("Booking ID not found.")
    else:
        cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
        conn.commit()
        print("Booking deleted successfully.")

    conn.close()
    pause()


def show_availability():
    print_line()
    print("ROOM AVAILABILITY")
    print_line()
    available_rooms = get_available_rooms()
    for room, count in available_rooms.items():
        print(f"{room} Rooms Available: {count}")
    pause()


def show_menu():
    while True:
        print_line()
        print("HOTEL MANAGEMENT SYSTEM")
        print_line()
        print("1. Book a Room")
        print("2. View All Bookings")
        print("3. Search Booking by ID")
        print("4. Delete a Booking")
        print("5. Show Room Availability")
        print("6. Exit")
        print_line()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            book_room()
        elif choice == '2':
            view_all_bookings()
        elif choice == '3':
            search_booking()
        elif choice == '4':
            delete_booking()
        elif choice == '5':
            show_availability()
        elif choice == '6':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    setup_database()
    show_menu()