from flask import Flask, render_template, redirect, url_for, request
from wtforms import Form, StringField, TextAreaField, validators, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from flask_bootstrap import Bootstrap
import datetime
import time

now = datetime.datetime.today()
levels = ('5-Star', '4-Star', '3-Star', '2-Star', '1-Star')

app = Flask(__name__)
Bootstrap(app)

def check_checkin_date(form, field):
	if now > field.data:
		raise ValidationError('Input Valid Date')

def check_checkout_date(min=now):
	message = 'Input a valid date'

	def _check_checkout_date(form, field):
		if field.data < min:
			raise ValidationError(message)

	return _check_checkout_date

class SearchForm(Form):
	current_city = StringField('Current City', [
		validators.DataRequired()])
	budget = IntegerField('Budget', [
		validators.NumberRange(min=250, message='Must be more than 250 dollars'),
		validators.DataRequired()])
	people = IntegerField('Number of People', [
		validators.DataRequired(),
		validators.NumberRange(min=1, message='There must be atleast 1 person')])
	checkin = DateField('Check In Date', [
		validators.required(),
		check_checkin_date], format = '%Y-%m-%d')
	checkout = DateField('Check Out Date', [
		validators.required(),
		check_checkin_date,
		check_checkout_date(min=checkin)], format = '%Y-%m-%d')


@app.route('/', methods=['GET', 'POST'])

def index():
	form = SearchForm(request.form)
	if request.method == 'POST' and form.validate():
		current_city = form.current_city.data
		budget = form.budget.data
		people = form.people.data
		checkin = form.checkin.data
		checkout = form.checkout.data

		return redirect(url_for('results'))

	return render_template('index.html', form=form)

class FilterForm(Form):
	current_city = StringField('Current City', [
		validators.DataRequired()])
	budget = IntegerField('Budget', [
		validators.NumberRange(min=250, message='Must be more than 250 dollars'),
		validators.DataRequired()])
	people = IntegerField('Number of People', [
		validators.DataRequired(),
		validators.NumberRange(min=1, message='There must be atleast 1 person')])
	checkin = DateField('Check In Date', [
		validators.required(),
		check_checkin_date], format = '%Y-%m-%d')
	checkout = DateField('Check Out Date', [
		validators.required(),
		check_checkin_date,
		check_checkout_date(min=checkin)], format = '%Y-%m-%d')
	rating = SelectField('Hotel Rating', choices=[(rating, rating) for rating in levels])


@app.route('/results', methods=['GET', 'POST'])

def results():
	form = FilterForm(request.form)
	if request.method == 'POST' and form.validate():
		current_city = form.current_city.data
		budget = form.budget.data
		people = form.people.data
		checkin = form.checkin.data
		checkout = form.checkout.data
		rating = form.rating.data

		return redirect(url_for('results'))

	return render_template('results.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
