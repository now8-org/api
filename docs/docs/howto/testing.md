# Testing

We use [`pytest`](https://docs.pytest.org/) to test our code.

You can run the current tests from the root directory of the repository
by executing:

```python
python -m pytest
```

## Testing scopes

We use three testing scopes: unit, integration and
end-to-end (e2e).

Unit testing is a testing method by which individual units of source
code are tested to determine if they are ready to use,
whereas integration testing checks integration between software modules
at the boundaries. Lastly, e2e tetsing checks the system as a whole
assessing that the functionality expected by the user works as expected
and that there are no system errors.

Unit tests should be fast and not relay on unnecessary pieces of code or
external dependencies such as databases.

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

One of this cycles might have subcycles. For example, if you want to
add a new high level function for which you write an end-to-end (E2E)
test, start writing a test for that function and use small cycles of
TDD for the helper functions or dependencies in lower level layers that
the new function requires.
