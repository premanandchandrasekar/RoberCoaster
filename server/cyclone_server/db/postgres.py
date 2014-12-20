from twisted.internet import defer
import query
from datetime import datetime
import psycopg2



class PostgresDatabase(object):
    def __init__(self, connection, cache=None):
        self.connection = connection
        self.cache = cache

    def get_list_of_merchant(self):
        return self.connection.runQuery(
            query._GET_LIST_OF_MERCHANT).\
            addCallback(self._got_merchant_list)
            
    def _got_merchant_list(self, rows):
        l = []
        if rows:
            for row in rows:
                l.append({'id': row.id, 'merchant_name': row.name,
                         'merchant_sentiment' : row.sentiment, 'merchant_count' :row.count})
        return l
        
    def get_female_customer_for_merchant(self,id):
        return self.connection.runQuery(
            query._GET_FEMALE_CUSTOMER_FOR_MERCHANT, (id,)).\
            addCallback(lambda x : x[0])
            
    def get_male_customer_for_merchant(self,id):
        return self.connection.runQuery(
            query._GET_MALE_CUSTOMER_FOR_MERCHANT, (id,)).\
            addCallback(lambda x : x[0])            

    def get_merchant_product_list_by_merchant_id(self, merchant_id):
        return self.connection.runQuery(
            query._GET_COLLABORATIVE_FILTERING_BY_MERCHANT_ID, (merchant_id, merchant_id)).\
            addCallback(lambda x : [row[0] for row in x]).\
            addErrback(lambda x : False)

                
    

