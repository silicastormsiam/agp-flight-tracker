# AGP - Flight Tracker 2.4

## Overview
The AGP - Flight Tracker 2.4 is a Flask-based web application for tracking flight tickets, developed by Andrew Holland. It allows users to add, edit, and delete tickets, displaying details like airline, date, route, class, distance traveled, seat, and other data. The app uses a persistent CSV file (`tickets.csv`) for ticket storage and Geopy for dynamic distance calculations based on airport IATA codes. Version 2.4.0 introduces a scalable UI with a single dynamic ticket action form. This project, completed in one day (11-07-2025) despite no prior Python experience, showcases CLI, Docker, and PMI-driven project management skills.

## Version
- **2.4.0** (17-07-2025): Added dynamic ticket action form with AJAX for scalability, updated to v2.4.0.
- **2.3.0** (17-07-2025): Enhanced logging with geocoded coordinates, added PMI note, streamlined file management.
- **2.2.3** (17-07-2025): Added Docker Compose compatibility, ensured IATA validation, added .env usage.

## Setup Instructions
1. **Prerequisites**:
   - Docker installed on Synology DSM (Container Manager).
   - Python 3.9-slim Docker image.
   - Internet access for Geopy Nominatim API.

2. **Clone Repository**:
   ```bash
   git clone https://github.com/silicastormsiam/agp-flight-tracker.git
   cd agp-flight-tracker
   ```

3. **Directory Setup**:
   ```bash
   mkdir -p /volume1/docker/ticket-tracker/templates
   ```

4. **Deploy Files**:
   - Copy `app.py`, `templates/index.html`, `README.markdown`, `LICENSE.txt`, `.env`, `compose.yaml` to `/volume1/docker/ticket-tracker`.
   - Set permissions:
     ```bash
     chown admin:users /volume1/docker/ticket-tracker
     chmod 755 /volume1/docker/ticket-tracker
     chmod 664 /volume1/docker/ticket-tracker/app.py
     chmod 664 /volume1/docker/ticket-tracker/templates/index.html
     chmod 664 /volume1/docker/ticket-tracker/README.markdown
     chmod 664 /volume1/docker/ticket-tracker/LICENSE.txt
     chmod 664 /volume1/docker/ticket-tracker/.env
     chmod 664 /volume1/docker/ticket-tracker/compose.yaml
     ```

5. **Run Container**:
   ```bash
   cd /volume1/docker/ticket-tracker
   docker-compose -f compose.yaml up -d
   ```

6. **Access**:
   - Visit `http://192.168.1.248:5002`.

## Dependencies
- Flask (3.1.1, BSD 3-Clause)
- python-dotenv (1.1.1, BSD 3-Clause)
- requests (2.32.4, Apache 2.0)
- geopy (2.4.1, MIT License)
- jQuery (3.6.0, MIT License)

## Usage
- **Add Ticket**: Enter airline, date (DD-MM-YYYY), route (e.g., URT-DMK), class, seat, and optional data via the form.
- **Edit/Delete**: Enter a ticket ID in the dynamic action form to load details, then edit or delete.
- **Distance**: Calculated dynamically using Geopy’s Nominatim, cached in `/app/routes.csv`.

## Logs
- Check logs for debugging:
  ```bash
  docker logs ticket-tracker
  tail -n 25 /volume1/docker/ticket-tracker/ticket_tracker.log
  ```
- Clear logs if needed:
  ```bash
  rm /volume1/docker/ticket-tracker/ticket_tracker.log
  ```

## File Management
- Generated files: `tickets.csv`, `routes.csv` (do not edit manually).
- Clear `routes.csv` to recalculate distances:
  ```bash
  rm /volume1/docker/ticket-tracker/routes.csv
  ```

## Author
- Andrew Holland ([silicastormsiam](https://github.com/silicastormsiam))

## License
See `LICENSE.txt` file for details.