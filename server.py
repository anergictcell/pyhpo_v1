import argparse

from flask import Flask
from flask import request, redirect, Response, make_response
from flask import jsonify

from werkzeug.urls import url_encode

from pyhpo.ontology import Ontology
from pyhpo.set import HPOSet, BasicHPOSet
from pyhpo.annotations import Gene, Omim


SECRET_KEY = 'abcc'


def auth():
    if request.path == '/login':
        return None
    if request.cookies.get('sonosuser') == SECRET_KEY:
        return None
    return redirect('/login')


app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='static'
)


@app.route('/login', methods=['GET', 'POST'])
def login():
    res = redirect('/')
    res.set_cookie(
        'sonosuser',
        SECRET_KEY,
        max_age=60*60*24*365)
    return res


@app.route('/term/<int:term_index>', methods=['GET'])
def get_term_by_index(term_index):
    res = Ontology[term_index]
    if res:
        return jsonify(res.toJSON(verbose=True))
    else:
        return 'Invalid HPO-Term', 404


@app.route('/term/<string:term_index>', methods=['GET'])
def get_term_by_name(term_index):
    res = Ontology.get_hpo_object(term_index)
    if res:
        return jsonify(res.toJSON(verbose=True))
    else:
        return 'Invalid HPO-Term', 404


@app.route('/set/<string>/<action>', methods=['GET'])
def work_with_set(string, action):
    s = HPOSet.from_serialized(string)
    if action == 'ic':
        return jsonify({'ic': s.information_content()})
    if action == 'variance':
        return jsonify({'variance': s.variance()})
    if action == 'terms':
        return jsonify({'terms': s.toJSON()})

    return 'Invalid Action', 404


@app.route('/set/<set1>/similarity/<set2>', methods=['GET'])
def set_similarity(set1, set2):
    s1 = HPOSet.from_serialized(set1)
    s2 = HPOSet.from_serialized(set2)
    return jsonify({'similarity': s1.similarity(s2)})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run PyHPO as daemon HTTP server')
    parser.add_argument('-p', '--port', type=int, default=8080)
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--auth', action='store_true')
    args = parser.parse_args()

    if args.auth:
        app.before_request(auth)

    print('Loading Ontology')
    Ontology()
    app.run(host=args.host, port=args.port, debug=True)
