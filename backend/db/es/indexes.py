INDEX_RUBRICS = "rubrics"
MAPPING_FOR_INDEX_PRODUCTS = {
    "properties": {
        "id": {
            "type": "integer",
        },
        "text": {"type": "text"},
    }
}

all_indexes = {INDEX_RUBRICS: MAPPING_FOR_INDEX_PRODUCTS}
