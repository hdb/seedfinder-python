# Example Usage

seedfinder-python can be used as a library or CLI

## CLI

```bash
# first set your API key using the SF_API_KEY environment variable
export SF_API_KEY=YOUR_API_KEY

seedfinder --limit 10 --not-interactive "granddaddy"
```

## Library Usage

Initialize the API object

```python
from seedfinder import SeedFinder

sf = SeedFinder('YOUR API KEY')
```

Search for strains

```python
sf.searchStrain('fuel')
```

Search for a strain using exact query

```python
sf.searchStrain('Alien Kush', exact=True)
```

Search by word and get detailed strain information from the first result

```python
search_results = sf.searchStrain('purp')
first_result = [v for k,v in search_results['strains'].items()][0]
sf.strainInfo(first_result['id'], first_result['brid'])
```

Get three generations of parent strains

```python
sf.parents('Girl_Scout_Cookies', breeder_id='Clone_Only_Strains', generations=3)
```

Get direct (first generation) hybrids

```python
sf.hybrids('Puta_Breath', breeder_id='ThugPug_Genetics')
```

List all of a breeder's strains

```python
sf.breederInfo('Exotic_Genetix')
```
