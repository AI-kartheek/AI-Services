from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PredictForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Predict')

class PredictBatchForm(FlaskForm):
	file_data = FileField('Upload CSV File')
	submit = SubmitField('Predict Batch')