### FAST API & Cohere Together - For a test

#### Instruction to use 

```python
python -m venv dev
source dev/bin/activate
pip install -r requirements.txt
export cohere_api_key=COHERE Token.
export user_name= Username for Basic Auth.
export user_password=Password for Basic Auth.
uvicorn main:app --reload
```

- use URL #http://localhost:8000/docs