import random

def hangman():
    words = ["python", "java", "swift", "javascript"]
    word = random.choice(words)
    guessed = "_" * len(word)
    guessed_correctly = set()
    attempts = 6

    print("Welcome to Hangman!")
    
    while attempts > 0 and guessed != word:
        print(f"Word: {guessed}")
        print(f"Attempts left: {attempts}")
        
        guess = input("Guess a letter: ").lower()
        
        if guess in guessed_correctly:
            print("You've already guessed that letter.")
        elif guess in word:
            guessed_correctly.add(guess)
            guessed = "".join([letter if letter in guessed_correctly else "_" for letter in word])
        else:
            attempts -= 1
            print("Incorrect guess.")
    
    if guessed == word:
        print(f"Congratulations! You've guessed the word: {word}")
    else:
        print(f"Sorry, you've run out of attempts. The word was: {word}")

hangman()
