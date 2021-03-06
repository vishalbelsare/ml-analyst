import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.tree import DecisionTreeClassifier
from evaluate_model import evaluate_model

dataset = sys.argv[1]
num_param_combinations = int(sys.argv[2])
random_seed = int(sys.argv[3])

np.random.seed(random_seed)

pipeline_components = [RobustScaler, DecisionTreeClassifier]
pipeline_parameters = {}

min_impurity_decrease_values = np.random.exponential(scale=0.01, size=num_param_combinations)
max_features_values = np.random.choice(list(np.arange(0.01, 1., 0.01)) + ['sqrt', 'log2', None], size=num_param_combinations)
criterion_values = np.random.choice(['gini', 'entropy'], size=num_param_combinations)
max_depth_values = np.random.choice(list(range(1, 51)) + [None], size=num_param_combinations)

all_param_combinations = zip(min_impurity_decrease_values, max_features_values, criterion_values, max_depth_values)
pipeline_parameters[DecisionTreeClassifier] = \
   [{'min_impurity_decrease': min_impurity_decrease, 'max_features': max_features, 'criterion': criterion, 'max_depth': max_depth, 'random_state': 324089}
     for (min_impurity_decrease, max_features, criterion, max_depth) in all_param_combinations]

evaluate_model(dataset, pipeline_components, pipeline_parameters)
