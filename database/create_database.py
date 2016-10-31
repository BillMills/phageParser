import pyorient, logging, datetime

a = str(datetime.date.today())
logging.basicConfig(filename=a+'.log',level=logging.WARNING, format='%(asctime)s %(message)s')

def create_database(database):
    try:
        client = pyorient.OrientDB("192.168.56.8", 2424)
        client.connect("root", "rootpwd")
        if not client.db_exists(database, pyorient.STORAGE_TYPE_MEMORY ):
            client.db_create(database, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)
            logging.info(database,"created")
            client.db_open(database, "root", "rootpwd")
            client.command("create class DR extends V")
            client.command("create class Spacer extends V")
            client.command("create class related_Spacer extends E")
            client.command("create class related_CRISPR extends E")
        else:
            logging.info(database,"already exists")
    except Exception as e:
        logging.error("Connection failed:", e)

create_database('phageParser')