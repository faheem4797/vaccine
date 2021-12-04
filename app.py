# doing necessary imports
from logging import error
from flask import Flask, render_template, request, jsonify, make_response, json
from werkzeug.datastructures import ImmutableMultiDict
from flask_cors import CORS, cross_origin
import os
import cv2
import werkzeug


app = Flask(__name__)  # initialising the flask app with the name 'app'


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    data = dict(request.form)
    type = data['type']
    imagefile = request.files['image']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    imagefile.save("./uploadedimages/" + filename)
    res = imageProcess(type, filename)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def imageProcess(type, filename):

    smallPortionsCertificate = ['assets/new1.jpg', 'assets/new2.jpg',
                                'assets/new3.jpg', 'assets/new4.jpg', 'assets/new5.jpg']

    smallPortionsCard = ['assets/card1.jpg', 'assets/card2.jpg',
                         'assets/card3.jpg', 'assets/card4.jpg', 'assets/card5.jpg']

    if (type == 'Certificate'):
        count = 0

        for j in smallPortionsCertificate:
            img = cv2.imread("uploadedimages/" + filename, 0)
            template = cv2.imread(j, 0)
            h, w = template.shape
            method = cv2.TM_CCORR_NORMED
            try:
                img2 = img.copy()
                result = cv2.matchTemplate(img2, template, method)

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                location = max_loc  # Top left of rectangle
                threshold = 0.9

                if max_val >= threshold:
                    bottom_right = (location[0] + w, location[1] + h)
                    if((j == 'assets/new1.jpg' and location == (0, 0) and bottom_right == (941, 238)) or (j == 'assets/new2.jpg' and location == (0, 0) and bottom_right == (164, 490)) or (j == 'assets/new3.jpg' and location == (0, 369) and bottom_right == (1227, 486)) or (j == 'assets/new4.jpg' and location == (917, 198) and bottom_right == (1227, 510)) or (j == 'assets/new5.jpg' and location == (0, 676) and bottom_right == (1227, 869))):
                        print('Match found. Count incremented')
                        count = count + 1
                        print(count)
                    else:

                        print('Match not found')

            except:
                return 'error'
        if (count == 5):
            return 'Yes'
        else:
            return 'No'

    elif (type == 'Card'):
        count = 0
        for j in smallPortionsCard:
            img = cv2.imread("uploadedimages/" + filename, 0)
            template = cv2.imread(j, 0)
            h, w = template.shape
            method = cv2.TM_CCORR_NORMED
            try:
                img2 = img.copy()
                result = cv2.matchTemplate(img2, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                location = max_loc  # Top left of rectangle
                threshold = 0.9

                if max_val >= threshold:
                    bottom_right = (location[0] + w, location[1] + h)
                    if((j == 'assets/card1.jpg' and location == (26, 13) and bottom_right == (783, 173)) or (j == 'assets/card2.jpg' and location == (422, 416) and bottom_right == (906, 790)) or (j == 'assets/card3.jpg' and location == (455, 339) and bottom_right == (788, 788)) or (j == 'assets/card4.jpg' and location == (18, 554) and bottom_right == (902, 788)) or (j == 'assets/card5.jpg' and location == (689, 635) and bottom_right == (903, 930))):

                        print('Match found. Count incremented')
                        count = count + 1
                    else:

                        print('Match not found')

            except:
                return 'error'
        if (count == 5):
            count = 0
            return 'Yes'
        else:
            count = 0
            return 'No'


if __name__ == '__main__':
    
    print("Starting app on port %d" % port)
    app.run(debug=False, port=8000, host='0.0.0.0')
'''if __name__ == "__main__":
    # running the app on the local machine on port 5000
    app.run(port=5000, debug=True)'''
