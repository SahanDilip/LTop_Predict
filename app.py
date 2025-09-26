from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

def predict_price(features):
    filename = 'website/predictor.pickle'
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model.predict([features])[0]

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint that returns JSON response"""
    try:
        feature_list = []
        EUR_to_LKR = 430

        # Get form data
        ram = int(request.form.get('ram'))
        weight = float(request.form.get('weight'))
        company = request.form.get('company')
        typename = request.form.get('typename')
        opsys = request.form.get('opsys')
        cpuname = request.form.get('cpuname')
        gpuname = request.form.get('gpuname')
        touchscreen = 1 if request.form.get("touchscreen") else 0
        ips = 1 if request.form.get("ips") else 0

        # Build feature list (same as your existing code)
        feature_list.append(ram)
        feature_list.append(weight)
        feature_list.append(touchscreen)
        feature_list.append(ips)

        # One-hot encoding (same as your existing code)
        companies = ['Acer', 'Apple', 'Asus', 'Dell', 'HP', 'Lenovo', 'MSI', 'Other', 'Toshiba']
        for c in companies:
            feature_list.append(1 if company.lower() == c.lower() else 0)

        typen = ['2 in 1 Convertible','Gaming','Netbook','Notebook','Ultrabook','Workstation']
        for t in typen:
            feature_list.append(1 if typename == t else 0)

        oss = ['Chrome OS','Linux','Mac','No OS','Other','Windows']
        for o in oss:
            feature_list.append(1 if opsys == o else 0)

        cpus = ['AMD','Intel Celeron Dual','Intel Core M','Intel Core i3','Intel Core i5',
                'Intel Core i7','Intel Pentium Quad','Other']
        for cpu in cpus:
            feature_list.append(1 if cpuname == cpu else 0)

        gpus = ['AMD','Intel','Nvidia']
        for g in gpus:
            feature_list.append(1 if gpuname == g else 0)
            
        pred = predict_price(feature_list)
        pred_in_lkr = pred * EUR_to_LKR

        return jsonify({
            'success': True,
            'prediction': pred_in_lkr,
            'currency': 'LKR'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
