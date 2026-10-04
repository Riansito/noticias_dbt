import pytest

# Aqui podemos colocar fixtures compartilhadas entre os testes
@pytest.fixture
def dummy_fixture():
    return True
