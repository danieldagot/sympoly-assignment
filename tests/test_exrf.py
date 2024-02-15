from pydantic import ValidationError
import schemas
from exrf import parse_exrf
import pytest

def test_parse_exrf_to_dict_v2():
    # Path to the EXRF file you want to test
    file_path = "./exrf_examples/8TYCNHmc6m9O.exrf"
    
    # Use your parsing function to get the data
    parsed_data = parse_exrf(file_path)
    print(parsed_data)
    
    # Attempt to create an instance of your MercuryEXRF model with the parsed data
    try:
        exrf_instance = schemas.MercuryEXRF(**parsed_data)
    except ValidationError as e:
        pytest.fail(f"Validation failed: {e.errors}")
    
    # # If needed, perform additional assertions here, for example:
    # assert isinstance(exrf_instance.Reporter, shemas.), "Reporter is not an instance of the expected Pydantic model"
    # assert isinstance(exrf_instance.Report, ReportDetails), "Report is not an instance of the expected Pydantic model"
    # Further assertions can be added as needed to validate the structure and data types of your parsed data
