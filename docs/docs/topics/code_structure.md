# Code structure

The main package is contained in the `now8_api/` directory. The structure is as
follows:

```
  +------------+  +-----------+
  | db backend |  | City APIs |
  +------------+  +-----------+
        |                |
+-------|----------------|---+
|       |                |   |
|  +------+  +--------+  |   |
|  | data |  | domain |  |   |
|  +------+  +--------+  |   |
|   |   |        |       |   |
|   |  +-------------------+ |
|   |  |     service       | |
|   |  +-------------------+ |
|   |        |               |
| +-------------+            |
| | entrypoints |            |
| +-------------+            |
|       |                    |
+-------|--------------------+
        |
   +----------+
   | frontend |
   +----------+

```

Each component should only connect with its connected ones. Each component
contains a `__init__.py` file that stores the functions shared in the
component, for example a `hello_world()` function shared among different
entrypoints (API, CLI, …). Apart from this components, there is the
`__init__.py` file of the `now8_api` package.

## Components

### Data

This component is responsible for abstracting the data persistence.

#### Database

Abstraction of the local database.

### Domain

`domain` contains the business actors and logic. It has no dependencies,
so that it can be tested alone and the code is as simple and clear as
possible.

### Service

This component obtains data from the `data` or from the City APIs
and interacts
with `doamin` to validate it and process it
when called by the `entrypoints` component.

Having this layer decouples the `domain` from the `data` and the
`entrypoints`, which facilitates testing and implementing new functionality.

#### City Data

Abstraction of city transport APIs and other city data sources.


### Entrypoints

This component provides access to the `now8_api` package functionality. The main
entrypoint is a HTTP REST API but other entrypoints, such as CLIs, should be
placed here.
