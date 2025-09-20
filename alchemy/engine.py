from sqlalchemy import column, create_engine, select, table

class AlchemyEngine:
    class Omega:
        engine = create_engine('postgresql://omega:omega@localhost:5432/omega')

        with engine.begin() as connection:
            result = connection.execute(select(column('id'))).fetchall()
            print(result)