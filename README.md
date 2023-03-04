# se2021-23t1-einvoicing-api-template

To install the required modules in a virtual environment, run: 
```bash
source env/bin/activate && pip3 install -r requirements.txt
```

To run the server, execute:
```bash
uvicorn src.server:app --reload
```

To run the tests, run the server then:
```bash
pytest
```
