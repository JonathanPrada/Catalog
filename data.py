from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Category, Items, Users

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Categories
Soccer = Category(name="Soccer")
session.add(Soccer)
session.commit()

Basketball = Category(name="Basketball")
session.add(Basketball)
session.commit()

Baseball = Category(name="Baseball")
session.add(Baseball)
session.commit()

Frisbee = Category(name="Frisbee")
session.add(Frisbee)
session.commit()

Snowboarding = Category(name="Snowboarding")
session.add(Snowboarding)
session.commit()

Rockclimbing = Category(name="Rockclimbing")
session.add(Rockclimbing)
session.commit()

Foosball = Category(name="Foosball")
session.add(Foosball)
session.commit()

Skating = Category(name="Skating")
session.add(Skating)
session.commit()

Hockey = Category(name="Hockey")
session.add(Hockey)
session.commit()

print "Added categories!"
