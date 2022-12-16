import matplotlib.pyplot as plt
from data.dataset_tools import generate_basic_timeseries_splitted_normalized_dataset
import torch
import numpy as np
from metrics import Metrics

if __name__ == '__main__':

    model_type = "nice"

    model_name = "model_1"

    if model_type == "simple_gan":
        from parameters.simple_gan import Model
        from parameters.simple_gan.utils import Trainer
        model = Model(len_input=10)
        trainer = Trainer(model)

    if model_type == "nice":
        from parameters.nice import NICE
        from parameters.nice.utils import Trainer
        size_uniform_windows = 1/13
        noise_input = torch.distributions.Normal(
            torch.tensor(0.), torch.tensor(1.))

        coupling = 4
        len_input_output = 10
        mid_dim = 10
        hidden = 4
        mask_config = 1.

        model = NICE(prior=size_uniform_windows,
                     coupling=coupling,
                     len_input=len_input_output,
                     mid_dim=mid_dim,
                     hidden=hidden,
                     mask_config=mask_config)

        trainer = Trainer(model)

    elif model_type == "nice_conditional":
        from parameters.nice_conditional import NICE_CONDITIONAL
        from parameters.nice_conditional.utils import Trainer
        sigma = 0.1
        noise_input = torch.distributions.Normal(
            torch.tensor(0.), torch.tensor(1.))
        coupling = 4
        len_input_output = 10
        mid_dim = 10
        # hidden = 4
        hidden = 4
        mask_config = 1
        model = NICE_CONDITIONAL(prior=noise_input,
                                 coupling=coupling,
                                 len_input=len_input_output,
                                 mid_dim=mid_dim,
                                 hidden=hidden,
                                 mask_config=mask_config)
        trainer = Trainer(model, 0.1)

    model_path = "parameters/{}/models_saved/{}.pt".format(
        model_type, model_name)
    dataset = generate_basic_timeseries_splitted_normalized_dataset(
        "df_train", proportion_test=0.8)
    training_set = dataset[0][0]
    testing_set = dataset[0][1]
    max_temperature = dataset[1]
    min_temperature = dataset[2]
    model_trained = trainer.load_model(model_path)

    time = testing_set[1]
    time_interval = [time[0], time[-1]]

    n_test = len(time)

    generated_sample = trainer.generate_sample(n_test, time_interval)

    fig, axs = plt.subplots(nrows=10, ncols=2, figsize=(10, 30))
    fig.subplots_adjust(hspace=.5, wspace=0.5)

    for i in range(10):
        axs[i][0].hist(testing_set[0][:, i], bins=30)
        axs[i][0].axis(xmin=-0.5, xmax=0.5)
        axs[i][1].hist(generated_sample[:, i], bins=30)
        axs[i][1].axis(xmin=-0.5, xmax=0.5)
    plt.show()
