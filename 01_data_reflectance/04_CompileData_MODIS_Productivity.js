/* -*- coding: utf-8 -*-
---------------------------------------------------------------------------
Modis Terra+Aqua combined net primary productivity metrics 2000-2020
Author: Timm Nawrocki, Alaska Center for Conservation Science
Last Updated: 2022-12-14
Usage: Must be executed from the Google Earth Engine code editor.
Description: This script produces a set of standardized net primary productivity metrics from the MOD17A3HGF.006 and MYD17A3HGF.006 collections, which summarize net primary productivity from MODIS Terra and Aqua (respectively). Only high quality pixels (qa band greater than or equal to 40) are selected. Original units are retained.
---------------------------------------------------------------------------*/


// 1. DEFINE PROPERTIES

// Define an area of interest geometry.
var area_feature = ee.FeatureCollection('projects/accs-geospatial-processing/assets/gmt2_studyarea');
// Define select spectral bands.
var year_starts = [
  '2000-01-01',
  '2001-01-01',
  '2002-01-01',
  '2003-01-01',
  '2004-01-01',
  '2005-01-01',
  '2006-01-01',
  '2007-01-01',
  '2008-01-01',
  '2009-01-01',
  '2010-01-01',
  '2011-01-01',
  '2012-01-01',
  '2013-01-01',
  '2014-01-01',
  '2015-01-01',
  '2016-01-01',
  '2017-01-01',
  '2018-01-01',
  '2019-01-01',
  '2020-01-01',
  '2021-01-01'
  ]

// 2. DEFINE FUNCTIONS

// Define function to apply quality assurance mask
function apply_qa_mask(image) {
  var image_mask = image.select('Npp_QC').gte(40);
  var image_masked = image.updateMask(image_mask);
  return image_masked;
}

// Define function to combine terra and aqua using mean rule
function combine_npp(terra_image, aqua_image) {
  var modis_collection = ee.ImageCollection([terra_image, aqua_image]);
  var modis_image = modis_collection.mean();
  return modis_image;
}

// 3. PROCESS MODIS DATA

// Import MODIS Terra Net Annual Primary Production (500 m)
var collection_terra = ee.ImageCollection('MODIS/006/MOD17A3HGF')
  .filterBounds(area_feature)
  .filter(ee.Filter.date('2000-01-01', '2021-01-01'))
  .map(apply_qa_mask);
print('MODIS Terra Net Primary Production: ', collection_terra)

// Import MODIS Aqua Net Annual Primary Production (500 m)
var collection_aqua = ee.ImageCollection('MODIS/006/MYD17A3HGF')
  .filterBounds(area_feature)
  .filter(ee.Filter.date('2000-01-01', '2021-01-01'))
  .map(apply_qa_mask);
print('MODIS Aqua Net Primary Production: ', collection_aqua)

// Generate list of images from collection
var terra_list = ee.ImageCollection(collection_terra).toList(999);
var aqua_list = ee.ImageCollection(collection_aqua).toList(999);

// Process images for 2000
var year = 0;
var image_2000 = ee.Image(ee.List(terra_list).get(year));

// Process images for 2001
var year = 1
var image_2001 = ee.Image(ee.List(terra_list).get(year));

// Process images for 2002
var year = 2
var terra_2002 = ee.Image(ee.List(terra_list).get(year));
var aqua_2002 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2002 = combine_npp(terra_2002, aqua_2002);

// Process images for 2003
var year = 3
var terra_2003 = ee.Image(ee.List(terra_list).get(year));
var aqua_2003 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2003 = combine_npp(terra_2003, aqua_2003);

// Process images for 2004
var year = 4
var terra_2004 = ee.Image(ee.List(terra_list).get(year));
var aqua_2004 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2004 = combine_npp(terra_2004, aqua_2004);

// Process images for 2005
var year = 5
var terra_2005 = ee.Image(ee.List(terra_list).get(year));
var aqua_2005 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2005 = combine_npp(terra_2005, aqua_2005);

// Process images for 2006
var year = 6
var terra_2006 = ee.Image(ee.List(terra_list).get(year));
var aqua_2006 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2006 = combine_npp(terra_2006, aqua_2006);

// Process images for 2007
var year = 7
var terra_2007 = ee.Image(ee.List(terra_list).get(year));
var aqua_2007 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2007 = combine_npp(terra_2007, aqua_2007);

// Process images for 2008
var year = 8
var terra_2008 = ee.Image(ee.List(terra_list).get(year));
var aqua_2008 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2008 = combine_npp(terra_2008, aqua_2008);

// Process images for 2009
var year = 9
var terra_2009 = ee.Image(ee.List(terra_list).get(year));
var aqua_2009 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2009 = combine_npp(terra_2009, aqua_2009);

// Process images for 2010
var year = 10
var terra_2010 = ee.Image(ee.List(terra_list).get(year));
var aqua_2010 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2010 = combine_npp(terra_2010, aqua_2010);

// Process images for 2011
var year = 11
var terra_2011 = ee.Image(ee.List(terra_list).get(year));
var aqua_2011 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2011 = combine_npp(terra_2011, aqua_2011);

// Process images for 2012
var year = 12
var terra_2012 = ee.Image(ee.List(terra_list).get(year));
var aqua_2012 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2012 = combine_npp(terra_2012, aqua_2012);

// Process images for 2013
var year = 13
var terra_2013 = ee.Image(ee.List(terra_list).get(year));
var aqua_2013 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2013 = combine_npp(terra_2013, aqua_2013);

// Process images for 2014
var year = 14
var terra_2014 = ee.Image(ee.List(terra_list).get(year));
var aqua_2014 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2014 = combine_npp(terra_2014, aqua_2014);

// Process images for 2015
var year = 15
var terra_2015 = ee.Image(ee.List(terra_list).get(year));
var aqua_2015 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2015 = combine_npp(terra_2015, aqua_2015);

// Process images for 2016
var year = 16
var terra_2016 = ee.Image(ee.List(terra_list).get(year));
var aqua_2016 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2016 = combine_npp(terra_2016, aqua_2016);

// Process images for 2017
var year = 17
var terra_2017 = ee.Image(ee.List(terra_list).get(year));
var aqua_2017 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2017 = combine_npp(terra_2017, aqua_2017);

// Process images for 2018
var year = 18
var terra_2018 = ee.Image(ee.List(terra_list).get(year));
var aqua_2018 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2018 = combine_npp(terra_2018, aqua_2018);

// Process images for 2019
var year = 19
var terra_2019 = ee.Image(ee.List(terra_list).get(year));
var aqua_2019 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2019 = combine_npp(terra_2019, aqua_2019);

// Process images for 2020
var year = 20
var terra_2020 = ee.Image(ee.List(terra_list).get(year));
var aqua_2020 = ee.Image(ee.List(aqua_list).get(year-2));
var image_2020 = combine_npp(terra_2020, aqua_2020);

// Display test image
var visualization = {
  bands: ['Npp'],
  min: 0.0,
  max: 2500.0,
  palette: ['bbe029', '0a9501', '074b03']
};
var qc_visualization = {
  bands: ['Npp_QC'],
  min: 0.0,
  max: 100,
  palette: ['bbe029', '0a9501', '074b03']
}

Map.addLayer(image_2020, qc_visualization, 'NPP_QC')
Map.addLayer(image_2020, visualization, 'NPP');

// 4. EXPORT DATA
// Export 2000
Export.image.toDrive({
  image: image_2000.select('Npp'),
  description: 'MODIS_2000_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2001
Export.image.toDrive({
  image: image_2001.select('Npp'),
  description: 'MODIS_2001_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2002
Export.image.toDrive({
  image: image_2002.select('Npp'),
  description: 'MODIS_2002_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2003
Export.image.toDrive({
  image: image_2003.select('Npp'),
  description: 'MODIS_2003_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2004
Export.image.toDrive({
  image: image_2004.select('Npp'),
  description: 'MODIS_2004_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2005
Export.image.toDrive({
  image: image_2005.select('Npp'),
  description: 'MODIS_2005_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2006
Export.image.toDrive({
  image: image_2006.select('Npp'),
  description: 'MODIS_2006_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2007
Export.image.toDrive({
  image: image_2007.select('Npp'),
  description: 'MODIS_2007_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2008
Export.image.toDrive({
  image: image_2008.select('Npp'),
  description: 'MODIS_2008_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2009
Export.image.toDrive({
  image: image_2009.select('Npp'),
  description: 'MODIS_2009_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2010
Export.image.toDrive({
  image: image_2010.select('Npp'),
  description: 'MODIS_2010_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2011
Export.image.toDrive({
  image: image_2011.select('Npp'),
  description: 'MODIS_2011_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2012
Export.image.toDrive({
  image: image_2012.select('Npp'),
  description: 'MODIS_2012_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2013
Export.image.toDrive({
  image: image_2013.select('Npp'),
  description: 'MODIS_2013_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2014
Export.image.toDrive({
  image: image_2014.select('Npp'),
  description: 'MODIS_2014_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2015
Export.image.toDrive({
  image: image_2015.select('Npp'),
  description: 'MODIS_2015_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2016
Export.image.toDrive({
  image: image_2016.select('Npp'),
  description: 'MODIS_2016_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2017
Export.image.toDrive({
  image: image_2017.select('Npp'),
  description: 'MODIS_2017_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2018
Export.image.toDrive({
  image: image_2018.select('Npp'),
  description: 'MODIS_2018_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2019
Export.image.toDrive({
  image: image_2019.select('Npp'),
  description: 'MODIS_2019_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});

// Export 2020
Export.image.toDrive({
  image: image_2020.select('Npp'),
  description: 'MODIS_2020_NPP',
  folder: 'gmt2_productivity',
  scale: 500,
  crs: 'EPSG:3338',
  region: area_feature,
  maxPixels: 1e12
});