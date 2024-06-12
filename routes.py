from flask import render_template, redirect, url_for, flash, jsonify
from forms import LoginForm, RegistrationForm, RecipeForm
from models import User, Recipe, Comment, Rating
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, instructions=form.instructions.data, user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added successfully!')
        return redirect(url_for('recipes'))
    return render_template('add_recipe.html', title='Add Recipe', form=form)

@app.route('/recipes', methods=['GET'])
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', title='Recipes', recipes=recipes)

