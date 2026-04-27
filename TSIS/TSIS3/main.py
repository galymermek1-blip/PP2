from ui import main_menu, leaderboard_screen, settings_screen
from racer import run_game

while True:
    action = main_menu()

    if action == "play":
        while True:
            result = run_game()
            if result == "menu":
                break

    elif action == "leaderboard":
        leaderboard_screen()

    elif action == "settings":
        settings_screen()

    elif action == "quit":
        break