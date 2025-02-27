from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, RadioField, PasswordField, IntegerField, FloatField
from wtforms.validators import InputRequired, EqualTo

class RegistrationForm(FlaskForm):
    user_id = StringField("Username: ", 
                          validators=[InputRequired()])
    password = PasswordField("Password", 
                             validators=[InputRequired()])
    password2 = PasswordField("Repeat password: ", 
                             validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class AdminForm(FlaskForm):
    admin = StringField("Admin: ", validators=[InputRequired()])
    passw = PasswordField("Password: ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class ExtraForm(FlaskForm):
    extras = RadioField("Any particular milk preference?",
            choices=["Oat milk", "Soy milk", "Low fat milk", "Whole milk", "None"],
            default="None")
    submit = SubmitField("Submit")

class AddForm(FlaskForm):
    name = StringField("Name of item: ", validators=[InputRequired()])
    price = FloatField("Price of item: ", validators=[InputRequired()])
    desc = StringField("Description of item: ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class RemoveForm(FlaskForm):
    name = StringField("Name of item: ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class EditForm(FlaskForm):
    name = StringField("Name of item: ", validators=[InputRequired()])
    name2 = StringField("New name of item: ")
    price = FloatField("New price of item: ", validators=[InputRequired()])
    desc = StringField("New description of item: ", validators=[InputRequired()])
    submit = SubmitField("Submit")



