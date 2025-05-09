// https://gee-community-catalog.org/projects/esrilc2020/

var esri_lulc10 = ee.ImageCollection("projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m");

// Define a dictionary which will be used to make legend and visualize image on map
var dict = {
  "names": [
    "Water",
    "Trees",
    "Grass",
    "Flooded Vegetation",
    "Crops",
    "Scrub/Shrub",
    "Built Area",
    "Bare Ground",
    "Snow/Ice",
    "Clouds"
  ],
  "colors": [
    "#1A5BAB",
    "#358221",
    "#A7D282",
    "#87D19E",
    "#FFDB5C",
    "#EECFA8",
    "#ED022A",
    "#EDE9E4",
    "#F2FAFF",
    "#C8C8C8"
  ]};

// Create a panel to hold the legend widget
var legend = ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '8px 15px'
  }
});

// Function to generate the legend
function addCategoricalLegend(panel, dict, title) {
  
  // Create and add the legend title.
  var legendTitle = ui.Label({
    value: title,
    style: {
      fontWeight: 'bold',
      fontSize: '18px',
      margin: '0 0 4px 0',
      padding: '0'
    }
  });
  panel.add(legendTitle);
  
  var loading = ui.Label('Loading legend...', {margin: '2px 0 4px 0'});
  panel.add(loading);
  
  // Creates and styles 1 row of the legend.
  var makeRow = function(color, name) {
    // Create the label that is actually the colored box.
    var colorBox = ui.Label({
      style: {
        backgroundColor: color,
        // Use padding to give the box height and width.
        padding: '8px',
        margin: '0 0 4px 0'
      }
    });
  
    // Create the label filled with the description text.
    var description = ui.Label({
      value: name,
      style: {margin: '0 0 4px 6px'}
    });
  
    return ui.Panel({
      widgets: [colorBox, description],
      layout: ui.Panel.Layout.Flow('horizontal')
    });
  };
  
  // Get the list of palette colors and class names from the image.
  var palette = dict['colors'];
  var names = dict['names'];
  loading.style().set('shown', false);
  
  for (var i = 0; i < names.length; i++) {
    panel.add(makeRow(palette[i], names[i]));
  }
  
  Map.add(panel);
  
}


/*
  // Display map and legend ///////////////////////////////////////////////////////////////////////////////
*/

// Add the legend to the map
addCategoricalLegend(legend, dict, 'ESRI 2020 Land Cover');

// Add image to the map
Map.addLayer(esri_lulc10.mosaic(), {min:1, max:10, palette:dict['colors']}, 'ESRI LULC 10m')

// TIMM ADDED

var esri_image = esri_lulc10.mosaic();
print(esri_image)

// Load covariates
var area_feature = ee.FeatureCollection('projects/akveg-map/assets/study_areas/YukonFlats_StudyArea');
var elevation_image = ee.Image('projects/akveg-map/assets/covariates_v20240711/Elevation_10m_3338').rename(['elevation']);

// Define projection
var projection = elevation_image.select('elevation').projection().getInfo();
print(projection)

// Export geotiff to storage
Export.image.toCloudStorage({
  image: esri_image,
  description: 'esri_lulc10',
  bucket: 'akveg-data',
  fileNamePrefix: 'yukon_flats/esrilc_10m_3338.tif',
  crs: projection.crs,
  crsTransform: projection.transform,
  region: area_feature,
  fileFormat: 'GeoTIFF',
  formatOptions: {
    cloudOptimized: true
  },
  maxPixels: 1e13
});