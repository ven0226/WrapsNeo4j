__author__ = 'Venkatesh'
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
        print url
        response =  requests.post(url,data=data)
        response = json.loads(response.text)
        return response

    def addPerson(self, name, skills,courses):
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

        i = 1
        for key in courses:
            query = "START n=node:node_auto_index(name={name})"\
                    " WITH count(*) as exists"\
                    " WHERE exists=0 "\
                    " CREATE (e {name:{name}, type:'course'})"
            batch.append(self.__cypher_query_batch_request_body(i, query, name=key))
            i += 1
            query1 = "start d=node:node_auto_index(name={name}), e=node:node_auto_index(name={course})"\
                     " CREATE UNIQUE d-[r:KNOWS]->e"
            batch.append(self.__cypher_query_batch_request_body(i, query1, name=name, course=key))
            i += 1
        self.__post_batch_request(batch)

    def getCount(self):
        query = "start n=node(*) match (n{type:'skill'})-[r]-() return n, count(r) as rel_count order by rel_count desc"
        response = self.cypher_query(query)
        return response['data']

    def getPeople(self,term):
        query = "start n=node(*) match (n{name:'"+term+"'})<-[r]-(x) return x.name"
        response = self.cypher_query(query)
        return response['data']

    def whoIsCool(self,me):
        query = "START n=node(*) MATCH ({name:'"+me+"'})-[r]->(x)<-[r2]-(n)"\
                " return n,count(x)AS num_rels,collect(x.name) order by num_rels desc"
        response = self.cypher_query(query)
        return response['data']


#addp = RestClient()
#print addp.whoIsCool("Venky")
