import json
import os
from abc import ABC, abstractmethod

import requests


class API(ABC):
    @abstractmethod
    def uploading(self):
        pass


class HeadHunterAPI(API):
    def __init__(self):
        self.params = None
        self.vacancies = None
        self.response_data = None
        self.response_url = None

    def uploading(self, *args):
        self.params = {'text': args,
                       'page': 1,
                       'per_page': 100
                       }
        self.response_url = requests.get('https://api.hh.ru/vacancies?only_with_salary=true', params=self.params)
        self.response_data = json.loads(self.response_url.text)
        self.vacancies = self.response_data['items']
        return self.vacancies


class SuperJobAPI(API):
    API_KEY = os.environ.get('API-KEY')
    KEY = {'X-Api-App-Id': API_KEY}

    def __init__(self):
        self.params = None
        self.vacancies = None
        self.response_data = None
        self.response = None
        self.response_url = None

    def uploading(self, *args):
        self.params = [("keywords", [("srws", 1), ("skwc", "particular"), ("keys", args)]),
                       ("period", 7),
                       ("count", 100)]
        self.response_url = 'https://api.superjob.ru/2.0/vacancies'
        self.response = requests.get(self.response_url, headers=self.KEY, params=self.params)
        self.response_data = json.loads(self.response.text)
        self.vacancies = self.response_data['objects']
        return self.vacancies

