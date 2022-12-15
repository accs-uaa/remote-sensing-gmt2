/* -*- coding: utf-8 -*-
---------------------------------------------------------------------------
Modis Terra+Aqua combined phenology metrics 2001-2019
Author: Timm Nawrocki, Alaska Center for Conservation Science
Last Updated: 2022-12-14
Usage: Must be executed from the Google Earth Engine code editor.
Description: This script produces a set of standardized phenology metrics from the MCD12Q2.006 collection, which summarizes vegetation phenology from MODIS Enhanced Vegetation Index. Only high quality pixels (qa band equals 0 or 1) are selected. All values are exported as day of year.
---------------------------------------------------------------------------*/


// 1. DEFINE PROPERTIES

// Define an area of interest geometry.
var area_feature = ee.FeatureCollection('projects/accs-geospatial-processing/assets/gmt2_studyarea');
// Define select spectral bands.
var year_starts = [
  '2001-01-01',
  '2002-01-01',
  '2003-01-01',
  '2003-12-31',
  '2005-01-01',
  '2006-01-01',
  '2007-01-01',
  '2007-12-31',
  '2009-01-01',
  '2010-01-01',
  '2011-01-01',
  '2011-12-31',
  '2013-01-01',
  '2014-01-01',
  '2015-01-01',
  '2015-12-31',
  '2017-01-01',
  '2018-01-01',
  '2019-01-01'
  ]
var bands_original = [
  'MidGreenup_1',
  'Maturity_1',
  'Senescence_1',
  'MidGreendown_1'
  ]
var bands_new = [
  'midgreenup_doy',
  'maturity_doy',
  'senescence_doy',
  'midgreendown_doy'
  ]

// 2. DEFINE FUNCTIONS

// Helper function to extract the values from specific bits
// The input parameter can be a ee.Number() or ee.Image()
// Code adapted from https://gis.stackexchange.com/a/349401/5160
var bitwiseExtract = function(input, fromBit, toBit) {
  var maskSize = ee.Number(1).add(toBit).subtract(fromBit);
  var mask = ee.Number(1).leftShift(maskSize).subtract(1);
  return input.rightShift(fromBit).bitwiseAnd(mask);
}

// Define function to calculate day offset
function calculate_offset(date_string) {
  var day_offset = ee.Date(date_string).difference(ee.Date('1970-01-01'), 'days').add(1);
  return day_offset;
}

// Define function to calculate day of year (doy) metrics
function calculate_doy(image, name_original, name_new, day_offset) {
  var image_doy = image.select(name_original)
    .subtract(day_offset)
    .rename(name_new);
  return image_doy;
}

// Define function to apply quality assurance mask
function apply_qa_mask(image, qa_detailed, bit_start, bit_end) {
  var image_mask = bitwiseExtract(qa_detailed, bit_start, bit_end).lte(1);
  var image_masked = image.updateMask(image_mask);
  return image_masked;
}

// Define function to create day of year image
function create_doy_image(image, bands_original, bands_new, year_start) {
  var qa_detailed = image.select('QA_Detailed_1');
  var day_offset = calculate_offset(year_start);
  // Calculate doy metrics
  var midgreenup_doy = calculate_doy(image, bands_original[0], bands_new[0], day_offset);
  var maturity_doy = calculate_doy(image, bands_original[1], bands_new[1], day_offset);
  var senescence_doy = calculate_doy(image, bands_original[2], bands_new[2], day_offset);
  var midgreendown_doy = calculate_doy(image, bands_original[3], bands_new[3], day_offset);
  // Apply quality masks
  var midgreenup_masked = apply_qa_mask(midgreenup_doy, qa_detailed, 2, 3);
  var maturity_masked = apply_qa_mask(maturity_doy, qa_detailed, 6, 7);
  var senescence_masked = apply_qa_mask(senescence_doy, qa_detailed, 10, 11);
  var midgreendown_masked = apply_qa_mask(midgreendown_doy, qa_detailed, 8, 9);
  // Create new image
  var new_image = ee.Image([
    midgreenup_masked,
    maturity_masked,
    senescence_masked,
    midgreendown_masked
    ]
  );
  return new_image;
}

// 3. PROCESS MODIS DATA

// Import MODIS MCD12Q2 (Terra+Aqua Land Cover Dynamics Yearly 500 m)
var collection = ee.ImageCollection('MODIS/006/MCD12Q2')
  .filterBounds(area_feature)
  .filter(ee.Filter.date('2001-01-01', '2019-12-31'));
print('MODIS Land Cover Dynamics: ', collection)

// Generate list of images from collection
var collection_list = ee.ImageCollection(collection).toList(999);

// Process images for 2001
var year = 0;
var image_2001 = ee.Image(ee.List(collection_list).get(year));
var image_2001_doy = create_doy_image(image_2001, bands_original, bands_new, year_starts[year]);

// Process images for 2002
var year = 1;
var image_2002 = ee.Image(ee.List(collection_list).get(year));
var image_2002_doy = create_doy_image(image_2002, bands_original, bands_new, year_starts[year]);

// Process images for 2003
var year = 2;
var image_2003 = ee.Image(ee.List(collection_list).get(year));
var image_2003_doy = create_doy_image(image_2003, bands_original, bands_new, year_starts[year]);

// Process images for 2004
var year = 3;
var image_2004 = ee.Image(ee.List(collection_list).get(year));
var image_2004_doy = create_doy_image(image_2004, bands_original, bands_new, year_starts[year]);

// Process images for 2005
var year = 4;
var image_2005 = ee.Image(ee.List(collection_list).get(year));
var image_2005_doy = create_doy_image(image_2005, bands_original, bands_new, year_starts[year]);

// Process images for 2006
var year = 5;
var image_2006 = ee.Image(ee.List(collection_list).get(year));
var image_2006_doy = create_doy_image(image_2006, bands_original, bands_new, year_starts[year]);

// Process images for 2007
var year = 6;
var image_2007 = ee.Image(ee.List(collection_list).get(year));
var image_2007_doy = create_doy_image(image_2007, bands_original, bands_new, year_starts[year]);

// Process images for 2008
var year = 7;
var image_2008 = ee.Image(ee.List(collection_list).get(year));
var image_2008_doy = create_doy_image(image_2008, bands_original, bands_new, year_starts[year]);

// Process images for 2009
var year = 8;
var image_2009 = ee.Image(ee.List(collection_list).get(year));
var image_2009_doy = create_doy_image(image_2009, bands_original, bands_new, year_starts[year]);

// Process images for 2010
var year = 9;
var image_2010 = ee.Image(ee.List(collection_list).get(year));
var image_2010_doy = create_doy_image(image_2010, bands_original, bands_new, year_starts[year]);

// Process images for 2011
var year = 10;
var image_2011 = ee.Image(ee.List(collection_list).get(year));
var image_2011_doy = create_doy_image(image_2011, bands_original, bands_new, year_starts[year]);

// Process images for 2012
var year = 11;
var image_2012 = ee.Image(ee.List(collection_list).get(year));
var image_2012_doy = create_doy_image(image_2012, bands_original, bands_new, year_starts[year]);

// Process images for 2013
var year = 12;
var image_2013 = ee.Image(ee.List(collection_list).get(year));
var image_2013_doy = create_doy_image(image_2013, bands_original, bands_new, year_starts[year]);

// Process images for 2014
var year = 13;
var image_2014 = ee.Image(ee.List(collection_list).get(year));
var image_2014_doy = create_doy_image(image_2014, bands_original, bands_new, year_starts[year]);

// Process images for 2015
var year = 14;
var image_2015 = ee.Image(ee.List(collection_list).get(year));
var image_2015_doy = create_doy_image(image_2015, bands_original, bands_new, year_starts[year]);

// Process images for 2016
var year = 15;
var image_2016 = ee.Image(ee.List(collection_list).get(year));
var image_2016_doy = create_doy_image(image_2016, bands_original, bands_new, year_starts[year]);

// Process images for 2017
var year = 16;
var image_2017 = ee.Image(ee.List(collection_list).get(year));
var image_2017_doy = create_doy_image(image_2017, bands_original, bands_new, year_starts[year]);

// Process images for 2018
var year = 17;
var image_2018 = ee.Image(ee.List(collection_list).get(year));
var image_2018_doy = create_doy_image(image_2018, bands_original, bands_new, year_starts[year]);

// Process images for 2019
var year = 18;
var image_2019 = ee.Image(ee.List(collection_list).get(year));
var image_2019_doy = create_doy_image(image_2019, bands_original, bands_new, year_starts[year]);

// 4. EXPORT DATA
// Export 2001
Export.image.toDrive({
  image: image_2001_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2001_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2001_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2001_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2001_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2001_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2001_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2001_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2002
Export.image.toDrive({
  image: image_2002_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2002_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2002_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2002_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2002_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2002_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2002_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2002_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2003
Export.image.toDrive({
  image: image_2003_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2003_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2003_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2003_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2003_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2003_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2003_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2003_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2004
Export.image.toDrive({
  image: image_2004_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2004_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2004_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2004_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2004_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2004_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2004_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2004_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2005
Export.image.toDrive({
  image: image_2005_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2005_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2005_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2005_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2005_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2005_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2005_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2005_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2006
Export.image.toDrive({
  image: image_2006_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2006_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2006_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2006_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2006_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2006_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2006_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2006_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2007
Export.image.toDrive({
  image: image_2007_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2007_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2007_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2007_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2007_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2007_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2007_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2007_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2008
Export.image.toDrive({
  image: image_2008_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2008_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2008_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2008_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2008_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2008_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2008_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2008_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2009
Export.image.toDrive({
  image: image_2009_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2009_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2009_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2009_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2009_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2009_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2009_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2009_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2010
Export.image.toDrive({
  image: image_2010_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2010_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2010_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2010_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2010_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2010_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2010_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2010_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2011
Export.image.toDrive({
  image: image_2011_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2011_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2011_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2011_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2011_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2011_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2011_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2011_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2012
Export.image.toDrive({
  image: image_2012_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2012_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2012_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2012_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2012_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2012_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2012_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2012_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2013
Export.image.toDrive({
  image: image_2013_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2013_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2013_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2013_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2013_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2013_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2013_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2013_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2014
Export.image.toDrive({
  image: image_2014_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2014_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2014_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2014_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2014_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2014_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2014_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2014_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2015
Export.image.toDrive({
  image: image_2015_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2015_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2015_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2015_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2015_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2015_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2015_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2015_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2016
Export.image.toDrive({
  image: image_2016_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2016_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2016_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2016_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2016_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2016_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2016_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2016_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2017
Export.image.toDrive({
  image: image_2017_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2017_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2017_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2017_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2017_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2017_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2017_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2017_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2018
Export.image.toDrive({
  image: image_2018_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2018_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2018_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2018_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2018_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2018_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2018_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2018_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2019
Export.image.toDrive({
  image: image_2019_doy.select('midgreenup_doy'),
  description: 'MCD12Q2006_2019_01_midgreenup',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2019_doy.select('maturity_doy'),
  description: 'MCD12Q2006_2019_02_maturity',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2019_doy.select('senescence_doy'),
  description: 'MCD12Q2006_2019_03_senescence',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});
Export.image.toDrive({
  image: image_2019_doy.select('midgreendown_doy'),
  description: 'MCD12Q2006_2019_04_midgreendown',
  folder: 'gmt2_phenology',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});