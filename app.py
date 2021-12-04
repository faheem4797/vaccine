# doing necessary imports
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import os
import cv2
import werkzeug


app = Flask(__name__)  # initialising the flask app with the name 'app'


@app.route('/upload', methods=['POST'])
def upload():
    if(request.method == "POST"):
        data = request.data
        type = data['type']
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("/uploadedimages/" + filename)
        a = imageProcess(type, filename)
        return jsonify({
            "message": a
        })


def imageProcess(type, filename):

    smallPortionsCertificate = ['assets/new1.jpg', 'assets/new2.jpg',
                                'assets/new3.jpg', 'assets/new4.jpg', 'assets/new5.jpg']

    smallPortionsCard = ['assets/card1.jpg', 'assets/card2.jpg',
                         'assets/card3.jpg', 'assets/card4.jpg', 'assets/card5.jpg']

# Start Here. Add an if-else for card or certificate. Change the lower checks to see if all 5 are correct
    if (type == 'Certificate'):
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
                count = 0

                if max_val >= threshold:
                    bottom_right = (location[0] + w, location[1] + h)
                    if((j == 'assets/new1.jpg' and location == (0, 0) and bottom_right == (941, 238)) or (j == 'assets/new2.jpg' and location == (0, 0) and bottom_right == (164, 490)) or (j == 'assets/new3.jpg' and location == (0, 369) and bottom_right == (1227, 486)) or (j == 'assets/new4.jpg' and location == (917, 198) and bottom_right == (1227, 510)) or (j == 'assets/new5.jpg' and location == (0, 676) and bottom_right == (1227, 869))):
                        print('Match found. Count incremented')
                        count = count + 1
                        # Change to 2 different if else for card and certificate elahda elahda
                        # else:
                        #   break
                    else:
                        count = count - 1
                        print('Match not found. Count deprecated')
                if (count == 5):
                    return 'Yes'
                    print('Send http response that image matches')
                else:
                    return 'No'
                    print('Send http response that image doesnt matche')
            except:
                return 'error'
                print('error bhai')

    elif (type == 'Card'):
        print('')
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
                count = 0

                if max_val >= threshold:
                    bottom_right = (location[0] + w, location[1] + h)
                    if((j == 'assets/card1.jpg' and location == (26, 13) and bottom_right == (783, 173)) or (j == 'assets/card2.jpg' and location == (422, 416) and bottom_right == (906, 790)) or (j == 'assets/card3.jpg' and location == (455, 339) and bottom_right == (788, 788)) or (j == 'assets/card4.jpg' and location == (18, 554) and bottom_right == (902, 788)) or (j == 'assets/card5.jpg' and location == (689, 635) and bottom_right == (903, 930))):

                        print('Match found. Count incremented')
                        count = count + 1
                        # Change to 2 different if else for card and certificate elahda elahda
                        # else:
                        #   break
                    else:
                        count = count - 1
                        print('Match not found. Count deprecated')

                if (count == 5):
                    return 'Yes'
                    print('Send http response that image matches')
                else:
                    return 'No'
                    print('Send http response that image doesnt matche')

            except:
                return 'error'
                print('error bhai')

                
                
    else:
        return 'heavy error'

if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
'''if __name__ == "__main__":
    # running the app on the local machine on port 8000
    app.run(port=5000, debug=True)'''
