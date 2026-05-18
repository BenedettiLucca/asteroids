# Testing

To run the regression tests for this project, use the following command:

```bash
python3 -m unittest discover -s tests -v
```

## Test Coverage
- `tests/test_storage.py`: Verifies high-score persistence logic, including fallback for missing or corrupt files.
