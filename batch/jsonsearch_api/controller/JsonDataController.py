from flask import Flask, jsonify, Response
from flask_restful import Resource, Api, request
from jsonsearch_api.service.payloadDataPersist import JsonHandler
from io import StringIO
import json
import os
from jsonsearch_api.constants import LoggerConfig
import logging

app = Flask(__name__)
api = Api(app)


class WebhooksPayloadPersist(Resource):


    def get(self):

        hostAddress = os.environ['HOST_ADDRESS']
        port = os.environ['PORT']

        try:

            searchData = request.args.get('searchData')
            if(searchData == None):
                print("Request data is not Found")
                ioData = StringIO()
                json.dump({'Error': 'Please pass searchData value as query string'},ioData)
                return ioData.getvalue(),500

            app.logger.info('get Data %s', searchData)
            jsonFetch = JsonHandler(hostAddress, port)
            dictData = jsonFetch.searchJsonElasticData(searchData)
        except Exception as err:
            app.logger.error('Exception occured during fetching %s', str(err))
            return Response('Exception occured due to {0}'.format(err), status=500, mimetype='text/plain')

        message = json.dumps(dictData)
        app.logger.info('get Data %s', len(dictData))
        return Response(message, status=200, mimetype='application/json')
        #return jsonify(mapData), 201

    def post(self):
        hostAddress = os.environ['HOST_ADDRESS']
        port = os.environ['PORT']

        try:

            jsonData = request.data
            app.logger.info('post data %s ', jsonData)
            dictData = json.loads(jsonData)
            jsonStore = JsonHandler(hostAddress,port)
            jsonStore.dumpJsonElasticSearchData(dictData)
            app.logger.info('dump data completed - length %s ', len(dictData))

        except Exception as err:
            app.logger.error('Exception occured during dumping %s', str(err))
            return Response('Exception occured due to {0}'.format(err), status=500, mimetype='text/plain')
        return Response('Data Created', status=201, mimetype='text/plain')


api.add_resource(WebhooksPayloadPersist, '/names_score_data')

if __name__ == '__main__':
    logger = LoggerConfig.ClassLoggers()
    log_level = os.environ['LOG_LEVEL']
    console_level = os.environ['CONSOLE_LEVEL']
    if log_level == 'DEBUG':
        log_level = logging.DEBUG
    elif log_level == 'INFO':
        log_level = logging.INFO

    if console_level == 'DEBUG':
        console_level = logging.DEBUG
    elif console_level == 'INFO':
        console_level = logging.INFO
    logger.function_logger(log_level, console_level, funcName=__name__)

    app.run(debug=True,host='0.0.0.0')