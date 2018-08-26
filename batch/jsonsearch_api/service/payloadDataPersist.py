from jsonsearch_api.constants import PayloadConstants
from elasticsearch import Elasticsearch
from jsonsearch_api.constants import LoggerConfig
import logging





class JsonHandler:


    def __init__(self, host, port):
        self.es_config = Elasticsearch([{'host': host, 'port': port}])
        self.logger = logging.getLogger(__name__)

    class StuNames:

        def __init__(self, name, score):
            self.name = name
            self.score = score

    # serialize the data using StuNames class as JSON and
    # dumping the data into elastic search
    def dumpJsonElasticSearchData(self, dictData):
        i = PayloadConstants.INDEX_COUNT

        self.logger.info('dumping the json mapData %s', dictData)
        try:
            for key, value in dictData.items():
                self.es_config.index(index="stuname", doc_type='studentNames', body=self.StuNames(key, value).__dict__, id=i)
                i = i + 1
            self.logger.info('dumped the json data, total indexed data: %d',i)
            PayloadConstants.INDEX_COUNT = i
        except Exception as err:
            self.logger.error('Exception occured during dumping %s', str(err))

    # retrieving the data in fast efficient manner
    def searchJsonElasticData(self, searchData):

        self.logger.info('fetching the indexed data using %s', searchData)
        try:

            data = self.es_config.search(index='stuname', body={
                "query": {"regexp": {"name": searchData + "[a-z]+|([a-z])+_" + searchData + "[a-z]*"}}}, sort='score:desc')
            dataMap = map(lambda mapData: (mapData['_source']['name'], mapData['_source']['score']),
                          data['hits']['hits'][0:10])
            dictval = {str(key): value for key, value in dataMap}
            self.logger.info('fetched the data using total data no :%d', len(dictval))
        except Exception as err:
            self.logger.error('Exception occured during fetching %s', str(err))
        return dictval




if __name__ == '__main__':
    # data
    mapNames = {'surrou_vig': 700, 'surrou_vignesh': 900, 'vignesh': 100,
                'vigneshwar': 200, 'venkavig': 1000, 'vrgr_vignesh': 1200, '_vignesh': 1500}

    jsonHandle = JsonHandler('localhost', 9200)
    jsonHandle.dumpJsonElasticSearchData(mapNames)

    for namesOrder in jsonHandle.searchJsonElasticData('vig'):
        print(namesOrder)
