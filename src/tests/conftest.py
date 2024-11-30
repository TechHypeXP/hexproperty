import pytest
import logging

@pytest.fixture(autouse=True)
def setup_logging():
    """Sets up logging for all tests"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
