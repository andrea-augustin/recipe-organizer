# recipe-organizer
Einleitung: Was ist das Ziel vom Tool bzw. warum gibt es das?

## Requirements
recipe-organizer is written in Python 3.7 and packages needed to run the code can be found in `requirements.txt`

## Architecture/Flow of data


## How to use recipe-organizer
### Website scrapers
To start one of the scrapers, grab one of the scrapers and execute `python grabbers/scraper_name.py`. 
All scrapers will save recipes into a single `.txt` file named after the page on the main folder of the project. T
he structure of each `.txt` file is the following:

```
Titel (name of the recipe)
URL (link to the original recipe)
Portionen (servings)
Dauer (prep time)
Kategorien (categories like dietary or type of course)
Zutaten (a list of ingredients; each ingredient is one line)
Zubereitung (instructions; each step is one line)
```

If a page contains additional release information of a recipe (released in a magazine or book?), the recipe will be 
saved into a `.txt` file named after the release information. 


### PDF scraper (currently work in progress)

PDF parsing will be started by executing `python pdf_parsing/pdf_recipe_extractor.py`. 
The user will be asked to select a `.pdf` file from their system.
The script will then parse the file and save all parsed recipes into a `.txt` file with the same structure as the files in website scrapers.