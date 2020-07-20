# FigShare

## First attempt

There are VU datasets in Figshare, but how do you search by affiliation?

- https://knowledge.figshare.com/articles/item/how-to-use-advanced-search-in-figshare- 
- https://figshare.com/search?q=VU%20AND%20amsterdam&searchMode=1&types=3
- https://figshare.com/search?q=Vrije%20AND%20amsterdam&searchMode=1&types=3

## Second attempt

### Using the logged in user website "search function"

Figshare has no insitution/affiliation field in it's metadata so you have to rely on what people put in the "desciption"! There is also no access to the users email from the the public search interface.

The public web based search is extremely limited and by default returns results from resources FigShare has scraped off the web, Mendalay, Zenodeo, etc. so the search must be limited to.

- source: figshare.com

The search function also defaults to a substring search (looking for individual words in a phrase) unless quoted and typed using the :: descriptors. In addition the search could be limited to:

- type: dataset 

Although I have not done that with following search term that gives 26 results (down from seventeen thousand if you search for VU University Amsterdam)

`(:description: "VU" OR :description: "Vrije") AND :description: "Amsterdam"`

Not particularly impressive.

