import pytest


@pytest.fixture
def temporary_directories_with_files(tmpdir):
    """Create temporary source and replica directories with some files for testing."""
    source = tmpdir.mkdir("source")
    replica = tmpdir.mkdir("replica")

    source.join("file1.txt").write("content1")
    source.join("file2.txt").write("content2")

    yield source, replica


@pytest.fixture
def exemplary_log_file(tmpdir):
    yield str(tmpdir.join("sync.log"))
