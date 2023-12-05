# json_relational: Transforming Nested JSON to Relational Format

`json_relational` is a small Python package for converting complex, nested JSON data into a flat, relational format. This transformation makes it significantly easier to work with JSON data in contexts where relational databases are more suitable, such as SQL databases. The package is designed to be dynamic and flexible, accommodating various levels of nested structures and converting them into a format that can be easily mapped to SQL tables.

## Features

- **Dynamic Nesting Handling**: Effortlessly manages various levels of nested JSON data.
- **SQL Table Ready**: Transforms JSON into a format that is easily convertible to SQL tables.
- **Customizable Depth Control**: Set the maximum depth for flattening nested structures.
- **Key Mapping Support**: Allows for the remapping of keys to desired names in the output.

## Installation

To install `json_relational`, clone the repository from GitHub and install it using pip:

```bash
git clone https://github.com/gr0vity-dev/json-relational.git
cd json_relational
pip install .
```

## Usage

Here's a simple example to demonstrate how `json_relational` can be used to transform nested JSON data into a relational format:

```python
from json_relational import JsonRelational
import json

# Example JSON data
json_data = {
    "type": "employee",
    "id": 123,
    "data": {
        "department": "sales",
        "manager": "Bob"
    }
}

# Create an instance of JsonRelational
jr = JsonRelational()

# Flatten the JSON data
flattened_data = jr.flatten_json(json_data)

print(json.dumps(flattened_data, indent=4))

```

### Output:

The output will be a dictionary containing flattened data, along with mappings and accumulated children, ready to be transformed into SQL tables.

```json
{
    "log": [
        {
            "sql_id": 1,
            "type": "employee",
            "id": 123
        }
    ],
    "data": [
        {
            "sql_id": 1,
            "department": "sales",
            "manager": "Bob"
        }
    ],
    "mappings": [
        {
            "main_type": "log",
            "main_sql_id": 1,
            "link_type": "data",
            "link_sql_id": 1
        }
    ]
}
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/gr0vity-dev/json-relational/issues).

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

`json_relational` offers an innovative solution for managing and transforming JSON data into a relational structure, making it an invaluable tool for database management, data analysis, and software development involving complex JSON data structures.
