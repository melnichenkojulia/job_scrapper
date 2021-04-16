import pymongo


def update_vacancies(data):
    connect = pymongo.MongoClient()
    vac = connect["job_seeking"]["vacancy"]
    for i in data:
        print('i', i)
        vac.update_one({'_id': i.pop('url')}, {'$set': i}, upsert=True)

def get_urls_parsing(client, date):
    urls = []
    for doc in client["job_seeking"]["vacancy"].find():
        if 'time_parsed' not in doc.keys() or doc['time_parsed'] < date:
            urls.append(doc['_id'])
    return urls