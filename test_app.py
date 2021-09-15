import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *


class CaptoneTestCase(unittest.TestCase):

    def setUp(self):

        self.market_owner_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1icFJOTlhPOThDajJHaUtlemtOdCJ9.eyJpc3MiOiJodHRwczovL2Rldi14MWJkOGgzci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzOTJhMzE2MzI2MWEwMDY4N2JhZTE5IiwiYXVkIjoicG90aW9uIiwiaWF0IjoxNjMxNDc3NjU1LCJleHAiOjE2MzE1NDk2NTUsImF6cCI6Ijg1T1dkM0xkeW5jVnNjeWt3dHVNTUtxbzEwMkh6UzNrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6Ym90dGxlIiwiYWRkOnBvdGlvbiIsImFkZDp3aXphcmQiLCJkZWxldGU6cG90aW9uIiwiZGVsZXRlOndpemFyZCIsInVwZGF0ZTpib3R0bGUiXX0.Du8eMRztBvUMdigmNMz6P3JhxlmSUUNjy7w9ee3fY6GbMkIlCja-QaJYcL2CIi6Gu8O0tR7Z93Yyznl2a4dHl9oK7YsHyKd7lfBE_WCQUhXA9SNxsbds6qsCfT__x8d9DByEpCIWqhRW32xItz3dmCJKScRKMK9diXsfKKyfhwHqOUl9sqBg0RdswtTyPXgwA0ueLJsCOrj7gA7RIeDseq5mYOcP6km9h4tKW8rS3L_PKlsT7-TK6aFRcs-x49MH-ZIaEQpZTadn5eSKUKgm67BeuNlbq6JihEVCRAPiKTERkJAndNi-cpMyTeSaoRk5EFeeanqBltfTBxIfela_5A'
        self.wizard_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1icFJOTlhPOThDajJHaUtlemtOdCJ9.eyJpc3MiOiJodHRwczovL2Rldi14MWJkOGgzci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzOTJhYmI5NTE4MzkwMDcwODJiZjc4IiwiYXVkIjoicG90aW9uIiwiaWF0IjoxNjMxNDc3NDMyLCJleHAiOjE2MzE1NDk0MzIsImF6cCI6Ijg1T1dkM0xkeW5jVnNjeWt3dHVNTUtxbzEwMkh6UzNrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6Ym90dGxlIiwidXBkYXRlOmJvdHRsZSJdfQ.hEh3x_77XbX0I-F6_1mNlQc7AaUO0XFnfE1rkF9znXGMjXE7LT1YksfbM3MkPJEh-3lusUT-782X_BAY4iiMsyQjJakB16AtUIKVzO0RqjA5zN47d2HUenKLeBPgwWs8e8vjHY4uBt4QcUZNk1pYf67flcAZxruL2N60aqmFjg7oj9tTnLTc9Jzpv8T-HBg4CA3V3a8_AmAMy-uMIw3cqqIoYAE2yFWQzTAGQk2-UNZAxJbV2s2g2apLOWlZxi5nHNWaU10crOcVoH_nLv3lFWwer0Ro0iZ_d4vTqi3Lla82AsfKGLV1lFCKBKqhJbmlcHvz-W0NbngWXtX_qySeoA'
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


        # db data
        self.W1 = Wizard(name="Gandalf",info="he will not let you pass")
        self.W2 = {
            'name':"the necromancer",
            'info':"don't forget to say hi to his skeleton"
            }


        self.P1 = Potion(name="the invisibility potion",effect="its in the name")
        self.P2 = {
            'name':"water breathing potion",
            'effect':"drink it and you will breath under water...or turn into a fish..."
            }

        self.B1 = {
            'w_id':0,
            'p_id':0,
            'quantity':6,
            'price':30
            }

        self.B2 = {
            'w_id':0,
            'p_id':0,
            'quantity':9,
            'price':25
            }

        self.B3 = {
            'w_id':0,
            'p_id':0,
            'quantity':-9,
            'price':-25
            }


    def tearDown(self):
       
        db.session.query(Bottle).delete()
        db.session.query(Wizard).delete()
        db.session.query(Potion).delete()
        db.session.commit()

            
    def test_error_404_wizards(self):
        resp = self.client().get('/wizards')
        self.assertEqual(resp.status_code, 404)
    
    def test_wizards(self):
        db.session.add(self.W1)
        db.session.commit()

        resp = self.client().get('/wizards')

        self.assertEqual(resp.status_code, 200)

    

    def test_potions(self):
        db.session.add(self.P1)
        db.session.commit()
        resp = self.client().get('/potions')

        self.assertEqual(resp.status_code, 200)

    def test_error_404_potions(self):
        resp = self.client().get('/potions')

        self.assertEqual(resp.status_code, 404)

    def test_add_wizard(self): 
        resp = self.client().post('/wizard/add',json=self.W2, headers={
            "Authorization": 'Bearer ' + self.market_owner_token})

        self.assertEqual(resp.status_code, 200)


    def test_error_401_add_wizard(self):
        # without auth token
        resp = self.client().post('/wizard/add',json=self.W2)

        self.assertEqual(resp.status_code, 401)

    def test_add_potion(self): 
        resp = self.client().post('/potion/add',json=self.P2, headers={
            "Authorization": 'Bearer ' + self.market_owner_token})

        self.assertEqual(resp.status_code, 200)


    def test_error_401_add_potion(self):
        # without auth token
        resp = self.client().post('/potion/add',json=self.P2)

        self.assertEqual(resp.status_code, 401)

    def test_delete_wizard(self):
        db.session.add(self.W1)
        db.session.commit()
        w_id=self.W1.id
        resp = self.client().delete('/wizard/delete/{}'.format(w_id), headers={
            "Authorization": 'Bearer ' + self.market_owner_token})

        self.assertEqual(resp.status_code, 200)

    def test_error_404_delete_wizard(self):
        # without adding the wizard to delete it
        w_id=self.W1.id
        resp = self.client().delete('/wizard/delete/{}'.format(w_id), headers={
            "Authorization": 'Bearer ' + self.market_owner_token})
        
        self.assertEqual(resp.status_code, 404)

    def test_delete_potion(self):
        db.session.add(self.P1)
        db.session.commit()
        p_id=self.P1.id
        resp = self.client().delete('/potion/delete/{}'.format(p_id), headers={
            "Authorization": 'Bearer ' + self.market_owner_token})

        self.assertEqual(resp.status_code, 200)

    def test_error_403_delete_potion(self):
        # using the wrong auth token
        db.session.add(self.P1)
        db.session.commit()
        p_id=self.P1.id
        resp = self.client().delete('/potion/delete/{}'.format(p_id), headers={
            "Authorization": 'Bearer ' + self.wizard_token})
        
        self.assertEqual(resp.status_code, 403)


    def test_get_wizard_potions(self):
        db.session.add(self.W1)
        db.session.commit()
        w_id=self.W1.id
        resp = self.client().get('/wizard_potions/{}'.format(w_id))

        self.assertEqual(resp.status_code, 200)


    def test_error_404_get_wizard_potions(self):
        w_id=self.W1.id
        resp = self.client().get('/wizard_potions/{}'.format(w_id))

        self.assertEqual(resp.status_code, 404)


    def test_add_bottle(self):
        db.session.add(self.W1)
        db.session.add(self.P1)
        db.session.commit()

        self.B1['w_id']=self.W1.id
        self.B1['p_id']=self.P1.id
        resp = self.client().post('/bottle/add',json=self.B1, headers={
            "Authorization": 'Bearer ' + self.wizard_token})

        self.assertEqual(resp.status_code, 200)

    def test_error_401_add_bottle(self):
        # without auth token
        db.session.add(self.W1)
        db.session.add(self.P1)
        db.session.commit()

        self.B1['w_id']=self.W1.id
        self.B1['p_id']=self.P1.id
        resp = self.client().post('/bottle/add',json=self.B1)

        self.assertEqual(resp.status_code, 401)

    def test_update_bottle(self):
        db.session.add(self.W1)
        db.session.add(self.P1)
        db.session.commit()

        self.B1['w_id']=self.W1.id
        self.B1['p_id']=self.P1.id
        new_bottle = Bottle(w_id=self.B1['w_id'], p_id=self.B1['p_id'],
        quantity=self.B1['quantity'],price=self.B1['price'])
        db.session.add(new_bottle)
        db.session.commit()


        self.B2['w_id']=self.W1.id
        self.B2['p_id']=self.P1.id

        resp = self.client().patch('/bottle/update',json=self.B2, headers={
            "Authorization": 'Bearer ' + self.wizard_token})

        self.assertEqual(resp.status_code, 200)



    def test_error_422_update_bottle(self):
        #B3 has unwanted negative values

        self.W1.insert()
        self.P1.insert()
        db.session.commit()

        self.B1['w_id']=self.W1.id
        self.B1['p_id']=self.P1.id

        new_bottle = Bottle(w_id=self.B1['w_id'],p_id=self.B1['p_id'],
        quantity=self.B1['quantity'],price=self.B1['price'])

        db.session.add(new_bottle)
        db.session.commit()


        self.B3['w_id']=self.W1.id
        self.B3['p_id']=self.P1.id

        resp = self.client().patch('/bottle/update',json=self.B3, headers={
            "Authorization": 'Bearer ' + self.wizard_token})

        self.assertEqual(resp.status_code, 422)
        
    
# run testing
if __name__ == "__main__":
    unittest.main()

