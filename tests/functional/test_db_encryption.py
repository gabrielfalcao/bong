#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcao <gabriel@nacaolivre.org>
#
import nacl.secret
import nacl.utils
import sqlalchemy as db
from sure import scenario
from datetime import datetime
from bong.framework.db import Model, engine


metadata = db.MetaData()


def now():
    return datetime(2012, 12, 12)


SECRET_KEY_TEST1 = '\x1e\xebo\xa4\xf4\xc8\x06\xe8`\xdah\xf6\x97B\xb9\xa9\x18\x8f\xe4\x1ft\\p\x89^)\xa0G\xe4>\x83X'
SECRET_KEY_TEST2 = '\t\x8ba@\xcf5\xe9\x82\xe7\x1c\x18\xec\xceDQ\x91N\xf5\xfd\xefI\xcb\x126\xfb\xd8\xb1E\xd0\x15\x1f.'


def prepare_db(context):
    engine.connect()
    metadata.drop_all(engine)
    metadata.create_all(engine)


class SensitiveDataModel(Model):

    table = db.Table(
        'sensitive_data',
        metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('ssn', db.LargeBinary),
        db.Column('age', db.Integer),
        db.Column('created_at', db.LargeBinary, default=now)
    )
    encryption = {
        'ssn': SECRET_KEY_TEST1,
        'created_at': SECRET_KEY_TEST2,
    }


def test_serialize_value_encrypted():
    "Model.serialize_value with a model that has a secret key should encrypt its value"

    box1 = nacl.secret.SecretBox(SECRET_KEY_TEST1)
    box2 = nacl.secret.SecretBox(SECRET_KEY_TEST2)

    sdm = SensitiveDataModel()

    result1 = sdm.encrypt_attribute('ssn', '123.45.678')
    result1.should_not.equal('123.45.678')
    box1.decrypt(result1).should.equal('123.45.678')

    result2 = sdm.encrypt_attribute('created_at', '2014-05-20 18:45:00')
    result2.should_not.equal('2014-05-20 18:45:00')
    box2.decrypt(result2).should.equal('2014-05-20 18:45:00')


def test_deserialize_value_encrypted():
    "Model.deserialize_value with a model that has a secret key should decrypt its value"

    nonce1 = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    nonce2 = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    box1 = nacl.secret.SecretBox(SECRET_KEY_TEST1)
    box2 = nacl.secret.SecretBox(SECRET_KEY_TEST2)

    sdm = SensitiveDataModel()

    enc1 = box1.encrypt("999.77.555", nonce1)
    enc2 = box2.encrypt("2014-05-20 18:45:00", nonce2)

    result1 = sdm.decrypt_attribute('ssn', enc1)
    result2 = sdm.decrypt_attribute('created_at', enc2)

    result1.should.equal('999.77.555')
    result2.should.equal("2014-05-20 18:45:00")


@scenario(prepare_db)
def test_serialization_seamless(context):
    "Model.serialize_value with a model that has a secret key should encrypt its value"

    sdm_id1 = SensitiveDataModel.create(ssn='123.22.321').id

    sdm_fresh = SensitiveDataModel.find_one_by(id=sdm_id1)

    data = sdm_fresh.to_dict()

    data.should.equal({
        'age': None,
        'created_at': '2012-12-12T00:00:00',
        'id': 1,
        'ssn': '123.22.321'
    })
