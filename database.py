# provides number of functions to manipulate run time environment
import sys


# Used when writing the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String


# We will use in the configuration and class code
from sqlalchemy.ext.declarative import declarative_base


# We use to create our foreign key relationships, used for mapper too
from sqlalchemy.orm import relationship


# We use in our configuration file end of code
from sqlalchemy import create_engine


# Let sql alchemy know that our classes are special sqlalchemy classes
# That correspond to tables in our database
# Our class code will inherit this base class
Base = declarative_base()


class Category(Base):
    # create table representation
    __tablename__ = 'category'
    # Use mapper code to create columns with variables representing col attributes
    name = Column(
        String(80), nullable=False)

    id = Column(
        Integer, primary_key=True)


class Items(Base):
    __tablename__ = 'items'
    name = Column(
        String(80), nullable=False)

    id = Column(
        Integer, primary_key=True)

    description = Column(
        String(250))

    category_id = Column(
        Integer, ForeignKey('category.id'))

    category = relationship(Category)

class Users(Base):
    __tablename__ = 'users'
    name = Column(
        String(80), nullable=False)

    id = Column(
        Integer, primary_key=True)

    email = Column(
        String(250), nullable=False)


# Instance of create engine and point to our database
engine = create_engine(
    'sqlite:///catalog.db')


# Goes into the database and adds classes as new tables
Base.metadata.create_all(engine)

print "Created the catalog database!"