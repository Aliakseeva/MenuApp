import pytest

from MenuApp.src.main import app as apps
from fastapi.testclient import TestClient


client = TestClient(apps)

URL = '/api/v1/menus'
DATA = {'title': 'Title', 'description': 'Description'}
UPDATED_DATA = {'title': 'Upd title', 'description': 'Upd description'}


class TestMenu:
    def setup_class(self):
        self.response_menu_post = client.post(URL, json=DATA)
        self.menu_id = self.response_menu_post.json()['id']

    @pytest.mark.create
    def test_menu_create(self):
        response = self.response_menu_post

        assert response.status_code == 201
        assert response.json()['title'] == DATA['title']
        assert response.json()['description'] == DATA['description']
        assert isinstance(response.json()['id'], str)

    @pytest.mark.read
    def test_menu_read(self):
        response = client.get(f'{URL}/{self.menu_id}')

        assert response.status_code == 200

        assert response.json()['title'] == DATA['title']
        assert response.json()['description'] == DATA['description']
        assert isinstance(response.json()['id'], str)

        response404 = client.get(f'{URL}/0')
        assert response404.json() == dict(detail='menu not found')
        assert response404.status_code == 404

    @staticmethod
    def test_menu_list_read():
        response = client.get(URL)

        assert response.status_code == 200

        assert isinstance(response.json(), list)
        assert response.json()[0]['title'] == DATA['title']
        assert response.json()[0]['description'] == DATA['description']
        assert type(response.json()[0]['id']) == str

    def test_menu_patch(self):
        response = client.patch(f'{URL}/{self.menu_id}', json=UPDATED_DATA)

        assert response.status_code == 200

        assert response.json()['id'] == str(self.menu_id)
        assert response.json()['title'] == UPDATED_DATA['title']
        assert response.json()['description'] == UPDATED_DATA['description']

        response404 = client.patch(f'{URL}/0', json=UPDATED_DATA)
        assert response404.status_code == 404
        assert response404.json() == dict(detail='menu not found')

    def test_menu_delete(self):
        response = client.delete(f'{URL}/{self.menu_id}')
        assert response.status_code == 200
        assert response.json() == {'status': True, 'message': 'The menu has been deleted'}

        response404 = client.get(f'{URL}/{self.menu_id}')
        assert response404.status_code == 404
        assert response404.json() == dict(detail='menu not found')
