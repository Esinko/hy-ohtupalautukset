"""
Web UI for Kivi-Paperi-Sakset (Rock-Paper-Scissors) game
Uses Flask to provide a simple web interface for the game
"""
from flask import Flask, render_template, request, session, redirect, url_for
from typing import Dict, Type
from kps_peli import KiviPaperiSakset, Game_Moves, Winning_Combos
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly
import os

app = Flask(__name__, template_folder='../templates')
# Note: For production, use a fixed secret key from environment variable
# e.g., app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.secret_key = os.urandom(24)

# Available game types
GAME_TYPES: Dict[str, Type[KiviPaperiSakset]] = {
    "pelaaja_vs_pelaaja": KPSPelaajaVsPelaaja,
    "tekoaly": KPSTekoaly,
    "parempi_tekoaly": KPSParempiTekoaly
}

GAME_NAMES = {
    "pelaaja_vs_pelaaja": "Ihmistä vastaan",
    "tekoaly": "Tekoälyä vastaan",
    "parempi_tekoaly": "Parannettua tekoälyä vastaan"
}

MAX_ROUNDS = 3  # Games automatically end after 5 rounds

def get_game():
    """Get or create the current game instance"""
    if 'game_type' not in session:
        return None
    
    game_type = session['game_type']
    if game_type not in GAME_TYPES:
        return None
    
    # Recreate game state from session
    game = GAME_TYPES[game_type]()
    game.player1_points = session.get('player1_points', 0)
    game.player2_points = session.get('player2_points', 0)
    game.tie_count = session.get('tie_count', 0)
    
    return game

def save_game(game):
    """Save game state to session"""
    session['player1_points'] = game.player1_points
    session['player2_points'] = game.player2_points
    session['tie_count'] = game.tie_count

@app.route('/')
def index():
    """Main page - choose game type"""
    return render_template('index.html', game_types=GAME_TYPES, game_names=GAME_NAMES)

@app.route('/start', methods=['POST'])
def start_game():
    """Start a new game"""
    game_type = request.form.get('game_type')
    
    if game_type not in GAME_TYPES:
        return redirect(url_for('index'))
    
    # Initialize new game session
    session['game_type'] = game_type
    session['player1_points'] = 0
    session['player2_points'] = 0
    session['tie_count'] = 0
    session['rounds_played'] = 0
    session['game_over'] = False
    session['last_player1_move'] = None
    session['last_player2_move'] = None
    session['last_result'] = None
    session['player1_waiting'] = False  # For two-player mode
    
    # Initialize AI if needed
    if game_type == 'tekoaly':
        session['ai_counter'] = 0
    elif game_type == 'parempi_tekoaly':
        session['ai_memory'] = []
        session['ai_memory_size'] = 10
    
    return redirect(url_for('play'))

@app.route('/play')
def play():
    """Game play page"""
    game = get_game()
    if not game:
        return redirect(url_for('index'))
    
    # Check if game is over
    if session.get('game_over', False):
        return redirect(url_for('game_over'))
    
    game_name = GAME_NAMES[session['game_type']]
    last_result = session.get('last_result')
    last_player1_move = session.get('last_player1_move')
    last_player2_move = session.get('last_player2_move')
    rounds_played = session.get('rounds_played', 0)
    player1_waiting = session.get('player1_waiting', False)
    
    return render_template('play.html', 
                         game=game, 
                         game_name=game_name,
                         game_type=session['game_type'],
                         moves=Game_Moves,
                         last_result=last_result,
                         last_player1_move=last_player1_move,
                         last_player2_move=last_player2_move,
                         rounds_played=rounds_played,
                         max_rounds=MAX_ROUNDS,
                         player1_waiting=player1_waiting)

@app.route('/move', methods=['POST'])
def make_move():
    """Process a move"""
    game = get_game()
    if not game:
        return redirect(url_for('index'))
    
    # Check if game is already over
    if session.get('game_over', False):
        return redirect(url_for('game_over'))
    
    player1_move = request.form.get('player1_move')
    
    if not player1_move or player1_move not in Game_Moves:
        return redirect(url_for('play'))
    
    game_type = session['game_type']
    
    if game_type == 'pelaaja_vs_pelaaja':
        # Two-player mode with hidden moves
        if not session.get('player1_waiting', False):
            # Player 1 just made their move, wait for player 2
            session['player1_move_temp'] = player1_move
            session['player1_waiting'] = True
            return redirect(url_for('play'))
        else:
            # Player 2 is making their move
            player2_move = player1_move  # The form value is actually player 2's move
            player1_move = session.get('player1_move_temp')
            session['player1_waiting'] = False
            session.pop('player1_move_temp', None)
    else:
        # AI modes
        if game_type == 'tekoaly':
            # Simple AI - deterministic rotation
            ai_counter = session.get('ai_counter', 0)
            ai_counter += 1
            session['ai_counter'] = ai_counter
            player2_move = Game_Moves[ai_counter % 3]
        else:  # parempi_tekoaly
            # Improved AI - remembers player moves
            ai_memory = session.get('ai_memory', [])
            
            if not ai_memory:
                player2_move = "k"
            else:
                # Count player moves
                move_counts = {move: ai_memory.count(move) for move in Game_Moves}
                
                # Choose counter-move based on most frequent player move
                if move_counts["k"] > move_counts["p"] and move_counts["k"] > move_counts["s"]:
                    player2_move = "p"
                elif move_counts["p"] > move_counts["k"] and move_counts["p"] > move_counts["s"]:
                    player2_move = "s"
                else:
                    player2_move = "k"
            
            # Remember this move
            ai_memory.append(player1_move)
            if len(ai_memory) > session.get('ai_memory_size', 10):
                ai_memory.pop(0)
            session['ai_memory'] = ai_memory
    
    # Record the moves
    game.record_moves(player1_move, player2_move)
    save_game(game)
    
    # Increment round counter
    session['rounds_played'] = session.get('rounds_played', 0) + 1
    
    # Store move history for display
    session['last_player1_move'] = player1_move
    session['last_player2_move'] = player2_move
    
    # Determine result
    if player1_move == player2_move:
        session['last_result'] = 'tie'
    else:
        if player2_move == Winning_Combos.get(player1_move):
            session['last_result'] = 'win'
        else:
            session['last_result'] = 'lose'
    
    # Check if game should end
    if session['rounds_played'] >= MAX_ROUNDS:
        session['game_over'] = True
        return redirect(url_for('game_over'))
    
    return redirect(url_for('play'))

@app.route('/game_over')
def game_over():
    """Game over page showing final results"""
    game = get_game()
    if not game:
        return redirect(url_for('index'))
    
    game_name = GAME_NAMES[session.get('game_type', 'tekoaly')]
    rounds_played = session.get('rounds_played', 0)
    
    # Determine winner
    if game.player1_points > game.player2_points:
        winner = "Pelaaja 1 voitti pelin!"
    elif game.player2_points > game.player1_points:
        winner = "Pelaaja 2 voitti pelin!"
    else:
        winner = "Peli päättyi tasapeliin!"
    
    return render_template('game_over.html',
                         game=game,
                         game_name=game_name,
                         rounds_played=rounds_played,
                         winner=winner)

@app.route('/reset')
def reset():
    """Reset the game"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # DEVELOPMENT ONLY - Debug mode should NOT be used in production
    # For production deployment, use a WSGI server like gunicorn or waitress
    # with debug=False
    app.run(debug=True, host='0.0.0.0', port=5000)
