# sqlalchemy database
from importlib import metadata
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Boolean
import os
import sys
from src.res.constants import db_path

metadata = MetaData()
engine=create_engine('sqlite:///'+res.constants.db_path, echo=True) # type: ignore
table_sentences = Table('sentences', metadata,
              Column('index', Integer, primary_key=True),
              Column('sentence', String),
              Column('es', String),
              Column('fr', String),
              Column('de', String),
              Column('it', String),
              Column('pt', String),
              Column('ru', String),
              Column('ja', String),
              Column('ko', String),
              Column('pl', String),
              Column('hard', Boolean),
              )

def create_database():
    metadata.create_all(engine)

def drop_database():
    metadata.drop_all(engine)

def insert_sentence(index, sentence, es, fr, de, it, pt, ru, ja, ko, pl, hard):
    with engine.connect() as connection:
        connection.execute(table_sentences.insert().values(index=index, sentence=sentence, es=es, fr=fr, de=de, it=it, pt=pt, ru=ru, ja=ja, ko=ko, pl=pl, hard=hard))
        connection.commit()

def get_sentence(index):
    with engine.connect() as connection:
        result = connection.execute(table_sentences.select().where(table_sentences.columns.index == index))
        return result.fetchone()

def get_all_sentences():
    with engine.connect() as connection:
        result = connection.execute(table_sentences.select())
        return result.fetchall()

def get_last_index():
    with engine.connect() as connection:
        result = connection.execute(table_sentences.select().with_only_columns(table_sentences.columns.index).order_by(table_sentences.columns.index.desc()).limit(1))
        result = result.fetchone()
        if result is None:
            return 0
        return result[0]
    
def update_hard_by_index(index : int, value : bool):
    with engine.connect() as connection:
        connection.execute(table_sentences.update().where(table_sentences.columns.index == index).values(hard=value))
        connection.commit()

def drop_sentence_by_index(index : int):
    with engine.connect() as connection:
        connection.execute(table_sentences.delete().where(table_sentences.columns.index == index))
        connection.commit()

if __name__=='__main__':
    create_database()
    # insert_sentence(4, 'Hello', 'Hola', 'Bonjour', 'Hallo', 'Ciao', 'Olá', 'Привет', 'こんにちは', '안녕하세요', 'Cześć', False)


