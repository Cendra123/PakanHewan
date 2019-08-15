import os

from flask import Flask
from flask import render_template
from . import SLIQ as sl
# from . import Sliq_Debug as sl
from pprint import pprint
import random
# from . import SLIQ


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        # tree =0
        # train =0
        # test =0
        # tree, train, test = SLIQ.train('data_exercise_2.csv', 2.0/3, 1)

        # with open('DATASET.csv') as f:
        with open('data_exercise_2.csv') as f:
            file = f.read()

        attr, trainData, testData = sl.datasets(file, 5/6)

        print("-----------attr-----------")
        pprint(attr)

        print("-----------trainData-----------")
        pprint(trainData)

        attrList, classList = sl.presort(attr, trainData)

        # middlestep = 0

        print("-----------Attr-----------")
        pprint(attr)

        print("-----------AttrList-----------")
        pprint(attrList)

        print("-----------ClassList-----------")
        pprint(classList)

        tree = sl.generate_tree(attr, attrList, classList)  # middlestep)
        print("-----------Fix Tree-----------")
        pprint(tree)

        testPerTra = sl.test_tree(tree, trainData)
        testPerTes = sl.test_tree(tree, testData)

        print("-----------TEST TRAIN-----------")
        print(testPerTra)

        print("-----------TEST TEST-----------")
        print(testPerTes)

        # return "backed"
        return render_template('base.html',tree = tree, testPerTes = testPerTes, testPerTra = testPerTra)

    @app.route('/dashboard')
    def dashboard():
        return "dashboard"

    @app.route('/js')
    def js():
        return render_template('JS.html')

    return app