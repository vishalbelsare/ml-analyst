import sys
import pandas as pd
import numpy as np

from sklearn.feature_selection import SelectFromModel, RFE
from sklearn.ensemble import ExtraTreesClassifier

from sklearn.ensemble import RandomForestClassifier
from evaluate_model import evaluate_model
from preprocessors import preprocessor_dict

# inputs
dataset = sys.argv[1]
save_file = sys.argv[2]
num_param_combinations = int(sys.argv[3])
random_seed = int(sys.argv[4])
preps = sys.argv[5]


np.random.seed(random_seed)

# construct pipeline
pipeline_components = []
pipeline_parameters = {}

for p in preps.split(','):
    pipeline_components.append(preprocessor_dict[p])
    if pipeline_components[-1] is SelectFromModel:
        pipeline_parameters[SelectFromModel] = [{'estimator': ExtraTreesClassifier(n_estimators=100, random_state=324089)}]
    elif pipeline_components[-1] is RFE:
        pipeline_parameters[RFE] = [{'estimator': ExtraTreesClassifier(n_estimators=100, random_state=324089)}]

pipeline_components.append(RandomForestClassifier)

# parameters for method
n_estimators_values = np.random.choice(list(range(50, 1001, 50)), size=num_param_combinations)
min_impurity_decrease_values = np.random.exponential(scale=0.01, size=num_param_combinations)
max_features_values = np.random.choice(list(np.arange(0.01, 1., 0.01)) + ['sqrt', 'log2', None], size=num_param_combinations)
criterion_values = np.random.choice(['gini', 'entropy'], size=num_param_combinations)
max_depth_values = np.random.choice(list(range(1, 51)) + [None], size=num_param_combinations)

all_param_combinations = zip(n_estimators_values, min_impurity_decrease_values, max_features_values, criterion_values, max_depth_values)
pipeline_parameters[RandomForestClassifier] = \
   [{'n_estimators': n_estimators, 'min_impurity_decrease': min_impurity_decrease, 'max_features': max_features, 'criterion': criterion, 'max_depth': max_depth, 'random_state': 324089}
     for (n_estimators, min_impurity_decrease, max_features, criterion, max_depth) in all_param_combinations]

#evaluate
evaluate_model(dataset, save_file, random_seed, pipeline_components, pipeline_parameters)
