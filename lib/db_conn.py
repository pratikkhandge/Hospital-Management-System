import pymongo


class MongoConn(object):
    """
    Description: Mongo database operations api
    """
    def __init__(self, collection=None):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.cursor = self.client.Apollo[collection]

    def read_document(self, data):
        """
        Description: Api to read document from database
        """
        result = self.cursor.find_one(data)
        if result:
            return result
        else:
            return None

    def insert_document(self, data):
        """
        Description: Api to insert document in database
        """
        try:
            self.cursor.insert(data)
        except Exception as e:
            print e

    def get_all_document(self):
        """

        :return:
        """
        try:
            result = self.cursor.find()
            return list(result)
        except Exception as e:
            print e

    def insert_with_unique_id(self, doc):
        """

        :return:
        """
        doc['PatientId'] = str(self.client.Apollo.Counter.find_and_modify(
            query={'collection': 'Counter'},
            update={'$inc': {'id': 1}},
            fields={'id': 1, '_id': 0},
            new=True
        ).get('id'))
        try:
            self.cursor.insert(doc)
        except pymongo.errors.DuplicateKeyError as e:
            self.insert_with_unique_id(doc)