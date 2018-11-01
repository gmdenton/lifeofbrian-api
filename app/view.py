from . import errors
from . import models
from . import app
from constants import *
from flask import logging
import uuid
import time
from flask import request
from flask import Response
from flask import jsonify
from flask import json

"""API base class. Implements time tracking, transaction_id flow_name and standard error message dict. """


class BaseAPI(object):

    def __init__(self, flow_name):
        self.flow_name = flow_name;
        self.err = {"errorCode": 0, "errorMessage": ""}
        self.logger = logging.getLogger()
        self._StartTime = 0
        self._EndTime = 0
        self.resp = None
        self.transaction_id = ''

    def set_start_time(self):
        self._StartTime = int(round(time.time()) * 1000)

    def get_execution_time(self):
        self._EndTime = int(round(time.time()) * 1000)
        return self._EndTime - self._StartTime

    @staticmethod
    def get_transaction_id():
        return str(uuid.uuid4())

    def set_transaction_id(self):
        if request.headers.get('X-TransactionId') is not None:
            self.transaction_id = request.headers.get('X-TransactionId')
        else:
            self.transaction_id = self.get_transaction_id()
            request.headers = {'X-TransactionId': self.transaction_id}

    def error_handler(self, statuscode, error=None):
        if statuscode == 400:
            return errors.bad_request(error)
        elif statuscode == 404:
            return errors.not_found(error)
        else:
            return errors.technnical_error(error)

    def process_request(self):
        raise NotImplementedError("Abstract method. To be implemented in ancestor classes")

    def validate(self):
        raise NotImplementedError("Abstract method. To be implemented in ancestor classes")


""" Class to implement API to create a new customer """


class CreateCheese(BaseAPI):

    def __init__(self):
        super().__init__("Create_Cheese")

    def validate(self):
        if not request.json or not request.json['name'] or not request.json['description']:
            self.err['errorCode'] = 400
            self.err['errorMessage'] = 'Missing required field'

    def fill_cheese(self):
        cheese = models.Cheese(request.json.get('name'), request.json.get('description'), request.json.get('size'), request.json.get('stock'), request.json.get('origin'), request.json.get('no_stock_reason'))
        return cheese

    def process_request(self):
        self.set_transaction_id()
        self.set_start_time()
        self.validate()
        if self.err['errorCode'] > 0:
            self.error_handler(self.err['errorCode'], self.err['errorMessage'])
        else:
            dbc = models.DBCustomer()
            dbc.insert(self.fill_cheese())
            self.logger.info('flow_name={} TransactionId={}, request payload={}'.format(self.flow_name, self.transaction_id, json.dumps(request.json)))
            if dbc.errorCode is None:
                self.resp = Response(json.dumps(dbc.cheese), status=201, headers={'X-TransactionID': self.transaction_id}, mimetype='application/json')
                self.logger.info(
                    'flow_name={} TransactionId={}, payload={} time taken={}'.format(self.flow_name, self.transaction_id,
                                                                               json.dumps(dbc.cheese), self.get_execution_time()))

                return jsonify(dbc.cheese)

            else:
                return self.error_handler(dbc.errorCode, dbc.error)


""" Class to implement API to return a list of all customers """


class ReadCheeseShop(BaseAPI):

    def __init__(self):
        super().__init__("Read_Cheese")

    def validate(self):
        pass

    def process_request(self):
        self.set_transaction_id()
        self.set_start_time()
        dbc = models.DBCustomer()
        dbc.read()
        if dbc.errorCode is None:
            self.resp = Response(json.dumps(dbc.cheeseshop['cheeses']), status=200, headers={'X-TransactionID': self.transaction_id},
                                 mimetype='application/json')
            self.logger.info(
                'flow_name={} TransactionId={}, payload={} time taken={}'.format(self.flow_name, self.transaction_id,
                                                                                 json.dumps(dbc.cheeseshop['cheeses']),
                                                                                 self.get_execution_time()))
            return jsonify({"Cheeses": dbc.cheeseshop['cheeses']})
        else:
            return self.error_handler(dbc.errorCode, dbc.error)


""" Class to implement API to return a single cheese """


class GetCheese(BaseAPI):

    def __init__(self):
        super().__init__("Get_Cheese")

    def validate(self):
        pass

    def process_request(self, cheese):
        self.set_transaction_id()
        self.set_start_time()
        dbc = models.DBCustomer()
        dbc.get(cheese)
        if dbc.errorCode is None:
            self.resp = Response(json.dumps(dbc.cheese), status=200,
                                 headers={'X-TransactionID': self.transaction_id},
                                 mimetype='application/json')
            self.logger.info(
                'flow_name={} TransactionId={}, payload={} time taken={}'.format(self.flow_name, self.transaction_id,
                                                                                 json.dumps(dbc.cheese),
                                                                                 self.get_execution_time()))
            return jsonify(dbc.cheese)
        else:
            return self.error_handler(dbc.errorCode, dbc.error)


@app.route(base_url, methods=['POST'])
def create_cheese():
    ch = CreateCheese()
    return ch.process_request()


@app.route(base_url, methods=['GET'])
def read_cheese():
    rc = ReadCheeseShop()
    return rc.process_request()


@app.route(base_url+'/<string:cheese>', methods=['GET'])
def get_cheese(cheese):
    gc = GetCheese()
    return gc.process_request(cheese)