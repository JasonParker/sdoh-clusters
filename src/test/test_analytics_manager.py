from pathlib import Path

# Example of importing custom module (analytics_manager) from custom package (src)
from src.models.analytics_manager import AnalyticsManager


# Simple Example Test
def test_example():
    some_result = 2 + 2
    assert some_result ==  4

    
# Test Setup
project_dir = Path(__file__).resolve().parents[2]

# Test data is prepopulated with cluster centers
# or other values where desired cluster is known
# If using DatabaseProvider, can use mocking to pass test data
data_filepath = project_dir / 'data' / 'test_data.csv'
model_filepath = project_dir / 'models' / 'final_clustering.pkl'

manager = AnalyticsManager(str(model_filepath), str(data_filepath))
output = manager.process()
  

# Actual tests (integration)
def test_urbanite():
    assert output[0] == 'Isolated Urbanites'
    
    
def test_multiple():
    assert output[1] == 'Average Suburbia'
    assert output[2] == 'Small Town USA'
    assert output[3] == 'Rural Relationships'
    assert output[4] == 'Vulnerable Locations'
