# FastAPI Project

## Description
This is a FastAPI project that provides a RESTful API service.

## Installation
```bash
pip install fastapi
pip install uvicorn
```

## Usage
To run the server:
```bash
uvicorn main:app --reload
```

## Code Examples
```python
# Basic GET endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Path parameter example
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Query parameter example
@app.get("/query/")
def read_query(name: str, age: int = None):
    return {"name": name, "age": age}
```

## Features
- Fast performance
- Automatic API documentation
- Data validation
- Easy to use

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn

## License
MIT License

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author
Aaman Lamba

## Based on
[Fast API Tutorial](https://fastapi.tiangolo.com/tutorial/)