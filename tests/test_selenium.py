import re

import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

from app import create_app, db, fake
import threading
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome(chrome_options=options)
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

        # suppress logging to keep unittest output clean
        import logging
        logger = logging.getLogger('werkzeug')
        logger.setLevel("ERROR")

        # create the database and populate with some fake data
        db.create_all()
        Role.insert_roles()
        fake.users(10)
        fake.posts(10)

        # add an administrator user
        admin_role = Role.query.filter_by(permissions=0xff).first()
        admin = User(email='john14@example.com',
                     username='john14', password='cat',
                     role=admin_role, confirmed=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the Flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search(r'Hello,\sStranger!',
                                  self.client.page_source))

        # navigate to login page
        self.client.find_element(by=By.LINK_TEXT, value='Log In')
        self.assertIn('<h1>Login</h1>', self.client.page_source)

        # log in
        self.client.find_element(By.NAME, 'email').send_keys('john14@example.com')
        self.client.find_element(By.NAME, 'password').send_keys('cat')
        self.client.find_element(By.NAME, 'submit').click()
        self.assertTrue(re.search(r'Hello,\s+john14!', self.client.page_source))

        # navigate to the user's profile page
        self.client.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn('<h1>john14</h1>', self.client.page_source)

