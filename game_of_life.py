import flask
from flask import request
import numpy as np
from scipy.signal import convolve2d

#----------- GAME OF LIFE CODE -------------#

def life_step(board):
    neighbors = convolve2d(board, np.ones((3,3)), mode='same',boundary='wrap') - board
    next_board = (board & (neighbors == 2)) | (neighbors == 3)
    return next_board

#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("index.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # get the board, a list of lists
    data = request.get_json()
    print 'data is:', data

    board = data['board']

    # Generate the next board and convert from np array to list
    # so it can be jsonified
    next_board = life_step(board)
    results = {"board": next_board.tolist()}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

if __name__ == "__main__":
    app.run(debug=True)


"""
$.ajax({
  method: "POST",
  contentType: "application/json; charset=utf-8",
  url: "/score",
  data: { board: [1,2,3], name: "John", location: "Boston" },
  success: function(res) {console.log('success', res);},
  error: function(err) {console.log('fail', err);}
});
"""
