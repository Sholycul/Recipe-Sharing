from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
import os
import pandas as pd
from wtforms import StringField, PasswordField, EmailField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash



class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(message='Required')])
    password = PasswordField(label='Password', validators=[DataRequired('Required'), Length(min=8)])
    submit = SubmitField(label="Log In")

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    submit = SubmitField('Submit')



app = Flask(__name__)
app.secret_key = "This-is-the-string-i-want"
Bootstrap(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# Define the path to your CSV or XLSX file
USERDATA_FILE = 'users.xlsx'
RECIPEDATA_FILE = 'recipes.xlsx'

def save_to_file(data, path=USERDATA_FILE):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame([data])
    
    if not os.path.isfile(path):
        # If file does not exist, create it and add the header
        data.to_excel(path, index=False)
        data.to_csv('users.csv', index=False)
    else:
        # If file exists, append the new data without writing the header again
        existing_df = pd.read_excel(path)
        updated_df = pd.concat([existing_df, data], ignore_index=True)
        updated_df.to_excel(path, index=False)

def get_users():
    if os.path.isfile(USERDATA_FILE):
        return pd.read_excel(USERDATA_FILE)
    return pd.DataFrame()

def get_recipes():
    if os.path.isfile(RECIPEDATA_FILE):
        return pd.read_excel(RECIPEDATA_FILE)
    return pd.DataFrame()

data_available = get_recipes()

def authenticate_user(email, password):
    users_df = get_users()
    user = users_df[users_df['email'] == email]
    if not user.empty and check_password_hash(user.iloc[0]['password'], password):
        return True
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if request.method == 'POST' and register_form.validate_on_submit():
        # Extract data from the form
        user_data = {
            'email': register_form.email.data,
            'password': generate_password_hash(register_form.password.data)
        }
        # Save data to the file
        save_to_file(user_data)
        return redirect(url_for('success'))
    return render_template('register.html', form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        if authenticate_user(login_form.email.data, login_form.password.data):
            return redirect(url_for('add_recipe'))
        else:
            return render_template('login.html', form=login_form, error="Invalid email or password")
    return render_template('login.html', form=login_form)

@app.route('/success')
def success():
    return "Registration successful!"

@app.route('/recipe_success')
def recipe_success():
    return "Added Recipe successful!"

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    recipe_form = RecipeForm()
    if request.method == 'POST' and recipe_form.validate_on_submit():
        recipe_data = {
            'title': recipe_form.title.data,
            'ingredients': recipe_form.ingredients.data,
            'instructions': recipe_form.instructions.data
        }
        save_to_file(recipe_data, path=RECIPEDATA_FILE)
        return redirect(url_for('recipe_success'))
    return render_template('add_recipe.html', form=recipe_form)

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    all_recipes = data_available
    return render_template('recipes.html', recipes=all_recipes, item_list=[0, 1])


if __name__ == "__main__":
    app.run(debug=True)
