# recipe-organizer
The Recipe Organizer is a tool for collecting and processing recipes from different sources (websites, books, magazines, ...) to easily search for recipes by specific ingredients and/or categories.
 
## Requirements
recipe-organizer is written in Python 3.7 and packages needed to run the code can be found in `requirements.txt`

## Architecture/Flow of data
![overview_data_processing](https://github.com/andrea-augustin/recipe-organizer/blob/main/architecture_data_handling.png)

## How to use recipe-organizer
### Website scrapers
To start one of the scrapers, grab one of the scrapers and execute `python grabbers/scraper_name.py`. 
All scrapers will save recipes into a single `.json` file named after the page on the main folder of the project. 
Each recipe in the `.json` file contains the following information:

```
name of the recipe
url of the recipe
servings
total prep time
a list categories like dietary or type of course (if available)
a list of ingredients
a list of instructions
```

If a page contains additional release information of a recipe (released in a magazine or book?), the recipe will be 
saved into a `.json` file named after the release information. 


### PDF scraper (currently work in progress)

PDF parsing will be started by executing `python pdf_parsing/pdf_recipe_extractor.py`. 
The user will be asked to select a `.pdf` file from their system.
The script will then parse the file and save all parsed recipes into a `.json` file with the same structure as the files in [website scrapers](README.md#website-scrapers).


###
