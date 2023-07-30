import json
import pandas as pd
from whoosh.index import create_in
from whoosh.fields import Schema, ID, TEXT
from whoosh.qparser import QueryParser
from flask import Flask, render_template, request
from fuzzywuzzy import fuzz

def search_index(query):
    # Read JSON data
    data = []
    desiredLines = 20000
    with open("data.json", 'r') as f:
        for line_num, line in enumerate(f, start = 1):
            if line_num > desiredLines:
                break
            data.append(json.loads(line))

    # Create DataFrame
    dict_ = {'id':[], 'submitter':[], 'abstract': [], 'authors': [], 'title': [], 'references': [], 'license': [], 'doi': []}
    for article in data:
        dict_['id'].append(article['id'])
        dict_['submitter'].append(article['submitter'])
        dict_['title'].append(article['title'])
        dict_['authors'].append(article['authors'])
        dict_['abstract'].append(article['abstract'])
        dict_['references'].append(article['journal-ref'])
        dict_['license'].append(article['license'])
        dict_['doi'].append(article['doi'])
    df = pd.DataFrame(dict_, columns=['id', 'submitter', 'title', 'authors', 'abstract', 'references', 'license', 'doi'])

    # Create Whoosh index
    schema = Schema(id=ID(stored=True), submitter=TEXT(stored=True), authors=TEXT(stored=True), abstract=TEXT(stored=True), title=TEXT(stored=True), references=TEXT(stored=True), doi=ID(stored=True), license=ID(stored=True))
    ix = create_in(".", schema)

    # Index documents
    writer = ix.writer(limitmb=2048)
    for _, row in df.iterrows():
        writer.add_document(
            id=str(row.get("id")),
            submitter=row.get("submitter"),
            authors=row.get("authors"),
            abstract=row.get("abstract"),
            title=row.get("title"),
            references=row.get("references"),
            license=row.get("license"),
            doi=str(row.get("doi"))
        )
    writer.commit()

    # Search the index
    with ix.searcher() as searcher:
        parser = QueryParser("abstract", ix.schema)
        myquery = parser.parse(query)
        search_results = searcher.search(myquery, limit = 5)

        fuzzy_results = []
        for res in search_results:
            title = res["title"]
            abstract = res["abstract"]
            similarity = fuzz.ratio(query, title)  # Adjust the fuzziness threshold as needed
            fuzzy_results.append({'title': title, 'abstract': abstract, 'similarity': similarity})
        
        # Sort the results by similarity score
        fuzzy_results = sorted(fuzzy_results, key=lambda x: x['similarity'], reverse=True)
        
        return fuzzy_results

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        search_results = search_index(query)
        return render_template('index.html', results=search_results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)