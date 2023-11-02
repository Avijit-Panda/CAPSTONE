from flask import render_template , url_for ,flash, redirect, request, Response
from mainflask.forms import RegistrationForm, LoginForm, UpdateAccountForm
from mainflask import app, db, bcrypt
from mainflask.models import User, Post, Response
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from mainflask.blinkdetect import gen_frames


    
posts=[
    {
        "author": "Dr.XYZ",
        "title":"ADHD",
        "content":"Content 1"
    },
    {
        "author":"Dr.ABC",
        "title":"ADHD Blog",
        "content":"Content 2"
    }]

@app.route("/")
def default():
   
    return "<h1> this is the default page no</h1>"
@app.route("/home")
def home():
    if current_user.is_authenticated:
        user_id = current_user.id
        query = text("""
                WITH finaltable AS (
                SELECT r.user_id, r.answer, r.question_number
                FROM response r
                WHERE r.user_id = :user_id
                ORDER BY r.id DESC
                LIMIT 18
            )
            SELECT COUNT(*)
            FROM finaltable f
            JOIN answers a ON f.answer = a.answers
            AND f.question_number = a.question_id
            ;
            """)
    
        result = db.session.execute(query, {"user_id": user_id})
        quiz_count = result.scalar()
    else:
        quiz_count=0
    
    return render_template("home.html",posts=posts,quiz_count=quiz_count)
   
    


@app.route("/about")
def about():
    
    return render_template("about.html" , title="About")

@app.route("/bionic")
def bionicreader():
    
    return render_template("bionicread.html" , title="Bionic Reader")

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():  
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('login' ))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

       
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
             login_user(user, remember=form.remember.data)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect(url_for('home'))  
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file=url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/quiz', methods=['GET','POST'])
def quiz():    
    if request.method == 'POST':
        responses = []
        count=0
        for key, value in request.form.items():
            if key.startswith('answer'):
                question_number = int(key.replace('answer', ''))
                answer = value
                user_id = current_user.id
                response = Response(question_number=question_number, answer=answer,user_id=user_id)
                db.session.add(response)
                count+=1
        if count==18:
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('Please answer all questions', 'danger')
            return redirect(url_for('quiz'))
            
    return render_template('quiz.html')


@app.route("/todo")
def todo():
    user_id = current_user.id
    todo_list = Todo.query.filter_by(user_id=user_id)
    return render_template("base.html", todo_list=todo_list)    

@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form.get("title")
    user_id = current_user.id
    new_todo = Todo(title=title, user_id=user_id,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    user_id = current_user.id
    todo = Todo.query.filter_by(id=todo_id,user_id=user_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    user_id = current_user.id
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))

def url_summarize(url):
    parser = HtmlParser.from_url(url, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 5)
    return summary

def doc_summarize(file_path):
    parser = PlaintextParser.from_file(file_path, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 5)
    return summary

@app.route('/textsum', methods=['GET', 'POST'])
def textsum():
    if request.method == 'POST':
        url = request.form['url']
        doc_path = request.form['doc_path']
        if url:
            summary = url_summarize(url)
        elif doc_path:
            summary = doc_summarize(doc_path)
        else:
            summary = None
        return render_template('textsummarizer.html', summary=summary)
    return render_template('textsummarizer.html')

    


    

