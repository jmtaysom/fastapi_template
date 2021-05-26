from requests.models import Response


def test_root(client):
    with client:
        response: Response = client.get('/')
        assert response.status_code == 200
        assert response.json() == {
            'status': 'healthy',
            'database': 'connected'
        }


def test_404(client):
    with client:
        response: Response = client.get('/404')
        assert response.status_code == 404
