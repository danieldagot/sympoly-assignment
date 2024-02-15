run:
	uvicorn main:app --reload
start:
	poetry shell 
	uvicorn main:app --reload
init: 
	poetry install --no-root
	poetry shell 
	uvicorn main:app --reload

