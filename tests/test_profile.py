from urls import Urls

import pytest
import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from hotwing_core import Profile

class TestProfile():
    def test_load_url(self):
        urls = Urls()
        for i in range(20):
            url = urls.random['location']
            try:
                p = Profile(url)
            except:
                print url
                raise
                