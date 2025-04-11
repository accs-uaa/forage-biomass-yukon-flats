# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process automated checks
# Author: Timm Nawrocki
# Last Updated: 2025-04-09
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Post-process automated checks" creates attribute tables and pyramids for rasters that result from the automated checks.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
from akutils import *
import arcpy

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data')
work_geodatabase = os.path.join(project_folder, 'AKVEG_YukonFlats.gdb')
output_folder = os.path.join(project_folder, 'Data_Input/stratification')

# Define input datasets
parsed_input = os.path.join(output_folder, 'intermediate/AKVEG_Parsed_10m_3338.tif')

# Define attribute dictionaries
parsed_dictionary = {0: 'not assigned',
                     1: 'coniferous trees',
                     2: 'deciduous trees',
                     3: 'mixed trees',
                     4: 'shrub mesic',
                     5: 'shrub wet',
                     6: 'herbaceous mesic',
                     7: 'herbaceous wet',
                     10: 'spruce-lichen woodland',
                     11: 'white spruce woodland',
                     12: 'white spruce forest',
                     13: 'black spruce woodland',
                     14: 'black spruce forest mesic',
                     15: 'mixed spruce woodland',
                     16: 'mixed spruce forest',
                     17: 'black spruce-tussock woodland',
                     18: 'black spruce peatland',
                     20: 'poplar forest',
                     21: 'aspen forest',
                     22: 'birch forest',
                     30: 'white spruce-poplar forest & woodland',
                     31: 'white spruce-aspen forest & woodland',
                     32: 'white spruce-birch forest & woodland',
                     33: 'black spruce-deciduous forest & woodland',
                     34: 'mixed spruce-birch forest & woodland',
                     40: 'tussock tundra low shrub',
                     41: 'tussock tundra dwarf shrub',
                     50: 'alder mesic',
                     51: 'alder-willow mesic',
                     52: 'willow mesic',
                     53: 'birch-willow mesic',
                     54: 'birch shrub / birch-ericaceous mesic',
                     55: 'dwarf shrub-lichen',
                     56: 'ericaceous dwarf shrub',
                     57: 'dryas-ericaceous dwarf shrub',
                     58: 'dryas-willow dwarf shrub',
                     60: 'shrub-sphagnum wet',
                     61: 'dwarf shrub-sphagnum wet',
                     62: 'alder-willow wet',
                     63: 'willow wet',
                     64: 'birch-willow wet',
                     70: 'Calamagrostis meadow mesic',
                     71: 'forb-graminoid meadow mesic alkaline',
                     72: 'forb-graminoid meadow mesic acidic',
                     80: 'sedge meadow wet',
                     81: 'sedge-Calamagrostis meadow wet',
                     82: 'forb-graminoid meadow wet',
                     90: 'burned',
                     91: 'recent burn recovering birch-willow mesic',
                     92: 'recent burn recovering birch-willow wet',
                     95: 'developed',
                     96: 'barren / sparse',
                     97: 'permanent snow / ice',
                     98: 'water',
                     100: 'white spruce active floodplain',
                     101: 'poplar (white spruce) active floodplain',
                     102: 'birch (white spruce) active floodplain',
                     103: 'alder-willow active floodplain',
                     104: 'willow active floodplain'}

# Retrieve attribute code block
label_block = get_attribute_code_block()

# Post-process parsed foliar cover results
print('Post-processing parsed foliar cover results...')
iteration_start = time.time()
print('\tCalculating statistics...')
arcpy.management.CalculateStatistics(parsed_input)
arcpy.management.BuildRasterAttributeTable(parsed_input, 'Overwrite')
# Calculate attribute label field
print('\tBuilding attribute table...')
label_expression = f'get_response(!VALUE!, {parsed_dictionary}, "value")'
arcpy.management.CalculateField(parsed_input,
                                'label',
                                label_expression,
                                'PYTHON3',
                                label_block)
# Build pyramids
print('\tBuilding pyramids...')
arcpy.management.BuildPyramids(parsed_input,
                               -1,
                               'NONE',
                               'NEAREST',
                               'LZ77',
                               '',
                               'OVERWRITE')
end_timing(iteration_start)
