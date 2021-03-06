from fastai.text import *
from .databunch import DashTextDatabunch

import fastai
import torch.optim
from fastai.text.models.transformer import init_transformer
import copy

class DashTextLearner:

    @staticmethod
    def create_text_learner(response):
        path = Path('./tmp/models/')

        if response['text']['model']['type'] == "classifier":
            data, data_lm = DashTextDatabunch.create_text_databunch(response)
            c_method = response['text']['model']['classifier']['method']
            l_method = response['text']['model']['language_model']['method']
            response_lm = copy.deepcopy(response)
            response_lm['core']['data']['label']['method'] = 'for_lm'
            lm = DashTextLearner.create_text_lm_learner_default(data_lm, response['text']['model']['language_model']['default'])
            lm.fit_one_cycle(response["text"]["model"]["classifier"]["lm_train_epochs"])
            lm.save_encoder('lm_encoder')
            data.vocab.itos = data_lm.vocab.itos
            clas = DashTextLearner.create_text_classifier_learner_default(data, response['text']['model']['classifier']['default'])
            clas.load_encoder('lm_encoder')
            return clas
        
        if response['text']['model']['type'] == "language_model":
            data = DashTextDatabunch.create_text_databunch(response)
            if response['text']['model']['language_model']['method'] == "default":
                return DashTextLearner.create_text_lm_learner_default(data, response['text']['model']['language_model']['default'])

    
    @staticmethod
    def create_text_lm_learner_default(data, response):

        if response["arch"] == 'AWD_LSTM':
            config = response['configs']['AWD_LSTM']

        if response["arch"] == 'Transformer':
            config = response['configs']['Transformer']
            config['act'] = eval(config['act'])
            config['init'] = eval(config['init'])

        if response["arch"] == 'TransformerXL':
            config = response['configs']['TransformerXL']
            config['act'] = eval(config['act'])
            config['init'] = eval(config['init'])
        
        arch = eval(response['arch'])
        return language_model_learner(data, arch, config = config, **response['extra'])


    @staticmethod
    def create_text_classifier_learner_default(data, response):

        if response["arch"] == 'AWD_LSTM':
            config = response['configs']['AWD_LSTM']

        if response["arch"] == 'Transformer':
            config = response['configs']['Transformer']
            config['act'] = eval(config['act'])
            config['init'] = eval(config['init'])

        if response["arch"] == 'TransformerXL':
            config = response['configs']['TransformerXL']
            config['act'] = eval(config['act'])
            config['init'] = eval(config['init'])

        arch = eval(response['arch'])
        return text_classifier_learner(data, arch, config = config, **response['extra'])
