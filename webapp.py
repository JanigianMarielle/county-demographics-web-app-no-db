from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

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
    county2 = county_greatest_change(state)
    fact = "In " + state + ", The greatest amount of time it takes to commute to work " + str(county) + "."
    fact2 = "In " + state + ", The greatest change in popultion " + county2 + "."
    return render_template('home.html', state_options=states, funFact=fact, funFact2=fact2)
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('demographics.json') as miscellaneous_data:
        counties = json.load(miscellaneous_data)
    states=[]
    
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def greatest_time_county(state):
    """Return the county that has the largest communute to work time."""
    with open('demographics.json') as miscellaneous_data:
        counties = json.load(miscellaneous_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Miscellaneous"]["Mean Travel Time to Work"] > highest:
                highest = c["Miscellaneous"]["Mean Travel Time to Work"]
                county = c["County"]
    return highest
    
def county_greatest_change(state):
    """Return the county that has the greatest percent chnage in population."""
    with open('demographics.json') as population_data:
        counties = json.load(population_data)
        highest=0
        county=""
        for c in counties:
            if c["State"] == state:
                if c["Population"]["Population Percent Change"] > highest:
                    highest = c["Population"]["Population Percent Change"]
                    county = c["County"]
                    
    return county

def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
