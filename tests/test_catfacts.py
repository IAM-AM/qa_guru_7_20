import jsonschema
import allure
import json

from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType

from utils import load_schema


def catfacts_api(method, url, **kwargs):
    new_url = 'https://catfact.ninja' + url

    with allure.step(f'{method.upper()} {url}'):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)

            allure.attach(body=message.encode('utf8'), name='Curl',
                          attachment_type=AttachmentType.TEXT, extension='txt')
            try:
                allure.attach(body=json.dumps(response.json(), indent=4).encode('utf8'), name='Response Json',
                              attachment_type=AttachmentType.JSON, extension='json')
            except:
                allure.attach(body=response.content, name='Response',
                              attachment_type=AttachmentType.TEXT, extension='txt')
    return response


def test_get_breeds_status_code_is_ok():
    response = catfacts_api(
        'get',
        url='/breeds')

    assert response.status_code == 200


def test_get_breeds_schema_validation():
    schema = load_schema('get_breeds.json')

    response = catfacts_api(
        'get',
        url='/breeds')

    jsonschema.validate(response.json(), schema)


def test_get_fact_status_code_is_ok():
    response = catfacts_api(
        'get',
        url='/fact')

    assert response.status_code == 200


def test_get_random_fact_schema_validation():
    schema = load_schema('get_fact.json')
    response = catfacts_api(
        'get',
        url='/fact')

    jsonschema.validate(response.json(), schema)
