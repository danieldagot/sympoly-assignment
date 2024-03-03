# from pytest_bdd import scenarios, given, when, then, parsers
# import pytest
# from asgi_lifespan import LifespanManager
# from httpx import AsyncClient
# from pathlib import Path

# from main import create_app  # Adjust the import path according to your FastAPI app structure

# # Fixture for initializing the FastAPI application
# @pytest.fixture()
# def app():
#     return  create_app()

# # Fixture for initializing the HTTP client for tests
# @pytest.fixture()
# async def client_test(app):
#     """
#     Create an instance of the client for testing.
#     :return: yield HTTP client.
#     """
#     async with LifespanManager(app):
#         async with AsyncClient(app=app, base_url="http://testserver") as ac:  # Use 'testserver' as base URL
#             yield ac

# # Load scenarios from the feature file
# scenarios('../features/api.feature')

# # Helper function to get the relative path of the file
# def get_file_path(file_name):
#     base_dir = Path(__file__).resolve().parent.parent  # Adjust according to your project structure
#     file_path = base_dir / 'taskDocs' / 'exrf_examples' / file_name
#     logging.error(file_path)
#     return file_path

# @given(parsers.parse('I have a file named "{file_name}"'), target_fixture="file_path")
# def i_have_a_file_named(file_name):
#     file_path = get_file_path(file_name)
#     assert file_path.exists()
#     return file_path
# @pytest.mark.anyio
# @when("I upload the file", target_fixture="response")
# async def i_upload_the_file(client_test, file_path):
#     with file_path.open('rb') as file:
#         response = await client_test.post(
#             "/invoices",
#             files={"file": (file_path.name, file, "multipart/form-data")},
#         )
#     return response

# @then("I receive a successful upload response")
# def i_receive_a_successful_upload_response(response):
#     assert response.status_code == 200
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from main import app
import logging


# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/invoices")
#     logging.basicConfig(filename='app3.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     logging.error(response.json())
#     assert response.status_code == 200
#     assert response.json() == {"message": "Tomato"}
@pytest.fixture(name='client_test')
async def client_test():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
# async def client_test():
#     """
#     Create an instance of the client.
#     :return: yield HTTP client.
#     """
#     async with LifespanManager(app):
#         async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
#             yield ac

            
@pytest.mark.asyncio
async def test_populate_must_work(client_test):
    # Assuming the fixture correctly sets up and yields an AsyncClient instance
    client = await client_test.__anext__()
    response = await client.get("")
    
    print(response)
    assert response.status_code == 200
    # If you need to perform cleanup, consider using try/finally

    
# @pytest.mark.anyio
# async def text_get():
#     logging.basicConfig(filename='app3.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/invoices")
    
#     print(response.json())
#     logging.error(response.json())
#     assert response.status_code == 500



    