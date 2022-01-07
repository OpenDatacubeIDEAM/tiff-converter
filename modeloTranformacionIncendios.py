"""
Model exported as python.
Name : ModeloConversionIncendios
Group : CUBO
With QGIS : 32001
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsMessageLog
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsProcessingParameterVectorDestination
import processing


class Modeloconversionincendios(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('RasterNBR2', 'Raster NBR2', defaultValue=None))
        self.addParameter(QgsProcessingParameterString('Valormnimo', 'Valor minimo', multiLine=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterString('Valormximo', 'Valor maximo', multiLine=False, defaultValue=''))
        #self.addParameter(QgsProcessingParameterFile('shapefile', 'shapefile', behavior=QgsProcessingParameterFile.File, fileFilter='.shp', defaultValue=None))
        # 'OUTPUT' is the recommended name for the main output
        # parameter.
        self.addParameter(QgsProcessingParameterVectorDestination('Salida','Salida'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # r.reclass
        reglas="0 thru "+parameters['Valormnimo']+" =0 "+parameters['Valormnimo']+' thru ' +parameters['Valormximo'] +" =1 "+parameters['Valormximo']+" thru 100000=0"
        feedback.pushInfo(reglas)
        feedback.pushInfo(reglas)
        #QgsMessageLog.logMessage(reglas,QgsMessageLog.INFO)
        procesoCategorizacion=alg_params = {
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'input': parameters['RasterNBR2'],
            'rules': '',
            'txtrules': reglas,
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        reclasificacionProceso= processing.run('grass7:r.reclass', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #return results
        tiffReclasificado = reclasificacionProceso['output']
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'FIELD': 'Banda 1',
            'INPUT': tiffReclasificado,
            'OUTPUT': parameters['Salida']
        }
        outputs['PoligonizarRsterAVectorial'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results
        # Poligonizar (ráster a vectorial)
        
        

    def name(self):
        return 'ModeloConversionIncendios'

    def displayName(self):
        return 'ModeloConversionIncendios'

    def group(self):
        return 'CUBO'

    def groupId(self):
        return 'CUBO'

    def createInstance(self):
        return Modeloconversionincendios()
