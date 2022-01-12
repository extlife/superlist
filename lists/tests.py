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
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''test: redirects after POST'''
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-one-of-a-kind-list-in-the-world/')

    def test_only_saves_items_when_necessary(self):
        '''test: only saves items when necessary'''
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):
    '''List view test'''

    def test_uses_list_template(self):
        '''test: uses list template'''
        response = self.client.get('/lists/the-one-of-a-kind-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        '''test: displays all list items'''
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/the-one-of-a-kind-list-in-the-world/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')


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
