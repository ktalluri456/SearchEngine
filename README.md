# SearchEngine

This search engine functions as a Jupyter Notebook-based user-input search engine. It makes use of various APIs and data analysis to achieve the final result. 

## Tools used

The programming language used is Python. The API used for the structure and functionality is Whoosh. Also processed an entire JSON file that is not part of the code here that contains 3 GB of data I processed. 

## To import 

```zsh
pip install Whoosh
pip install Pandas
pip install Flask
```

## Usage

Type into the query string the item that you want to use. Make sure the unicode is still active so that the Whoosh searcher can process your input. You will need to find a CSV file that this program can read accurately. You may also modify the parameters to fit your needs. Using an HTML file, we render the application onto a web interface that will sort the results into a top 5 format.  

