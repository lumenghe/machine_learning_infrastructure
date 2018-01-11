import time
import xgboost as xgb
import scipy.stats as st
from sklearn.model_selection import ParameterGrid, ParameterSampler
from basemodel import BaseModel


class Model(BaseModel):
    def __init__(self, config):
        super(Model, self).__init__(config)
        self.model = None
        self.training_mode = config["training_mode"]
        if self.training_mode == "base":
            self.settings = {
                    "objective": config["objective"],
                    "eval_metric": config["eval_metric"],
                    "eta": config["eta"],
                    "max_depth": 4,
                    "silent": 1,
                }
            self.num_round = config["num_round"]
            self.early_stopping_rounds = config["early_stopping_rounds"]
        elif self.training_mode == "grid":
            self.settings = {
                    "objective": config["objective"],
                    "booster": config["booster"],
                    "eval_metric": config["eval_metric"],
                    "learning_rate": config["learning_rate"],
                    "lambda": config["lambda"],
                    "max_depth": config["max_depth"],
                    "silent": [1],
                }
            self.eval_metric = config["eval_metric"]
            self.n_iter_search = config["n_iter_search"]
            self.random_seed = config["random_seed"]
            self.kfold = config["kfold"]
            self.num_round = config["num_round"]
            self.early_stopping_rounds = config["early_stopping_rounds"]
        elif self.training_mode == "random":
            raise NotImplementedError
        else:
            raise ValueError("unknown training mode '{}'".format(self.training_mode))

    def init_train_data(self):
        super(Model, self).init_train_data_base()

    def init_submit_data(self, mode):
        super(Model, self).init_submit_data_base(mode)

    def train(self):
        print("Initializing train data...")
        self.init_train_data()
        if self.training_mode == "base":
            self.train_base()
        elif self.training_mode == "grid":
            self.train_grid()
        elif self.training_mode == "random":
            self.train_random()
        else:
            raise ValueError("unknown training mode '{}'".format(self.training_mode))
