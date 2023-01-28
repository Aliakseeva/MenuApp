from fastapi.testclient import TestClient

from MenuApp.src.main import app

client = TestClient(app)

response_menu_post = client.post(
    '/api/v1/menus', json={'title': 'Menu title', 'description': 'Menu description'},
)
menu_id = response_menu_post.json()['id']

URL = f'/api/v1/menus/{menu_id}/submenus'
DATA = {'title': 'Submenu title', 'description': 'Submenu description'}
UPDATED_DATA = {'title': 'Upd sm title', 'description': 'Upd sm description'}


class TestSubmenu:
    def setup_class(self):
        self.response_sm_post = client.post(URL, json=DATA)
        self.sm_id = self.response_sm_post.json()['id']

    def test_sm_create(self):
        response = self.response_sm_post

        assert response.status_code == 201

        assert response.json()['title'] == DATA['title']
        assert response.json()['description'] == DATA['description']
        assert isinstance(response.json()['id'], str)

        response_menu = client.get(f'/api/v1/menus/{menu_id}')
        assert response_menu.json()['submenus_count'] == 1

    def test_sm_read(self):
        response = client.get(f'{URL}/{self.sm_id}')

        assert response.status_code == 200

        assert response.json()['title'] == DATA['title']
        assert response.json()['description'] == DATA['description']
        assert isinstance(response.json()['id'], str)

        response404 = client.get(f'{URL}/0')
        assert response404.json() == dict(detail='submenu not found')
        assert response404.status_code == 404

    @staticmethod
    def test_sm_list_read():
        response = client.get(URL)

        assert response.status_code == 200

        assert isinstance(response.json(), list)
        assert response.json()[0]['title'] == DATA['title']
        assert response.json()[0]['description'] == DATA['description']
        assert isinstance(response.json()[0]['id'], str)

    def test_sm_patch(self):
        response = client.patch(f'{URL}/{self.sm_id}', json=UPDATED_DATA)

        assert response.status_code == 200

        assert response.json()['id'] == str(self.sm_id)
        assert response.json()['title'] == UPDATED_DATA['title']
        assert response.json()['description'] == UPDATED_DATA['description']

        response404 = client.patch(f'{URL}/0', json=UPDATED_DATA)
        assert response404.status_code == 404
        assert response404.json() == dict(detail='submenu not found')

    def test_sm_delete(self):
        response = client.delete(f'{URL}/{self.sm_id}')
        assert response.status_code == 200
        assert response.json() == {
            'status': True,
            'message': 'The submenu has been deleted',
        }

        response_none = client.get(URL)
        assert response_none.json() == []

        response_menu = client.get(f'/api/v1/menus/{menu_id}')
        assert response_menu.json()['submenus_count'] == 0

        response404 = client.get(f'{URL}/{self.sm_id}')
        assert response404.status_code == 404
        assert response404.json() == dict(detail='submenu not found')
