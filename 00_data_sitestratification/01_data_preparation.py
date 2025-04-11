# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Pre-process rasters
# Author: Timm Nawrocki
# Last Updated: 2025-04-08
# Usage: Execute in Python 3.9+.
# Description: "Pre-process rasters" combines adjacent raster tiles and extracts rasters to common extent, mask, grid, cell size, data type, and no data value.
# ---------------------------------------------------------------------------

# Import packages
import os
import glob
import time
import numpy as np
import rasterio
from osgeo import gdal
from osgeo.gdalconst import GDT_Byte
from osgeo.gdalconst import GDT_Int16
from akutils import *

# Set nodata value
nodata = -32768

# Configure GDAL
gdal.UseExceptions()

# Set root directory
drive = 'C:/'
root_folder = 'ACCS_Work'

# Define folder structure
veg10m_folder = os.path.join(drive, root_folder,
                             'Projects/VegetationEcology/AKVEG_Map/Data',
                             'Data_Output/data_package/version_2.0_20250103')
veg30m_folder = os.path.join('D:/', root_folder, 'Data/biota/vegetation/Alaska_PFT_TimeSeries/original')
topography_folder = os.path.join('D:/', root_folder, 'Data/topography/Alaska_Composite_DTM_10m/integer')
hydrography_folder = os.path.join('D:/', root_folder, 'Data/hydrography/processed')
intermediate_folder = os.path.join('D:/', root_folder,
                                   'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                                   'Data_Input/data_intermediate')
output_folder = os.path.join('D:/', root_folder,
                             'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                             'Data_Input/data_output')

# Define input files
area_file = os.path.join('D:/', root_folder,
                         'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                         'Data_Input/YukonFlats_MapDomain_10m_3338.tif')
fire_file = os.path.join(drive, root_folder,
                           'Projects/VegetationEcology/AKVEG_Map/Data',
                           'Data_Input/ancillary_data/processed/AlaskaYukon_FireYear_10m_3338.tif')
floodplain_file = os.path.join('D:/', root_folder,
                               'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                               'Data_Input/ancillary_data/unprocessed/floodplain_10m_3338.tif')
esa_file = os.path.join(drive, root_folder,
                        'Projects/VegetationEcology/AKVEG_Map/Data',
                        'Data_Input/ancillary_data/processed/AlaskaYukon_ESAWorldCover2_10m_3338.tif')
esri_file = os.path.join('D:/', root_folder,
                         'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                         'Data_Input/ancillary_data/unprocessed/esrilc_10m_3338.tif')
height_file = os.path.join('D:/', root_folder,
                           'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                           'Data_Input/canopy_height/intermediate/height_10m_3338.tif')
alkaline_file = os.path.join('D:/', root_folder,
                         'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                         'Data_Input/ancillary_data/unprocessed/alkaline_10m_3338.tif')
correction_file = os.path.join('D:/', root_folder,
                         'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data',
                         'Data_Input/ancillary_data/unprocessed/correction_10m_3338.tif')

# Create input list for vegetation 10 m
veg10m_list = ['alnus', 'betshr', 'bettre', 'brotre', 'dryas', 'dsalix', 'empnig', 'erivag',
               'mwcalama', 'ndsalix', 'nerishr', 'picgla', 'picmar', 'poptre', 'populbt',
               'rhoshr', 'sphagn', 'vaculi', 'vacvit', 'wetsed']
veg30m_list = ['tmLichenLight', 'Graminoid', 'Forb']
veg30m_names = ['lichen', 'gramin', 'forb']
topography_list = ['Elevation', 'Exposure', 'HeatLoad', 'Position',
                   'RadiationAspect', 'Relief', 'Roughness', 'Slope']
topography_names = ['elevat', 'expos', 'heatload', 'position',
                    'aspect', 'relief', 'rough', 'slope']
hydrography_list = ['RiverDist', 'StreamDist', 'Wetness']
hydrography_names = ['river', 'stream', 'wetness']

# Define area bounds
area_bounds = raster_bounds(area_file)

# Process vegetation 10 m
count = 0
for name in veg10m_list:
    # Define input file
    input_file = os.path.join(veg10m_folder, name, name + '_10m_3338.tif')
    # Define output file
    output_file = os.path.join(intermediate_folder, name + '_10m_3338.tif')
    if os.path.exists(output_file) == 0:
        print(f'Processing data for {name}...')
        iteration_start = time.time()
        # Resample and reproject
        gdal.Warp(output_file,
                  input_file,
                  srcSRS='EPSG:3338',
                  dstSRS='EPSG:3338',
                  outputType=GDT_Int16,
                  workingType=GDT_Byte,
                  xRes=10,
                  yRes=-10,
                  srcNodata=255,
                  dstNodata=nodata,
                  outputBounds=area_bounds,
                  resampleAlg='bilinear',
                  targetAlignedPixels=False,
                  creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
        end_timing(iteration_start)
    count += 1

# Process vegetation 30 m
count = 0
for name in veg30m_list:
    # Define input file
    input_file = os.path.join(veg30m_folder, 'ABoVE_PFT_Top_Cover_' + name + '_2020.tif')
    # Define output file
    output_name = veg30m_names[count]
    output_file = os.path.join(intermediate_folder, output_name + '_10m_3338.tif')
    if os.path.exists(output_file) == 0:
        print(f'Processing data for {name}...')
        iteration_start = time.time()
        # Resample and reproject
        gdal.Warp(output_file,
                  input_file,
                  srcSRS='ESRI:102001',
                  dstSRS='EPSG:3338',
                  outputType=GDT_Int16,
                  workingType=GDT_Byte,
                  xRes=10,
                  yRes=-10,
                  srcNodata=255,
                  dstNodata=nodata,
                  outputBounds=area_bounds,
                  resampleAlg='bilinear',
                  targetAlignedPixels=False,
                  creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
        end_timing(iteration_start)
    count += 1

# Process topography data
count = 0
for name in topography_list:
    # Define input file
    input_file = os.path.join(topography_folder, name + '_10m_3338.tif')
    # Define output file
    output_name = topography_names[count]
    output_file = os.path.join(intermediate_folder, output_name + '_10m_3338.tif')
    if os.path.exists(output_file) == 0:
        print(f'Processing data for {name}...')
        iteration_start = time.time()
        # Resample and reproject
        gdal.Warp(output_file,
                  input_file,
                  srcSRS='EPSG:3338',
                  dstSRS='EPSG:3338',
                  outputType=GDT_Int16,
                  workingType=GDT_Int16,
                  xRes=10,
                  yRes=-10,
                  srcNodata=nodata,
                  dstNodata=nodata,
                  outputBounds=area_bounds,
                  resampleAlg='bilinear',
                  targetAlignedPixels=False,
                  creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
        end_timing(iteration_start)
    count += 1

# Process hydrography data
count = 0
for name in hydrography_list:
    # Define input file
    input_file = os.path.join(hydrography_folder, name + '_10m_3338.tif')
    # Define output file
    output_name = hydrography_names[count]
    output_file = os.path.join(intermediate_folder, output_name + '_10m_3338.tif')
    if os.path.exists(output_file) == 0:
        print(f'Processing data for {name}...')
        iteration_start = time.time()
        # Resample and reproject
        gdal.Warp(output_file,
                  input_file,
                  srcSRS='EPSG:3338',
                  dstSRS='EPSG:3338',
                  outputType=GDT_Int16,
                  workingType=GDT_Int16,
                  xRes=10,
                  yRes=-10,
                  srcNodata=nodata,
                  dstNodata=nodata,
                  outputBounds=area_bounds,
                  resampleAlg='bilinear',
                  targetAlignedPixels=False,
                  creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
        end_timing(iteration_start)
    count += 1

# Process floodplain raster
output_file = os.path.join(intermediate_folder, 'floodplain_10m_3338.tif')
if os.path.exists(output_file) == 0:
    print(f'Processing data for floodplain...')
    iteration_start = time.time()
    # Resample and reproject
    gdal.Warp(output_file,
              floodplain_file,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=GDT_Int16,
              workingType=GDT_Int16,
              xRes=10,
              yRes=-10,
              srcNodata=nodata,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Process fire raster
output_file = os.path.join(intermediate_folder, 'fireyear_10m_3338.tif')
if os.path.exists(output_file) == 0:
    print(f'Processing data for fire year...')
    iteration_start = time.time()
    # Resample and reproject
    gdal.Warp(output_file,
              fire_file,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=GDT_Int16,
              workingType=GDT_Int16,
              xRes=10,
              yRes=-10,
              srcNodata=nodata,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Process ESA World Cover raster
output_file = os.path.join(intermediate_folder, 'esacover_10m_3338.tif')
if os.path.exists(output_file) == 0:
    print(f'Processing data for ESA world cover...')
    iteration_start = time.time()
    # Resample and reproject
    gdal.Warp(output_file,
              esa_file,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=GDT_Int16,
              workingType=GDT_Int16,
              xRes=10,
              yRes=-10,
              srcNodata=nodata,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Process ESRI World Cover raster
output_file = os.path.join(intermediate_folder, 'esricover_10m_3338.tif')
if os.path.exists(output_file) == 0:
    print(f'Processing data for ESRI world cover...')
    iteration_start = time.time()
    # Resample and reproject
    gdal.Warp(output_file,
              esri_file,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=GDT_Int16,
              workingType=GDT_Byte,
              xRes=10,
              yRes=-10,
              srcNodata=255,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Process height raster
output_file = os.path.join(intermediate_folder, 'height_10m_3338.tif')
if os.path.exists(output_file) == 0:
    print(f'Processing data for canopy height...')
    iteration_start = time.time()
    # Resample and reproject
    gdal.Warp(output_file,
              height_file,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=GDT_Int16,
              workingType=GDT_Byte,
              xRes=10,
              yRes=-10,
              srcNodata=255,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Process alkaline raster
output_file = os.path.join(intermediate_folder, 'alkaline_10m_3338.tif')
if os.path.exists(output_file) == 0:
    print(f'Processing data for alkaline...')
    iteration_start = time.time()
    # Resample and reproject
    gdal.Warp(output_file,
              alkaline_file,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=GDT_Int16,
              workingType=GDT_Byte,
              xRes=10,
              yRes=-10,
              srcNodata=255,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Process correction raster
output_file = os.path.join(intermediate_folder, 'correction_10m_3338.tif')
if os.path.exists(output_file) == 0:
    print(f'Processing data for correction...')
    iteration_start = time.time()
    # Resample and reproject
    gdal.Warp(output_file,
              correction_file,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=GDT_Int16,
              workingType=GDT_Byte,
              xRes=10,
              yRes=-10,
              srcNodata=255,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Create list of all intermediate datasets
intermediate_files = glob.glob(f'{intermediate_folder}' + '/*.tif')

# Update mask for output raster
for file in intermediate_files:
    # Define output file
    file_name = os.path.split(file)[1]
    output_file = os.path.join(output_folder, file_name)
    if os.path.exists(output_file) == 0:
        print(f'Updating mask for {file_name}...')
        iteration_start = time.time()
        input_raster = rasterio.open(file)
        input_profile = input_raster.profile.copy()
        area_raster = rasterio.open(area_file)
        with rasterio.open(output_file, 'w', **input_profile, BIGTIFF='YES') as dst:
            # Find number of raster blocks
            window_list = []
            for block_index, window in area_raster.block_windows(1):
                window_list.append(window)
            # Iterate processing through raster blocks
            count = 1
            progress = 0
            for block_index, window in area_raster.block_windows(1):
                area_block = area_raster.read(window=window,
                                              masked=False)
                raster_block = input_raster.read(window=window,
                                                 masked=False)
                # Set no data values in input raster to 0
                raster_block = np.where(raster_block == nodata, 0, raster_block)
                # Set no data values from area raster to no data
                raster_block = np.where(area_block != 1, nodata, raster_block)
                # Write results
                dst.write(raster_block,
                          window=window)
                # Report progress
                count, progress = raster_block_progress(10, len(window_list), count, progress)
        end_timing(iteration_start)
