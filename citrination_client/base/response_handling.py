from errors import *

def raise_on_response(response):
    _check_response_for_version_mismatch(response)
    _check_response_for_feature_availability(response)
    _check_response_for_authorization(response)
    _check_response_for_server_error(response)
    return response

def _check_response_for_authorization(response):
    if response.status_code == 401:
        raise UnauthorizedAccessException()

def _check_response_for_feature_availability(response):
    if response.status_code == 403:
        raise FeatureUnavailableException()

def _check_response_for_server_error(response):
    if response.status_code >= 500:
        raise CitrinationServerErrorException(
                "Citrination returned an error code - code: {}, body: {}".format(response.status_code, response.content)
            )

def _check_response_for_version_mismatch(response):
    try:
        if response.status_code == 400:
            error_type = response_content["error_type"]
            if error_type == "Version Mismatch":
                raise APIVersionMismatchException()
        return response
    except KeyError:
        return response