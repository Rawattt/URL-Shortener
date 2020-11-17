from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import os
import json
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

developement = True


@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def yourUrl():
    if request.method == 'POST':
        urls = {}

        # Check if the the urls.json exists
        if os.path.exists('urls.json'):
            with open('urls.json', 'r') as open_file:
                urls = json.load(open_file)

        # Check if the "code" is already in use
        if request.form['code'] in urls.keys():
            flash("This short name is already taken. Please try another name")
            return redirect(url_for('urlshort.home'))

        # Check if the request is to shorten a url or a file
        # For a url
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}

        # For a file
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            base_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base_dir, 'static', 'user_files', full_name)
            f.save(path)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirectToURL(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))

    return abort(404)


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@bp.route('/about')
def about():
    return "this is a url shortener"


# if __name__ == "__main__":
#     if developement:
#         bp.run(debug=True)
#     else:
#         bp.run()
