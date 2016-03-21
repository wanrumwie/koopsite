import json
from urllib.parse import quote

from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.test import TestCase

from functional_tests.koopsite.ft_base import DummyUser
from koopsite.functions import parseClientRequest, get_or_none
from koopsite.viewsajax import ajaxSelRowIndexToSession, \
                        ajaxStartRowIndexFromSession, BrowseTableArray


'''
function selElementArr(){
    // only selected element in table
    var arr = {};
    arr.browTabName = $( "#browTabName" ).val(); // name of table for session dictionary
    arr.parent_id   = '';                        // parent folder id - for compatibility with Folders model
    arr.sendMail    = $( "#id_cond" ).prop( "checked" );  // send mail to user condition
    arr.selRowIndex = $( "#selRowIndex" ).val(); // selected row index
    arr.model       = selElement.model;          // selected element model name
    arr.id          = selElement.id;             // selected element id
    arr.name        = selElement.name;           // selected element name
//    console.log('arr=', arr);
    return arr;
}
function ajax_selRowIndexToSession() {
    var arr = selElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/ajax-selrowindex-to-session";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    as.success = function( json ) { };            // response no needed
    as.error = function( xhr ) {
            xhrErrorAlert( xhr, 'ajax_selRowIndexToSession' );
        };
    $.ajax( as );
    return false;
}
'''

# TODO-2016 01 29 створити аналогічний DummyAjaxRequest для XHRClientRequest
class DummyAjaxRequest:
    """
    Емуляція запиту ajax, сформованого в js
    Фактично відтворюються відповідні змінні і функції з файлів js
    """
    '''
    def __init__(self,  browTabName="",
                        parent_id  ="",
                        sendMail   ="",
                        selRowIndex="",
                        model      ="",
                        id         ="",
                        name       ="",
                        **kwargs):
        self.browTabName = browTabName
        self.parent_id   = parent_id
        self.sendMail    = sendMail
        self.selRowIndex = selRowIndex
        self.model       = model
        self.id          = id
        self.name        = name
        self.kwargs      = kwargs
        self.selElement = {'model': model, 'id': id, 'name': name}

    def selElementArr(self):
        arr = {
        'browTabName' : self.browTabName,
        'parent_id'   : self.parent_id,
        'sendMail'    : self.sendMail,
        'selRowIndex' : self.selRowIndex,
        'model'       : self.selElement.get('model'),
        'id'          : self.selElement.get('id'),
        'name'        : self.selElement.get('name'),
        }
        return arr
    '''
    def __init__(self,  **kwargs):
        self.kwargs      = kwargs

    def ajax_data(self):
        arr = self.kwargs
        json_string = json.dumps(arr)
        data = {
                'client_request' : json_string,
                # 'csrfmiddlewaretoken': csrf_token
            }
        return data

class DummyXHRrequest(DummyAjaxRequest):

    def ajax_data(self):
        arr = self.kwargs
        json_string = json.dumps(arr)
        encoded_json_string = quote(json_string)
        data = {
                "HTTP_X_CLIENT_REQUEST" : json_string,
            }
        return data


class AjaxSelRowIndexToSessionTest(TestCase):

    def test_function(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'fred',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        response = ajaxSelRowIndexToSession(request)

        # Чи в сесію записано правильні дані?
        expected = {'Selections': {'users_table': {'': {'model': "user", 'id': "1", 'selRowIndex': '0'}}}}
        self.assertEqual(request.session, expected)
        self.assertTrue(isinstance(response, HttpResponse))

        # Чи ф-ція повертає правильний response?
        expected = [b'{"server_response": {"id": "1", "selRowIndex": "0", "model": "user"}}']
        self.assertEqual(json.loads(response._container[0].decode()) , json.loads(expected[0].decode()))
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_function_return_response_bad_request_if_non_mathing_data(self):
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'FOLDER',
                    'id'          :'1',
                    'name'        :'fred',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        response = ajaxSelRowIndexToSession(request)
        self.assertEqual(request.session, {})
        self.assertTrue(isinstance(response, HttpResponseBadRequest))
        expected = [b'ajaxSelRowIndexToSession: \n Bad data in request.POST: model name does not correspond to table name \n model=FOLDER \n browTabName=users_table']
        self.assertEqual(response._container, expected)
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_function_return_response_bad_request_if_no_client_request(self):
        request = self.client.request()
        request.POST = {}
        request.session = {}
        response = ajaxSelRowIndexToSession(request)
        self.assertEqual(request.session, {})
        self.assertTrue(isinstance(response, HttpResponseBadRequest))
        expected = [b"ajaxSelRowIndexToSession: No 'client_request' in request.POST"]
        self.assertEqual(response._container, expected)
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)


class AjaxStartRowIndexFromSessionTest(TestCase):

    def test_function_return_HttpResponse(self):
        ajax_data = DummyAjaxRequest(browTabName='folders_contents',
                                       parent_id='1',
                                       selRowIndex='0').ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {'Selections': {'folders_contents': {'1': {'model': "user", 'id': "1", 'selRowIndex': '0'}}}}
        response = ajaxStartRowIndexFromSession(request)
        self.assertTrue(isinstance(response, HttpResponse))

        # Чи ф-ція повертає правильний response?
        expected = [b'{"server_response": {"id": "1", "selRowIndex": "0", "model": "user"}}']
        self.assertEqual(json.loads(response._container[0].decode()) , json.loads(expected[0].decode()))
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_function_return_HttpResponse_2(self):
        json_s = '{"browTabName":"folders_contents","parent_id":"1","selRowIndex":"0"}'
        request = self.client.request()
        request.POST = {'client_request': json_s}
        expected = {'sendMail': None, 'id': None, 'name': None, 'browTabName': 'folders_contents', 'parent_id': '1', 'selRowIndex': '0', 'model': None}
        expected = {'browTabName': 'folders_contents', 'parent_id': '1', 'selRowIndex': '0'}
        self.assertEqual(parseClientRequest(request.POST), expected)
        request.session = {
                   'Selections':
                        {"folders_contents":
                             {"1":
                                 {'model'       : "folder",
                                  'id'          : "1",
                                  'selRowIndex' : "2",
                                 },
                             },
                        },
                   }
        response = ajaxStartRowIndexFromSession(request)
        self.assertTrue(isinstance(response, HttpResponse))

        # Чи ф-ція повертає правильний response?
        expected = [b'{"server_response": {"id": "1", "selRowIndex": "2", "model": "folder"}}']
        self.assertEqual(json.loads(response._container[0].decode()) , json.loads(expected[0].decode()))
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_function_return_response_bad_request_if_non_matching_data(self):
        ajax_data = DummyAjaxRequest(browTabName='folders_contents',
                                       model='USER',
                                       parent_id='1',
                                       selRowIndex='0').ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {'Selections': {'folders_contents': {'1': {'model': "user", 'id': "1", 'selRowIndex': '0'}}}}
        response = ajaxStartRowIndexFromSession(request)
        self.assertTrue(isinstance(response, HttpResponseBadRequest))
        expected = [b'ajaxStartRowIndexFromSession: \n Bad data in request.POST: model name does not correspond to table name \n model=USER \n browTabName=folders_contents']
        self.assertEqual(response._container, expected)
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_function_return_response_bad_request_if_no_client_request(self):
        request = self.client.request()
        request.POST = {}
        response = ajaxStartRowIndexFromSession(request)
        self.assertTrue(isinstance(response, HttpResponseBadRequest))
        expected = [b"ajaxStartRowIndexFromSession: No 'client_request' in request.POST"]
        self.assertEqual(response._container, expected)
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)


class BrowseTableArrayTest(TestCase):

    def setUp(self):
        DummyUser().create_dummy_user('fred', id=1)
        DummyUser().create_dummy_user('john', id=2)
        self.bta_cls = BrowseTableArray

    def test_get_qs_array(self):
        qs = User.objects.all()
        expected = {0: {0: {'id': '1', 'model': 'user', 'name': 'fred'}}, 1: {0: {'id': '2', 'model': 'user', 'name': 'john'}}}
        arr = self.bta_cls().get_qs_array(qs)
        self.assertEqual(arr, expected)

    def test_get_qs_array_2(self):
        qs = User.objects.all()
        sel_model_id = {'id': '2', 'model': 'user', 'name': 'john'}
        expected = {0: {0: {'id': '1', 'model': 'user', 'name': 'fred'}}, 1: {0: {'id': '2', 'model': 'user', 'name': 'john'}}}
        arr, sel_index = self.bta_cls().get_qs_array(qs, sel_model_id=sel_model_id)
        self.assertEqual(arr, expected)
        self.assertEqual(sel_index, 1)
        sel_model_id = {'id': '3', 'model': 'user', 'name': 'john'}
        arr, sel_index = self.bta_cls().get_qs_array(qs, sel_model_id=sel_model_id)
        self.assertEqual(arr, expected)
        self.assertEqual(sel_index, 0)

    def test_get_table_headers(self):
        expected = {0:'', 1:'Name'}
        cap = self.bta_cls().get_table_headers()
        self.assertEqual(cap, expected)

    def test_get_row(self):
        user = get_or_none(User, id=1)
        expected = {0: {'id': '1', 'model': 'user', 'name': 'fred'}}
        row = self.bta_cls().get_row(user)
        self.assertEqual(row, expected)

    def test_get_row_2(self):
        user = get_or_none(User, id=3)
        expected = None
        row = self.bta_cls().get_row(user)
        self.assertEqual(row, expected)

    def test_get_model_id_name(self):
        user = get_or_none(User, id=1)
        expected = {'id': '1', 'model': 'user', 'name': 'fred'}
        m_id_n = self.bta_cls().get_model_id_name(user)
        self.assertEqual(m_id_n, expected)

    def test_get_model_id_name_2(self):
        user = get_or_none(User, id=3)
        expected = {}
        m_id_n = self.bta_cls().get_model_id_name(user)
        self.assertEqual(m_id_n, expected)

    def test_get_cell(self):
        user = get_or_none(User, id=1)
        expected = {'id': '1', 'model': 'user', 'name': 'fred'}
        row = self.bta_cls().get_cell(user, 0)
        self.assertEqual(row, expected)

    def test_get_cell_99(self):
        user = get_or_none(User, id=1)
        expected = None
        row = self.bta_cls().get_cell(user, 99)
        self.assertEqual(row, expected)

    def test_get_cell_changes(self):
        old = {
                0: {'name': 'fred', 'id': '1', 'model': 'user'},
                1: 'alfa',
                2: 250,
                }
        new = old.copy()
        expected = {0: {'name': 'fred', 'id': '1', 'model': 'user'},}
        changes = self.bta_cls().get_cell_changes(old, new)
        self.assertEqual(changes, expected)

        new = old.copy()
        new[1] = 'beta'
        expected = {0: {'name': 'fred', 'id': '1', 'model': 'user'}, 1: 'beta'}
        changes = self.bta_cls().get_cell_changes(old, new)
        self.assertEqual(changes, expected)

        new = old.copy()
        new[0] = {'name': 'paul', 'id': '1', 'model': 'user'}
        new[1] = 'beta'
        expected = {0: {'name': 'paul', 'id': '1', 'model': 'user'}, 1: 'beta'}
        changes = self.bta_cls().get_cell_changes(old, new)
        self.assertEqual(changes, expected)

    def test_get_supplement_data(self):
        user = get_or_none(User, id=1)
        expected = {}
        data = self.bta_cls().get_supplement_data(user)
        self.assertEqual(data, expected)

