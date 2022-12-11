import matplotlib.pyplot as plt
from data.dataset_tools import generate_basic_timeseries_splitted_normalized_dataset
import torch
import numpy as np

model_type = "nice"
model_name = "model_1"

if model_type == "simple_gan":
    from models.simple_gan import Model
    from models.simple_gan import Trainer
    model = Model()
    trainer = Trainer(model)
    model_path = "parameters/simple_gan/{}.pt".format(model_name)

if model_type == "nice":
    from models.nice import NICE
    from models.nice import Trainer
    noise_input = torch.distributions.Normal(
        torch.tensor(0.), torch.tensor(1.))

    coupling = 4
    len_input_output = 10
    mid_dim = 10
    hidden = 4
    mask_config = 1.

    model = NICE(prior=noise_input, 
            coupling=coupling, 
            len_input=len_input_output, 
            mid_dim=mid_dim, 
            hidden=hidden, 
            mask_config=mask_config)


dataset = generate_basic_timeseries_splitted_normalized_dataset("df_train", proportion_test = 1.)
training_set = dataset[0][0]
testing_set = dataset[0][1]
max_temperature = dataset[1]
min_temperature = dataset[2]

model_trained = trainer.load_model(model_path)


time = training_set[1]
time_interval = [time[0], time[-1]]

n_test = 10000

generated_sample = trainer.generate_sample( n_test , time_interval)
print(generated_sample.shape)

fig, axs = plt.subplots(nrows=10, ncols=2, figsize=(10, 30))
fig.subplots_adjust(hspace = .5, wspace=0.5)

axs = axs.ravel()

for i in range(10):
    axs[2*i].hist(training_set[0][:,i])
    axs[2*i+1].hist(generated_sample[:,i],bins=30)
    axs[2*i+1].axis(xmin=0.,xmax=1.)

plt.show()