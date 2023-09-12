from collector import Redfin
import asyncio
from dataProcess import *
def setup():
    client = Redfin()
    semaphore = asyncio.Semaphore(250)
    valid_conn  = sqlite3.connect("validAddress.db")
    invalid_conn = sqlite3.connect("invalidAddress.db")
    setup_db(valid_conn, "validAddress")
    setup_db(invalid_conn, "invalidAddress")
    filepath= ""
    asyncio.run(process_geojson_data(filepath,valid_conn,invalid_conn,semaphore,client))


    valid_conn.close()
    invalid_conn.close()

