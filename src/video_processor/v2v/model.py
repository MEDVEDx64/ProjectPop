import os
import json
import jsonschema

from keras.models import load_model

from .exception import V2VInputError

class ModelDescription(object):
    SCHEMA = {
        'type' : 'object',
        'required': True,
        'properties': {
            'picture': {
                'type': 'object',
                'required': True,
                'properties': {
                    'input': {
                        'type': 'object',
                        'required': True,
                        'properties': {
                            'width': {
                                'type': 'integer',
                                'required': True
                            },
                            'height': {
                                'type': 'integer',
                                'required': True
                            }
                        }
                    },
                    'output': {
                        'type': 'object',
                        'required': True,
                        'properties': {
                            'width': {
                                'type': 'integer',
                                'required': True
                            },
                            'height': {
                                'type': 'integer',
                                'required': True
                            }
                        }
                    }
                }
            }
        }
    }

    def __init__(self, dsc_path: str):
        with open(dsc_path, 'r') as f:
            dsc = json.load(f)
            #jsonschema.validate(dsc, self.SCHEMA)
            self.input_dimensions = (dsc['picture']['input']['width'],
                                     dsc['picture']['input']['height'])
            self.output_dimensions = (dsc['picture']['output']['width'],
                                      dsc['picture']['output']['height'])

class PictureProcessorModel(object):
    def __init__(self, dsc_path):
        if not dsc_path.endswith('.json'):
            raise V2VInputError('Description Path argument must point to a .json file')

        self.model = None
        self.model_path = dsc_path[:-4] + 'h5'
        if not os.path.exists(dsc_path) or not os.path.exists(self.model_path):
            raise V2VInputError('Model (.h5) nor description (.json) files are missing')

        self.description = ModelDescription(dsc_path)
        self.model = load_model(self.model_path)
