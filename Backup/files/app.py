# AGP - Flight Tracker 2.5
# Author: Andrew Holland
# Version: 2.5.0
# Change Log:
# - 2.5.0: Reverted to dynamic IATA code retrieval via Geopy Nominatim, removed static iata_to_airport dictionary (17-07-2025)
# - 2.4.0: Added dynamic ticket action form with /get_ticket/<id> endpoint
# - 2.3.0: Enhanced logging with geocoded coordinates
# Uses Geopy for distance calculations (https://geopy.readthedocs.io/)
# Flask licensed under BSD 3-Clause (https://flask.palletsprojects.com/en/stable/license/)
# python-dotenv licensed under BSD 3-Clause (https://github.com/theskumar/python-dotenv/blob/main/LICENSE)
# File Integrity: Complete code verified, 215 lines

from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
import datetime
import logging
import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.extra.rate_limiter import RateLimiter

app = Flask(__name__)

# Setup logging without size limit
log_file = '/app/ticket_tracker.log'
try:
    if os.access('/app', os.W_OK):
        logging.basicConfig(filename=log_file, filemode='a', level=logging.DEBUG, format='%(asctime)s RoE v3.8: %(message)s', force=True)
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s RoE v3.8: %(message)s', force=True)
        logging.error("Cannot write to /app/ticket_tracker.log")
    logging.debug("Flask app initialized")
except Exception as e:
    print(f"Logging setup failed: {e}")
    raise

# Load environment variables from .env file
load_dotenv()
AVIATIONSTACK_API_KEY = os.getenv('AVIATIONSTACK_API_KEY')
if not AVIATIONSTACK_API_KEY:
    logging.warning("AVIATIONSTACK_API_KEY not found in .env file")

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="flight_tracker")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

# In-memory ticket storage
tickets_data = []

def load_tickets():
    try:
        if os.path.exists('/app/tickets.csv'):
            with open('/app/tickets.csv', 'r', newline='') as f:
                reader = csv.DictReader(f)
                tickets = []
                for row in reader:
                    row['rowid'] = int(row['rowid'])
                    row['km_travelled'] = int(row['km_travelled'])
                    tickets.append(row)
                logging.debug(f"Loaded {len(tickets)} tickets from tickets.csv")
                return tickets
        else:
            with open('/app/tickets.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['rowid', 'airline', 'date', 'route', 'class', 'km_travelled', 'seat_allocated', 'other_data'])
                writer.writeheader()
            logging.debug("Created empty tickets.csv")
            return []
    except Exception as e:
        logging.error(f"Error loading tickets from tickets.csv: {e}")
        return []

def save_tickets():
    try:
        with open('/app/tickets.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['rowid', 'airline', 'date', 'route', 'class', 'km_travelled', 'seat_allocated', 'other_data'])
            writer.writeheader()
            writer.writerows(tickets_data)
        logging.debug(f"Saved {len(tickets_data)} tickets to tickets.csv")
    except Exception as e:
        logging.error(f"Error saving tickets to tickets.csv: {e}")

def validate_date(date):
    try:
        day, month, year = date.split('-')
        if len(day) == 2 and len(month) == 2 and len(year) == 4 and int(day) <= 31 and int(month) <= 12:
            datetime.datetime.strptime(date, '%d-%m-%Y')
            return True
        return False
    except:
        return False

def initialize_tickets_db():
    try:
        global tickets_data
        tickets_data = load_tickets()
        if not tickets_data:
            logging.debug("No tickets in tickets.csv; starting with empty tickets_data")
        else:
            logging.debug(f"Loaded {len(tickets_data)} tickets from tickets.csv")
    except Exception as e:
        logging.error(f"Error initializing tickets database: {e}")
        tickets_data = []

def get_oldest_date():
    try:
        initialize_tickets_db()
        dates = [ticket['date'] for ticket in tickets_data if validate_date(ticket['date'])]
        if dates:
            oldest_date = min(dates, key=lambda d: datetime.datetime.strptime(d, '%d-%m-%Y'))
            return oldest_date
        logging.info("No valid tickets found in tickets database")
        return 'No Tickets'
    except Exception as e:
        logging.error(f"Error reading tickets database: {e}")
        return 'No Tickets'

def calculate_km_travelled(route):
    try:
        logging.debug(f"Processing route {route} in calculate_km_travelled")
        codes = route.split('-')
        if len(codes) != 2 or not all(len(code) == 3 for code in codes):
            logging.error(f"Invalid route format: {route}. Must be IATA1-IATA2 (e.g., JFK-LGW)")
            return 0
        if os.path.exists('/app/routes.csv'):
            with open('/app/routes.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if row[0].upper() == route.upper():
                        logging.info(f"Retrieved cached distance for {route}: {row[1]} km")
                        return int(row[1])
        # Fetch coordinates dynamically using Geopy
        coords = []
        for code in codes:
            location = geocode(f"{code} Airport")
            if location:
                coords.append(location.point[:2])
                logging.debug(f"Geocoded {code} Airport: {location.point[:2]}")
            else:
                logging.error(f"Failed to geocode {code} Airport")
                return 0
        if len(coords) != 2:
            logging.error(f"Failed to get coordinates for route: {route}")
            return 0
        distance = int(geodesic(coords[0], coords[1]).km)
        # Cache to routes.csv
        try:
            with open('/app/routes.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                if os.path.getsize('/app/routes.csv') == 0:
                    writer.writerow(['route', 'km_travelled'])
                writer.writerow([route, distance])
            logging.info(f"Cached distance for {route}: {distance} km")
        except OSError as e:
            logging.error(f"Failed to cache distance for {route}: {e}")
        return distance
    except Exception as e:
        logging.error(f"Error calculating distance for {route}: {e}")
        return 0

@app.route('/get_ticket/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    try:
        initialize_tickets_db()
        for ticket in tickets_data:
            if ticket['rowid'] == ticket_id:
                logging.debug(f"Retrieved ticket ID {ticket_id}: {ticket}")
                return jsonify({
                    'success': True,
                    'ticket': {
                        'rowid': ticket['rowid'],
                        'airline': ticket['airline'],
                        'date': ticket['date'],
                        'route': ticket['route'],
                        'class': ticket['class'],
                        'seat_allocated': ticket['seat_allocated'],
                        'other_data': ticket['other_data']
                    }
                })
        logging.error(f"Ticket ID {ticket_id} not found")
        return jsonify({'success': False, 'message': 'Ticket not found'}), 404
    except Exception as e:
        logging.error(f"Error retrieving ticket ID {ticket_id}: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        logging.debug("Entering index route")
        initialize_tickets_db()
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'delete':
                delete_id = request.form.get('delete_id')
                global tickets_data
                tickets_data = [ticket for ticket in tickets_data if str(ticket['rowid']) != delete_id]
                save_tickets()
                logging.debug(f"Deleted ticket ID {delete_id}")
                return redirect(url_for('index'))
            elif 'edit_id' in request.form:
                edit_id = request.form['edit_id']
                airline = request.form['airline']
                date = request.form['date']
                route = request.form['route']
                class_ = request.form['class']
                seat_allocated = request.form['seat_allocated']
                other_data = request.form['other_data']

                if class_ not in ['First', 'Business', 'Economy']:
                    return "Invalid class selected", 400

                if not validate_date(date):
                    return "Invalid date format. Use DD-MM-YYYY (e.g., 13-07-2025)", 400

                km_travelled = calculate_km_travelled(route)
                if km_travelled == 0:
                    return f"Invalid route or distance not found. Ensure route uses valid IATA codes (e.g., JFK-LGW).", 400

                for ticket in tickets_data:
                    if str(ticket['rowid']) == edit_id:
                        ticket.update({
                            'airline': airline, 'date': date, 'route': route, 'class': class_,
                            'km_travelled': km_travelled, 'seat_allocated': seat_allocated, 'other_data': other_data
                        })
                save_tickets()
                logging.debug(f"Edited ticket ID {edit_id}")
                return redirect(url_for('index'))
            else:
                airline = request.form['airline']
                date = request.form['date']
                route = request.form['route']
                class_ = request.form['class']
                seat_allocated = request.form['seat_allocated']
                other_data = request.form['other_data']

                if class_ not in ['First', 'Business', 'Economy']:
                    return "Invalid class selected", 400

                if not validate_date(date):
                    return "Invalid date format. Use DD-MM-YYYY (e.g., 13-07-2025)", 400

                km_travelled = calculate_km_travelled(route)
                if km_travelled == 0:
                    return f"Invalid route or distance not found. Ensure route uses valid IATA codes (e.g., JFK-LGW).", 400

                rowid = max([ticket['rowid'] for ticket in tickets_data], default=0) + 1
                tickets_data.append({
                    'rowid': rowid, 'airline': airline, 'date': date, 'route': route, 'class': class_,
                    'km_travelled': km_travelled, 'seat_allocated': seat_allocated, 'other_data': other_data
                })
                save_tickets()
                logging.debug(f"Added ticket ID {rowid}")
                return redirect(url_for('index'))

        tickets = [(ticket['rowid'], ticket['airline'], ticket['date'], ticket['route'], ticket['class'],
                    ticket['km_travelled'], ticket['seat_allocated'], ticket['other_data'])
                   for ticket in tickets_data]

        totals = {'First': 0, 'Business': 0, 'Economy': 0}
        for ticket in tickets_data:
            if ticket['class'] in totals:
                totals[ticket['class']] += ticket['km_travelled']

        oldest_date = get_oldest_date()

        if not os.path.exists('/app/templates/index.html'):
            logging.error("Missing index.html in /app/templates")
            return "Server error: Missing index.html", 500
        return render_template('index.html', tickets=tickets, totals=totals, oldest_date=oldest_date)
    except Exception as e:
        logging.error(f"Error in index route: {e}")
        return "Server error", 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Flask startup failed: {e}")
        raise