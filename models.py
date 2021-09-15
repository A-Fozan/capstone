from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
import os


database_path = os.environ['DATABASE_URL']
#database_path = 'postgresql://@localhost:5432/capstone'


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    db.create_all()


"""
the Potion model that represent potion types
it has a name and an effect
"""
class Potion(db.Model):  
  __tablename__ = 'Potions'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String)
  effect = Column(db.String)

  def __init__(self, name, effect=""):
    self.name = name
    self.effect = effect

  def insert(self):
        db.session.add(self)
        db.session.commit()

  def update(self):
        db.session.commit()

  def delete(self):
        db.session.delete(self)
        db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'effect': self.effect
      }
  

"""
the Wizard model represents the wizard that sells the bottles of potions.
it has a name and general info about them
"""
      
class Wizard(db.Model):  
  __tablename__ = 'Wizards'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String)
  info = Column(db.String)

  def __init__(self,name="",info=""):
    self.name = name
    self.info = info

  def insert(self):
        db.session.add(self)
        db.session.commit()

  def update(self):
        db.session.commit()

  def delete(self):
        db.session.delete(self)
        db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'info': self.info
      }


"""
the Bottle model represends the bottles that a wizard sells. 
the bottle has a potion and wizard id as well as a quantity and price.
"""
class Bottle(db.Model):  
  __tablename__ = 'Bottles'
  w_id = Column(db.Integer, db.ForeignKey(Wizard.id), primary_key=True)
  p_id = Column(db.Integer, db.ForeignKey(Potion.id), primary_key=True)
  quantity = Column(db.Integer)
  price = Column(db.Integer)


  def __init__(self,w_id, p_id, quantity=0, price=0):
    self.w_id = w_id
    self.p_id = p_id
    self.quantity = quantity
    self.price = price

  def insert(self):
        db.session.add(self)
        db.session.commit()

  def update(self):
        db.session.commit()

  def delete(self):
        db.session.delete(self)
        db.session.commit()

  def format(self):
    return {
      'w_id': self.w_id,
      'p_id': self.p_id,
      'quantity': self.quantity,
      'price': self.price
      }



