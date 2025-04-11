# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Enforce minimum mapping unit
# Author: Timm Nawrocki
# Last Updated: 2025-04-09
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Enforce minimum mapping unit" removes and replaces map units less than 1 acre in area.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
from akutils import *
import arcpy
from arcpy.sa import Con
from arcpy.sa import ExtractByAttributes
from arcpy.sa import ExtractByMask
from arcpy.sa import Nibble
from arcpy.sa import Raster
from arcpy.sa import RegionGroup
from arcpy.sa import SetNull

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data')
work_geodatabase = os.path.join(project_folder, 'AKVEG_YukonFlats.gdb')
input_folder = os.path.join(project_folder, 'Data_Input/stratification/intermediate')
output_folder = os.path.join(project_folder, 'Data_Input/stratification')

# Define input datasets
area_input = os.path.join(project_folder, 'Data_Input/YukonFlats_MapDomain_10m_3338.tif')
preliminary_input = os.path.join(input_folder, 'AKVEG_Parsed_10m_3338.tif')

# Define output datasets
region_output = os.path.join(input_folder, 'region_output.tif')
mask_output = os.path.join(input_folder, 'mask_output.tif')
nibble_output = os.path.join(input_folder, 'nibble_output.tif')
revised_output = os.path.join(output_folder, 'YukonFlats_EVT_10m_3338_4.tif')

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

# Set overwrite option
arcpy.env.overwriteOutput = True

# Specify core usage
arcpy.env.parallelProcessingFactor = '0'

# Set workspace
arcpy.env.workspace = work_geodatabase

# Set snap raster and extent
arcpy.env.snapRaster = area_input
arcpy.env.extent = Raster(area_input).extent

# Set output coordinate system
arcpy.env.outputCoordinateSystem = Raster(area_input)

# Set cell size environment
cell_size = arcpy.management.GetRasterProperties(area_input, 'CELLSIZEX', '').getOutput(0)
arcpy.env.cellSize = int(cell_size)

# Enforce MMU
print('Enforcing minimum mapping unit...')
iteration_start = time.time()
# Calculate regions
print('\tCalculating contiguous value areas...')
prelim_raster = Raster(preliminary_input)
region_initial = RegionGroup(prelim_raster,
                             'EIGHT',
                             'WITHIN',
                             'NO_LINK')
print('\tExporting region raster...')
arcpy.management.CopyRaster(region_initial,
                            region_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '32_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(region_output)
# Create mask
print('\tCalculating mask...')
criteria = f'COUNT > 4'
mask_1 = ExtractByAttributes(region_initial, criteria)
mask_2 = SetNull((((prelim_raster >= 0) & (prelim_raster <= 7))
                 | (prelim_raster == 95) | (prelim_raster == 96)
                 | (prelim_raster == 97) | (prelim_raster == 98)),
                 mask_1)
print('\tExporting mask raster...')
mask_export = Con(mask_2 >= 32767, 32767, mask_2)
arcpy.management.CopyRaster(mask_export,
                            mask_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '16_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(mask_output)
# Replace removed data
print('\tReplacing contiguous areas below minimum mapping unit...')
nibble_initial = Nibble(prelim_raster,
                        mask_2,
                        'DATA_ONLY',
                        'PROCESS_NODATA')
# Export nibble raster
print('\tExporting modified raster...')
arcpy.management.CopyRaster(nibble_initial,
                            nibble_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '16_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(nibble_output)
# Add removed data
print('\tReplacing removed values for linear features...')
replace_raster = Con(((prelim_raster == 95) | (prelim_raster == 96)
                      | (prelim_raster == 97) | (prelim_raster == 98)),
                     prelim_raster, nibble_initial)
# Extract raster to study area
print('\tExtracting raster to map domain...')
extract_raster = ExtractByMask(replace_raster, area_input)
# Export modified raster
print('\tExporting modified raster...')
arcpy.management.CopyRaster(extract_raster,
                            revised_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '16_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(revised_output)
arcpy.management.BuildRasterAttributeTable(revised_output, 'Overwrite')
# Calculate attribute label field
print('\tBuilding attribute table...')
label_expression = f'get_response(!VALUE!, {parsed_dictionary}, "value")'
arcpy.management.CalculateField(revised_output,
                                'label',
                                label_expression,
                                'PYTHON3',
                                label_block)
# Build pyramids
print('\tBuilding pyramids...')
arcpy.management.BuildPyramids(revised_output,
                               -1,
                               'NONE',
                               'NEAREST',
                               'LZ77',
                               '',
                               'OVERWRITE')
end_timing(iteration_start)
