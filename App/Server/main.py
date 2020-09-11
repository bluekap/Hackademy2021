import io
import os

from flask import Flask, render_template, request, jsonify, redirect

import ocr
import parsingtesting
import budget

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./uploads/"
app.config['RESOURCE_FOLDER'] = "./resources/"


@app.route('/')
def home():
	########## Insert Visualizations according to the JSON ###################

	return {"user" : "George W.", "spends" : budget.get_spends(), 'thresholds' : budget.get_budget()}



@app.route('/ocr')
def ocr(url = "gs://images-hackathon-288506/images/billing-invoice-with-payment-plan.png"):
	image = request.files['file']
	if image.filename != None:
		file_path = os.path.join(app.config["UPLOAD_FOLDER"],image.filename)
		image.save(file_path)
		print("File saved successfully : {}".format(file_path))
		texts = ocr.get_text_from_url(url)
		############# Insert Function Call here to identify products & respective value ################
		parsed_output = parsingtesting.get_products()
		######## and then Mapping to categories ###############

	return "File saved successfully"


@app.route('/offers')
def offers():
	return "George, based on your purchases\n We would like to offer you a 9% discount on your next Apparel Shopping!!\n Use BBJJKKK2020 for your purchase!"


@app.route('/budget')
def budget():
	if request.method == "POST":
		new_data = request.get("data")
		budget.update_spends(new_data)
	############################## Insert Budget App call here #########################
	else:
		return budget.get_budget()


@app.route('/notifs')
def get_notifs():
	return {'data':["You have exceeded your Apparel Budget for September exceeded by 15%","Grocery spends reached 50%", "Electronics spends reached 90%"]}


if __name__ == "__main__":
	app.run(port=int(443))