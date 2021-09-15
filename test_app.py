import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *


class CaptoneTestCase(unittest.TestCase):

    def setUp(self):

        self.market_owner_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1icFJOTlhPOThDajJHaUtlemtOdCJ9.eyJpc3MiOiJodHRwczovL2Rldi14MWJkOGgzci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzOTJhMzE2MzI2MWEwMDY4N2JhZTE5IiwiYXVkIjoicG90aW9uIiwiaWF0IjoxNjMxNzM1NjY2LCJleHAiOjE2MzE4MDc2NjYsImF6cCI6Ijg1T1dkM0xkeW5jVnNjeWt3dHVNTUtxbzEwMkh6UzNrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6Ym90dGxlIiwiYWRkOnBvdGlvbiIsImFkZDp3aXphcmQiLCJkZWxldGU6cG90aW9uIiwiZGVsZXRlOndpemFyZCIsInVwZGF0ZTpib3R0bGUiXX0.ytUyhwxZdyykCixsjRyNvFX0d9UkDFX917-Jcl1kWDbR5mRX7wgL048Dyl96G6iayNt862Fxzi1DH1Q-lxlu2Cnpwvwp_0YhMrEZ34rzZQBg8uOrt5WcYxyJrTNU0Ym-Lrs1FSFAvD3dWzrGJ42SRwcMbOsYj9jU0Xn1GR-JfRhJGtGUdw9KOdE8KmnskrK4suTvmCTskSRtkCyWCInyCJS5vxKaFq9I1mLM2Vkp38PbCQqz8ow6MpTLRjqMeFGG19NOvISx8ZzF85JoGnFIr6lvjymyH20A-gk-lpozrIQI80bi5K9Q8eUglAA-gCv33XIufMM-ci3LFnAu_hTFtg'
        self.wizard_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1icFJOTlhPOThDajJHaUtlemtOdCJ9.eyJpc3MiOiJodHRwczovL2Rldi14MWJkOGgzci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzOTJhYmI5NTE4MzkwMDcwODJiZjc4IiwiYXVkIjoicG90aW9uIiwiaWF0IjoxNjMxNzM1NzYzLCJleHAiOjE2MzE4MDc3NjMsImF6cCI6Ijg1T1dkM0xkeW5jVnNjeWt3dHVNTUtxbzEwMkh6UzNrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6Ym90dGxlIiwidXBkYXRlOmJvdHRsZSJdfQ.yVWg8cSKgYdqZB-6vhyDasXgmKmbeLGtWQTJ_tl5h5PhfiWDhbRz5zCBXw0iw37GCWfkesddawPAfQOpSAklJNT4p0I856ouRBT_TveCtyUeCJGqC2PC1wFqpV-jo5Pa0ozPYS8IJOPMbjIGZ81ODDnz8K3geNGOmFokQQbotKzQI4z9vTFsygAmrQnpWoQzkmx74Vb1QahjOw7g9_iQFPLnXUhDuNLmeWQlEH-huspln8PsZSlZCznQU4Lo8mMmvJqJLBpDSSUYWAhbYgTR1NV5jXz3aYNJFWfBrbmzlEHx87d74xjSIWTfvMy0if4wxDaoWowMfZqmsDkSTpFiSA'
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

