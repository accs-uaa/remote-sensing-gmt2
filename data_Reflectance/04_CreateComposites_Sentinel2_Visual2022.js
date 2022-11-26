/* -*- coding: utf-8 -*-
---------------------------------------------------------------------------
Cloud-reduced Seasonal Median Composite of Midsummer 2022 Sentinel 2 Imagery
Author: Timm Nawrocki, Alaska Center for Conservation Science
Last Updated: 2022-11-21
Usage: Must be executed from the Google Earth Engine code editor.
Description: This script produces a set of cloud-reduced median composite for bands 1-12 plus Enhanced Vegetation Index-2 (EVI2), Normalized Burn Ratio (NBR), Normalized Difference Moisture Index (NDMI), Normalized Difference Snow Index (NDSI), Normalized Difference Vegetation Index (NDVI), Normalized Difference Water Index (NDWI) using the Sentinel-2 Surface Reflectance collection. The composite is centered around June 20 - August 20 of 2022 to enable visual interpretation of features.
---------------------------------------------------------------------------*/

// 1. DEFINE PROPERTIES

// Define an area of interest geometry.
var area_feature = ee.FeatureCollection('projects/accs-geospatial-processing/assets/gmt2_studyarea');

// Define properties
var start_year = 2022
var end_year = 2022
var start_month = 5
var end_month = 10
var cloud_threshold = 40

// 2. DEFINE FUNCTIONS

// Define a function to mask image edges
function mask_edges(image) {
  var mask = image.select('B8A').mask().updateMask(image.select('B9').mask());
  return image.updateMask(mask);
}

// Define a function to mask clouds using cloud probability
function mask_cloud_probability(image) {
  var clouds = ee.Image(image.get('cloud_mask')).select('probability');
  var mask = clouds.lt(cloud_threshold);
  return image.updateMask(mask);
}

// Define a function to mask clouds and cirrus using QA band
function mask_cloud_cirrus(image) {
	var qa = image.select('QA60');
	// Bits 10 and 11 are clouds and cirrus, respectively.
	var cloud_bit_mask = 1 << 10;
	var cirrus_bit_mask = 1 << 11;
	//Both flags should be set to zero, indicating clear conditions.
	var mask = qa.bitwiseAnd(cloud_bit_mask).eq(0)
		.and(qa.bitwiseAnd(cirrus_bit_mask).eq(0));
	return image.updateMask(mask);
}

// Define a function for EVI-2 calculation.
function add_EVI2(image) {
  // Assign variables to the red and green Sentinel-2 bands.
  var red = image.select('B4');
  var green = image.select('B3');
  //Compute the Enhanced Vegetation Index-2 (EVI2).
  var evi2_calc = red.subtract(green)
    .divide(red.add(green.multiply(2.4)).add(1))
    .rename('EVI2');
  // Return the masked image with an EVI-2 band.
  return image.addBands(evi2_calc);
}

// Define a function for NBR calculation.
function add_NBR(image) {
  //Compute the Normalized Burn Ratio (NBR).
  var nbr_calc = image.normalizedDifference(['B8', 'B12'])
    .rename('NBR');
  // Return the masked image with an NBR band.
  return image.addBands(nbr_calc);
}

// Define a function for NDMI calculation.
function add_NDMI(image) {
  //Compute the Normalized Difference Moisture Index (NDMI).
  var ndmi_calc = image.normalizedDifference(['B8', 'B11'])
    .rename('NDMI');
  // Return the masked image with an NDMI band.
  return image.addBands(ndmi_calc);
}

// Define a function for NDSI calculation.
function add_NDSI(image) {
  //Compute the Normalized Difference Snow Index (NDSI).
  var ndsi_calc = image.normalizedDifference(['B3', 'B11'])
    .rename('NDSI');
  // Return the masked image with an NDSI band.
  return image.addBands(ndsi_calc);
}

// Define a function for NDVI calculation.
function add_NDVI(image) {
  //Compute the Normalized Difference Vegetation Index (NDVI).
  var ndvi_calc = image.normalizedDifference(['B8', 'B4'])
    .rename('NDVI');
  // Return the masked image with an NDVI band.
  return image.addBands(ndvi_calc);
}

// Define a function for NDWI calculation.
function add_NDWI(image) {
  //Compute the Normalized Difference Water Index (NDWI).
  var ndwi_calc = image.normalizedDifference(['B3', 'B8'])
    .rename('NDWI');
  // Return the masked image with an NDWI band.
  return image.addBands(ndwi_calc);
}

// 3. CREATE CLOUD-REDUCED IMAGE COLLECTION

// Define select spectral bands.
var bands = ['B2',
            'B3',
            'B4',
            'B5',
            'B6',
            'B7',
            'B8',
            'B8A',
            'B11',
            'B12',
            'EVI2',
            'NBR',
            'NDMI',
            'NDSI',
            'NDVI',
            'NDWI']

// Import Sentinel 2 Cloud Probability
var s2_cloud = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')
  .filterBounds(area_feature)
  .filter(ee.Filter.calendarRange(start_year, end_year, 'year'))
  .filter(ee.Filter.calendarRange(start_month, end_month, 'month'));

// Import Sentinel-2 Level 2A Data
var s2_sr = ee.ImageCollection('COPERNICUS/S2_SR')
  .filterBounds(area_feature)
  .filter(ee.Filter.calendarRange(start_year, end_year, 'year'))
  .filter(ee.Filter.calendarRange(start_month, end_month, 'month'))
  .map(mask_edges);

// Join imagery and cloud probability datasets
var s2sr_join = ee.Join.saveFirst('cloud_mask').apply({
  primary: s2_sr,
  secondary: s2_cloud,
  condition:
      ee.Filter.equals({leftField: 'system:index', rightField: 'system:index'})
});

// Mask the Sentinel-2 imagery
var s2sr_masked = ee.ImageCollection(s2sr_join)
  .map(mask_cloud_probability)
  .map(mask_cloud_cirrus)
  .map(add_EVI2)
  .map(add_NBR)
  .map(add_NDMI)
  .map(add_NDSI)
  .map(add_NDVI)
  .map(add_NDWI)
  .select(bands);

// 4. CREATE MEDIAN COMPOSITES

// Filter image collection targeted around June 10.
var filter_midsummer = ee.Filter.or(
  ee.Filter.date('2022-06-20', '2022-08-20'));
var collection_midsummer = s2sr_masked.filter(filter_midsummer);

// Make median composites from the image collections.
var median_midsummer = collection_midsummer.median();

// Define visualizations.
var rgbVis = {
  min: 0,
  max: 3000,
  bands: ['B4', 'B3', 'B2']
};
var firVis = {
  min:0,
  max: [3500, 6000, 2000],
  bands: ['B11','B8','B4']
};

// Add image to the map.
Map.addLayer(median_midsummer, firVis, 'Midsummer SR Median Composite');

// Add study area to map
var empty = ee.Image().byte();
var outlines = empty.paint({
  featureCollection: area_feature,
  color: 'red',
  width: 2
});
Map.addLayer(outlines, {palette: 'FFFF00'}, 'Study Area');

// Export images for June to Google Drive.
Export.image.toDrive({
  image: median_midsummer,
  description: 'Sent2_Midsummer',
  folder: 'gmt2_sentinel2',
  scale: 10,
  region: area_feature,
  maxPixels: 1e12
});
