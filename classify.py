import random
import time
import joblib
import numpy as np
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import LinearSVC

import util
from sklearn.feature_extraction.text import TfidfVectorizer
from util import logger


def solution(mal_path_train, good_path_train):
    mal_path_train += "/json"
    good_path_train += "/json"

    mal_data_train = util.get_file_list(mal_path_train)
    good_data_train = util.get_file_list(good_path_train)
    all_data = []
    all_data.extend(mal_data_train)
    all_data.extend(good_data_train)

    feature_vector = TfidfVectorizer(input='filename', tokenizer=lambda x: x.split('\n'), token_pattern=None,
                                     binary=True)

    mal_labels = np.ones(len(good_data_train))
    good_labels = np.empty(len(mal_data_train))
    good_labels.fill(-1)
    y = np.concatenate((mal_labels, good_labels), axis=0)
    logger.info("label generated successfully")

    x_train_samples, x_test_samples, y_train, y_test = train_test_split(all_data, y, test_size=0.3,
                                                                        random_state=random.randint(0, 100))
    x_train = feature_vector.fit_transform(x_train_samples)
    x_test = feature_vector.transform(x_test_samples)

    time_pre = time.time()
    logger.info("start to train the svm model...")
    parameters = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
    grid = GridSearchCV(LinearSVC(), parameters, cv=3, scoring='f1', n_jobs=-1)
    models = grid.fit(x_train, y_train)
    logger.info(
        "find the best model successfully after %s sec." % (round(time.time() - time_pre, 2)))
    model = models.best_estimator_
    logger.info("Best Model Selected : {}".format(model))
    print("the name of the model:")
    model_name = input()
    joblib.dump(grid, model_name + ".pkl")

    time_pre = time.time()
    y_predict = models.predict(x_test)
    logger.info("time for classification is %s sec." % (round(time.time() - time_pre, 2)))
    accuracy = accuracy_score(y_test, y_predict)
    logger.info("the accuracy = {}".format(accuracy))
    print(metrics.classification_report(y_test,
                                        y_predict, labels=[1, -1],
                                        target_names=['malware', 'goodware']))
