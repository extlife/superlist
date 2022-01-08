from django.test import TestCase
from lists.models import Item

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

class ItemModelTest(TestCase):
    '''Item model test'''

    def test_saving_and_retrieving_items(self):
        '''test: saving and retrieving items'''
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
