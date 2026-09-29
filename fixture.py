# fixture is a resuable setup function that prepaers a data,browser 

import pytest

@pytest.fixture
def sample_data():
    return{
        "name":"pavan",
        "age":30
    }

def getdata(sample_data):
    print(sample_data["name"])