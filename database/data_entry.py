import pyorient, logging, datetime, orient, rabbit_send

a = str(datetime.date.today())
logging.basicConfig(filename=a+'.log',level=logging.WARNING, format='%(asctime)s %(message)s')

def connection():
    try:
        client = pyorient.OrientDB("192.168.56.8", 2424)
        client.db_open("Euclid", "root", "rootpwd")
        logging.info("Connection to database established.")
    except Exception as e:
        logging.error("Connection failed:", e)

    return client

def DR_entry(file):
    lines = open(file, 'r').readlines()
    for line in lines:
        if '>' in line:
            list = []
            spacers = line[1:].split('|')
            for spacer in spacers:
                list.append(spacer.replace('\n', ''))
        else:
            for gen in list:
                dict = {'CRISPR': line.replace('\n', ''), 'spacer': gen}
                command = "insert into DR content %s" % (dict)
                rabbit_send.send(command)

def spacer_entry(file):
    lines = open(file,'r').readlines()
    for line in lines:
        if '>' in line:
            list = []
            spacers = line[1:].split('|')
            for spacer in spacers:
                list.append(spacer.replace('\n',''))
        else:
            for gen in list:
                a,b = gen.rsplit('_',1)
                dict = {'CRISPR': line.replace('\n',''),'spacer':a,'repeater':b}
                command = "insert into Spacer content %s" % (dict)
                rabbit_send.send(command)

def link_spacer():
    client = orient.connection()
    results = client.query("select distinct(spacer) from Spacer",-1)
    for result in results:
        a = result.distinct
        command = "create edge related_spacer from (select from DR where spacer = '%s') to (select from Spacer where spacer = '%s')" % (a,a)
        client.command(command)
    client.db_close()

def link_DR():
    client = orient.connection()
    results = client.query("select distinct(CRISPR) from DR",-1)
    for result in results:
        a = result.distinct
        command = "create edge related_CRISPR from (select from DR where CRISPR = '%s') to (select from Spacer where CRISPR = '%s')" % (a,a)
        client.command(command)
    client.db_close()

file = '../data/DRdatabase.txt'
DR_entry(file)

file = '../data/spacerdatabase.txt'
spacer_entry(file)

link_spacer()