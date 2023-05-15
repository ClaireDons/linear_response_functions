# linear_response_functions
Repository for the linear response function (LRF) calculations for BISICLES and analysis, based on [Levermann et al. 2020](https://esd.copernicus.org/articles/11/35/2020/).
This project takes a directory of BISICLES plot files for a LRF simulation run. It then runs the stats file tool to create a csv of summary statistics and subsequently calculate the LRF and rolling mean for that simulation. 

## Setup

1. You need to have the BISICLES filetools compiled on your system, instructions on how to do this can be found [here](https://davis.lbl.gov/Manuals/BISICLES-DOCS/readme.html)
2. Clone the repository to your desired location
3. Create and activate a new virtual environment
4. Install the required Python environment using `pip install -r requirements.txt`

## Usage
### Running the project

To run the project, you should only need to edit the `calculate_lrf.py` file. Change the paths at the top to correspond to yours and change the `EXPERIMENT` variable to the amount of addition basal melt for that simulation. The inputs required are:

* PATH to input data directory with plot files
* MASK_PATH to directory with Antarctica region masks
* CSV_PATH output path for csv files
* STATS_TOOL path to compiled stats filetool driver
* EXPERIMENT number by which basal melt was increased for the run

If you do not have Antarctica region masks, you can create some from the `BISICLES/applications/bedmachine/maskeMasksfromVel` directory. 
