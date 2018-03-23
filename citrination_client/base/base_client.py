import requests
import json
from citrination_client.util.quote_finder import quote
from response_handling import raise_on_response, check_general_success, check_for_rate_limiting
from errors import *

DEFAULT_FAILURE_MESSAGE = "There was an error communicating with Citrination"

class BaseClient(object):
    """
    Base class that holds the universal constructor, utilities, etc
    """

    def __init__(self, api_key, webserver_host, api_members=[], suppress_warnings=False):
        """
        Constructor.

        :param webserver_host: local pointer to the tunnel to the cmc web host.
        """
        if api_key == None or len(api_key) == 0:
            raise CitrinationClientError("API key must be present to instantiate the client")

        self.headers = {
            'X-API-Key': quote(api_key),
            'Content-Type': 'application/json',
            'X-Citrination-API-Version': '1.0.0'
        }
        self.suppress_warnings = suppress_warnings
        self.api_url = webserver_host + '/api'
        self.api_members = api_members

    # ==== Private Utilities ===

    def _handle_response(self, response, failure_message=DEFAULT_FAILURE_MESSAGE):
        raise_on_response(response)
        check_general_success(response, failure_message)
        return response

    def _get_qualified_route(self, route):
        """
        Get a fully qualified api route.
        :param route: the route (e.g., /model)
        :return: the fully qualified route (e.g., https://citrination.com/model)
        """
        return "{}/{}".format(self.api_url, route)

    def _warn(self, message):
        if not self.suppress_warnings:
            print("Citrination Client Warning - {}".format(message))

    def _get_headers(self, headers=None):
        if headers:
            return headers
        else:
            return self.headers

    def _get(self, route, headers=None, failure_message=None):
        """
        Execute a post request and return the result
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        response_lambda = (lambda: requests.get(self._get_qualified_route(route), headers=headers, verify=False))
        response = check_for_rate_limiting(response_lambda(), response_lambda)
        return self._handle_response(response, failure_message)

    def _post_json(self, route, data, headers=None, failure_message=None):
        return self._post(route, json.dumps(data), headers)

    def _post(self, route, data, headers=None, failure_message=None):
        """
        Execute a post request and return the result
        :param data:
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        response_lambda = (lambda: requests.post(self._get_qualified_route(route), headers=headers, data=data, verify=False))
        response = check_for_rate_limiting(response_lambda(), response_lambda)
        return self._handle_response(response, failure_message)

    def _put_json(self, route, data, headers=None, failure_message=None):
        return self._put(route, json.dumps(data), headers)

    def _put(self, route, data, headers=None, failure_message=None):
        """
        Execute a put request and return the result
        :param data:
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        response_lambda = (lambda: requests.put(self._get_qualified_route(route), headers=headers, data=data, verify=False))
        response = check_for_rate_limiting(response_lambda(), response_lambda)
        return self._handle_response(response, failure_message)

    def _delete(self, route, headers=None, failure_message=None):
        """
        Execute a delete request and return the result
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        response_lambda = (lambda: requests.delete(self._get_qualified_route(route), headers=headers, verify=False))
        response = check_for_rate_limiting(response_lambda(), response_lambda)
        return self._handle_response(response, failure_message)

    def __repr__(self):
        return "{}".format(self.api_members)