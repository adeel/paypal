'''
Uses Paypal's Adaptive Payments API <https://www.x.com/docs/DOC-1414> to send
money.  Only the Pay operation is implemented here.
'''

import json
import urllib2

def send(amount, recipient, sender=None, return_url=None, cancel_url=None,
  options={}):
  '''
  Note that `amount` should be provided either as a float or as a string with
  exactly two digits after the decimal point.  `recipient` should be the
  e-mail address of the recipient.  Specify `sender` if this is an implicit
  approval payment.
  
  The dictionary `options` should contain the Paypal API credentials: app_id,
  email, username, password, signature, environment.  The environment is
  'sandbox' or 'production'.
  
  Returns the Paypal URL for logging in and approving the payment.  You don't
  need that if this is an implicit approval payment.
  '''
  headers = {
    'X-PAYPAL-APPLICATION-ID': options['app_id'],
    'X-PAYPAL-SECURITY-USERID': options['username'],
    'X-PAYPAL-SECURITY-PASSWORD': options['password'],
    'X-PAYPAL-SECURITY-SIGNATURE': options['signature'],
    'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
    'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON'
  }

  data = {'actionType': 'PAY',
    'returnUrl': return_url, 'cancelUrl': cancel_url,
    'requestEnvelope': {'errorLanguage': 'en_US'}, 'currencyCode': 'USD',
    'receiverList': {'receiver': [
      {'email': recipient, 'amount': '%.2f' % amount}]}}

  if sender:
    data.update({'senderEmail': sender})

  request = urllib2.Request(_get_api_url(options), headers=headers,
    data=json.dumps(data))

  response = json.loads(urllib2.urlopen(request).read())
  if response['responseEnvelope']['ack'] != 'Success':
    return False

  return _get_payment_url(options) % response['payKey']

def _get_api_url(options):
  if options['environment'] == 'sandbox':
    return 'https://svcs.sandbox.paypal.com/AdaptivePayments/Pay'
  else:
    return 'https://svcs.paypal.com/AdaptivePayments/Pay'

def _get_payment_url(options):
  if options['environment'] == 'sandbox':
    return 'https://www.sandbox.paypal.com/webscr?cmd=_ap-payment&paykey=%s'
  else:
    return 'https://www.paypal.com/webscr?cmd=_ap-payment&paykey=%s'
