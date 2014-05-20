# -*- coding:utf-8 -*-
def _getTarget():
    from alchemyjsonschema import SchemaFactory
    return SchemaFactory

def _makeOne(*args, **kwargs):
    from alchemyjsonschema import (
        SingleModelWalker, 
        DefaultClassfier
    )
    return _getTarget()(SingleModelWalker, DefaultClassfier)


## definition
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Group(Base):
    """model for test"""
    __tablename__ = "Group"

    pk = sa.Column(sa.Integer, primary_key=True, doc="primary key")
    name = sa.Column(sa.String(255), default="", nullable=False)
    color = sa.Column(sa.Enum("red", "green", "yellow", "blue"))

def test_type__is_object():
    target = _makeOne()
    result = target.create(Group)

    assert "type" in result
    assert result["type"] == "object"

def test_properties__are__all_of_columns():
    target = _makeOne()
    result = target.create(Group)

    assert "properties" in result
    assert list(sorted(result["properties"].keys())) == ["color", "name", "pk"]

def test_required__are__nullable_is_false_columns():
    target = _makeOne()
    result = target.create(Group)

    assert "required" in result
    assert list(sorted(result["required"])) == ["name", "pk"]

def test_title__id__model_class_name():
    target = _makeOne()
    result = target.create(Group)

    assert "title" in result
    assert result["title"] == Group.__name__

def test_description__is__docstring_of_model():
    target = _makeOne()
    result = target.create(Group)

    assert "description" in result
    assert result["description"] == Group.__doc__

def test_properties__all__this_is_slackoff_little_bit__all_is_all(): #hmm.
    target = _makeOne()
    result = target.create(Group)

    assert result["properties"] == {'color': {'maxLength': 6,
                                              'oneOf': ('red', 'green', 'yellow', 'blue'),
                                              'type': 'string'},
                                    'name': {'maxLength': 255, 'type': 'string'},
                                    'pk': {'description': 'primary key', 'type': 'integer'}}


### adaptive
def test__filtering_by__includes():
    target = _makeOne()
    result = target.create(Group, includes=["pk"])
    assert list(sorted(result["properties"].keys())) == ["pk"]


def test__filtering_by__excludes():
    target = _makeOne()
    result = target.create(Group, excludes=["pk"])
    assert list(sorted(result["properties"].keys())) == ["color", "name"]