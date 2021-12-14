from flask import Flask, request, render_template, flash, redirect, session
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, FeedbackForm
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authenticate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
 
app.config['SECRET_KEY'] = 'trisolarian879'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
 
connect_db(app)

@app.route('/')
def home():
    """Render all users in database"""
    users = User.query.all()
    return render_template('base.html', users=users)


@app.route('/register', methods=['GET','POST'])
def register():
    """Show user form(GET) to register and process form to register(POST)"""
    form = RegisterForm()

    #validatate submitte form
    if form.validate_on_submit():
        """If form is submitted register user[POST]"""
        #get user data form form 
        userName = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # create new user
        new_user = User.register(userName, password, email, first_name, last_name)

        #if error occurs during commit, clear session and redirect to
        # /register and display error to user.
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Username not available')
            return redirect('/register')
        
        session['user_name'] = new_user.username
        return redirect('/secrets')
    else:
        """Render form for registration[GET]"""
        return render_template("register.html", form=form)


@app.route('/secrets')
def secrets():
    """Return secrets page to user"""
    return render_template("secrets.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Get login page and authenticate user if login in form is submitted[POST]"""
    #instantiate login form
    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
 
        # authenticate will return a user or False
        user = User.authenticate(name, pwd)
 
        if user:
            session["user_name"] = user.username  # keep logged in
            return redirect(f"/users/{session['user_name']}")
        else:
            flash("Bad name/password")
            # form.username.errors = ["Bad name/password"]
   
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    """Logout User"""
    flash("You have been logged out")
    session.pop('user_name')
    return redirect('/')

@app.route('/users/<username>')
def users(username):
    """Display user Info"""
    user = User.query.filter_by(username=username).first()

    return render_template("user.html", user=user)

@app.route('/feedback/<username>', methods=['GET', 'POST'])
def feedback(username):
    """ Display Form to submit feedback[GET] and Process form[POST]"""
    form = FeedbackForm()

    if form.validate_on_submit():
        """Process form if validated"""
        title = form.title.data
        content = form.content.data

        user_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(user_feedback)
        db.session.commit()
        
        return redirect(f'/users/{username}')
    else:
        """Display Feedback form"""
        return render_template("feedback_form.html", form=form, username=username)

@app.route('/feedback/edit/<int:id>', methods=['GET','POST'])
def edit_form(id):
    """Edit Feedback"""
    #query feedback
    feedback = Feedback.query.get_or_404(id)
    #pre populate form
    form = FeedbackForm(obj=feedback)
    # query User
    username = feedback.usr.username

    if form.validate_on_submit():
        """Process submitted form"""
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        """Render Sibmission form"""
        return render_template("edit_form.html", form=form, username=username, feedback=feedback)


