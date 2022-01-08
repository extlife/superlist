from django.test import TestCase

# Create your tests here.

class HomePageTest(TestCase):
    '''Home page test'''

    def test_home_page_returns_correct_html(self):
        '''test: home page returns correct html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_cave_a_POST_request(self):
        '''test: can save post-request'''
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')
