
# Install dependencies, preferably in a virtualenv:
#
#     pip install flask matplotlib
#
# Run the development server:
#
#     python app.py
#
# Go to http://localhost:5000/plot.png and see a plot of random data.

import random
from sklearn.externals import joblib
from flask import Flask, make_response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pickle
import matplotlib.pyplot as plt

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


app = Flask(__name__, static_url_path='/static/')

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/plot.png',  methods = ['POST', 'GET'])
def plot():
    #fig = Figure()
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/showstats',  methods = ['POST', 'GET'])
def showstats():
    # get the parameters, family and tag are int type
    family = int(request.form['family'])  
    tag = int(request.form['tag'])  
    keyword = str(request.form['keyword'])
    tag_choices = ["","Microsoft","Turbotax"]

    if not keyword:
        keyword = tag_choices[tag]    

    tagged_review_file = open('../project/taggedDigitSoftwareReviews', "rb")
    tagged_reviews = pickle.load(tagged_review_file)
    tagged_review_file.close()

    user_key_words = keyword   # e.g., Turbotax
    user_key_words = user_key_words.lower()
    target = tagged_reviews[tagged_reviews.tags.str.match(user_key_words)]
    all_negative_reviews = tagged_reviews[tagged_reviews.sentiment == 'Negative']
    all_positive_reviews = tagged_reviews[tagged_reviews.sentiment == 'Positive']
    target_negative_reviews = target[target.sentiment == 'Negative']
    target_positive_reviews = target[target.sentiment == 'Positive']

    date_sorted_tagged_reviews=tagged_reviews.sort_values(by='review_date')
    date_sorted_target_reviews=target.sort_values(by='review_date')

    t=date_sorted_tagged_reviews.groupby('review_date').mean()
    t_target = date_sorted_target_reviews.groupby('review_date').mean()
    l1=list(t.length)
    l2=list(t.index)
    l3=list(t.star_rating)
    l1_target=list(t_target.length)
    l2_target=list(t_target.index)
    l3_target=list(t_target.star_rating)

    fig = plt.figure(figsize=(20,10))
    axis1 = fig.add_subplot(2, 1, 1)
    axis1.scatter(target['length'],target['star_rating'])

    axis2 = fig.add_subplot(2, 1, 2)
    axis2.scatter(l2_target, l3_target)
   
    canvas = FigureCanvas(fig)
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response




if __name__ == '__main__':
    app.run(debug=True)