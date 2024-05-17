import random
from datetime import datetime
from utils.score import Score
from utils.user_manager import UserManager

class DiceGame:
    def __init__(self):
        self.user_manager = UserManager()
        self.scores = []
        self.user_manager.load_users()
        self.load_scores()

    def main_menu(self):
        print("Welcome to dice roll game!")
        while True:
            print("\nMain Menu")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def register(self):
        username = input("Enter username (at least 4 characters), or leave blank to cancel: ").strip()
        if not username:
            return
        if not self.user_manager.validate_username(username):
            print("Username must be at least 4 characters long.")
            return
        password = input("Enter password (at least 8 characters), or leave blank to cancel: ").strip()
        if not password:
            return
        if not self.user_manager.validate_password(password):
            print("Password must be at least 8 characters long.")
            return
        result = self.user_manager.register_user(username, password)
        print(result)

    def login(self):
        username = input("Enter username, or leave blank to cancel: ").strip()
        if not username:
            return
        password = input("Enter password, or leave blank to cancel: ").strip()
        if not password:
            return
        user = self.user_manager.login_user(username, password)
        if user:
            print(f"Welcome, {username}!")
            self.user_menu(user)
        else:
            print("Invalid username or password.")

    def user_menu(self, user):
        while True:
            print(f"\nMenu for {user.username}:")
            print("1. Start game")
            print("2. Show top scores")
            print("3. Log out")
            choice = input("Enter your choice, or leave blank to cancel: ").strip()
            if choice == '1':
                self.start_game(user)
            elif choice == '2':
                self.show_top_scores()
            elif choice == '3' or choice == '':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def start_game(self, user):
        total_points = 0
        rounds_played = 0
        stages_won = 0

        print("Starting game...")
        while rounds_played < 3:
            input("Press Enter to roll the dice...")
            player_roll = random.randint(1, 6)
            computer_roll = random.randint(1, 6)
            print(f"{user.username} rolled: {player_roll}")
            print(f"CPU rolled: {computer_roll}")

            if player_roll > computer_roll:
                print("You win this round!")
                total_points += player_roll
            elif player_roll < computer_roll:
                print("CPU wins this round!")
            else:
                print("It's a tie!")
                continue

            rounds_played += 1

        if total_points > 0:
            stages_won = 1  # Since the player won at least one round, they win one stage
            print(f"GAME OVER. You won {stages_won} stage(s) and scored {total_points} point(s)!")
            self.update_scores(user.username, total_points, stages_won)
        else:
            print("GAME OVER. You didn't win any stages.")

    def update_scores(self, username, points, stages_won):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        score = Score(username, points, stages_won, date)
        self.scores.append(score)
        self.save_scores()

    def save_scores(self):
        with open('scores.txt', 'w') as file:
            for score in self.scores:
                file.write(f"{score.username},{score.points},{score.stages_won},{score.date}\n")

    def load_scores(self):
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    username, points, stages_won, date = line.strip().split(',')
                    self.scores.append(Score(username, int(points), int(stages_won), date))
        except FileNotFoundError:
            pass

    def show_top_scores(self):
        if not self.scores:
            print("No scores available yet.")
            return

        sorted_scores = sorted(self.scores, key=lambda x: x.points, reverse=True)[:10]
        print("Top Scores:")
        for idx, score in enumerate(sorted_scores, 1):
            print(f"{idx}. {score.username} - Points: {score.points}, Wins: {score.stages_won}, Date: {score.date}")
