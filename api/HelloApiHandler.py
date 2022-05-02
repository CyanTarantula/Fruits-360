from flask_restful import Api, Resource, reqparse
import werkzeug
import os

class HelloApiHandler(Resource):
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Base_Message"
        }

    def post(self):
        print("Self:", self)
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('message', type=str)
        # parser.add_argument('file', type=object)

        parser.add_argument('img_file', type=object)
        # parser.add_argument('img_file', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()

        print("Args:", args)
        print("File:", args['img_file'])
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')
        
        if (args['img_file'] != None):
            print("Yayy!")
            image_file = args['img_file']
            image_file.save("uploads/imageToPredict.jpg")

        request_type = args['type']
        request_json = args['message']
        # # ret_status, ret_msg = ReturnData(request_type, request_json)
        # # currently just returning the req straight
        ret_status = request_type
        ret_msg = request_json

        if ret_msg:
            message = "Your Message Requested: {}".format(ret_msg)
        else:
            message = "No Msg"
        
        final_ret = {"status": "Success", "message": message}

        return final_ret
