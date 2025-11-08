import pandas as pd
import numpy as np
from pathlib import Path
import os


STATE_KEY_NAME = "region_key"
WEATHER_KEY_NAME = "avg_weather_data"
RECOMMENDATION_KEY_NAME = "final_recommendation"
FINAL_RECOMMENDATION_KEY_NAME = "final_profitable_crop"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


WEATHER_CSV_PATH = os.path.join(BASE_DIR, 'data', 'weather_data.csv') 
CROP_CSV_PATH = os.path.join(BASE_DIR, 'data', 'crop_suitability.csv')
SALES_CSV_PATH = os.path.join(BASE_DIR, 'data', 'crop_sales.csv')

REGIONS = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry']

