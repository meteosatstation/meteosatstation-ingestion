import os
import logging
import pymongo
import gridfs

# create logger
log = logging.getLogger(__name__)

# setup the database
try:
    # get mongodb connection string
    mongo_connection_string = os.environ.get('MONGODB_CONNECTION_STRING',
                                             'mongodb://root:password@localhost:27017/admin')
    mongo_client = pymongo.MongoClient(mongo_connection_string)

    # create clients for config db and files db
    mongo_database_string = os.environ.get('MONGODBO_DATABASE', 'meteosatstation')
    mongo_database = mongo_client[mongo_database_string]

    # get collections
    mongo_collection_config = mongo_database['config']
    mongo_gridfs_client = gridfs.GridFS(mongo_database, 'ingest_files')

except Exception as e:
    log.fatal('Unable to connect to database: %s', str(e))


def get_config():
    log.info("Fetching configuration from database")

    # get the instance id from environment variables
    instance_id = os.environ.get('INGESTION_INSTANCE_ID', 0)

    try:
        config = mongo_collection_config.find_one(
            {
                'component': 'ingestion',
                'instance_id': instance_id
            }
        )

        return config
    except Exception as e:
        log.fatal('Unable to get configuration from database: %s', str(e))

    return {}


def load_file(file, config):
    log.info("Loading file %s into database", file)

    try:
        base_name = os.path.basename(file)

        # check if the file is already there
        if not mongo_gridfs_client.exists(filename=base_name):
            file_handle = open(file, "rb")

            mongo_gridfs_client.put(
                file_handle,
                filename=base_name,
                create_time=os.path.getctime(file)
            )

            file_handle.close()
        else:
            log.info("File %s already exists in database, not uploading", file)

    except Exception as e:
        log.error("Unable to load file %s into database: %s", file, str(e))
        raise Exception(e)
