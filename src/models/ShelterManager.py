import folium as fl
import pandas as pd
from src import constants as c
from src.models import shelter
import numpy as np


class ShelterManager():
    def __init__(self, dataFileName):
        self.dataFileName = dataFileName
        aggregatedData = self.read_file_and_aggregate(dataFileName)
        self.shelters = []
        grouped_df = aggregatedData.groupby(c.DATA_ADDRESS)
        result = {}
        for name, group in grouped_df:
            address_key = tuple(name[:-3])  # Assuming last 3 columns are not part of the address
            if address_key not in result:
                result[address_key] = []
            result[address_key].append(group.to_dict('records'))
        for index, row in aggregatedData.iterrows():
            self.shelters.append(
                shelter.Shelter(row)
            )

    def read_file_and_aggregate(self, file_name):
        # reading the json file of the dataset using the pandas library
        data = pd.read_json(file_name)
        data = data.replace(["M6J1E6"], "M6J 1E6")
        data = data.replace(["M5A-2N2"], "M5A 2N2")
        # data = data.drop(columns=["SHELTER_PROVINCE"], axis=1)
        # Define columns to group by (excluding date and occupancy)
        group_cols = ['ORGANIZATION_NAME', 'SHELTER_NAME', 'SHELTER_ADDRESS', 'SHELTER_CITY', 'SHELTER_PROVINCE',
                      'SHELTER_POSTAL_CODE', 'FACILITY_NAME', 'PROGRAM_NAME', 'SECTOR']

        # Group by the defined columns and aggregate occupancy data
        grouped_df = data.groupby(group_cols).agg(OCCUPANCY_DATES=('OCCUPANCY_DATE', lambda x: x.tolist()),
                                                  OCCUPANCIES=('OCCUPANCY', lambda x: x.tolist()),
                                                  CAPACITIES=('CAPACITY', lambda x: x.tolist()))

        # Reset index to bring grouped columns back as regular columns
        grouped_df = grouped_df.reset_index()
        return grouped_df
