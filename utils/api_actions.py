import requests

class APIActions:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        return response.json()

    def post(self, endpoint, data=None):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        return response.json()