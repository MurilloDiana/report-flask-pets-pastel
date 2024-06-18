from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pandas as pd

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://osder:78575353@cluster0.jdqqlsg.mongodb.net/vet_cristo?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

@app.route('/api/report_pets')
def report():
    try:
        visits = list(mongo.db.visits.find())
        pets = list(mongo.db.pets.find())
        df_visits = pd.DataFrame(visits)
        df_pets = pd.DataFrame(pets)

        df_visits['date'] = pd.to_datetime(df_visits['date'])
        merged_df = df_visits.merge(df_pets, left_on='id_Patient', right_on='id')
        atenciones_por_species = merged_df['specie'].value_counts()

        data = {
            'species': atenciones_por_species.index.tolist(),
            'counts': atenciones_por_species.tolist()
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



