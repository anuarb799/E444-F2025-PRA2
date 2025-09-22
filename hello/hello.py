from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    uoftmail = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

def checkmail(form, field):
    if "utoronto" not in field.data.lower():
        raise ValidationError("")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/reset')
def reset():
    session.pop('name', None)
    session.pop('uoftmail', None)
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        uoft_address = session.get('uoftmail')
        
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if uoft_address is not None and uoft_address != form.uoftmail.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['uoftmail'] = form.uoftmail.data
        
        return redirect(url_for('index'))
    
    uoftmail = session.get('uoftmail')

    yesflag = bool(uoftmail and "utoronto" in uoftmail.lower())
    return render_template('index.html', form=form, name=session.get('name'), uoftmail = session.get('uoftmail'), yesflag=yesflag)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
