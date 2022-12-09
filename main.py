import classify
import get_apk_data
import argparse
import logging
logging.basicConfig(level=logging.INFO)

def parse_args():
    '''
    Configure all parameters required by this method
    :return: configured args
    '''
    args = argparse.ArgumentParser(description="args for the classification")
    args.add_argument("--test_path", default="./dataset/test",
                      help="apk for test")
    args.add_argument("--mal_train_path", default="./dataset/malware_train",
                      help="malware for the training part")
    args.add_argument("--good_train_path", default="./dataset/goodware_train",
                      help="goodware for the training part")
    args.add_argument("--mal_train_test", default="./dataset/malware_test",
                      help="malware for the testing part")
    args.add_argument("--good_train_test", default="./dataset/goodware_test",
                      help="goodware for the testing part")
    return args.parse_args()


def classification(args):
    '''
    step1: Perform feature engineering to extract feature information of all samples
    step2: Generate the characteristic feature space to this method
    step3: Call various classification methods and output various evaluation indicators
    :param args: configured args
    '''
    mal_path_train = args.mal_train_path
    good_path_train = args.good_train_path
    mal_path_test = args.mal_train_test
    good_path_test = args.good_train_test
    # test_path = args.test_path
    # get_apk_data.solution(test_path)
    get_apk_data.solution(mal_path_train, good_path_train, mal_path_test, good_path_test)

    classify.solution(mal_path_train, good_path_train)


if __name__ == '__main__':
    args = parse_args()
    classification(args)


