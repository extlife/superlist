from django.test import TestCase
from lists.models import Item, List

# Create your tests here.

class HomePageTest(TestCase):
    '''Home page test'''

    def test_home_page_returns_correct_html(self):
        '''test: home page returns correct html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

class ListViewTest(TestCase):
    '''List view test'''

    def test_uses_list_template(self):
        '''test: uses list template'''
        response = self.client.get('/lists/the-one-of-a-kind-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        '''test: displays all list items'''
        list_ = List.objects.create()
        Item.objects.create(text='item 1', list=list_)
        Item.objects.create(text='item 2', list=list_)

        response = self.client.get('/lists/the-one-of-a-kind-list-in-the-world/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

class NewListTest(TestCase):
    '''New list test'''

    def test_can_cave_a_POST_request(self):
        '''test: can save post-request'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''test: redirects after POST'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-one-of-a-kind-list-in-the-world/')

class ListAndItemModelTest(TestCase):
    '''List and item model test'''

    def test_saving_and_retrieving_items(self):
        '''test: saving and retrieving items'''
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
