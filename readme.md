# SeedFinder

Simple Python wrapper for [seedfinder.eu](https://en.seedfinder.eu/)'s API.

## Setup

You will need to [create an account](https://en.seedfinder.eu/register.html) at seedfinder.eu and [verify a domain or IP](https://en.seedfinder.eu/userarea/action/jsonapi.html) in order to access the API.

To authorize requests, you need to either make a request from a verfied address or initialize the SeedFinder object with your API token.

Note: seedfinder.eu requires registering an address *even if you are only accessing the API by token*.

[seedfinder.eu's API documentation](https://en.seedfinder.eu/api/json)

## Usage

Initialize the API object

```python
from seedfinder import SeedFinder

sf = SeedFinder('YOUR API KEY')
```

Search for a strain

```python
sf.searchStrain('fuel')
```

Exact search for a strain

```python
sf.searchStrain('Alien Kush', exact=True)
```

Get detailed strain information from the first search result

```python
search_results = sf.searchStrain('purp')
first_result = [v for k,v in search_results['strains'].items()][0]
sf.strainInfo(first_result['id'], first_result['brid'])
```

Get three generations of parent strains

```python
sf.parents(strain_id='Girl_Scout_Cookies', breeder_id='Clone_Only_Strains', generations=3)
```

Get direct (first generation) hybrids

```python
sf.hybrids(strain_id='Puta_Breath',breeder_id='ThugPug_Genetics')
```

List all of a breeder's strains

```python
sf.breederInfo('Exotic_Genetix')
```
