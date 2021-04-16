import pymongo


def update_vacancies(data):
    connect = pymongo.MongoClient()
    vac = connect["job_seeking"]["vacancy"]
    for i in data:
        print('i', i)
        vac.update_one({'_id': i.pop('url')}, {'$set': i}, upsert=True)

