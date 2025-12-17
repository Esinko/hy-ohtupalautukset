# Kivi-Paperi-Sakset (Rock-Paper-Scissors)

A Rock-Paper-Scissors game implementation with both CLI and Web UI interfaces.

## Features

- **Player vs Player**: Two players on the same device
- **Player vs AI**: Simple deterministic AI opponent
- **Player vs Improved AI**: AI that learns from your moves (remembers last 10 moves)

## Installation

Install dependencies using Poetry:

```bash
poetry install
```

## Running the Application

### Web UI (Recommended)

Start the Flask development server:

```bash
poetry run python src/web_app.py
```

Then open your browser and navigate to: http://localhost:5000

**Note**: This runs a development server with debug mode enabled. For production deployment, use a production-grade WSGI server like gunicorn or waitress with debug mode disabled.

### CLI Interface

Run the command-line version:

```bash
poetry run python src/index.py
```

## Game Rules

- **K (Kivi)** = Rock: Beats Scissors
- **P (Paperi)** = Paper: Beats Rock  
- **S (Sakset)** = Scissors: Beats Paper

## Web UI Screenshots

The web UI features a clean, wireframe-style design with:
- Game mode selection
- Live score tracking
- Round history display
- Visual feedback for wins, losses, and ties

## Project Structure

- `src/index.py` - CLI entry point
- `src/web_app.py` - Flask web application
- `src/kps_peli.py` - Base game logic
- `src/kps_pelaaja_vs_pelaaja.py` - Two-player mode
- `src/kps_tekoaly.py` - Simple AI mode
- `src/kps_parempi_tekoaly.py` - Improved AI mode
- `src/tekoaly.py` - Simple AI implementation
- `src/tekoaly_parannettu.py` - Improved AI implementation
- `src/tekoaly_base.py` - Base AI class with memory buffer
- `templates/` - HTML templates for web UI
