# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os, pprint
# from django.http import QueryDict
from django.test import TestCase
from easyrequest_app.models import LoginHelper, PatronApiHelper


login_helper = LoginHelper()


class LoginHelperTest( TestCase ):
    """ Tests models.LoginHelper() """

    def test__get_referrer_host( self ):
        """ Tests extract of host from full referrer url. """
        referrer_url = 'http://josiah.brown.edu/search~S7?/tDeath+Without+Weeping%3A+The+Violence+of+Everyday+Life+in+Brazil/tdeath+without+weeping+the+violence+of+everyday+life+in+brazil/1%2C1%2C4%2CB/frameset&FF=tdeath+without+weeping+the+violence+of+everyday+life+in+brazil&2%2C%2C4   '
        self.assertEqual(
            'josiah.brown.edu',
            login_helper.get_referrer_host(referrer_url) )
        referrer_url = 'foo'
        self.assertEqual(
            '',
            login_helper.get_referrer_host(referrer_url) )

    def test__process_items( self ):
        """ Tests extract from api lookup on bib. """
        item_barcode = '31236074994859'
        api_dct = {
         u'query': {u'timestamp': u'2019-09-05 13:22:12.841357',
                    u'url': u'https://library.brown.edu/availability_api/v2/bib_items/b6150593/'},
         u'response': {u'bib': {u'author': u'Richardson, Mark, 1962- author',
                                u'title': u'Zen and now : on the trail of Robert Pirsig and Zen and the art of motorcycle maintenance',
                                u'url': u'https://search.library.brown.edu/catalog/b6150593'},
                       u'items': [{u'barcode': u'31236074994859',
                                   u'callnumber': u'CT275.P648 R53 2008',
                                   u'item_id': u'i165116687',
                                   u'location': u'ANNEX',
                                   u'status': u'AVAILABLE'}],
                       u'items_count': 1,
                       u'sierra_api': u'SNIP (irrelevant for test)',
                       u'sierra_api_query': u'https://catalog.library.brown.edu:443/iii/sierra-api/v5/bibs/?id=6150593',
                       u'time_taken': u'0:00:00.493448'}
        }
        self.assertEqual(
            ( 'CT275.P648 R53 2008', 'i16511668' ),
            login_helper.process_items( api_dct, item_barcode )
            )

    # def test__process_items( self ):
    #     """ Tests extract from api lookup on bib. """
    #     item_barcode = '31236074994859'
    #     api_dct = {
    #         'query': {
    #             'query_key': 'bib',
    #             'query_timestamp': '2015-08-31 15:33:28.988222',
    #             'query_value': 'b6150593',
    #             'url': 'https://library.brown.edu/availability_service/v2/bib/b6150593/'},
    #         'response': {
    #             'backend_response': [ {
    #                 'bibid': '.b61505936',
    #                 'callnumber': 'CT275.P648 R53 2008',
    #                 'holdings_data': [ {
    #                     'callNumber': 'CT275.P648 R53 2008 ',
    #                     'localLocation': 'ANNEX',
    #                     'publicNote': 'AVAILABLE'}],
    #                 'isbn': '9780307269706',
    #                 'issn': 'issn_not_available',
    #                 'items_data': [ {
    #                     'barcode': '31236074994859',
    #                     'callnumber': None,
    #                     'callnumber_interpreted': 'CT275.P648 R53 2008 None',
    #                     'item_id': 'i165116687',
    #                     'itype': '0',
    #                     'itype_interpreted': 'coming',
    #                     'location': 'qs',
    #                     'location_interpreted': 'coming',
    #                     'status': '-',
    #                     'status_interpreted': 'coming'}],
    #                 'josiah_bib_url': 'https://josiah.brown.edu/record=b6150593',
    #                 'lccn': '2008017156',
    #                 'oclc_brown': 'ocn226308091',
    #                 'title': 'Zen and now : on the trail of Robert Pirsig and Zen and the art of motorcycle maintenance /'}],
    #             'response_timestamp': '2015-08-31 15:33:29.034138'}
    #         }
    #     self.assertEqual(
    #         ( 'CT275.P648 R53 2008', 'i16511668' ),
    #         login_helper.process_items( api_dct, item_barcode )
    #         )

    # end class class LoginHelperTest


class PatronApiHelperTest( TestCase ):
    """ Tests models.PatronApiHelper() """

    def test__instantiation_good( self ):
        """ Tests instantition on good barcode.
            Note:  will only work if patron-api is configured to accept incoming request from test-IP,
                   but if developing locally, that should be done anyway. """
        TEST_PATRON_BARCODE = unicode( os.environ['EZRQST__TEST_PATRON_BARCODE'] )
        TEST_PATRON_API_NAME = unicode( os.environ['EZRQST__TEST_PATRON_API_NAME'] )
        print 'TEST_PATRON_API_NAME...'; print TEST_PATRON_API_NAME
        papi_helper = PatronApiHelper( TEST_PATRON_BARCODE )
        self.assertEqual(
            TEST_PATRON_API_NAME,
            papi_helper.patron_name
            )

    # end class PatronApiHelperTest
