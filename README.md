# Job Scrapper

This repo contains all the code developed to scrape jobs at well known websites such as [Indeed](https://www.indeed.com/) and [LinkedIn](https://linkedin.com/) using [Selenium](https://www.selenium.dev/). At the current stage, only the Indeed bot was implemented.

## Installation
In order to run this project you'll need to have ```Python >= 3.10``` installed.
To install the required packages, please run the bash script bellow and make sure that you are in the project directory. All the necessary modules will be downloaded using [pip](https://pip.pypa.io/en/stable/) package manager.
```bash
pip install -r requirements.txt
```

## Usage

To  run this project simply run the following bash command after you set all the [search parameters](#search-parameters) that you desire.

```bash
python3 main.py
```
### Search parameters
In order to update the search parameters please navigate to the ```config.py``` file. All the variables will be described in the tables bellow.

#### Bot parameters
| Key         | Possible values|
| :------------------:|---------------|
| ```Indeed``` | ```True``` in order to run the Indeed bot or ```False``` otherwise.
| ```LinkedIn``` | ```True``` in order to run the LinkedIn bot or ```False``` otherwise. 

#### Search parameters
| Key         | Possible values|
| :------------------:|---------------|
| ```KEYWORDS``` |  Insert a ```str``` that describes the job that you want to search.
| ```LOCATION``` | Insert a ```str``` containing the disered job location.

*Note:* Once you run the ```main.py``` file you will be prompted if you want to set additional filters and parameters for Indeed.com . This was required since there are different filters depending on your location.

#### Additional Parameters
| Key         | Possible values|
| :------------------:|---------------|
| ```OUTPUT_FILE_NAME``` | ```str``` containing the desired output file name.
| ```COUNTRY``` |```"PT"```, ```"ES"```, ```"DE"```, ```"USA"``` or ```"UK"```. This value is dependent on your location. If your country is not an option feel free to add the respective key and value in the ```options.py``` file.
| ```FILTER_COMPANIES``` | ```list``` object that contains all the non-desired companies to be filtered.
| ```COMPANY_SIMILARITY_THRESHOLD``` | ```int``` value between ```0``` and ```100```. In order to filter the unwanted companies, fuzzy logic was implemented. This value defines the ratio required between the Websites' scraped company name and the name inserted by yourself. The default value is ```85```.

