# AGP - Flight Tracker 2.5
A Flask-based web application for tracking flight data, deployed on Synology NAS with DSM’s Container Manager, embracing a Cyberpunk Monk aesthetic.

## Overview
AGP - Flight Tracker 2.5 enables users to enter and manage flight data from boarding passes, calculating "Km Travelled" for First, Business, and Economy classes with a grand total. It uses Geopy’s Nominatim API for dynamic IATA code coordinate retrieval and caches distances in `routes.csv`. The app supports editing/deleting entries via a sequential Ticket ID.

## Project Phases (PMI-PMBOK)
- **Initiating**: Defined goals for a flight data tracking GUI.
- **Planning**: Designed GUI and planned GPS data retrieval.
- **Executing**: Developed Python app (`app.py`, `templates/index.html`) with Geopy integration.
- **Monitoring and Controlling**: Validated distance calculations (e.g., JFK-LGW ~5570 km).
- **Closing**: Deployed via Docker (`compose.yaml`) with persistent data.

## Key Features
- **Flight Data Entry**: Input boarding pass details, including IATA codes (e.g., URT-DMK).
- **Dynamic Distance Calculation**: Uses Geopy’s Nominatim API to retrieve coordinates for IATA codes, caches in `routes.csv`.
- **Scalable UI**: Dynamic form with AJAX for editing/deleting tickets.
- **Persistent Storage**: Tickets stored in `tickets.csv` persist across restarts.
- **Logging**: Geocoded coordinates logged in `ticket_tracker.log`.
- **Files**: Includes the following in [files](./files):
  - `app.py`: Main Flask application.
  - `templates/index.html`: GUI template.
  - `README.markdown`: Project documentation.
  - `LICENSE`: MIT license file.
  - `.env`: Environment variables (e.g., AVIATIONSTACK_API_KEY).
  - `compose.yaml`: Docker Compose configuration.
  - `tickets.csv`: Stores ticket data.
  - `routes.csv`: Caches route distances.
  - `ticket_tracker.log`: Logs geocoding and app activity.

## Setup Instructions for Synology NAS (DSM 7.2 or later)
1. **Clone Repository**:
   ```bash
   git clone https://github.com/silicastormsiam/agp-flight-tracker.git
   cd agp-flight-tracker
   ```
2. **Directory Setup**:
   ```bash
   mkdir -p /volume1/docker/flight-tracker/templates
   ```
3. **Deploy Files**:
   - Copy files from [files](./files) (`app.py`, `templates/index.html`, `README.markdown`, `LICENSE`, `.env`, `compose.yaml`, `tickets.csv`, `routes.csv`, `ticket_tracker.log`) to `/volume1/docker/flight-tracker`.
4. **Set Permissions**:
   ```bash
   sudo chown admin:users /volume1/docker/flight-tracker
   sudo chmod 755 /volume1/docker/flight-tracker
   sudo chmod 664 /volume1/docker/flight-tracker/app.py
   sudo chmod 664 /volume1/docker/flight-tracker/templates/index.html
   sudo chmod 664 /volume1/docker/flight-tracker/README.markdown
   sudo chmod 664 /volume1/docker/flight-tracker/LICENSE
   sudo chmod 664 /volume1/docker/flight-tracker/.env
   sudo chmod 664 /volume1/docker/flight-tracker/compose.yaml
   sudo chmod 664 /volume1/docker/flight-tracker/tickets.csv
   sudo chmod 664 /volume1/docker/flight-tracker/routes.csv
   sudo chmod 664 /volume1/docker/flight-tracker/ticket_tracker.log
   ```
5. **Run Container**:
   ```bash
   cd /volume1/docker/flight-tracker
   docker-compose -f compose.yaml up -d
   ```
6. **Access**: Open the configured Docker port (e.g., http://<NAS_IP>:5002) in a browser.

## Technical Details
- **Technologies**: Python 3.9, Flask (3.1.1), Geopy (2.4.1), python-dotenv (1.1.1), requests (2.32.4), jQuery (3.6.0), Docker.
- **License**: MIT (see [files/LICENSE](./files/LICENSE)).

## Badges
![Python](https://img.shields.io/badge/Python-FF69B4?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-00FF00?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-800080?logo=docker&logoColor=white)

*Last updated: July 18, 2025*
