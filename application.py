from flask import Flask, request, render_template,jsonify
from flask_cors import CORS,cross_origin
from src.pipeline.model_comparison import get_model_comparison_metrics
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app = application
CORS(app)

@app.route('/')
@cross_origin()
def home_page():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def predict_datapoint():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        data = CustomData(
            age = int(request.form.get('age')),
            gender = request.form.get('gender'),
            subscription_type = request.form.get('subscription_type'),
            watch_hours = float(request.form.get('watch_hours')),
            last_login_days = int(request.form.get('last_login_days')),
            region = request.form.get('region'),
            device = request.form.get('device'),
            monthly_fee = float(request.form.get('monthly_fee')),
            payment_method = request.form.get('payment_method'),
            number_of_profiles = int(request.form.get('number_of_profiles')),
            avg_watch_time_per_day = float(request.form.get('avg_watch_time_per_day')),
            favorite_genre = request.form.get('favorite_genre')
        )

        pred_df = data.get_data_as_dataframe()

        print(pred_df)

        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(pred_df)
        results = 'Churned' if int(pred['prediction']) == 1 else 'Not Churned'
        return render_template('index.html',results=results,pred_df = pred_df)
    
@app.route('/predictAPI',methods=['POST'])
@cross_origin()
def predict_api():
    if request.method=='POST':
        data = CustomData(
            age = int(request.json['age']),
            gender = request.json['gender'],
            subscription_type = request.json['subscription_type'],
            watch_hours = float(request.json['watch_hours']),
            last_login_days = int(request.json['last_login_days']),
            region = request.json['region'],
            device = request.json['device'],
            monthly_fee = float(request.json['monthly_fee']),
            payment_method = request.json['payment_method'],
            number_of_profiles = int(request.json['number_of_profiles']),
            avg_watch_time_per_day = float(request.json['avg_watch_time_per_day']),
            favorite_genre = request.json['favorite_genre']
        )

        pred_df = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(pred_df)

        dct = {
            'churned': int(pred['prediction']),
            'status': 'Churned' if int(pred['prediction']) == 1 else 'Not Churned',
            'probability': pred['probability'],
        }
        return jsonify(dct)


@app.route('/modelComparisonAPI', methods=['GET'])
@cross_origin()
def model_comparison_api():
    comparison = get_model_comparison_metrics()
    return jsonify(comparison)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)