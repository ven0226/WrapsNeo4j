import requests
import json


HOST = "127.0.0.1"
PORT = 7474

base_url = 'http://%s:%d/db/data/' % (HOST, PORT)

class RestClient(object):

    def cypher_query(self, query, **kwargs):
        args = {'query': query}
        if kwargs:
            args["params"] = kwargs
        response = self.post_request('cypher', args)
        return response

    def __cypher_query_batch_request_body(self, qid, query, **kwargs):
        args = {'query': query}
        if kwargs:
            args["params"] = kwargs
        body = {
                'method': 'POST',
                'to': 'cypher',
                'body': args,
                'id': qid}
        return body
    
    def __post_batch_request(self, args):
        response = self.post_request('batch', args)
        return response

    
    def post_request(self, requestURL, requestArgs):
        headers = {'Content-Type': ['application/json']}
        url = base_url + requestURL
        data = json.dumps(requestArgs)
        response =  requests.post(url,data=data)
        response = json.loads(response.text)
        return response

    def addPerson(self, name, skills):
        batch = []
        query = "START n=node:node_auto_index(name={name})"\
                " WITH count(*) as exists"\
                " WHERE exists=0 "\
                " CREATE (e {name:{name}, type:'person'})"
        batch.append(self.__cypher_query_batch_request_body(0, query, name=name))
        i = 1
        for key in skills:
            query = "START n=node:node_auto_index(name={name})"\
                    " WITH count(*) as exists"\
                    " WHERE exists=0 "\
                    " CREATE (e {name:{name}, type:'skill'})"
            batch.append(self.__cypher_query_batch_request_body(i, query, name=key))
            i += 1
            query1 = "start d=node:node_auto_index(name={name}), e=node:node_auto_index(name={skill})"\
                     " CREATE UNIQUE d-[r:KNOWS]->e"
            batch.append(self.__cypher_query_batch_request_body(i, query1, name=name, skill=key))
            i += 1
        self.__post_batch_request(batch)

addp = RestClient()
addp.addPerson("Venky", ["Java","C++","SQL"])

