from fastapi.testclient import TestClient

from MenuApp.src.main import app

client = TestClient(app)

response_menu_post = client.post(
    '/api/v1/menus', json={'title': 'Menu title', 'description': 'Menu description'},
)
menu_id = response_menu_post.json()['id']

response_sm_post = client.post(
    f'/api/v1/menus/{menu_id}/submenus',
    json={'title': 'Submenu title', 'description': 'Submenu description'},
)
sm_id = response_sm_post.json()['id']

URL = f'/api/v1/menus/{menu_id}/submenus/{sm_id}/dishes'
DATA = {
    'title': 'Dish title',
    'description': 'Dish description', 'price': '99.99',
}
UPDATED_DATA = {
    'title': 'Upd dish title',
    'description': 'Upd dish description',
    'price': '100.00',
}


class TestDish:
    def setup_class(self):
        self.response_dish_post = client.post(URL, json=DATA)
        self.dish_id = self.response_dish_post.json()['id']

    def test_dish_create(self):
        response = self.response_dish_post

        assert response.status_code == 201

        assert response.json()['title'] == DATA['title']
        assert response.json()['description'] == DATA['description']
        assert response.json()['price'] == DATA['price']
        assert isinstance(response.json()['id'], str)

        response_menu = client.get(f'/api/v1/menus/{menu_id}')
        assert response_menu.json()['dishes_count'] == 1

    def test_dish_read(self):
        response = client.get(f'{URL}/{self.dish_id}')

        assert response.status_code == 200

        assert response.json()['title'] == DATA['title']
        assert response.json()['description'] == DATA['description']
        assert response.json()['price'] == DATA['price']

        assert isinstance(response.json()['id'], str)

        response404 = client.get(f'{URL}/0')
        assert response404.json() == dict(detail='dish not found')
        assert response404.status_code == 404

    @staticmethod
    def test_dish_list_read():
        response = client.get(URL)

        assert response.status_code == 200

        assert isinstance(response.json(), list)
        assert response.json()[0]['title'] == DATA['title']
        assert response.json()[0]['description'] == DATA['description']
        assert response.json()[0]['price'] == DATA['price']
        assert isinstance(response.json()[0]['id'], str)

    def test_dish_patch(self):
        response = client.patch(f'{URL}/{self.dish_id}', json=UPDATED_DATA)

        assert response.status_code == 200

        assert response.json()['id'] == str(self.dish_id)
        assert response.json()['title'] == UPDATED_DATA['title']
        assert response.json()['description'] == UPDATED_DATA['description']
        assert response.json()['price'] == UPDATED_DATA['price']

        response404 = client.patch(f'{URL}/0', json=UPDATED_DATA)
        assert response404.status_code == 404
        assert response404.json() == dict(detail='dish not found')

    def test_sm_delete(self):
        response = client.delete(f'{URL}/{self.dish_id}')
        assert response.status_code == 200
        assert response.json() == {
            'status': True,
            'message': 'The dish has been deleted',
        }

        response_none = client.get(URL)
        assert response_none.json() == []

        response_menu = client.get(f'/api/v1/menus/{menu_id}')
        assert response_menu.json()['dishes_count'] == 0

        response404 = client.get(f'{URL}/{self.dish_id}')
        assert response404.status_code == 404
        assert response404.json() == dict(detail='dish not found')
