from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import db, User, Question, Comment
from forms import AuthForm, QuestionForm, CommentForm
from diagnostics import DIAGNOSTICS
from quiz import QUIZ_DATA
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')

app.config['SECRET_KEY'] = 'a_key_very_secret'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Image Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, UPLOAD_FOLDER)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)

# Flask login Configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('forum'))
    
    form = AuthForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            login_user(user)
            flash(f'Login successful! Welcome, {user.name}!', 'success')
            return redirect(url_for('forum'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html', form=form, is_register=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('forum'))
    
    form = AuthForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already registered!', 'danger')
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('User registered successfully! Please log in to continue.', 'success')
            return redirect(url_for('login'))
            
    return render_template('login.html', form=form, is_register=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out of your account.', 'info')
    return redirect(url_for('home'))

# Forum Routes
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    form = QuestionForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to log in to post.', 'warning')
            return redirect(url_for('login'))
        
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_filename = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        question = Question(
            content=form.content.data, 
            author=current_user,
            image_file=image_filename
        )
        db.session.add(question)
        db.session.commit()
        flash('Your question has been posted successfully!', 'success')
        return redirect(url_for('forum'))
        
    questions = Question.query.order_by(Question.date_posted.desc()).all()
    comment_form = CommentForm()
    return render_template('forum.html', questions=questions, form=form, comment_form=comment_form)

@app.route('/forum/question/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.author != current_user:
        abort(403)
    
    form = QuestionForm()
    if form.validate_on_submit():
        question.content = form.content.data
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('forum'))
    elif request.method == 'GET':
        form.content.data = question.content
        
    return render_template('edit.html', form=form)

@app.route('/forum/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.author != current_user:
        abort(403)
        
    if question.image_file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], question.image_file)
        if os.path.exists(image_path):
            os.remove(image_path)
            
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'info')
    return redirect(url_for('forum'))

@app.route('/forum/question/<int:question_id>/comment', methods=['POST'])
@login_required
def add_comment(question_id):
    question = Question.query.get_or_404(question_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, question=question)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
    return redirect(url_for('forum'))

# Reaction Routes
@app.route('/forum/comment/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return redirect(url_for('forum'))

@app.route('/forum/comment/<int:comment_id>/dislike', methods=['POST'])
@login_required
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.dislikes += 1
    db.session.commit()
    return redirect(url_for('forum'))

@app.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.author != current_user:
        flash('You are not authorized to edit this comment.', 'danger')
        return redirect(url_for('forum'))
    
    if request.method == 'POST':
        comment.content = request.form.get('content')
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('forum'))
        
    return render_template('edit.html', comment=comment)

@app.route('/forum/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'info')
    return redirect(url_for('forum'))

# Site Routes
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
    with app.app_context():
        db.create_all()
        print("Database connected and tables verified.")
    app.run(debug=True)