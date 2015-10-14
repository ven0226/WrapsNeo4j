__author__ = 'Venkatesh'

from flask import Flask
from flask import request
from flask import render_template
import requests
import json
import learning2
app = Flask(__name__)

@app.route('/populateDB', methods=['POST'])
def parseJSON():
    try:
        #url = "http://152.23.71.153/link?url=https://www.linkedin.com/in/gautamjeyaraman"
        #url = urlName
        #print 'hello'
        urlName = request.form['urlName']
        urlFinal = "http://152.23.71.153:4567/link?url="+urlName
        print urlFinal
        resp = requests.get(url=urlFinal)

        parsed_json = json.loads(resp.text)
        #print parsed_json
        #for obj in parsed_json:
        #print parsed_json["name"]
        #print parsed_json['skills']
        #print parsed_json['courses']
        restClient = learning2.RestClient()
        restClient.addPerson(parsed_json["name"],parsed_json['skills'],parsed_json['courses'])
        return 'You are registered successfully. Thanks you!'
            #render_template('<html><body><h3>Your registered successfully. Thanks you!</h3></body></html>')
    except Exception as e:
        return 'You are registered successfully. Thanks you!'

def fetchData():
    restClient = learning2.RestClient()
    responseData = restClient.getCount()
    output = {}
    value = []

    innerDict = {}
    innerDict['skillList'] = {}
    #print responseData
    #for resp in responseData:
        #print resp
     #   print resp[0]['data']['name']
      #  print resp[1]
    #output['dashboard'] = value

def fetchData2():
    restClient = learning2.RestClient()
    responseData = restClient.whoIsCool('Venky')
    #output = {}
    #value = []

    #innerDict = {}
    #innerDict['skillList'] = {}
    #print responseData
    #for resp in responseData:
     #   print resp
      #  print resp[0]['data']['name']
      #  print resp[1]
       # print resp[2]
    #output['dashboard'] = value

if __name__ == '__main__':
    app.run(host='0.0.0.0')

fetchData2()