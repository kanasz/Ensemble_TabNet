import random
import time

import numpy as np
import torch
from imblearn.over_sampling import SMOTE

from base_functions import get_config_files, get_meanshift_cluster_counts, get_glass_4_data
from constants import LossFunction
from models.oc_bagging_tabnet_ensemble_parallel import GaOCBaggingTabnetEnsembleTunerParallel

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

if __name__ == '__main__':
    tabnet_max_epochs = 50
    num_generations = 50
    num_parents = 20  # 10
    population = 50  # 20
    start_time = time.time()
    actual_loss_function = LossFunction.CROSSENTROPYLOSS
    data = get_glass_4_data()
    numerical_cols = numerical_cols = list(data[0].columns.values)
    categorical_cols = None
    sampling_algorithm = SMOTE(random_state=42, k_neighbors=3)
    clusters, bandwidths = get_meanshift_cluster_counts(data[0], data[1], numerical_cols, categorical_cols,sampling_algorithm)

    clustering_params = {
        "bandwidths":bandwidths,
        "clusters":clusters,
        "type":"MS"
    }
    config_files = get_config_files("models/configurations")
    tuner = GaOCBaggingTabnetEnsembleTunerParallel(tabnet_max_epochs, num_generations, num_parents, population,
                                                    config_files=config_files, device='cuda', sampling_algorithm=sampling_algorithm,
                                                    numerical_cols=numerical_cols, categorical_cols=categorical_cols,
                                                    save_partial_output=True,clustering_params = clustering_params)
    tuner.run_experiment(data, 'smote_meanshift_glass_4/OC_TABNET_ENSEMBLE_SMOTE_MEANSHIFT_glass_4')
    print("--- total: %s seconds ---" % (time.time() - start_time))