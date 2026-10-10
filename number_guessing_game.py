import random

def number_guessing_game():
    """A simple number guessing game where the user tries to guess a random number."""
    print("=" * 50)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("Can you guess what it is?")
    print("=" * 50)

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        try:
            # Get user's guess
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts} - Enter your guess: "))
            attempts += 1

            # Check if the guess is correct
            if guess < secret_number:
                print("Too low! Try a higher number.")
            elif guess > secret_number:
                print("Too high! Try a lower number.")
            else:
                print(f"\n🎉 Congratulations! You guessed the number {secret_number} correctly!")
                print(f"It took you {attempts} {'try' if attempts == 1 else 'tries'}.")
                return

        except ValueError:
            print("Please enter a valid number!")
            # Don't count invalid input as an attempt

    # If we exit the loop, they've used all attempts
    print(f"\n💔 Sorry, you've used all {max_attempts} attempts.")
    print(f"The number I was thinking of was {secret_number}.")
    print("Better luck next time!")

def play_again():
    """Ask the user if they want to play again."""
    while True:
        choice = input("\nWould you like to play again? (yes/no): ").lower().strip()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

# Main game loop
if __name__ == "__main__":
    print("Starting the Number Guessing Game...\n")

    while True:
        number_guessing_game()
        if not play_again():
            print("\nThanks for playing! Goodbye!")
            break
        print("\n" + "="*50)