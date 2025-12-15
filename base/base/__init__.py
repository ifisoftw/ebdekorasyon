try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # PyMySQL is optional when using SQLite (tests/dev)
    pass


