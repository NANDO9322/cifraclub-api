"""API Module"""

import os
from flask import Flask, json, request
from cifraclub import CifraClub

app = Flask(__name__)

ALLOWED_ORIGINS = {
    'https://entoa-app.vercel.app',
    'https://tom-neon-iota.vercel.app',
    'http://localhost:5173',
}

@app.after_request
def cors(response):
    """Allow only Entoa clients to call the browser API."""
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Vary'] = 'Origin'
    return response

@app.route('/')
def home():
    """Home route"""
    return app.response_class(
        response=json.dumps({'api': 'Cifra Club API'}),
        status=200,
        mimetype='application/json'
    )

@app.route('/artists/<artist>/songs/<song>')
def get_cifra(artist, song):
    """Get cifra by artist and song"""
    cifraclub = CifraClub()
    result = cifraclub.cifra(artist, song)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False),
        status=502 if result.get('error') else 200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', '3000'), debug=True)
