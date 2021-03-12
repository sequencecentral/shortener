from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = datetime.now().strftime("%d%m%Y%H%M%S") #initialize at runtime
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
urls = []

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url'].lower()
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        elif 'http' not in url:
            ##add http if not in url
            url = 'https://'+url
        urls.append(url)
        hashid = hashids.encode(len(urls)-1)
        short_url = request.host_url + hashid
        return render_template('index.html', short_url=short_url)
    else:
        return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
    user_agent=request.user_agent
    #For IP logging:
    # user_IP=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        original_url = urls[original_id]
        print("SHORTCUT %s ACCESSED USING %s REDIRECTS TO %s" % (id,user_agent,original_url))
        # print('Redirecting to decoded id',original_url)
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')