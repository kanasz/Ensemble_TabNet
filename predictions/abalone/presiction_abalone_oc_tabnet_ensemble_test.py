import random
import time

import numpy as np
import torch

from base_functions import get_synthetic_data, get_slovak_data, get_config_files, get_abalone_9_vs_18_data, \
    get_abalone_20_vs_8_9_10_data, get_abalone_3_vs_11_data, get_abalone_19_vs_10_11_12_13_data
from constants import LossFunction, CLUSTER_COUNT, WEAK_CLASSIFIERS_COUNT, SYNTHETIC_MINORITY_COUNT
from models.oc_bagging_tabnet_ensemble_new import GaOCBaggingTabnetEnsembleTunerNew
from models.oc_bagging_tabnet_ensemble_parallel import GaOCBaggingTabnetEnsembleTunerParallel
from optimization.ga_boosting_tabnet_tuner import GaBoostingTabnetTuner
from optimization.ga_oc_bagging_tabnet_ensemble_tuner import GaOCBaggingTabnetEnsembleTuner

seed = 42
torch.manual_seed(seed)
random.seed(seed)
np.random.rand(seed)
random.SystemRandom(seed)
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)  # for multiGPUs.
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


# os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
# warnings.filterwarnings("ignore")
numerical_cols = ['Length', 'Diameter', 'Height', 'Whole_weight', 'Shucked_weight', 'Viscera_weight', 'Shell_weight']
categorical_cols = ['Sex']

if __name__ == '__main__':
    tabnet_max_epochs = 50
    num_generations = 50
    num_parents = 20  # 10
    population = 50  # 20
    start_time = time.time()
    contamination = '0.02'
    features = '200'
    samples = 200
    actual_loss_function = LossFunction.CROSSENTROPYLOSS


    config_files = get_config_files("../../models/configurations")

    tuner = GaOCBaggingTabnetEnsembleTunerParallel(tabnet_max_epochs, num_generations, num_parents, population, config_files=config_files, device='cuda',
                                              numerical_cols=numerical_cols, categorical_cols=categorical_cols)
    data = get_abalone_20_vs_8_9_10_data()
    tuner.evaluate_experiment_from_pkl(data, actual_loss_function,
                                       'results/OC_TABNET_ENSEMBLE_CROSSENTROPYLOSS_abalone_20_vs_8_9_10_0.02_CLUSTER_COUNT_{}_CLASSIFIER_COUNT_{}_SYNTH_COUNT_{}_2'
                                       .format(CLUSTER_COUNT, WEAK_CLASSIFIERS_COUNT, SYNTHETIC_MINORITY_COUNT))
    '''
    tuner = GaOCBaggingTabnetEnsembleTunerParallel(tabnet_max_epochs, num_generations, num_parents, population,
                                              config_files=config_files, device='cuda',
                                              numerical_cols=numerical_cols, categorical_cols=categorical_cols)
    data = get_abalone_9_vs_18_data()
    tuner.evaluate_experiment_from_pkl(data, actual_loss_function,
                                       'results/OC_TABNET_ENSEMBLE_CROSSENTROPYLOSS_abalone_9_vs_18_0.02_CLUSTER_COUNT_{}_CLASSIFIER_COUNT_{}_SYNTH_COUNT_{}'
                                       .format(CLUSTER_COUNT, WEAK_CLASSIFIERS_COUNT, SYNTHETIC_MINORITY_COUNT))

    tuner = GaOCBaggingTabnetEnsembleTunerParallel(tabnet_max_epochs, num_generations, num_parents, population,
                                              config_files=config_files, device='cuda',
                                              numerical_cols=numerical_cols, categorical_cols=categorical_cols)
    data = get_abalone_3_vs_11_data()
    tuner.evaluate_experiment_from_pkl(data, actual_loss_function,
                                       'results/OC_TABNET_ENSEMBLE_CROSSENTROPYLOSS_abalone_3_vs_11_0.02_CLUSTER_COUNT_{}_CLASSIFIER_COUNT_{}_SYNTH_COUNT_{}_2'
                                       .format(CLUSTER_COUNT, WEAK_CLASSIFIERS_COUNT, SYNTHETIC_MINORITY_COUNT))



    tuner = GaOCBaggingTabnetEnsembleTunerParallel(tabnet_max_epochs, num_generations, num_parents, population,
                                              config_files=config_files, device='cuda',
                                              numerical_cols=numerical_cols, categorical_cols=categorical_cols)
    data = get_abalone_19_vs_10_11_12_13_data()
    tuner.evaluate_experiment_from_pkl(data, actual_loss_function,
                                       'results/OC_TABNET_ENSEMBLE_CROSSENTROPYLOSS_abalone_19_vs_10_11_12_13_0.02_CLUSTER_COUNT_{}_CLASSIFIER_COUNT_{}_SYNTH_COUNT_{}_2'
                                       .format(CLUSTER_COUNT, WEAK_CLASSIFIERS_COUNT, SYNTHETIC_MINORITY_COUNT))


    '''






