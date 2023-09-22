import pytest


@pytest.fixture
def setup_temp_dirs_with_files(tmpdir):
    """Create temporary source and replica directories with some files for testing."""
    source = tmpdir.mkdir("source")
    replica = tmpdir.mkdir("replica")

    # Add some files to source
    source.join("file1.txt").write("content1")
    source.join("file2.txt").write("content2")

    yield source, replica


@pytest.fixture
def setup_temp_log_file(tmpdir):
    """Create a temporary log file."""
    log_file = tmpdir.join("sync.log")
    yield log_file