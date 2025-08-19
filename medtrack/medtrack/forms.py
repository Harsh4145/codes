from __future__ import annotations

from datetime import date

from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DecimalField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=128)])
	remember_me = BooleanField("Remember me")
	submit = SubmitField("Login")


class MedicineForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired(), Length(max=200)])
	manufacturer = StringField("Manufacturer", validators=[Length(max=200)])
	batch_number = StringField("Batch #", validators=[Length(max=100)])
	expiry_date = DateField("Expiry Date", validators=[DataRequired()], format="%Y-%m-%d")
	quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
	low_stock_threshold = IntegerField("Low Stock Threshold", validators=[DataRequired(), NumberRange(min=0)])
	unit_price = DecimalField("Unit Price", places=2, rounding=None, validators=[DataRequired(), NumberRange(min=0)])
	submit = SubmitField("Save")


class TransactionForm(FlaskForm):
	type = SelectField("Type", choices=[("PURCHASE", "Purchase"), ("DISPENSE", "Dispense")], validators=[DataRequired()])
	quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
	notes = TextAreaField("Notes", validators=[Length(max=255)])
	submit = SubmitField("Record")