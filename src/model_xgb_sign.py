import time
import xgboost as xgb
from basemodel import BaseModel
from preprocessing import preprocess
from data import *
from eval import sign_eval

class Model(BaseModel):
    def __init__(self, config):
        super(Model, self).__init__(config)
        self.model = None
        self.settings = {}
        self.settings["eta"] = config["eta"]
        self.settings["objective"] = config["objective"]
        self.settings["eval_metric"] = config["eval_metric"]
        self.settings["max_depth"] = 4
        self.settings["silent"] = 1
        self.num_round = config["num_round"]
        self.early_stopping_rounds = config["early_stopping_rounds"]

    def init_train_data(self):
        super(Model, self).init_train_data_base()

    def train(self):
        print("Initializing train data...")
        self.init_train_data()
        print("Start model fitting...")
        t = time.time()
        xgb_train = xgb.DMatrix(self.xtrain.values, label=self.ytrain.values)
        xgb_valid = xgb.DMatrix(self.xvalid.values, label=self.yvalid.values)
        watchlist = [(xgb_train, "train"), (xgb_valid, "valid")]
        self.model = xgb.train(self.settings, xgb_train, self.num_round, watchlist, early_stopping_rounds=self.early_stopping_rounds, verbose_eval=10)
        total_time = int(time.time() - t)
        print("Trained model in {} secs".format(total_time))

    def save(self):
        self.model.save_model(self.params)
        print("Saved model at: {}".format(self.params))

    def load(self):
        self.model = xgb.Booster(model_file=self.params)
        print("Loaded model from: {}".format(self.params))

    def predict_from_x(self, x):
        xbg_data = xgb.DMatrix(x)
        pred = self.model.predict(xbg_data)
        return pred

    def eval(self):
        if self.config["eval_cat"] is not None:
            sign_eval(self, self.config)