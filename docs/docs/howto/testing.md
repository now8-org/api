# Testing

We use [`pytest`](https://docs.pytest.org/) to test our code.

You can run the current tests from the root directory of the repository
by executing:

```python
python -m pytest
```

## Testing scopes

There are two main testing scopes: unit testing and integration testing.

Unit testing is a testing method by which individual units of source
code are tested to determine if they are ready to use,
whereas integration testing checks integration between software modules.

Unit tests should be fast and not relay on other pieces of code or
external dependencies such as databases. Mock them if necessary.

## Test-driven development

We *try* to follow test-driven development (TDD) principles. The methodology
is as follows:

1. Write the unit and integration tests for the functionality to be
  implemented.
1. Run the tests and check that all of the new tests fail, to ensure that
  they are actually testing new features.
1. Implement a basic version of the required changes for the new tests
  to pass.
1. Check that all (old and new) tests pass.
1. Improve the implementation incrementally checking that all tests still
  pass.
