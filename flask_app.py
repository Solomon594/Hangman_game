from flask import Flask, render_template, request, redirect, url_for
import random
from hangman_words import word_list
from hangman_art import stages, logo

app = Flask(__name__)

def initialize_game():
    global chosen_word, word_length, end_of_game, lives, display
    chosen_word = random.choice(word_list)
    word_length = len(chosen_word)
    end_of_game = False
    lives = 6
    display = ['_'] * word_length

initialize_game()

@app.route('/')
def home():
    return render_template('index.html', display=' '.join(display), lives=lives, end_of_game=end_of_game)

@app.route('/guess', methods=['POST'])
def guess():
    global lives, end_of_game

    if not end_of_game:
        guess = request.form['letter']
        if guess in display:
            message = f"You've already guessed {guess}."
        else:
            for position in range(word_length):
                letter = chosen_word[position]
                if letter == guess:
                    display[position] = letter

            if guess not in chosen_word:
                lives -= 1
                message = f"You guessed {guess}, that's not in the word. You lose a life."
                if lives == 0:
                    end_of_game = True
                    message += "\nYou lose."
            else:
                if "_" not in display:
                    end_of_game = True
                    message = "You win."
                else:
                    message = f"Correct guess! {guess} is in the word."

        return render_template('index.html', display=' '.join(display), lives=lives, message=message, end_of_game=end_of_game)

    return redirect(url_for('home'))

@app.route('/restart')
def restart():
    initialize_game()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
