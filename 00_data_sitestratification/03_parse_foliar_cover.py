# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Parse foliar cover to types
# Author: Timm Nawrocki
# Last Updated: 2025-04-08
# Usage: Execute in Python 3.9+.
# Description: "Parse foliar cover to types" implements a programmatic key to create discrete types.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
import numpy as np
import rasterio
from akutils import *

# Set no data
nodata = -32768

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/AKVEG_EVT_YukonFlats/Data')
foliar_folder = os.path.join(project_folder, 'Data_Input/foliar_cover')
derived_folder = os.path.join(project_folder, 'Data_Input/foliar_derived')
ancillary_folder = os.path.join(project_folder, 'Data_Input/ancillary_data')
output_folder = os.path.join(project_folder, 'Data_Input/stratification/intermediate')

# Define input files
area_input = os.path.join(project_folder, 'Data_Input/YukonFlats_MapDomain_10m_3338.tif')
alnus_input = os.path.join(foliar_folder, 'alnus_10m_3338.tif')
betshr_input = os.path.join(foliar_folder, 'betshr_10m_3338.tif')
bettre_input = os.path.join(foliar_folder, 'bettre_10m_3338.tif')
brotre_input = os.path.join(foliar_folder, 'brotre_10m_3338.tif')
dryas_input = os.path.join(foliar_folder, 'dryas_10m_3338.tif')
dsalix_input = os.path.join(foliar_folder, 'dsalix_10m_3338.tif')
empnig_input = os.path.join(foliar_folder, 'empnig_10m_3338.tif')
erivag_input = os.path.join(foliar_folder, 'erivag_10m_3338.tif')
forb_input = os.path.join(foliar_folder, 'forb_10m_3338.tif')
gramin_input = os.path.join(foliar_folder, 'gramin_10m_3338.tif')
lichen_input = os.path.join(foliar_folder, 'lichen_10m_3338.tif')
mwcalama_input = os.path.join(foliar_folder, 'mwcalama_10m_3338.tif')
ndsalix_input = os.path.join(foliar_folder, 'ndsalix_10m_3338.tif')
nerishr_input = os.path.join(foliar_folder, 'nerishr_10m_3338.tif')
picgla_input = os.path.join(foliar_folder, 'picgla_10m_3338.tif')
picmar_input = os.path.join(foliar_folder, 'picmar_10m_3338.tif')
poptre_input = os.path.join(foliar_folder, 'poptre_10m_3338.tif')
populbt_input = os.path.join(foliar_folder, 'populbt_10m_3338.tif')
rhoshr_input = os.path.join(foliar_folder, 'rhoshr_10m_3338.tif')
sphagn_input = os.path.join(foliar_folder, 'sphagn_10m_3338.tif')
vaculi_input = os.path.join(foliar_folder, 'vaculi_10m_3338.tif')
vacvit_input = os.path.join(foliar_folder, 'vacvit_10m_3338.tif')
wetsed_input = os.path.join(foliar_folder, 'wetsed_10m_3338.tif')

picratio_input = os.path.join(derived_folder, 'picea_ratio_10m_3338.tif')
picsum_input = os.path.join(derived_folder, 'picea_sum_10m_3338.tif')
decratio_input = os.path.join(derived_folder, 'deciduous_ratio_10m_3338.tif')
ndshrub_input = os.path.join(derived_folder, 'alder_birch_willow_10m_3338.tif')
eridwarf_input = os.path.join(derived_folder, 'ericaceous_dwarf_10m_3338.tif')
wetland_input = os.path.join(derived_folder, 'wetland_indicator_10m_3338.tif')
picwet_input = os.path.join(derived_folder, 'picmar_wet_indicator_10m_3338.tif')
herbac_input = os.path.join(derived_folder, 'herbaceous_10m_3338.tif')

height_input = os.path.join(project_folder, 'Data_Input/canopy_height/height_10m_3338.tif')

esa_input = os.path.join(ancillary_folder, 'esacover_10m_3338.tif')
esri_input = os.path.join(ancillary_folder, 'esricover_10m_3338.tif')
fire_input = os.path.join(ancillary_folder, 'fireyear_10m_3338.tif')
flood_input = os.path.join(ancillary_folder, 'floodplain_10m_3338.tif')
alkaline_input = os.path.join(ancillary_folder, 'alkaline_10m_3338.tif')
correction_input = os.path.join(ancillary_folder, 'correction_10m_3338.tif')

# Define output file
parsed_output = os.path.join(output_folder, 'AKVEG_Parsed_10m_3338.tif')

# Prepare input rasters
area_raster = rasterio.open(area_input)
alnus_raster = rasterio.open(alnus_input)
betshr_raster = rasterio.open(betshr_input)
bettre_raster = rasterio.open(bettre_input)
brotre_raster = rasterio.open(brotre_input)
dryas_raster = rasterio.open(dryas_input)
dsalix_raster = rasterio.open(dsalix_input)
empnig_raster = rasterio.open(empnig_input)
erivag_raster = rasterio.open(erivag_input)
forb_raster = rasterio.open(forb_input)
gramin_raster = rasterio.open(gramin_input)
lichen_raster = rasterio.open(lichen_input)
mwcalama_raster = rasterio.open(mwcalama_input)
ndsalix_raster = rasterio.open(ndsalix_input)
nerishr_raster = rasterio.open(nerishr_input)
picgla_raster = rasterio.open(picgla_input)
picmar_raster = rasterio.open(picmar_input)
poptre_raster = rasterio.open(poptre_input)
populbt_raster = rasterio.open(populbt_input)
rhoshr_raster = rasterio.open(rhoshr_input)
sphagn_raster = rasterio.open(sphagn_input)
vaculi_raster = rasterio.open(vaculi_input)
vacvit_raster = rasterio.open(vacvit_input)
wetsed_raster = rasterio.open(wetsed_input)

picratio_raster = rasterio.open(picratio_input)
picsum_raster = rasterio.open(picsum_input)
decratio_raster = rasterio.open(decratio_input)
ndshrub_raster = rasterio.open(ndshrub_input)
eridwarf_raster = rasterio.open(eridwarf_input)
wetland_raster = rasterio.open(wetland_input)
picwet_raster = rasterio.open(picwet_input)
herbac_raster = rasterio.open(herbac_input)

height_raster = rasterio.open(height_input)

esa_raster = rasterio.open(esa_input)
esri_raster = rasterio.open(esri_input)
fire_raster = rasterio.open(fire_input)
flood_raster = rasterio.open(flood_input)
alkaline_raster = rasterio.open(alkaline_input)
correction_raster = rasterio.open(correction_input)

# Parse foliar cover
print(f'Parsing foliar cover to types...')
iteration_start = time.time()
input_profile = picgla_raster.profile.copy()
with rasterio.open(parsed_output, 'w', **input_profile, BIGTIFF='YES') as dst:
    # Find number of raster blocks
    window_list = []
    for block_index, window in area_raster.block_windows(1):
        window_list.append(window)
    # Iterate processing through raster blocks
    count = 1
    progress = 0
    for block_index, window in area_raster.block_windows(1):
        #### LOAD BLOCKS
        area_block = area_raster.read(window=window, masked=False)
        alnus_block = alnus_raster.read(window=window, masked=False)
        betshr_block = betshr_raster.read(window=window, masked=False)
        bettre_block = bettre_raster.read(window=window, masked=False)
        brotre_block = brotre_raster.read(window=window, masked=False)
        dryas_block = dryas_raster.read(window=window, masked=False)
        dsalix_block = dsalix_raster.read(window=window, masked=False)
        empnig_block = empnig_raster.read(window=window, masked=False)
        erivag_block = erivag_raster.read(window=window, masked=False)
        forb_block = forb_raster.read(window=window, masked=False)
        gramin_block = gramin_raster.read(window=window, masked=False)
        lichen_block = lichen_raster.read(window=window, masked=False)
        mwcalama_block = mwcalama_raster.read(window=window, masked=False)
        ndsalix_block = ndsalix_raster.read(window=window, masked=False)
        nerishr_block = nerishr_raster.read(window=window, masked=False)
        picgla_block = picgla_raster.read(window=window, masked=False)
        picmar_block = picmar_raster.read(window=window, masked=False)
        poptre_block = poptre_raster.read(window=window, masked=False)
        populbt_block = populbt_raster.read(window=window, masked=False)
        sphagn_block = sphagn_raster.read(window=window, masked=False)
        vaculi_block = vaculi_raster.read(window=window, masked=False)
        wetsed_block = wetsed_raster.read(window=window, masked=False)

        picratio_block = picratio_raster.read(window=window, masked=False)
        picsum_block = picsum_raster.read(window=window, masked=False)
        decratio_block = decratio_raster.read(window=window, masked=False)
        ndshrub_block = ndshrub_raster.read(window=window, masked=False)
        eridwarf_block = eridwarf_raster.read(window=window, masked=False)
        wetland_block = wetland_raster.read(window=window, masked=False)
        picwet_block = picwet_raster.read(window=window, masked=False)
        herbac_block = herbac_raster.read(window=window, masked=False)

        height_block = height_raster.read(window=window, masked=False)

        esa_block = esa_raster.read(window=window, masked=False)
        esri_block = esri_raster.read(window=window, masked=False)
        fire_block = fire_raster.read(window=window, masked=False)
        flood_block = flood_raster.read(window=window, masked=False)
        alkaline_block = alkaline_raster.read(window=window, masked=False)
        correction_block = correction_raster.read(window=window, masked=False)

        #### BEGIN PROGRAMMATIC KEY

        # Set base value
        out_block = np.where(area_block == 1, 0, nodata)

        #### 0. GROWTH HABIT SPLITS

        # 0.1 coniferous trees
        out_block = np.where((picsum_block >= 10)
                             & (decratio_block < 40),
                             1, out_block)
        out_block = np.where((out_block == 0) & (picsum_block >= 5) & (decratio_block < 40)
                             & ((esa_block == 10) | (height_block > 3)),
                             1, out_block)
        # 0.1 apply correction
        out_block = np.where((out_block == 1)
                             & ((height_block <= 2) | (esa_block != 10))
                             & ((fire_block >= 1975) & (fire_block < 2000) & (correction_block == 1))
                             & (picwet_block < 20),
                             0, out_block)
        # 0.2 deciduous trees
        out_block = np.where((out_block == 0) & (brotre_block >= 12) & (decratio_block >= 60)
                             & (brotre_block >= (ndshrub_block * 0.5))
                             & (((fire_block < 1975) & (height_block >= 2))
                                | (fire_block >= 1975)
                                | (brotre_block >= 25)),
                             2, out_block)
        # 0.3 mixed coniferous - deciduous trees
        out_block = np.where((out_block == 0) & (brotre_block >= 10) & (picsum_block >= 10)
                             & ((decratio_block >= 40) & (decratio_block < 60))
                             & ((height_block >= 2) | ((brotre_block + picsum_block) >= 40)),
                             3, out_block)
        # 0.4 shrub mesic
        out_block = np.where((out_block == 0)
                             & ((ndshrub_block + eridwarf_block + vaculi_block
                                + dryas_block + dsalix_block ) >= 15)
                             & (wetland_block < 8),
                             4, out_block)
        # 0.5 shrub wet
        out_block = np.where((out_block == 0)
                             & ((ndshrub_block + eridwarf_block + vaculi_block
                                 + dryas_block + dsalix_block) >= 15)
                             & (wetland_block >= 8),
                             5, out_block)
        # 0.6 herbaceous mesic
        out_block = np.where((out_block == 0)
                             & ((herbac_block + mwcalama_block) >= 15)
                             & (wetland_block < 8) & (brotre_block < 5),
                             6, out_block)
        # 0.7 herbaceous wet
        out_block = np.where((out_block == 0)
                             & ((herbac_block + mwcalama_block) >= 15)
                             & (wetland_block >= 8) & (brotre_block < 5),
                             7, out_block)

        #### 1. SPRUCE FOREST & WOODLAND

        # 1.10 spruce-lichen woodland
        out_block = np.where((out_block == 1) & (lichen_block >= 15) & (ndshrub_block <= 10)
                             & ((picsum_block + brotre_block) < 20),
                             10, out_block)
        # 1.11 white spruce woodland
        out_block = np.where((out_block == 1) & (picratio_block >= 60)
                             & ((picsum_block + brotre_block) < 20),
                             11, out_block)
        # 1.12 white spruce forest
        out_block = np.where((out_block == 1) & (picratio_block >= 60)
                             & ((picsum_block + brotre_block) >= 20),
                             12, out_block)
        # 1.13 black spruce woodland
        out_block = np.where((out_block == 1) & (picratio_block < 40)
                             & ((picsum_block + brotre_block) < 20),
                             13, out_block)
        # 1.14 black spruce forest
        out_block = np.where((out_block == 1) & (picratio_block < 40)
                             & ((picsum_block + brotre_block) >= 20),
                             14, out_block)
        # 1.15 mixed spruce woodland
        out_block = np.where((out_block == 1) & (picratio_block >= 40) & (picratio_block < 60)
                             & ((picsum_block + brotre_block) < 20),
                             15, out_block)
        # 1.16 mixed spruce forest
        out_block = np.where((out_block == 1) & (picratio_block >= 40) & (picratio_block < 60)
                             & ((picsum_block + brotre_block) >= 20),
                             16, out_block)
        # 1.17 black spruce-tussock woodland
        out_block = np.where(((out_block == 13) | (out_block == 14)
                              | (out_block == 15) | (out_block == 16))
                             & (erivag_block >= 20),
                             17, out_block)
        out_block = np.where(((out_block == 13) | (out_block == 14)
                              | (out_block == 15) | (out_block == 16))
                             & (erivag_block >= 15) & (ndshrub_block < 35),
                             17, out_block)
        # 1.18 black spruce peatland
        out_block = np.where(((out_block == 13) | (out_block == 14)
                              | (out_block == 15) | (out_block == 16))
                             & (picwet_block >= 8) & (ndsalix_block < 30),
                             18, out_block)

        #### 2. DECIDUOUS FOREST

        # 2.20 poplar forest
        out_block = np.where((out_block == 2)
                             & ((populbt_block + 0.1) > poptre_block)
                             & ((populbt_block + 0.1) > bettre_block),
                             20, out_block)
        # 2.21 aspen forest
        out_block = np.where((out_block == 2)
                             & ((poptre_block + 0.1) > populbt_block)
                             & ((poptre_block + 0.1) > bettre_block),
                             21, out_block)
        # 2.22 birch forest
        out_block = np.where((out_block == 2)
                             & ((bettre_block + 0.1) > populbt_block)
                             & ((bettre_block + 0.1) > poptre_block),
                             22, out_block)

        #### 3. SPRUCE - HARDWOOD FOREST & WOODLAND

        # 3.30 white spruce-poplar forest & woodland
        out_block = np.where((out_block == 3) & (picratio_block >= 60)
                             & ((populbt_block + 0.1) > poptre_block)
                             & ((populbt_block + 0.1) > bettre_block),
                             30, out_block)
        out_block = np.where((out_block == 3) & (picratio_block >= 40) & (picratio_block < 60)
                             & ((populbt_block + 0.1) > poptre_block)
                             & ((populbt_block + 0.1) > bettre_block),
                             30, out_block)
        # 3.31 white spruce-aspen forest & woodland
        out_block = np.where((out_block == 3) & (picratio_block >= 60)
                             & ((poptre_block + 0.1) > populbt_block)
                             & ((poptre_block + 0.1) > bettre_block),
                             31, out_block)
        out_block = np.where((out_block == 3) & (picratio_block >= 40) & (picratio_block < 60)
                             & ((poptre_block + 0.1) > populbt_block)
                             & ((poptre_block + 0.1) > bettre_block),
                             31, out_block)
        # 3.32 white spruce-birch forest & woodland
        out_block = np.where((out_block == 3) & (picratio_block >= 60)
                             & ((bettre_block + 0.1) > populbt_block)
                             & ((bettre_block + 0.1) > poptre_block),
                             32, out_block)
        # 3.33 black spruce-deciduous forest & woodland
        out_block = np.where((out_block == 3) & (picratio_block < 40)
                             & ((populbt_block + 0.1) > poptre_block)
                             & ((populbt_block + 0.1) > bettre_block),
                             33, out_block)
        out_block = np.where((out_block == 3) & (picratio_block < 40)
                             & ((poptre_block + 0.1) > populbt_block)
                             & ((poptre_block + 0.1) > bettre_block),
                             33, out_block)
        out_block = np.where((out_block == 3) & (picratio_block < 40)
                             & ((bettre_block + 0.1) > populbt_block)
                             & ((bettre_block + 0.1) > poptre_block),
                             33, out_block)
        # 3.34 mixed spruce-birch forest & woodland
        out_block = np.where((out_block == 3) & (picratio_block >= 40) & (picratio_block < 60)
                             & ((bettre_block + 0.1) > populbt_block)
                             & ((bettre_block + 0.1) > poptre_block),
                             34, out_block)

        #### 8. TUSSOCK TUNDRA TYPES

        # 8.40 tussock tundra low shrub
        out_block = np.where(((out_block == 0) | (out_block == 4) | (out_block == 5)
                              | (out_block == 6) | (out_block == 7))
                             & (erivag_block >= 20),
                             40, out_block)
        out_block = np.where(((out_block == 0) | (out_block == 4) | (out_block == 5)
                              | (out_block == 6) | (out_block == 7))
                             & (erivag_block >= 15) & (ndshrub_block < 35),
                             40, out_block)
        # 8.41 tussock tundra dwarf shrub
        out_block = np.where((out_block == 26) & (ndshrub_block < 8),
                             41, out_block)

        #### 4. SHRUB MESIC

        # 4.50 alder mesic
        out_block = np.where((out_block == 4)
                             & (alnus_block >= 12)
                             & ((alnus_block / (alnus_block + ndsalix_block  + 0.1)) >= 0.3),
                             50, out_block)
        # 4.51 alder-willow mesic
        out_block = np.where(((out_block == 4) | (out_block == 50))
                             & ((alnus_block + ndsalix_block) >= 12)
                             & (((alnus_block / (alnus_block + ndsalix_block  + 0.1)) >= 0.3)
                                & ((alnus_block / (alnus_block + ndsalix_block  + 0.1)) < 0.7)),
                             51, out_block)
        # 4.52 willow mesic
        out_block = np.where((out_block == 4)
                             & (ndsalix_block >= 10)
                             & ((ndsalix_block / (betshr_block + ndsalix_block  + 0.1)) >= 0.3),
                             52, out_block)
        # 4.53 birch-willow mesic
        out_block = np.where(((out_block == 4) | (out_block == 52))
                             & ((betshr_block + ndsalix_block) >= 12)
                             & (((ndsalix_block / (betshr_block + ndsalix_block  + 0.1)) >= 0.3)
                                & ((ndsalix_block / (betshr_block + ndsalix_block  + 0.1)) < 0.7)),
                             53, out_block)
        # 4.54 birch shrub / birch-ericaceous mesic
        out_block = np.where((out_block == 4)
                             & ((betshr_block + eridwarf_block + vaculi_block) >= 15)
                             & (betshr_block >= 5),
                             54, out_block)
        # 4.55 dwarf shrub-lichen
        out_block = np.where((out_block == 4)
                             & ((dsalix_block + dryas_block + eridwarf_block) >= 15)
                             & (lichen_block >= 20)
                             & (height_block < 1)
                             & (brotre_block < 5),
                             55, out_block)
        # 4.56 ericaceous dwarf shrub
        out_block = np.where((out_block == 4)
                             & ((dsalix_block + dryas_block + eridwarf_block) >= 15)
                             & (eridwarf_block >= 10)
                             & ((eridwarf_block / (eridwarf_block + dryas_block  + 0.1)) >= 0.3)
                             & (height_block < 1)
                             & (brotre_block < 5),
                             56, out_block)
        # 4.57 dryas-ericaceous dwarf shrub
        out_block = np.where(((out_block == 4) | (out_block == 56))
                             & ((dsalix_block + dryas_block + eridwarf_block) >= 15)
                             & (dryas_block >= 10)
                             & (((eridwarf_block / (eridwarf_block + dryas_block  + 0.1)) >= 0.3)
                                & ((eridwarf_block / (eridwarf_block + dryas_block  + 0.1)) < 0.7))
                             & (height_block < 1)
                             & (brotre_block < 5),
                             57, out_block)
        # 4.58 dryas-dwarf willow
        out_block = np.where(((out_block == 4))
                             & ((dsalix_block + dryas_block + eridwarf_block) >= 15)
                             & (dryas_block >= 10)
                             & (height_block < 1)
                             & (brotre_block < 5),
                             58, out_block)

        #### 5. SHRUB WET

        # 5.60 shrub-sphagnum wet
        out_block = np.where((out_block == 5)
                             & (sphagn_block >= 12),
                             60, out_block)
        # 5.61 dwarf shrub-sphagnum wet
        out_block = np.where((out_block == 60)
                             & (ndshrub_block < 15),
                             61, out_block)
        # 5.62 alder-willow wet
        out_block = np.where((out_block == 5)
                             & (alnus_block >= 10),
                             62, out_block)
        # 5.63 willow wet
        out_block = np.where((out_block == 5) & (ndsalix_block >= 10),
                             63, out_block)
        # 5.64 birch-willow wet
        out_block = np.where(((out_block == 5) | (out_block == 63))
                             & (betshr_block >= 10)
                             & (ndsalix_block < (betshr_block * 1.5)),
                             64, out_block)

        #### 6. HERBACEOUS MESIC

        # 6.70 Calamagrostis meadow mesic
        out_block = np.where((out_block == 6) & (mwcalama_block >= 8),
                             70, out_block)

        # 6.71 forb-graminoid meadow mesic alkaline
        out_block = np.where((out_block == 6) & (alkaline_block == 1),
                             71, out_block)

        # 6.72 forb-graminoid meadow mesic acidic
        out_block = np.where((out_block == 6) & (alkaline_block == 0),
                             72, out_block)

        #### 7. HERBACEOUS WET

        # 7.80 sedge meadow wet
        out_block = np.where((out_block == 7) & (wetsed_block >= 8),
                             80, out_block)

        # 7.81 sedge-Calamagrostis meadow wet
        out_block = np.where(((out_block == 80) |
                              ((out_block == 7) & ((wetland_block + mwcalama_block) >= 12)))
                             & ((mwcalama_block / (mwcalama_block + wetsed_block + 0.1)) >= 0.3),
                             81, out_block)

        # 7.82 forb-graminoid meadow wet
        out_block = np.where(out_block == 7,
                             82, out_block)

        #### CORRECTIONS

        # Apply corrections to willow wet
        out_block = np.where(((out_block == 0) | (out_block == 4) | (out_block == 5))
                             & ((brotre_block >= 3) | (poptre_block >= 3) | (ndsalix_block >= 3))
                             & (wetland_block >= 5),
                             63, out_block)
        # Apply corrections to birch-willow wet
        out_block = np.where((out_block == 5)
                             & (betshr_block >= 3),
                             64, out_block)
        # Apply corrections to aspen forest
        out_block = np.where(((out_block == 0) | (out_block == 4))
                             & ((brotre_block >= 3) | (poptre_block >= 3) | (ndsalix_block >= 3))
                             & (wetland_block < 5)
                             & (poptre_block > (ndsalix_block + 0.1)),
                             21, out_block)
        # Apply corrections to willow mesic
        out_block = np.where(((out_block == 0) | (out_block == 4))
                             & ((brotre_block >= 3) | (poptre_block >= 3) | (ndsalix_block >= 3))
                             & (wetland_block < 5),
                             52, out_block)
        # Apply corrections to birch-ericaceous mesic
        out_block = np.where((out_block == 4)
                             & (betshr_block >= 3),
                             54, out_block)

        #### 9. FIRE TYPES

        # 9.90 burned
        out_block = np.where(fire_block >= 2019,
                             90, out_block)

        # 9.91 recent burn recovering birch-willow mesic
        out_block = np.where((fire_block >= 2000) & (fire_block < 2019)
                             & ((out_block == 52) | (out_block == 53)),
                             91, out_block)
        out_block = np.where((fire_block >= 2000) & (fire_block < 2019)
                             & (out_block == 0)
                             & ((esa_block == 20) | (esa_block == 30))
                             & (wetland_block < 5),
                             91, out_block)

        # 9.92 recent burn recovering birch-willow wet
        out_block = np.where((fire_block >= 2000) & (fire_block < 2019)
                             & ((out_block == 62) | (out_block == 63) | (out_block == 64)),
                             92, out_block)
        out_block = np.where((fire_block >= 2000) & (fire_block < 2019)
                             & (out_block == 0)
                             & ((esa_block == 20) | (esa_block == 30))
                             & (wetland_block >= 5),
                             92, out_block)

        #### 10. FLOODPLAIN TYPES

        # 10.100 white spruce active floodplain
        out_block = np.where((flood_block == 1)
                             & ((out_block == 11) | (out_block == 12)
                                | (out_block == 15) | (out_block == 16)),
                             100, out_block)

        # 10.101 poplar (white spruce) active floodplain
        out_block = np.where((flood_block == 1) &
                             ((out_block == 20) | (out_block == 30)),
                             101, out_block)
        out_block = np.where((flood_block == 1) & (out_block == 21)
                             & (populbt_block >= (poptre_block * 0.75)),
                             101, out_block)

        # 10.102 birch (white spruce) active floodplain
        out_block = np.where((flood_block == 1) &
                             ((out_block == 22) | (out_block == 32) | (out_block == 34)),
                             102, out_block)

        # 10.103 alder-willow active floodplain
        out_block = np.where((flood_block == 1)
                             & ((out_block == 50) | (out_block == 51) | (out_block == 62)),
                             103, out_block)

        # 10.104 willow active floodplain
        out_block = np.where((flood_block == 1)
                             & (out_block == 52),
                             104, out_block)

        #### 12. SPARSE OR BARREN

        # 12.95 Developed
        out_block = np.where(esa_block == 50,
                             95, out_block)

        # 12.96 Barren / sparse
        out_block = np.where(esa_block == 60,
                             96, out_block)

        # 12.97 Snow / ice
        out_block = np.where((out_block == 0) & (esa_block == 70),
                             97, out_block)

        # 12.98 Water
        out_block = np.where((esa_block == 80) | (esri_block == 1),
                             98, out_block)

        # Set no data values from area raster to no data
        out_block = np.where(area_block != 1, nodata, out_block)
        # Write results
        dst.write(out_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)
