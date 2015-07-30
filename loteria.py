import random 
import os

from flask import (
	Flask,
	request, session,
	url_for, render_template, 
	redirect, abort
)


# Create a Flask application object
app = Flask(__name__) 

#Session variables are stored client-side (on the user's browser).
#The content of these variables is encrypted, so users can't actually
#read theirs contents. They could edit the session data, but because it 
#would not be "signed" with the secret key below, the server would
#reject is as invalid.
#You need to set a secret key (random text) and keep it secret! 
app.secret_key = "shhhhh! don't tell anyone what I am"

# The path to the directory containing our card images
# We will store a list of image file names in a session variable
IMG_DIR = app.static_folder

########################
### Helper functions ###
########################

def init_game():
	#Initialize a new deck (a list of filenames)
	image_names = os.listdir(IMG_DIR)
	#Shuffle the deck
	random.shuffle(image_names)
	#Store it in the user´s session
	#'session' is a special global object that Flask provides
	#wich exposes the basic session management functionality
	session['images'] = image_names

def select_from_deck():
	try:
		image_name = session['images'].pop()
	except IndexError:
		image_name = None
	return image_name

######################
### View functions ###
######################

#Decorator: pretty way to write
@app.route('/')
def index():
	init_game()
	return render_template("index.html")

#If users open this url, it is an error in the first time the browser 
#is opened 
@app.route('/draw')
def draw_card():
	if 'images' not in session:
		abort(400)
	image_name = select_from_deck()
	if image_name is None:
		return render_template("gameover.html")
	return render_template("showcard.html", image_name = image_name)

if __name__ == '__main__':
	app.run(debug = True) #True = Show error