import pytest


@pytest.fixture
def exemplary_log_file(tmpdir):
    yield str(tmpdir.join("sync.log"))
