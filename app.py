from flask import Flask, render_template, url_for, flash, redirect, session
from forms import SignupForm, LoginForm, TextForm
from config import SECRET_KEY
import db
import api

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def logged_in():
  if 'email' not in session:
    flash('Please log in first.', 'warning')
    return False
  return True

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if form.validate_on_submit():
    email = form.email.data.lower()
    if db.add_user(form.username.data, email, form.password.data):
      flash(f"Successfully registered {form.username.data}! Please log in.", 'success')
      return redirect(url_for('login'))
    flash('That email is already registered.', 'danger')
  return render_template('signup.html', title='Sign Up', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    email = form.email.data.lower()
    if db.check_user(email, form.password.data):
      session['email'] = email
      flash('Logged in successfully.', 'success')
      return redirect(url_for('profile'))
    flash('Invalid email or password.', 'danger')
  return render_template('login.html', title='Login', form=form)


@app.route('/profile')
def profile():
  if not logged_in():
    return redirect(url_for('login'))
  return render_template('profile.html', title='Profile', email=session['email'])


@app.route('/logout')
def logout():
  session.pop('email', None)
  return redirect(url_for('login'))


@app.route('/ner', methods=['GET', 'POST'])
def ner():
  if not logged_in():
    return redirect(url_for('login'))
  form = TextForm()
  result = None
  if form.validate_on_submit():
    result = api.ner(form.text.data)
    if result:
      db.save_history(session['email'], 'NER', form.text.data, result)
    else:
      flash('Could not analyze the text. Please try again.', 'danger')
  return render_template('ner.html', title='Named Entity Recognition',
                         form=form, result=result)


@app.route('/sentiment_analysis', methods=['GET', 'POST'])
def sentiment_analysis():
  if not logged_in():
    return redirect(url_for('login'))
  form = TextForm()
  result = None
  if form.validate_on_submit():
    result = api.sentiment(form.text.data)
    if result:
      db.save_history(session['email'], 'Sentiment', form.text.data, result)
    else:
      flash('Could not analyze the text. Please try again.', 'danger')
  return render_template('sentiment.html', title='Sentiment Analysis',
                         form=form, result=result)


@app.route('/language_detection', methods=['GET', 'POST'])
def language_detection():
  if not logged_in():
    return redirect(url_for('login'))
  form = TextForm()
  result = None
  if form.validate_on_submit():
    result = api.detect_language(form.text.data)
    if result:
      db.save_history(session['email'], 'Language', form.text.data, result)
    else:
      flash('Could not analyze the text. Please try again.', 'danger')
  return render_template('language.html', title='Language Detection',
                         form=form, result=result)


@app.route('/history')
def history():
  if not logged_in():
    return redirect(url_for('login'))
  rows = db.get_history(session['email'])
  return render_template('history.html', title='History', rows=rows)


if __name__ == '__main__':
  app.run(debug=True)