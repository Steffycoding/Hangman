import random
from colorama import Fore, Style

# Common words for Hangman
word_list = ["python", "hangman", "programming", "developer", "learning", "challenge", "colorful",
             "computer", "science", "keyboard", "software", "algorithm", "web", "application",
             "debugging", "community", "database", "iteration", "interface", "javascript"]

def choose_word(used_words):
    """
    Selects a random word from the predefined list that has not been used before in the game.

    Args:
        used_words (set): Set of words used in the current game.

    Returns:
        str: A word that has not been used in the current game.
    """
    available_words = set(word_list) - used_words
    if not available_words:
        # If all words have been used, reset the used words set
        used_words.clear()
        available_words = set(word_list)

    chosen_word = random.choice(list(available_words))
    used_words.add(chosen_word)
    return chosen_word

def display_word(word, guessed_letters):
    """
    Displays the word with guessed letters filled in and others as underscores.

    Args:
        word (str): The word to be guessed.
        guessed_letters (set): Set of letters guessed by the player.

    Returns:
        str: The word with blanks for unguessed letters.
    """
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def save_game(player_data):
    """Saves the player's progress."""
    with open(f"{player_data['name']}_saved_game.pkl", "wb") as file:
        pickle.dump(player_data, file)

def load_game(player_name):
    """Loads the player's saved game."""
    file_path = f"{player_name}_saved_game.pkl"
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return pickle.load(file)
    else:
        return None

def play_again():
    """Asks the user if they want to play again and returns True if yes, False otherwise."""
    answer = input("Do you want to play again? (yes/no): ").lower()
    return answer == 'yes' or answer == 'y'

def main():
    """Main function to run the Hangman game."""
    print(Fore.BLUE + "Welcome to Hangman!" + Style.RESET_ALL)

    player_name = input("Enter your name: ")
    player_password = input("Choose a password: ")

    player_data = load_game(player_name)

    if player_data and player_data["name"] == player_name and player_data["password"] == player_password:
        print(Fore.GREEN + f"Welcome back, {player_name}!" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"Welcome, {player_name}!" + Style.RESET_ALL)
        player_data = {"name": player_name, "password": player_password, "completed_game": False}

    used_words = set()

    while True:
        word_to_guess = choose_word(used_words)
        guessed_letters = set()
        incorrect_guesses = 0
        max_incorrect_guesses = 7  # Updated to give the player 7 lives

        while incorrect_guesses < max_incorrect_guesses:
            print("\n" + display_word(word_to_guess, guessed_letters))

            user_input = input("Guess a letter: ").lower()

            if user_input:
                user_input = user_input.lower()

                if len(user_input) == 1 and user_input.isalpha():
                    if user_input in guessed_letters:
                        print(Fore.YELLOW + "You've already guessed that letter. Try again." + Style.RESET_ALL)
                    elif user_input in word_to_guess:
                        print(Fore.GREEN + "Correct guess!" + Style.RESET_ALL)
                        guessed_letters.add(user_input)
                    else:
                        print(Fore.RED + "Incorrect guess. Lives remaining: " + str(max_incorrect_guesses - incorrect_guesses - 1) + Style.RESET_ALL)
                        incorrect_guesses += 1
                else:
                    print(Fore.YELLOW + "Please enter a valid single letter." + Style.RESET_ALL)

            if all(letter in guessed_letters for letter in word_to_guess):
                print("\n" + display_word(word_to_guess, guessed_letters))
                print(Fore.GREEN + "Congratulations! You've guessed the word: " + word_to_guess)
                print("You're a Hangman champion! 🎉" + Style.RESET_ALL)
                break

        else:
            print(Fore.RED + "Sorry, you've run out of lives. The correct word was: " + word_to_guess)
            print("Don't give up! You can do better next time. 💪" + Style.RESET_ALL)

        player_data["completed_game"] = True
        save_game(player_data)

        if not play_again():
            print("Thank you for playing Hangman! Goodbye!")
            break

if __name__ == "__main__":
    import pickle
    import os
    main()
