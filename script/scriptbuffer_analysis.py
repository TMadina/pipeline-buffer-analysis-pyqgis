
pipeline_layer = QgsProject.instance().mapLayersByName('pipeline_layer')[0]
wells_layer = QgsProject.instance().mapLayersByName('wells_layer')[0]

from qgis.PyQt.QtCore import QVariant

if 'near_pipeline' not in [field.name() for field in wells_layer.fields()]:
    wells_layer.dataProvider().addAttributes([
        QgsField('near_pipeline', QVariant.Bool)
    ])
    wells_layer.updateFields()

index = QgsSpatialIndex(pipeline_layer.getFeatures())

with edit(wells_layer):
    for well in wells_layer.getFeatures():
        geom = well.geometry()
        bbox = geom.buffer(1000, 20).boundingBox()
        candidate_ids = index.intersects(bbox)
        near_pipeline = False
        
        for fid in candidate_ids:
            pipeline = pipeline_layer.getFeature(fid)
            
            if pipeline.geometry().distance(geom) <= 1000:
                near_pipeline = True
                break
        
        if well['Citing_Typ'] == 'ACTUAL' and near_pipeline:
            well['near_pipeline'] = True
        else:
            well['near_pipeline'] = False
        
        wells_layer.updateFeature(well)