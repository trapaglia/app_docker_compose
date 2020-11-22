import time
from locust import HttpUser, task

class QuickstartUser(HttpUser):

    @task(1)
    def index(self):
        self.client.get('/')

    @task(3)
    def predict(self):
        for i in range(4):
            self.client.post('/predict', params={'text': 'dolar %d'%i})

    def on_start(self):
        pass
