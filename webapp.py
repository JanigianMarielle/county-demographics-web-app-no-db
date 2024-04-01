from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(state_fun_fact)

@app.route('/')
def home():
    states = get_state_options()
    #print(states)
    return render_template('home.html', state_options=states)

@app.route('/showFact')
def render_fact():
    states = get_state_options()
    state = request.args.get('state')
    county = name_orgin(state)
    fact = "In " + state + ", The average time it takes to get to work is" + county + "."
    return render_template('home.html', state_options=states, funFact=fact)
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('miscellaneous.json') as miscellaneous_data:
        time = json.load(miscellaneous_data)
    states=[]
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def name_origin(state):
    """Return the way the state recieved its name."""
    with open('miscellaneous.json') as miscellaneous:
        time = json.load(miscellaneous_data)
    highest=0
    miscellaneous = ""
    for t in time:
        if t["State"] == state:
            if t["Time"]["Number of minutes it takes to commute to work"] > highest:
                highest = m["Age"]["Percent Under 18 Years"]
                miscellaneous = t["Time"]
    return time

def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
