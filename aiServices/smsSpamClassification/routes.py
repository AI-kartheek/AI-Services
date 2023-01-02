import os 
from flask import Blueprint, render_template, redirect, url_for, request
from aiServices.smsSpamClassification.forms import PredictForm, PredictBatchForm
from aiServices.smsSpamClassification.predict import getPrediction, getBatchPrediction
from aiServices import app 

smsSpamClassif = Blueprint('smsSpamClassification', __name__)

@smsSpamClassif.route("/services/sms-spam-classification")
def details():
    return render_template("smsSpamClassification/details.html", title="sms-spam-classification")

@smsSpamClassif.route("/services/sms-spam-classification/predict", methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    spam_score, ham_score = None, None
    show_output = False
    if form.validate_on_submit():
        content = form.content.data 
        # spam_score = getPrediction(content) *100
        spam_score = 99.8
        ham_score = round(100 - spam_score, 1)
        show_output = True 
        # return redirect(url_for('smsSpamClassification.predict'))
    return render_template("smsSpamClassification/predict.html", title="predict", showPredict=False, form=form, spam_score=spam_score, ham_score=ham_score, show_output=show_output)

@smsSpamClassif.route("/services/sms-spam-classification/predict-batch", methods=['GET', 'POST'])
def predictBatch():
    form = PredictBatchForm()
    spam_count, ham_count, output_file_name = None, None, None
    show_output = False
    if form.validate_on_submit():
        # file_data = request.files.get('file_data')
        # new_file_name = 'input.csv' 
        # input_file_path = os.path.join(app.root_path, 'static/upload/' + new_file_name)
        # file_data.save(input_file_path)
        output_file_name = 'output.csv'
        # output_file_path = os.path.join(app.root_path, 'static/download/' + output_file_name)
        # spam_count, ham_count = getBatchPrediction(input_file_path, output_file_path)
        spam_count, ham_count = 29, 5
        show_output = True
    return render_template("smsSpamClassification/predictBatch.html", title="predict-batch", showPredict=True, form=form, spam_count=spam_count, ham_count=ham_count, show_output=show_output, output_file_name=output_file_name)

