 @echo on
 CALL venv\Scripts\activate
 CALL uvicorn webapp.main:app --reload --port 3979
 pause


