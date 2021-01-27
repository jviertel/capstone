import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Pedal, Manufacturer, setup_db

class TestPedalsAPI(unittest.TestCase):
    site_owner_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild3NW9Ya3ZhNHhEUmh3dGlwczlkMyJ9.eyJpc3MiOiJodHRwczovL2Rldi15azJtZ3RtYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxMDZiODlkZjdiNWEwMDcxOGRkN2FkIiwiYXVkIjoicGVkYWxzZGJhcGkiLCJpYXQiOjE2MTE3NzI5NDksImV4cCI6MTYxMTg1OTM0OSwiYXpwIjoidVdodFpqRDNVV0NITTlCZmN0RDN0WWNBaEFVbmhXc20iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptYW51ZmFjdHVyZXJzIiwiZGVsZXRlOnBlZGFscyIsInBhdGNoOm1hbnVmYWN0dXJlcnMiLCJwYXRjaDpwZWRhbHMiLCJwb3N0Om1hbnVmYWN0dXJlcnMiLCJwb3N0OnBlZGFscyJdfQ.lu1w8XG-Tre1RSHUv4MBQKWMOCv4W8Zes1kMPrcSk7Y1VjY6yeYOp63TwbL8lo7DAjPhQujxOgEvTjciNnQVBszecBNPo6AxQhmxqxRH4SXwiWh7UG1Jb72p8WB_tmN-0C93Qv49PhNpY3u9lqN0_X6BAx12EgIB40FelcEHu16xVSSl2ytSxOD1LX0pAO4SIaoQSAEDi4RcULPwcnYDGbyXVhgfmdP6VZ-pcruLatC5Wi1Oohi-tCrwBcrah9ZdO3MvyTo2UhnpaJrHCrscmZVdjrD_LmSgAcCCtiulU7iut_2peXM78fbUXX8YEko7-Lid5g92qT6EKRNzJh0s7A'

    contributor_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild3NW9Ya3ZhNHhEUmh3dGlwczlkMyJ9.eyJpc3MiOiJodHRwczovL2Rldi15azJtZ3RtYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxMDZiZmQ2OGJmMTgwMDY5ZWQ1ZDkyIiwiYXVkIjoicGVkYWxzZGJhcGkiLCJpYXQiOjE2MTE3NzMwNzIsImV4cCI6MTYxMTg1OTQ3MiwiYXpwIjoidVdodFpqRDNVV0NITTlCZmN0RDN0WWNBaEFVbmhXc20iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInBvc3Q6bWFudWZhY3R1cmVycyIsInBvc3Q6cGVkYWxzIl19.Cle2TZk64HZ2i_KlEsLhrGZiLwP0gR60xGUYzgXrojMRifxMRR17MGafAEWi6sp6X1r46uRFMCbhThakY6ooS3VStUqLJy9_Y6cMFbV-kutXwCnvuz6jm5VbE_gkZ8vk-7xVr027naRckIS4oLHFtiZ3GsTPA1CVwY8dTXc5xxDiX3C7NI_Nk7Kbn0w4Hiz3An3DB0hkYIfBj-Xgg1QrQbe-gPItX_liPgRKgmAbn7K7kCQvBwc8GLLqSSx3c2BvmECXS-t9lp93tLOLqQYFpJk7He5Vee2tLZumhPlGkGJoW-lfcOEOW1_gzS61fQ8eeb9lgX_qJgSVRLeIGOtiCw'

    def setUp(self):
        '''Run before tests'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:88c67e0d53bef241b661e0e3a6cb0cd1@localhost:5432/pedalsdb_test'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        '''Run after tests'''
        pass
    
    #Test successful get request to /manufacturers endpoint
    def test_get_manufacturers(self):
        res = self.client().get('/manufacturers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['num_manufacturers'])
        self.assertTrue(len(data['manufacturers']))
        self.assertEqual(data['success'], True)

    #Test 404 for page out of bounds
    def test_manufacturers_404_page_out_of_bounds(self):
        res = self.client().get('/manufacturers?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    #Test successful get request to /manufacturers/5/pedals
    def test_get_pedals_by_manufacturer(self):
        res = self.client().get('/manufacturers/5/pedals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['manufacturer_id'], 5)
        self.assertTrue(data['manufacturer_name'])
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])    
        self.assertEqual(data['success'], True)
    
    #Test 404 for page out of bounds
    def test_404_manufacturer_not_exists(self):
        res = self.client().get('/manufacturers/5000/pedals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    #Test post request to /manufacturers
    def test_post_manufacturer(self):
        res = self.client().post('/manufacturers', 
            json = {
                'name': 'Volcanic Audio',
                'website_link': 'https://www.volcanicaudio.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_manufacturer'])
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], True)

    #Test unsuccessful post request entry already exists to /manufacturers
    def test_manufacturer_already_exists(self):
        res = self.client().post('/manufacturers',
            json = {
                'name': 'Boss',
                'website_link': 'https://www.bossaudio.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['created_manufacturer'], None)
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], False)
    
    #Test post request to /pedals
    def test_post_pedal(self):
        res = self.client().post('/pedals',
            json = {
                'name': 'California Surf',
                'pedal_type': 'Reverb',
                'new_price': '$99.00',
                'used_price': '$65.00',
                'manufacturer_id': 37
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_pedal'])
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], True)

    #Test unsuccessful post request entry already exists to /pedals
    def test_pedal_already_exists(self):
        res = self.client().post('/pedals',
            json = {
                'name': 'Afterglow',
                'pedal_type': 'Chorus',
                'new_price': '$69.00',
                'used_price': '$39.00',
                'manufacturer_id': 43
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['created_pedal'], None)
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], False)

    #Test patch request to /manufacturers/37
    def test_update_manufacturer(self):
        res = self.client().patch('/manufacturers/37',
            json = {
                'name': 'Changed Name',
                'website_link': 'https://www.pedals.info.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated_manufacturer'], 37)
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], True)
    
    #Test unsuccessful patch request not found to /manufacturers/5000
    def test_patch_404_manufacturer_not_exists(self):
        res = self.client().patch('/manufacturers/5000',
            json = {
                'name': 'Changed Name',
                'website_link': 'https://www.pedals.info.com'
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')
    
    #Test patch request to /pedals/472
    def test_update_pedals(self):
        res = self.client().patch('/pedals/472',
            json = {
                'name': 'Hot Rod',
                'pedal_type': 'Distortion',
                'new_price': '$79.00',
                'used_price': '$45.00',
                'manufacturer_id': 25
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated_pedal'], 472)
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], True)
    
    #Test unsuccessful patch request not found to /pedals/5000
    def test_patch_404_pedal_not_exists(self):
        res = self.client().patch('/pedals/5000',
            json = {
                'name': 'Hot Rod',
                'pedal_type': 'Distortion',
                'new_price': '$79.00',
                'used_price': '$45.00',
                'manufacturer_id': 25
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    #Test delete request to /manufacturers/29
    def test_delete_manufacturer(self):
        res = self.client().delete('/manufacturers/29')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted_manufacturer'], 29)
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], True)    

    #Test delete manufacturer not found to /manufacturers/5000
    def test_404_manufacturer_to_delete_not_exists(self):
        res = self.client().delete('/manufacturers/5000')
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')
    
    #Test delete request to /pedals/600
    def test_delete_pedal(self):
        res = self.client().delete('/pedals/600')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted_pedal'], 600)
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], True)    

    #Test delete manufacturer not found to /manufacturers/5000
    def test_404_pedal_to_delete_not_exists(self):
        res = self.client().delete('/pedals/5000')
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    #Test post manufacturer with RBAC success to /manufacturers
    #with Contributor credentials
    def test_permissions_contributor(self):
        res = self.client().post('/manufacturers', 
            headers = {
                "Authorization": "Bearer {}".format(self.contributor_token)
            },
            json = {
                'name': 'Real Sounds',
                'website_link': 'https://www.realsounds.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_manufacturer'])
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], True)

    #Test post manufacturer with RBAS success to /manufacturers
    #with Site Owner credentials
    def test_permissions_site_owner(self):
        res = self.client().post('/manufacturers', 
            headers = {
                "Authorization": "Bearer {}".format(self.site_owner_token)
            },
            json = {
                'name': 'Extreme Pedals',
                'website_link': 'https://www.extremepedals.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_manufacturer'])
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], True)

    #Test update pedal with RBAC denied to /pedals/365
    #with Contributor credentials
    def test_permissions_denied_contributor(self):
        res = self.client().patch('/pedals/365',
            headers = {
                "Authorization": "Bearer {}".format(self.contributor_token)
            },
            json = {
                'name': 'Tailfin',
                'pedal_type': 'Vibrato',
                'new_price': '$89.00',
                'used_price': '$55.00',
                'manufacturer_id': 28
            })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data, 'Permission not in permissions list')


    #Test update pedal with RBAC success to /pedals/283
    #with Site Owner credentials
    def test_permissions_site_owner_update(self):
        res = self.client().patch('/pedals/283',
            headers = {
                "Authorization": "Bearer {}".format(self.site_owner_token)
            },
            json = {
                'name': 'Twister',
                'pedal_type': 'Rotary Speaker',
                'new_price': '$59.00',
                'used_price': '$39.00',
                'manufacturer_id': 17
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated_pedal'], 283)
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], True)
        


if __name__ == '__main__':
    unittest.main()
