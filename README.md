sdoh-clustering
==============================

An end to end example of a k-means clustering model for the Nashville Analytics Summit tutorial. We use publicly available data on the social determinants of health.


## Getting started
1. Clone or download this repository (need [help](https://help.github.com/en/articles/cloning-a-repository)?)

2. Install Python 3.4 or greater. We recommend the [Anaconda](https://www.anaconda.com/distribution/) distribution unless you are comfortable with package installation, Jupyter Lab/Notebook, and running Python scripts at the terminal (Mac) or Anaconda Prompt/Power Shell (Windows).

*If using an alternate distribution make sure you have installed numpy, pandas, scikit-learn (sklearn), matplotlib, seaborn, click, pytest, and Jupyter Lab. We will also make use of the standard packages logging, pickle, and pathlib.*

**Steps 3-6 will be covered in the tutorial, but are a good way to verify your requirements**

3. Start a Terminal (Mac) or the Anaconda Prompt (Windows). Type `jupyter lab` at the prompt and hit enter to start JupyterLab. It should open in a broswer window.

4. Navigate to your copy of this repository in the Jupyter Lab navigation pane on the left. Continue to the `sdoh-clustering/notebooks` subfolder and double click to open `2.0-clustering.ipynb`.

5. Open a terminal in Jupyter Lab (File -> New -> Terminal) and navigate to your copy of the `sdoh-clustering` folder. You can use `cd` to navitage on the command line:

```
cd /your/path/to/sdoh-clustering
```

6. Run `conda install pytest` at the terminal



**Extra Credit:**


7. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter) and create a new cookie cutter data science project by running the following at the terminal (Mac) or Anaconda prompt (Windows):

```
conda install -c conda-forge cookiecutter
cookiecutter https://github.com/drivendata/cookiecutter-data-science
```

8. Create a fresh conda environment, set it as the kernel for the notebook in this tutorial, and install required packages (can use environment.yml from github - see below)





## Development Environment
If you wish to replicate an anaconda environment with all requirements (excluding jupyter lab/notebook) run
`conda env create -f environment.yml` from the top level directory.

Note you can create your own environment yaml files using the command `conda env export > environment.yml`.
See the [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) documentation for more details. If you are not utilizing conda, you can acheive similar results with [pip](https://pip.pypa.io/en/stable/user_guide/#requirements-files).

## Data
As the dataset we use is small and publicly available, all raw, interim and processed datasets are included in the repository. If you wish to recreate the dataset, the raw data can be downloaded from http://www.countyhealthrankings.org/sites/default/files/chr_measures_CSV_2018.csv. Save `chr_measures_CSV_2018.csv` file in `data/raw` and run the command line script `make_dataset.py` from the top level directory of the project:

`python src/data/make_dataset.py --help`

If run with defaults, an interim dataset with mapped column names and all data will be written to `data/interim/chr_interim_2018.csv` and the final processed dataset ready to be used in the clustering will be written to `data/processed/chr_final_2018.csv`. The final dataset has only the columns to be used in the clustering and contains only county and county equivlent geographies - meaning state and national level information is dropped.

If you wish to run a model with different variables, you could start from the interim dataset or modify the source code to change the variables included in the final dataset.

## Clustering Model
After running `make_dataset.py` the clustering model can be trained using `notebooks/2.0-clustering.ipynb`. If needed, documentation on Jupyter notebooks can be found [here](https://jupyter.org/). The variables for this particular clustering model were selected using a combination of variance inflation factor to iteratively eliminate variables and business needs.

## Tests
Tests can be run using the pytest package. Simply run the command `pytest` from the terminal in the top level directory of the project in order to run all tests.

## Contact
Erica Zuhr - erica_zuhr@onlifehealth.com

Catherine Bass - cbass@onlifehealth.com


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
