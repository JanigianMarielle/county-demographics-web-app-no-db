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
    county = greatest_time_county(state)
    county = county_greatest_change(state)
    fact = "In " + state + ", The greatest amount of time it takes to commute to work" + county + "."
    fact2 = "In " + state + ", The greatest change in popultion" + county + "."
    return render_template('home.html', states=states, funFact=fact, funFact2=fact2)
    
def get_states():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('miscellaneous.json') as miscellaneous_data:
        counties = json.load(miscellaneous_data)
    states=[]
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
return states

def greatest_time_county(state):
    """Return the county that has the largest communute to work time."""
    with open('miscellaneous.json') as miscellaneous:
        counties = json.load(miscellaneous_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Time"]["Number of minutes it takes to commute to work"] > highest:
                highest = c["Time"]["Number of minutes it takes to commute to work"]
                county = c["County"]
    return county
    
def county_greatest_change(state):
    """Return the county that has the greatest percent chnage in population."""
    with open('population.json') as population:
        counties = json.load(population_data)
        highest=0
        county=""
        for c in counties:
            if c["State"] == state:
                if c["Time"]["Greatest change in popultion"] > highest:
                    highest c["Percent"]["Greatest change in popultion"]
                    county = c["County"]

def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
