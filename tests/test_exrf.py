# from pydantic import ValidationError
# from  models.invoiceModel import MercuryEXRF 
# from exrf import parse_exrf
# import pytest

# def test_parse_exrf_to_dict_v2():
#     # Path to the EXRF file you want to test
#     file_path = "/Users/daniedagot/Downloads/sympoly-assignment/taskDocs/exrf_examples/0zZw5Uas9Pkp.exrf"
    
#     # Use your parsing function to get the data
#     parsed_data = parse_exrf(file_path)
    
#     # Attempt to create an instance of your MercuryEXRF model with the parsed data
#     try:
#         exrf_instance =  MercuryEXRF(**parsed_data)
#     except ValidationError as e:
#         for error in e.errors():
#             print(f"Error in field {error['loc']}: {error['msg']}")
#         pytest.fail(f"Validation failed with detailed errors.")

#     # # If needed, perform additional assertions here, for example:
#     # assert isinstance(exrf_instance.Reporter, shemas.), "Reporter is not an instance of the expected Pydantic model"
#     # assert isinstance(exrf_instance.Report, ReportDetails), "Report is not an instance of the expected Pydantic model"
#     # Further assertions can be added as needed to validate the structure and data types of your parsed data

# def test_extra_field():
#     # Path to the EXRF file you want to test
#     file_path = "/Users/daniedagot/Downloads/sympoly-assignment/exrf_examples/8TYCNHmc6m9O.exrf"
#     # Use your parsing function to get the data
#     parsed_data = parse_exrf(file_path)
#     parsed_data["extra_field"] = "extra"
#     # Attempt to create an instance of your MercuryEXRF model with the parsed data
#     with pytest.raises(ValidationError) as e:
#         exrf_instance = schemas.MercuryEXRF(**parsed_data)
#     assert "extra_field" in str(e.value)
 
