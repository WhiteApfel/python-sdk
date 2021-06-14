from __future__ import absolute_import, unicode_literals
from pyfondy.resources import Resource
from datetime import datetime
from typing import Union, List

import pyfondy.helpers as helper


class Optional:
    def __init__(self):
        ...


class Checkout(Resource):
    def url(self,
            amount: Union[int, float],
            currency: str,
            order_id: Union[int, str] = None,
            order_desc: str = None,
            version: str = None,
            response_url: str = None,
            server_callback_url: str = None,
            payment_system: List[str] = None,
            default_payment_system: str = None,
            lifetime: int = None,
            merchant_data: str = None,
            preauth: bool = False,
            sender_email: str = None,
            delayed: bool = True,
            lang: str = None,
            product_id: str = None,
            required_rectoken: bool = False,
            verification: bool = False,
            verification_type: str = None,
            rectoken: str = None,
            receiver_rectoken: str = None,
            design_id: int = None,
            subscription: bool = False,
            subscription_callback_url: str = None):
        """
        Method to generate checkout url
        :param amount: order amount in NORMAL format. 10 - 10 dollars. 10.5 - 10 dollars and 50 cents
        :type amount: ``int`` or ``float
        :param currency: ``UAH``, ``RUB``, ``USD``, ``EUR``, ``GBR`` or ``CZK``
        :type currency: ``str``
        :param order_id: order id.
        :type order_id: ``int`` or ``str``, optional
        :param order_desc: order description
        :type order_desc: ``str``, optional
        :return: api response
        """
        if currency.upper() not in ['UAH', 'RUB', 'USD', 'EUR', 'GBR', 'CZK']:
            ValueError("currency must be UAH, RUB, USD, EUR, GBR or CZK")
        path = '/checkout/url/'
        order_id = str(order_id) or helper.generate_order_id()
        data = {
            'order_id': order_id,
            'order_desc': order_desc or helper.get_desc(order_id),
            'amount': int(amount * 100),
            'currency': currency,
        }
        params = self._required(data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    def token(self, amount: Union[int, float], currency: str, order_id: Union[int, str] = None, order_desc: str = None):
        """
        Method to generate checkout token
        :param amount: order amount in NORMAL format. 10 - 10 dollars. 10.5 - 10 dollars and 50 cents
        :type amount: ``int`` or ``float
        :param currency: ``UAH``, ``RUB``, ``USD``, ``EUR``, ``GBR`` or ``CZK``
        :type currency: ``str``
        :param order_id: order id.
        :type order_id: ``int`` or ``str``, optional
        :param order_desc: order description
        :type order_desc: ``str``, optional
        :return: api response
        """
        if currency.upper() not in ['UAH', 'RUB', 'USD', 'EUR', 'GBR', 'CZK']:
            ValueError("currency must be UAH, RUB, USD, EUR, GBR or CZK")
        path = '/checkout/token/'
        order_id = str(order_id) or helper.generate_order_id()
        data = {
            'order_id': order_id,
            'order_desc': order_desc or helper.get_desc(order_id),
            'amount': int(amount * 100),
            'currency': currency
        }
        params = self._required(data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    def verification(self, data):
        """
        Method to generate checkout verification url
        :param data: order data
        :return: api response
        """
        path = '/checkout/url/'
        verification_data = {
            'verification': 'Y',
            'verification_type': data.get('verification_type', 'code')
        }
        data.update(verification_data)
        params = self._required(data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    def subscription(self, data):
        """
        Method to generate checkout url with calendar
        :param data: order data
        data = {
            "currency": "UAH", -> currency ('UAH', 'RUB', 'USD')
            "amount": 10000, -> amount of the order (int)
            "recurring_data": {
                "every": 1, -> frequency of the recurring order (int)
                "amount": 10000, -> amount of the recurring order (int)
                "period": 'month', -> period of the recurring order ('day', 'month', 'year')
                "start_time": '2020-07-24', -> start date of the recurring order ('YYYY-MM-DD')
                "readonly": 'y', -> possibility to change parameters of the recurring order by user ('y', 'n')
                "state": 'y' -> default state of the recurring order after opening url of the order ('y', 'n')
            }
        }
        :return: api response
        """
        if self.api.api_protocol != '2.0':
            raise Exception('This method allowed only for v2.0')
        path = '/checkout/url/'
        recurring_data = data.get('recurring_data', '')
        subscription_data = {
            'subscription': 'Y',
            'recurring_data': {
                'start_time': recurring_data.get('start_time', ''),
                'amount': recurring_data.get('amount', ''),
                'every': recurring_data.get('every', ''),
                'period': recurring_data.get('period', ''),
                'readonly': recurring_data.get('readonly', ''),
                'state': recurring_data.get('state', '')
            }
        }

        helper.check_data(subscription_data['recurring_data'])
        self._validate_recurring_data(subscription_data['recurring_data'])
        subscription_data.update(data)
        params = self._required(subscription_data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    @staticmethod
    def _validate_recurring_data(data):
        """
        Validation recurring data params
        :param data: recurring data
        :return: exception
        """
        try:
            datetime.strptime(data['start_time'], '%Y-%m-%d')
        except ValueError:
            raise ValueError(
                "Incorrect date format. 'Y-m-d' is allowed")
        if data['period'] not in ('day', 'week', 'month'):
            raise ValueError(
                "Incorrect period. ('day','week','month') is allowed")

    def _required(self, data):
        """
        Required data to send
        :param data:
        :return: parameters to send
        """
        self.order_id = data.get('order_id') or helper.generate_order_id()
        order_desc = data.get('order_desc') or helper.get_desc(self.order_id)
        params = {
            'order_id': self.order_id,
            'order_desc': order_desc,
            'amount': data.get('amount', ''),
            'currency': data.get('currency', '')
        }
        helper.check_data(params)
        params.update(data)

        return params
