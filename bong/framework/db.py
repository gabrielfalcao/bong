#!/usr/bin/env python
# -*- coding: utf-8 -*-

# flake8: noqa
from __future__ import unicode_literals
import __builtin__

import inspect
import dateutil.parser
import datetime
from functools import partial
from decimal import Decimal

from redis import StrictRedis
from bong import settings
from bong.framework.formats import json

import sqlalchemy as db
from sqlalchemy import (
    create_engine,
    MetaData,
)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()


def get_redis_connection(db=0):
    """This function knows how to return a new `redis.StrictRedis`
    instance with the redis credentials from settings"""
    conf = settings.REDIS_URI

    return StrictRedis(
        db=db,
        host=conf.host,
        port=conf.port,

        # using `path` as password to support the URI like:
        # redis://hostname:port/veryverylongpasswordhashireallymeanSHA512
        password=conf.path,
    )


def DefaultForeignKey(field_name, parent_field_name,
                      ondelete=b'CASCADE', nullable=False, **kw):
    return db.Column(field_name, db.Integer,
                     db.ForeignKey(parent_field_name, ondelete=ondelete),
                     nullable=nullable, **kw)


def PrimaryKey(name=b'id'):
    return db.Column(name, db.Integer, primary_key=True)


class ORM(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'table'):
            return

        cls.__columns__ = {c.name: c.type.python_type
                           for c in cls.table.columns}
        setattr(ORM, name, cls)
        super(ORM, cls).__init__(name, bases, attrs)


class Manager(object):

    def __init__(self, model_klass, engine):
        self.model = model_klass
        self.engine = engine

    def from_result_proxy(self, proxy, result):
        """Creates a new instance of the model given a sqlalchemy
        result proxy"""
        if not result:
            return None

        data = dict(zip(proxy.keys(), result))
        return self.model(engine=self.engine, **data)

    def create(self, **data):
        """Creates a new model and saves it to MySQL"""
        instance = self.model(engine=self.engine, **data)
        return instance.save()

    def get_or_create(self, **data):
        """Tries to get a model from the database that would match the
        given keyword-args through `Model.find_one_by()`. If not
        found, a new instance is created in the database through
        `Model.create()`"""
        instance = self.find_one_by(**data)
        if not instance:
            instance = self.create(**data)

        return instance

    def query_by(self, order_by=None, **kw):
        """Queries the table with the given keyword-args and
        optionally a single order_by field.  This method is used
        internally and is not consistent with the other ORM methods by
        not returning a model instance.
        """
        conn = self.get_connection()
        query = self.model.table.select()
        for field, value in kw.items():
            query = query.where(getattr(self.model.table.c, field) == value)

        proxy = conn.execute(query.order_by(db.desc(
            getattr(self.model.table.c, order_by or 'id'))))
        return proxy

    def find_one_by(self, **kw):
        """Find a single model that could be found in the database and
        match all the given keyword-arguments"""
        proxy = self.query_by(**kw)
        return self.from_result_proxy(proxy, proxy.fetchone())

    def find_by(self, **kw):
        """Find a list of models that could be found in the database
        and match all the given keyword-arguments"""
        proxy = self.query_by(**kw)
        Models = partial(self.from_result_proxy, proxy)
        return map(Models, proxy.fetchall())

    def all(self):
        """Returns all existing rows as Model goloka"""
        return self.find_by()

    def get_connection(self):
        return self.engine.connect()


class Model(object):
    __metaclass__ = ORM

    manager = Manager

    @classmethod
    def using(cls, engine):
        return cls.manager(cls, engine)

    create = classmethod(lambda cls, **data: cls.using(engine).create(**data))
    get_or_create = classmethod(lambda cls, **data: cls.using(engine).get_or_create(**data))
    query_by = classmethod(lambda cls, order_by=None, **kw: cls.using(engine).query_by(order_by, **kw))
    find_one_by = classmethod(lambda cls, **kw: cls.using(engine).find_one_by(**kw))
    find_by = classmethod(lambda cls, **kw: cls.using(engine).find_by(**kw))
    all = classmethod(lambda cls: cls.using(engine).all())

    def __init__(self, engine=None, **data):
        '''A Model can be instantiated with keyword-arguments that
        have the same keys as the declared fields, it will make a new
        model instance that is ready to be persited in the database.

        DO NOT overwrite the __init__ method of your custom model.

        There are 2 possibilities of customization of your model in
        construction time:

        * Implement a `preprocess(self, data)` method in your model,
        this method takes the dictionary that has the
        keyword-arguments given to the constructor and should return a
        dictionary with that data "post-processed" This ORM provides
        the handy optional method `initialize` that is always called
        in the end of the constructor.

        * Implement the `initialize(self)` method that will be always
          called after successfully creating a new model instance.
        '''
        Model = self.__class__
        module = Model.__module__
        name = Model.__name__
        columns = self.__columns__.keys()
        preprocessed_data = self.preprocess(data)
        if not isinstance(preprocessed_data, dict):
            raise InvalidModelDeclaration(
                'The model `{0}` declares a preprocess method but '
                'it does not return a dictionary!'.format(name))

        self.__data__ = preprocessed_data

        self.engine = engine

        for k, v in data.iteritems():
            if k not in self.__columns__:
                msg = "{0} is not a valid column name for the model {2}.{1} ({3})"
                raise InvalidColumnName(msg.format(k, name, module, columns))

            setattr(self, k, v)

        self.initialize()

    def __repr__(self):
        return '<{0} id={1}>'.format(self.__class__.__name__, self.id)

    def preprocess(self, data):
        """Placeholder for your own custom preprocess method, remember
        it must return a dictionary"""
        return data

    def serialize_value(self, attr, value):
        col = self.table.columns[attr]

        if col.default and not value:
            if col.default.is_callable:
                value = col.default.arg(value)
            else:
                value = col.default.arg

        if isinstance(value, Decimal):
            return str(value)

        date_types = (datetime.datetime, datetime.date, datetime.time)
        if isinstance(value, date_types):
            return value.isoformat()

        if not value:
            return value

        data_type = self.__columns__.get(attr, None)
        builtins = dict(inspect.getmembers(__builtin__)).values()
        if data_type and not isinstance(value, data_type) and data_type in builtins:
            return data_type(value)

        return value

    def deserialize_value(self, attr, value):
        date_types = (datetime.datetime, datetime.date)

        kind = self.__columns__.get(attr, None)
        if issubclass(kind, date_types) and not isinstance(value, kind) and value:
            return dateutil.parser.parse(value)

        return value

    def __setattr__(self, attr, value):
        if attr in self.__columns__:
            self.__data__[attr] = self.deserialize_value(attr, value)
            return

        return super(Model, self).__setattr__(attr, value)

    def to_dict(self):
        """pre-serializes the model, returning a dictionary with
        key-values.

        This method can be overwritten by subclasses at will.
        """
        return self.serialize()

    def serialize(self):
        """pre-serializes the model, returning a dictionary with
        key-values.

        This method is use by the to_dict() and only exists as a
        separate method so that subclasses overwriting `to_dict` can
        call `serialize()` rather than `super(SubclassName,
        self).to_dict()`
        """

        keys = self.__columns__.keys()
        return dict([(k, self.serialize_value(k, self.__data__.get(k))) for k in self.__columns__.keys()])

    def to_insert_params(self):
        data = Model.serialize(self)

        primary_key_names = [x.name for x in self.table.primary_key.columns]
        keys_to_pluck = filter(lambda x: x not in self.__columns__, data.keys()) + primary_key_names

        # not saving primary keys, let's let the SQL backend to take
        # care of auto increment.

        # if we need fine tuning and allow manual primary key
        # definition, just go ahead and change this code and it's
        # tests :)
        for key in keys_to_pluck:
            data.pop(key)

        return data

    def to_json(self, indent=None):
        """Grabs the dictionary with the current model state returned
        by `to_dict` and serializes it to JSON"""
        data = self.to_dict()
        return json.dumps(data, indent=indent)

    def __getattr__(self, attr):
        if attr in self.__columns__.keys():
            value = self.__data__.get(attr, None)
            return self.serialize_value(attr, value)

        return super(Model, self).__getattribute__(attr)

    def delete(self):
        """Deletes the current model from the database (removes a row
        that has the given model primary key)
        """

        conn = self.get_engine().connect()

        return conn.execute(self.table.delete().where(
            self.table.c.id == self.id))

    @property
    def is_persisted(self):
        return 'id' in self.__data__

    def get_engine(self, input_engine=None):

        if not self.engine and not input_engine:
            raise EngineNotSpecified(
                "You must specify a SQLAlchemy engine object in order to "
                "do operations in this model instance: {0}".format(self))
        elif self.engine and input_engine:
            raise MultipleEnginesSpecified(
                "This model instance has a SQLAlchemy engine object already. "
                "You may not save it to another engine.")

        return self.engine or input_engine

    def save(self, input_engine=None):
        """Persists the model instance in the DB.  It takes care of
        checking whether it already exists and should be just updated
        or if a new record should be created.
        """

        conn = self.get_engine(input_engine).connect()

        mid = self.__data__.get('id', None)
        if mid is None:
            res = conn.execute(
                self.table.insert().values(**self.to_insert_params()))

            self.__data__['id'] = res.inserted_primary_key[0]
            self.__data__.update(res.last_inserted_params())
        else:
            res = conn.execute(
                self.table.update().values(**self.to_insert_params()).where(self.table.c.id == mid))
            self.__data__.update(res.last_updated_params())

        return self

    def refresh(self):
        new = self.find_one_by(id=self.id)
        self.set(**new.__data__)
        return self

    def set(self, **kw):
        """Sets multiple fields"""
        cols = self.__columns__.keys()

        for name, value in kw.items():
            if name not in cols:
                raise InvalidColumnName('{0}.{1}'.format(self, name))
            setattr(self, name, value)

    def get(self, name, fallback=None):
        """Get a field value from the model"""
        return self.__data__.get(name, fallback)

    def initialize(self):
        """Dummy method to be optionally overwritten in the subclasses"""

    def __eq__(self, other):
        """Just making sure models are comparable to each other"""
        if self.id and other.id:
            return self.id == other.id

        keys = set(self.__data__.keys() + other.__data__.keys())

        return all(
            [self.__data__.get(key) == other.__data__.get(key)
            for key in keys if key != 'id'])


class MultipleEnginesSpecified(Exception):
    pass


class EngineNotSpecified(Exception):
    pass


class InvalidColumnName(Exception):
    pass


class InvalidModelDeclaration(Exception):
    pass


class RecordNotFound(Exception):
    pass
