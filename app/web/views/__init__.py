import os
from flask import Blueprint, render_template, render_template_string, request, redirect, current_app as app

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import ValidationError, InputRequired
from packager import process_everything

view_blueprint = Blueprint('views', __name__, template_folder='templates')

class SetupForm(FlaskForm):
    content_path = StringField('Content path', validators=[InputRequired('Content path')])
    metadata_filename = StringField('Metadata filename', validators=[InputRequired('Metadata filename')])
    config_filename = StringField('Config filename', validators=[InputRequired('Config filename')])
    project_type = RadioField('Project type',
                choices=["archives", "chc", "etd"], 
                validators=[InputRequired('Project type required.')])

@view_blueprint.route("/setup", methods=["POST", "GET"])
def setup():
    setup_form = SetupForm()
    if setup_form.validate_on_submit():
        process = process_everything(setup_form.project_type.data, setup_form.metadata_filename.data, setup_form.config_filename.data, setup_form.content_path.data)
        if process == 0:
            return render_template_string("see work directory to view generated xml; zipped packages are in zips")
        else:
            return render_template_string("see log for messages; some errors were encountered.")

    return render_template('views/setup.html', title="Packager Setup", form=setup_form)
