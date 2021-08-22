# Code structure

The main module is contained in the `ntapi/` directory. The structure is as
follows:

```
ntapi
├── data
│   ├── __init__.py
│   ├── cities
│   │   ├── __init__.py
│   │   └── ...
│   ├── database
│   │   ├── __init__.py
│   │   └── ...
│   └── ...
├── entrypoints
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── ...
│   └── ...
├── logic
│   ├── __init__.py
│   └── ...
└── __init__.py
```

As you can see, there are three main directories: `data`, `entrypoints` and
`logic`. They are connected between them as follows:

```
 +---------------+
 | external deps |
 +---------------+
        |
+-------|---------+
|       |         |
|  +----------+   |
|  |   data   |   |
|  +----------+   |
|       |         |
| +------------+  |
| |   logic    |  |
| +------------+  |
|       |         |
| +-------------+ |
| | entrypoints | |
| +-------------+ |
|       |         |
+-------|---------+
        |
   +----------+
   | frontend |
   +----------+

```

Each component should only connect with its contiguous ones. Each component
contains a `__init__.py` file that stores the functions shared in the
component, for example a `hello_world()` function shared among different
entrypoints (API, CLI, …). Apart from this components, there is the
`__init__.py` file of the `ntapi` module.

## Components

### Data

This component is responsible for accessing the external dependencies
providing methods for the logic component that abstract the queries to
the database, external APIs and other data sources.

#### Cities

Abstraction of city transport APIs and other city data sources.

#### Database

Abstraction of the local database.

### Logic

This component obtains data from the `data` component and process them
when called by the `entrypoints` component.

### Entrypoints

This component provides access to the `ntapi` package functionality. The main
entrypoint is a HTTP REST API but other entrypoints, such as CLIs, should be
placed here.
