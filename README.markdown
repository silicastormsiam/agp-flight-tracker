# AGP - Flight Tracker 2.5.3

## Overview
The AGP - Flight Tracker 2.5.3 is a Flask-based web application for tracking flight tickets, developed by Andrew Holland. It allows users to add, edit, and delete tickets, displaying details like airline, date, route, class, distance traveled, seat, and other data. The app uses a persistent CSV file (`tickets.csv`) for ticket storage and Geopy’s Nominatim API for dynamic IATA code coordinate retrieval and distance calculations. Version 2.5.3 enhances the README with a file inventory section.

![Cyberpunk Monk Inspiration](cyberpunk-monk.jpg){: width="300px"}
*Figure 1: Inspiration for the Cyberpunk Monk aesthetic, featuring a man beside Buddha’s left arm, integrated into the UI design.*

The project, completed in one day (11-07-2025) despite no prior Python experience, showcases CLI, Docker, and PMI-driven project management skills.

## Version
- **2.5.3** (18-07-2025): Added File Inventory section to README.
- **2.5.2** (18-07-2025): Enhanced README with Cyberpunk Monk image inspiration.
- **2.5.1** (18-07-2025): Enhanced UI with Cyberpunk Monk design (neon colors, glow effects).

## Setup Instructions
1. **Prerequisites**:
   - Docker installed on Synology DSM (Container Manager).
   - Python 3.9-slim Docker image.
   - Internet access for Geopy Nominatim API.

2. **Directory Setup**:
   ```bash
   mkdir -p /volume1/docker/ticket-tracker/templates
   ```

3. **Deploy Files**:
   - Copy `app.py`, `templates/index.html`, `README.markdown`, `LICENSE.txt`, `.env`, `compose.yaml` to `/volume1/docker/ticket-tracker`.
   - Upload `silicaastormsiam_Cyberpunk_Monk.jpg` to `/volume1/docker/ticket-tracker` and rename to `cyberpunk-monk.jpg`.
   - Set permissions:
     ```bash
     sudo chown admin:users /volume1/docker/ticket-tracker
     sudo chmod 755 /volume1/docker/ticket-tracker
     sudo chmod 664 /volume1/docker/ticket-tracker/app.py
     sudo chmod 664 /volume1/docker/ticket-tracker/templates/index.html
     sudo chmod 664 /volume1/docker/ticket-tracker/README.markdown
     sudo chmod 664 /volume1/docker/ticket-tracker/LICENSE.txt
     sudo chmod 664 /volume1/docker/ticket-tracker/.env
     sudo chmod 664 /volume1/docker/ticket-tracker/compose.yaml
     sudo chmod 664 /volume1/docker/ticket-tracker/cyberpunk-monk.jpg
     ```

4. **Run Container**:
   ```bash
   cd /volume1/docker/ticket-tracker
   docker-compose -f compose.yaml up -d
   ```

5. **Access**:
   - Visit `http://192.168.1.248:5002` locally to verify.

## Dependencies
- Flask (3.1.1, BSD 3-Clause)
- python-dotenv (1.1.1, BSD 3-Clause)
- requests (2.32.4, Apache 2.0)
- geopy (2.4.1, MIT License)
- jQuery (3.6.0, MIT License)

## Usage
- **Add Ticket**: Enter airline, date (DD-MM-YYYY), route (e.g., JFK-LGW), class, seat, and optional data via the form.
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
- Preserve `routes.csv` to maintain historical distance data.
- Add `cyberpunk-monk.jpg` for README visual enhancement.

## File Inventory
- `app.py` (.py): Main Python application file implementing Flask logic and Geopy integration.
- `index.html` (.html): HTML template for the web interface with Cyberpunk Monk design.
- `README.markdown` (.markdown): Project documentation file, including setup instructions and file inventory.
- `LICENSE.txt` (.txt): License file detailing MIT License and dependencies.
- `compose.yaml` (.yaml): Docker Compose configuration for container deployment.
- `.env` (.env): Environment variable file for API keys (e.g., AVIATIONSTACK_API_KEY).
- `tickets.csv` (.csv): Data file storing ticket records.
- `routes.csv` (.csv): Data file caching route distances.
- `cyberpunk-monk.jpg` (.jpg): Image file for README visual enhancement.

## Author
- Andrew Holland

## License
See `LICENSE.txt` file for details.