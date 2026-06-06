from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_key_very_secret'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

DIAGNOSTICS = {
    'aloe_vera': {
        'name': 'Aloe Vera',
        'problems': {
            'yellowing': {'problem': 'Yellowing Leaves', 'cause': 'Overwatering', 'solution': 'Aloe leaves yellow when roots are suffocating. Stop watering and let soil dry completely.'},
            'sunburn': {'problem': 'Sunburn', 'cause': 'Excessive Direct Light', 'solution': 'Move to bright, indirect light to allow the plant to recover its natural green pigment.'},
            'mushy_base': {'problem': 'Mushy Leaf Base', 'cause': 'Root Rot', 'solution': 'Remove the plant, trim black/slimy roots, and repot in a fresh, dry succulent mix.'},
            'wrinkled_leaves': {'problem': 'Wrinkled Leaves', 'cause': 'Dehydration', 'solution': 'While it stores water, extreme wrinkles mean it is thirsty. Soak the soil thoroughly once.'},
            'brown_edges': {'problem': 'Brown Crispy Edges', 'cause': 'Low Humidity', 'solution': 'Though hardy, Aloe appreciates slightly more ambient humidity if the tips are browning.'}
        }
    },
    'monstera': {
        'name': 'Monstera Deliciosa',
        'problems': {
            'yellowing': {'problem': 'Yellowing Leaves', 'cause': 'Poor Drainage', 'solution': 'Ensure your pot has drainage holes. Monstera roots need oxygen, not stagnant water.'},
            'brown_edges': {'problem': 'Brown Crispy Edges', 'cause': 'Low Humidity', 'solution': 'Monstera loves tropical air. Use a humidifier or mist the leaves daily to maintain moisture.'},
            'leaf_spots': {'problem': 'Dark Brown Spots', 'cause': 'Fungal Infection', 'solution': 'Avoid getting water on the leaves during watering. Improve air circulation around the plant.'},
            'wilting': {'problem': 'Constant Wilting', 'cause': 'Inconsistent Rega', 'solution': 'Establish a schedule: water when the top 5cm of soil feel dry to the touch.'},
            'leggy_stems': {'problem': 'Leggy Stems', 'cause': 'Insufficient Light', 'solution': 'This plant is "stretching" for light. Move it closer to a window, but avoid harsh direct noon sun.'}
        }
    },
    'snake_plant': {
        'name': 'Snake Plant',
        'problems': {
            'mushy_base': {'problem': 'Mushy Leaf Base', 'cause': 'Overwatering', 'solution': 'Stop watering immediately. These plants thrive on neglect; only water when the soil is bone dry.'},
            'wrinkled_leaves': {'problem': 'Wrinkled Leaves', 'cause': 'Extreme Dehydration', 'solution': 'Give a deep watering. Once the water drains, discard any excess water from the saucer.'},
            'yellowing': {'problem': 'Yellowing Leaves', 'cause': 'Waterlogged Soil', 'solution': 'Check if the pot is too large. Excess soil holds too much water; repot in a smaller container.'},
            'leaf_drop': {'problem': 'Dropping Leaves', 'cause': 'Physical Stress', 'solution': 'Ensure the plant is stable. If it is leaning, stake it upright and check for stable soil conditions.'},
            'brown_edges': {'problem': 'Brown Crispy Edges', 'cause': 'Fluoride in Water', 'solution': 'Snake plants are sensitive. Try using filtered or distilled water instead of tap water.'}
        }
    },
    'peace_lily': {
        'name': 'Peace Lily',
        'problems': {
            'wilting': {'problem': 'Constant Wilting', 'cause': 'Dehydration', 'solution': 'Peace Lilies are dramatic. If it wilts, it needs water immediately. Keep the soil slightly moist always.'},
            'yellowing': {'problem': 'Yellowing Leaves', 'cause': 'Light Intensity', 'solution': 'Too much direct light can burn the leaves. Move it to a shadier corner of the room.'},
            'leaf_spots': {'problem': 'Dark Brown Spots', 'cause': 'Chemical Burn', 'solution': 'These spots often result from tap water salts. Let water sit overnight before using or use rainwater.'},
            'brown_edges': {'problem': 'Brown Crispy Edges', 'cause': 'Dry Air', 'solution': 'Place near a source of humidity. The kitchen or bathroom are ideal locations for this plant.'},
            'leggy_stems': {'problem': 'Leggy Stems', 'cause': 'Low Light', 'solution': 'Although they tolerate shade, they grow "leggy" without enough indirect light. Move to a brighter area.'}
        }
    },
    'pothos': {
        'name': 'Pothos',
        'problems': {
            'leggy_stems': {'problem': 'Leggy Stems', 'cause': 'Lack of Light', 'solution': 'Prune back the long, bare stems to encourage new growth from the base. Move to more light.'},
            'yellowing': {'problem': 'Yellowing Leaves', 'cause': 'Root Congestion', 'solution': 'Your Pothos might be root-bound. Check if roots are circling the pot and repot if necessary.'},
            'leaf_spots': {'problem': 'Dark Brown Spots', 'cause': 'Overwatering', 'solution': 'Pothos are prone to leaf spots if kept too wet. Let the soil dry between waterings.'},
            'wilting': {'problem': 'Constant Wilting', 'cause': 'Underwatering', 'solution': 'While they are tough, constant wilting means the roots are dehydrated. Water thoroughly.'},
            'brown_edges': {'problem': 'Brown Crispy Edges', 'cause': 'Low Humidity', 'solution': 'Even Pothos appreciate a misting session in dry winter months when heaters are on.'}
        }
    }
}

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
            error = "Sorry, we don't have a specific diagnosis for this combination yet. Please try selecting a different symptom or plant."
            
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

    flash("Message sent successfully! We'll respond as soon as possible.", "success")
    return redirect(url_for('contact'))


@app.route('/environments')
def environments():
    return render_template('environments.html')

@app.route('/fertilizer')
def fertilizer():
    return render_template('fertilizer.html')

QUIZ_DATA = [
    {"id": 0, "q": "Plants need to be fertilized every day.", "a": "False"},
    {"id": 1, "q": "Plants talk to each other through their roots.", "a": "True"},
    {"id": 2, "q": "All plants need direct sunlight to grow.", "a": "False"},
    {"id": 3, "q": "Cleaning dust off leaves helps plants breathe.", "a": "True"},
    {"id": 4, "q": "You should water your plants based on a strict schedule.", "a": "False"}
]

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