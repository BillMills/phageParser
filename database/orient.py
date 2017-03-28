import pyorient, logging, datetime

a = str(datetime.date.today())
logging.basicConfig(filename=a+'.log',level=logging.WARNING, format='%(asctime)s %(message)s')

def connection():
    try:
        client = pyorient.OrientDB("192.168.56.8", 2424)
        client.db_open("phageParser", "root", "rootpwd")
        logging.info("Connection to database established.")
    except Exception as e:
        logging.error("Connection failed:", e)

    return client

def orient_command(command):
    client = pyorient.OrientDB("192.168.56.8", 2424)
    # client.set_session_token(True)  # set true to enable the token based authentication
    client.db_open("phageParser", "root", "rootpwd")

    logging.info("Connection to database established.")
    ### store this token somewhere
    # sessionToken = client.get_session_token()
    client.command(command)
    client.db_close()