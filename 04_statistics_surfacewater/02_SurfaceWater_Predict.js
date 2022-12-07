/* -*- coding: utf-8 -*-
---------------------------------------------------------------------------
Seasonal Surface Water Sentinel-1 SAR for 2018-2021
Author: Timm Nawrocki, Alaska Center for Conservation Science
Last Updated: 2022-11-24
Usage: Must be executed from the Google Earth Engine code editor.
Description: This script produces median composites using ascending orbitals for the VV and VH polarizations from Sentinel-1.
---------------------------------------------------------------------------*/

// Create function for surface water threshold
var surface_water = function(image) {
  var thres = image.select('VV').lte(-15.178513401724654).rename('thres')
  return image.addBands(thres);
}

// Define an area of interest geometry.
var area_feature = ee.FeatureCollection('projects/accs-geospatial-processing/assets/gmt2_studyarea');

// Import the Sentinel-1 Image Collection VV and VH polarizations within study area and date range
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(area_feature)
  .filter(ee.Filter.calendarRange(2017, 2021, 'year'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
  .sort('system:time_start');
print('Sentinel 1:', s1);

// Create date array
var date_array = [['2017-05-02', '2018-06-30'],
  ['2017-06-15', '2017-07-25'],
  ['2017-07-10', '2017-08-20'],
  ['2017-08-05', '2017-09-15'],
  ['2017-09-01', '2017-10-10'],
  ['2018-05-02', '2018-06-30'],
  ['2018-06-15', '2018-07-25'],
  ['2018-07-10', '2018-08-20'],
  ['2018-08-05', '2018-09-15'],
  ['2018-09-01', '2018-10-10'],
  ['2020-05-02', '2020-06-30'],
  ['2020-06-15', '2020-07-25'],
  ['2020-07-10', '2020-08-20'],
  ['2020-08-05', '2020-09-15'],
  ['2020-09-01', '2020-10-10'],
  ['2021-05-02', '2021-06-30'],
  ['2021-06-15', '2021-07-25'],
  ['2021-07-10', '2021-08-20'],
  ['2021-08-05', '2021-09-15'],
  ['2021-09-01', '2021-10-10']];

// Create images
var image_array = [];
for (var i in date_array) {
  // Create date filter
  var filter_date = ee.Filter.or(
    ee.Filter.date(date_array[i][0], date_array[i][1]));
  
  // Filter image collection to dates
  var s1_subset = s1.filter(filter_date);
  
  // Create mean vv composite
  var vv_mean = s1_subset.select('VV').mean()
  
  // Append image to list
  image_array.push(vv_mean)
}

// Create image collection of mean composites
var vv_collection = ee.ImageCollection.fromImages(image_array);

// Apply the threshold function to all images
var vv_thres = vv_collection.map(surface_water)
print('VV Thresholded:', vv_thres)

// Calculate the seasonal water percentage
var water_percentage = vv_thres.select('thres').mean().multiply(100)
print('Water Percentage:', water_percentage)

// Identify test image
var test_image = ee.Image(vv_thres.select('thres').toBands().select(0));

// Add image to the map.
Map.centerObject(area_feature);
Map.addLayer(test_image, {min: 0, max: 1}, 'Test Threshold');
Map.addLayer(water_percentage, {min: 0, max: 100}, 'Water');

// Add study area to map
var empty = ee.Image().byte();
var outlines = empty.paint({
  featureCollection: area_feature,
  color: 'red',
  width: 2
});
Map.addLayer(outlines, {palette: 'FFFF00'}, 'Study Area');

// Export images to Google Drive.
Export.image.toDrive({
  image: water_percentage,
  description: 'GMT2_SeasonalWater_Percentage',
  folder: 'gmt2_surface_water',
  scale: 10,
	crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});