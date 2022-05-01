# seedfinder-python

Simple Python wrapper and CLI for [seedfinder.eu](https://en.seedfinder.eu/)'s API.

## Install

`pip install seedfinder`


## Setup

You will need to [create an account](https://en.seedfinder.eu/register.html) at seedfinder.eu and [verify a domain or IP](https://en.seedfinder.eu/userarea/action/jsonapi.html) in order to access the API.

To authorize requests, you need to either make a request from a verfied address or initialize the SeedFinder object with your API token.

Note: seedfinder.eu requires that you register an address *even if you are only accessing the API by token*.

## Usage & Documentation

seedfinder-python is usable as both a simple search CLI

```bash
seedfinder --limit 10 --not-interactive "granddaddy"
```

and as a library

```python
from seedfinder import SeedFinder

sf = SeedFinder('YOUR API KEY')
sf.searchStrain('Alien Kush', exact=True)
```

See [documentation](https://seedfinder-python.readthedocs.io/en/latest/) for usage details.

## API Reference

See seedfinder.eu's [API documentation](https://en.seedfinder.eu/api/json)
