# lift-js
A JavaScript interpreter written in Python that supports primary features of ECMAScript 2015

[![Build Status](https://travis-ci.com/wolongyuan/lift-js.svg?token=HxUpDBskpjanfstuWrzX&branch=master)](https://travis-ci.com/wolongyuan/lift-js)

## Getting Started

### Set up virtualenv

```bash
virtualenv env
```

### Install requirements

```bash
source env/bin/activate
make install
```

### Compile js program
```bash
make run a.js
```

### Running the tests
```bash
make test
```

### Lint
```bash
make lint
```

### Clean
```bash
make clean
```

### Generate docs
```bash
make doc
```

### Clean generated docs
```bash
make doc-clean
```

### Deactivate virtualenv
```bash
deactivate
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/wolongyuan/spreadsheet/blob/master/LICENSE) file for details