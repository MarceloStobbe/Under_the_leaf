# Under the Leaf 🌿

Under the Leaf is an interactive web application developed with Flask (Python), created for plant enthusiasts who want to better care for their green companions. The project offers a plant health diagnostic tool, environment guides, educational content, and organic fertilizer recipes.
**Check out the live version here:** [https://under-the-leaf.onrender.com](https://under-the-leaf.onrender.com)

## 🚀 Features
**Plant Diagnostics**: A tool to identify health issues (spots, yellowing, etc.) and receive personalized care solutions.

**Myths & Truths Quiz**: Test your knowledge about basic plant care.

**Environment Guide**: Discover which species thrive in each room of your house.

**Organic Fertilizers**: Tips on how to nourish your plants in an eco-friendly way.

## 🛠 Technologies Used
**Back-end**: Python, Flask.

**Front-end**: HTML5, CSS3, Bootstrap 5, Jinja2.

**Architecture**: Modular structure for diagnostic and quiz data.

## 📁 Project Structure
```text
Under_the_leaf/
└── project/                  # Root folder of the application
    ├── app.py                # Main application (routes and logic)
    ├── diagnostics.py        # Database for plant diagnostics
    ├── quiz.py               # Data for the myths and truths quiz
    ├── requirements.txt      # Project dependencies
    ├── static/               # Static files
    │   ├── css/              # CSS styles (style.css)
    │   └── img/              # Project images and logo
    ├── templates/            # HTML templates (Jinja2)
    │   ├── base.html         # Base layout
    │   ├── home.html         # Home page
    │   ├── about.html        # About page
    │   ├── help.html         # Diagnostic system
    │   ├── myths.html        # Myths quiz
    │   ├── contact.html      # Contact form
    │   ├── environments.html # Environment guide
    │   └── fertilizer.html   # Fertilizer tips
    └── venv/                 # Virtual environment
```

## ⚙️ How to Run
Clone this repository:

Bash

git clone https://github.com/MarceloStobbe/Under_the_leaf.git

Navigate to the project folder:

Bash

cd Under_the_leaf

Install dependencies:

Bash

pip install flask

Run the application:

Bash
python app.py

Access in your browser:

Open http://127.0.0.1:5000
## 🤖 AI Integration & Credits

This project was developed with the assistance of Gemini AI. Gemini played a key role in:

Logo Creation: Assisting in the conceptualization and design of the project's logo.

Content Research: Providing information on indoor plant care, identifying common plant health issues, developing organic fertilizer recipes, and recommending ideal plant species for different home environments.

## 👤 Author
Developed by Marcelo Stobbe.
