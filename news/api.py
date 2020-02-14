from flask import Flask, make_response
from flask_restful import reqparse, abort, Api, Resource
import json
from gnewsclient_in import MyNewsClient
from pprint import pprint


app = Flask(__name__)
api = Api(app)

#parser = reqparse.RequestParser()
#parser.add_argument('task')

class GoogleNews(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic', required=False, type=str)
        parser.add_argument('count', required=False, type=int)
        args = parser.parse_args()
        
        topic = args['topic'] is None and 'Top Stories' or args['topic']
        count = args['count'] is None and 5 or args['count']
        
        #client = MyNewsClient(language='korean', location='Republic of Korea', topic='Top Stories', max_results=5)
        client = MyNewsClient(language='korean', location='Republic of Korea', topic=topic, use_opengraph=True, max_results=count)
        resp = make_response(json.dumps(client.get_news(), ensure_ascii=False, indent=4))
        #sqlService = mySqlService()
        #resp = make_response(json.dumps(sqlService.selectAllToJson(), ensure_ascii=False, indent=4))
        return resp

    
api.add_resource(GoogleNews, '/googlenews')

if __name__ == '__main__':
    app.run(debug=True)
