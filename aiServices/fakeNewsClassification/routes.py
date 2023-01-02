import os 
from flask import Blueprint, render_template, redirect, url_for, request
from aiServices.fakeNewsClassification.forms import PredictForm, PredictBatchForm
from aiServices.fakeNewsClassification.predict import getPrediction, getBatchPrediction
from aiServices import app 

fakeNewsClassif = Blueprint('fakeNewsClassification', __name__)

@fakeNewsClassif.route("/services/fake-news-classification")
def details():
    return render_template("fakeNewsClassification/details.html", title="fake-news-classification")

@fakeNewsClassif.route("/services/fake-news-classification/predict", methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    fake_score, real_score = None, None
    show_output = False
    if form.validate_on_submit():
        content = form.content.data 
        fake_score = getPrediction(content) *100
        # fake_score = 99.8
        real_score = round(100 - fake_score, 1)
        show_output = True 
        # return redirect(url_for('fakeNewsClassification.predict'))
    return render_template("fakeNewsClassification/predict.html", title="predict", showPredict=False, form=form, fake_score=fake_score, real_score=real_score, show_output=show_output)

@fakeNewsClassif.route("/services/fake-news-classification/predict-batch", methods=['GET', 'POST'])
def predictBatch():
    form = PredictBatchForm()
    fake_count, true_count, output_file_name = None, None, None
    show_output = False
    if form.validate_on_submit():
        file_data = request.files.get('file_data')
        new_file_name = 'input.csv' 
        input_file_path = os.path.join(app.root_path, 'static/upload/' + new_file_name)
        file_data.save(input_file_path)
        output_file_name = 'output.csv'
        output_file_path = os.path.join(app.root_path, 'static/download/' + output_file_name)
        fake_count, true_count = getBatchPrediction(input_file_path, output_file_path)
        # fake_count, true_count = 29, 5
        show_output = True
    return render_template("fakeNewsClassification/predictBatch.html", title="predict-batch", showPredict=True, form=form, fake_count=fake_count, true_count=true_count, show_output=show_output, output_file_name=output_file_name)

