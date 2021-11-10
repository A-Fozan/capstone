import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
import auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.route('/')
  def welcome():
    return "welcome to the potion wizard market!!"

  """
   this endpoint returns all wizards that are in the database
   the format is a list of dictionaries, in json format
  """
  @app.route('/wizards')
  def get_wizards():

    all_wizards = db.session.query(Wizard).all()

    list_of_wizards = []
    for wizard in all_wizards:
      w = wizard.format()
      list_of_wizards.append(w)

    return jsonify({
      "success":True,
      "wizards":list_of_wizards
    })
    


  """
   this endpoint returns all potions that are in the database
   the format is a list of dictionaries, in json format
  """
  @app.route('/potions')
  def get_potions():

    all_potions = db.session.query(Potion).all()

    list_of_potions = []
    for potion in all_potions:
      p = potion.format()
      list_of_potions.append(p)

    return jsonify({
      "success":True,
      "potions":list_of_potions
    })

  
  """
   this endpoint returns all potion bottles that a wizards sells,
   given the wizard id.
   the format is a list of dictionaries, in json format
  """
  @app.route('/wizard_potions/<int:id>')
  def get_wizard_potions(id):

    wizard_potion_bottles = db.session.query(Bottle,Potion).filter(Bottle.w_id == id).join(Potion).all()

    if wizard_potion_bottles is None:
      abort(404)
  
    list_of_wizard_potion_bottles = []
    for bottle, potion in wizard_potion_bottles:
      bottle_format = Bottle.format()
      potion_format = Potion.format()
      if "id" in potion_format:
         del potion_format["id"]
      
      all_format = {**bottle_format, **potion_format}
      list_of_wizard_potion_bottles.append(all_format)

    
    return jsonify({
      "success":True,
      "id":id,
      "list":list_of_wizard_potion_bottles
    })




    """
    this endpoint is for adding a wizard
    returns the wizard ID if successful 
    """
  @app.route('/wizard/add', methods=['POST'])
  @auth.requires_auth('add:wizard')
  def add_wizard(jwt):
    body = request.get_json()
    if (body.get('name') is None) or (body.get('info') is None):
      abort(422)

    new_wizard= Wizard(
      name = body.get('name'),
      info = body.get('info')
    )

    
    db.session.add(new_wizard)
    db.session.commit()
    


    return jsonify({
      "success":True,
      "added":new_wizard.id
    })


    """
    this endpoint is for adding a potion
    returns the potion id if successful 
    """

  @app.route('/potion/add', methods=['POST'])
  @auth.requires_auth('add:potion')
  def add_potion(jwt):
    body = request.get_json()

    if (body.get('name') is None) or (body.get('effect') is None):
      abort(422)

    new_potion= Potion(
      name = body.get('name'),
      effect = body.get('effect')
    )

    
    db.session.add(new_potion)
    db.session.commit()
    
    


    return jsonify({
      "success":True,
      "added":new_potion.id
    })

    """
    this endpoint is for adding a bottle to a wizard's collection
    returns the wizard id and potion id if successful 
    """
  @app.route('/bottle/add', methods=['POST'])
  @auth.requires_auth('add:bottle')
  def add_bottle(jwt):
    body = request.get_json()

    if (body.get('w_id') is None) or (body.get('p_id') is None):
      abort(422)

    if (body.get('quantity') is None) or (body.get('price') is None):
      abort(422)

  
    if (body.get('quantity') < 0) or (body.get('price') < 0):
      abort(422)
    
    

    new_bottle= Bottle(
      w_id = body.get('w_id'),
      p_id = body.get('p_id'),
      quantity = body.get('quantity'),
      price = body.get('price')
    )

    
    db.session.add(new_bottle)
    db.session.commit()
    
    


    return jsonify({
      "success":True,
      "added":{
        "w_id":new_bottle.w_id,
        "p_id":new_bottle.p_id
      }
    })

    """
    this endpoint is for deleting a wizard
    returns the wizard id if successful 
    """

  @app.route('/wizard/delete/<int:id>', methods=['DELETE'])
  @auth.requires_auth('delete:wizard')
  def delete_wizard(jwt,id):

    wizard_to_delete = db.session.query(Wizard).filter(Wizard.id == id).one_or_none()
    del_id = wizard_to_delete.id
    if wizard_to_delete is None:
      abort(404)
    
    wizard_to_delete.delete()
    db.session.commit()
    
    


    return jsonify({
      "success":True,
      "deleted_wizard_id":del_id
    })



  
    """
    this endpoint is for deleting a potion
    returns the Potion id if successful 
    """

  @app.route('/potion/delete/<int:id>', methods=['DELETE'])
  @auth.requires_auth('delete:potion')
  def delete_potion(jwt,id):

    potion_to_delete = db.session.query(Potion).filter(Potion.id == id).one_or_none()
    del_id = potion_to_delete.id
    if potion_to_delete is None:
      abort(404)
    
    potion_to_delete.delete()
    db.session.commit()
    
    


    return jsonify({
      "success":True,
      "deleted_potion_id":del_id
    })


    """
    this endpoint is for updating the price and or quantity
    of a bottle that a wizard has.
    returns the wizard id and potion id if successful 
    """

  @app.route('/bottle/update', methods=['PATCH'])
  @auth.requires_auth('update:bottle')
  def update_bottle(jwt):
    body= request.get_json()

    w_id = body.get('w_id')
    p_id = body.get('p_id')

    bottle_to_update = db.session.query(Bottle).filter(Bottle.w_id == w_id, Bottle.p_id == p_id).one_or_none()

    if bottle_to_update is None:
      abort(404)

    if body.get('quantity') is not None:
      if body.get('quantity') < 0:
        abort(422)
      else:
        bottle_to_update.quantity = body.get('quantity')

    if body.get('price') is not None:
      if body.get('price') < 0:
        abort(422)
      else:
        bottle_to_update.quantity = body.get('price')

    db.session.commit()

    return jsonify({
      "success":True,
      "updated":{
        "w_id":bottle_to_update.w_id,
        "p_id":bottle_to_update.p_id
      }
    })


  '''
  Error handlers
  '''

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


  @app.errorhandler(401)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


  @app.errorhandler(403)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


    

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run()
