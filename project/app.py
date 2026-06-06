from flask import Flask, render_template, request, flash, redirect, url_for
from diagnostics import DIAGNOSTICS
from quiz import QUIZ_DATA

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_key_very_secret'

import os
app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help', methods=['GET', 'POST'])
def help():
    sorted_diagnostics = sorted(DIAGNOSTICS.items(), key=lambda item: item[1]['name'])
    result = None
    selected_plant_key = None
    error = None
    
    if request.method == 'POST':
        plant = request.form.get('plant')
        symptom = request.form.get('symptom')
        
        if plant in DIAGNOSTICS and symptom in DIAGNOSTICS[plant]['problems']:
            result = DIAGNOSTICS[plant]['problems'][symptom].copy()
            result['plant_name'] = DIAGNOSTICS[plant]['name']
            selected_plant_key = plant
        else:
            error = "Sorry, we don't have a specific diagnosis for this combination yet."
            
    return render_template('help.html', 
                           diagnostics=sorted_diagnostics, 
                           result=result, 
                           selected_plant_key=selected_plant_key,
                           error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    flash("Message sent successfully!", "success")
    return redirect(url_for('contact'))

@app.route('/environments')
def environments():
    return render_template('environments.html')

@app.route('/fertilizer')
def fertilizer():
    return render_template('fertilizer.html')

@app.route('/myths', methods=['GET', 'POST'])
def myths():
    score = None
    username = None
    
    if request.method == 'POST':
        score = 0
        username = request.form.get('username', 'Guest')
        for item in QUIZ_DATA:
            user_answer = request.form.get(f'q{item["id"]}')
            if user_answer == item["a"]:
                score += 2
                
    return render_template('myths.html', questions=QUIZ_DATA, score=score, username=username)

if __name__ == '__main__':
    app.run(debug=True)