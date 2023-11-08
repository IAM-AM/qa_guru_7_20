import json

import allure
import jsonschema
import requests
from allure_commons.types import AttachmentType
from curlify import to_curl
from requests import sessions

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


def test_status_code_is_ok():
    response = requests.get(url="https://reqres.in/api/users/")
    assert response.status_code == 200


def test_get_user():
    scheme = load_schema('get_user.json')
    response = requests.get(url='https://reqres.in/api/users/2')

    assert response.status_code == 200
    jsonschema.validate(response.json(), scheme)


def test_post_user():
    scheme = load_schema('post_user.json')
    response = requests.post(url='https://reqres.in/api/users/',
                             json={"name": "Alex", "job": "QA"}
                             )
    assert response.status_code == 201
    jsonschema.validate(response.json(), scheme)


def test_put_user():
    schema = load_schema('put_user.json')
    response = requests.put(
        url='https://reqres.in/api/users/2',
        json={
            "name": "Alex",
            "job": "Resident"
        }
    )
    assert response.status_code == 200
    assert response.json()['job'] == 'Resident'
    jsonschema.validate(response.json(), schema)


def test_delete_users():
    response = requests.delete(url="https://reqres.in/api/users/2")
    assert (response.status_code == 204)


def test_user_registration():
    schema = load_schema('user_registration.json')
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )
    assert response.status_code == 200
    assert response.json()['id'] == 4
    jsonschema.validate(response.json(), schema)


def test_unsuccessful_user_registration():
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "sydney@fife"
        }
    )
    assert response.status_code == 400
    response.json()['error'] = "Missing password"


def test_user_successful_login():
    schema = load_schema('successful_login.json')
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "1234"
        }
    )
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_user_unsuccessful_login():
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "peter@klaven",
        }
    )
    assert response.status_code == 400


def test_get_delayed_response():
    response = requests.get(url="https://reqres.in/api/users", params={"delay": 3})
    assert (response.status_code == 200)
