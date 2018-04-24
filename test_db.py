import psycopg2



def connect_postgres():
    try:
        connect_str = "dbname='metro' user='metro' host='localhost' " + \
                      "password='metro'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        #raise(e)
        #print(e)
    return conn