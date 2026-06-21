import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'success'
    assert 'Welcome' in json_data['message']

def test_calculate_no_mesh(client):
    rv = client.post('/api/calculate', json={})
    assert rv.status_code == 400
    assert 'error' in rv.get_json()

def test_calculate_cube(client):
    payload = {
        "mesh_path": "mesh/cube.trpa",
        "problem_type": "static",
        "solve_method": "direct",
        "elasticity": [2.0E+11],
        "poisson_ratio": [0.3],
        "boundary_conditions": [
            {"e": "0", "p": "z=0", "d": 7}  # 1 | 2 | 4 -> 7
        ],
        "surface_loads": [
            {"e": "1.0E+8", "p": "z=1", "d": 4}
        ]
    }

    rv = client.post('/api/calculate', json=payload)
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'success'
    results = json_data['results']
    assert len(results) > 0

    # We expect results to have names like 'U', 'V', 'W', etc.
    names = [r['name'] for r in results]
    assert 'U' in names
    assert 'V' in names
    assert 'W' in names
