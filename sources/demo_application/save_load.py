from keras.models import load_model
import json
import datetime


def save(model, filename, model_type):
    model.save(str('../models/'+filename))
    data = {'models': []}
    with open('../models/models_data.json', 'r') as meta:
        data = json.load(meta)
    with open('../models/models_data.json', 'w') as meta:
        data['models'].append({
            'filename': filename,
            'model_type': model_type,
            'create_time': str(datetime.datetime.now())
        })
        json.dump(data, meta)


def load(filename):
    model = load_model(str('../models/'+filename))
    return model
