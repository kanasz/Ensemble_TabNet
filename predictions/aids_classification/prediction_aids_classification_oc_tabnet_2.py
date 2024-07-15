from base_functions import get_fraudulent_claim_on_cars_physical_damage_data, get_aids_data
import time

from constants import LossFunction
from optimization.ga_boosting_aids_tabnet_tuner import GaBoostingAidsTabnetTuner
from optimization.ga_oc_bagging_tabnet_tuner import GaOCBaggingTabnetTuner

if __name__ == '__main__':
    categorical_cols = ['trt', 'hemo', 'homo', 'drugs', 'oprior', 'z30', 'race', 'gender', 'str2', 'strat', 'symptom',
                        'treat', 'offtrt']
    numerical_cols = ['time', 'age', 'wtkg', 'karnof', 'preanti', 'cd40', 'cd420', 'cd80', 'cd820']

    tabnet_max_epochs = 50
    num_generations = 50
    num_parents = 20  # 10
    population = 50  # 20
    start_time = time.time()
    samples = 2139
    data = get_aids_data(samples)
    actual_loss_function = LossFunction.CROSSENTROPYLOSS
    tuner = GaOCBaggingTabnetTuner(tabnet_max_epochs, num_generations, num_parents, population, device='cuda')

    tuner.evaluate_experiment_from_pkl(data, actual_loss_function,
                                       'results/OC_BAGGING_CROSSENTROPYLOSS_AIDS_{}_samples_{}_epochs'.format(samples, tabnet_max_epochs))
