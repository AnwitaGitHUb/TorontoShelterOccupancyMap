from typing import List

from src import constants as c
from src.models.shelter_program import shelterProgram
import pandas as pd

def init_data(file_name):
    """
    param file_name: The name of the json file which stores all the shelter data.
    :return: Modified pandas dataframe with all shelter information.
    """
    # reading the json file of the dataset using the pandas library
    data = pd.read_json(file_name)
    # replacing invalid postal codes
    data = data.replace(["M6J1E6"], "M6J 1E6")
    data = data.replace(["M5A-2N2"], "M5A 2N2")
    # drop province since it remains constant
    data = data.drop(columns=["SHELTER_PROVINCE"], axis=1)
    # Define columns to group by (excluding date and occupancy)
    group_cols = ['ORGANIZATION_NAME', 'SHELTER_NAME', 'SHELTER_ADDRESS', 'SHELTER_CITY',
                  'SHELTER_POSTAL_CODE', 'FACILITY_NAME', 'PROGRAM_NAME', 'SECTOR']

    # Group by the defined columns and aggregate occupancy data
    grouped_df = data.groupby(group_cols).agg(OCCUPANCY_DATES=('OCCUPANCY_DATE', lambda x: x.tolist()),
                                              OCCUPANCIES=('OCCUPANCY', lambda x: x.tolist()),
                                              CAPACITIES=('CAPACITY', lambda x: x.tolist()))

    # Reset index to bring grouped columns back as regular columns
    grouped_df = grouped_df.reset_index()
    return grouped_df
