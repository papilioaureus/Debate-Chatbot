from flask_testing import TestCase
#from your_web_app_module import create_app

class TestDebateBotWebApp(TestCase):
    
    def create_app(self):
        # Create your Flask app instance here
        app = create_app()
        app.config['TESTING'] = True
        return app
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('home.html')
