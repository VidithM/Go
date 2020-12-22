from flask import Flask, render_template, jsonify, request, redirect
import manifest
import sys
import _pickle as pickle

app = Flask(__name__)
INDEX_PATH = 'index.byte'


@app.route('/', methods = ['GET', 'POST']) 
def home():
    if(request.method == 'POST'):
        query = request.form['query']
        query = '+'.join(query.split(' '))
        return redirect('/search/' + query)

    return render_template('search.html')

@app.route('/search/<q>', methods = ['GET'])
def query(q):
    in_file = open(INDEX_PATH, 'rb')
    index = pickle.load(in_file)
    
    search_term = q.split('+')
    print(search_term, file=sys.stderr)
    
    ordered = []

    for manifest in index:      
        ordered.append((manifest.keywords, manifest.title, manifest.url, manifest.rank(search_term)))
    
    ordered.sort(key=lambda tup: tup[3], reverse=True)
    res = {}
    for i in range(20):
        print(ordered[i][0], ordered[i][3], file=sys.stderr)
        res[str(i)] = ({'title': ordered[i][1], 'url': ordered[i][2]})
    
    return render_template('results.html', results=res)
    
