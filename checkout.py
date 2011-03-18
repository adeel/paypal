'''
For express checkout transactions.  Uses the Paypal Express Checkout API.
Review Paypal's guide <http://bit.ly/hI6m7C> to see how exactly the process
works.
'''

import patcollins_paypal

def get_authorization_url(amount=None,
  return_url=None, cancel_url=None, options={}):
  '''
  Call this to start the checkout.  This calls the Paypal API to get the
  token and returns the Paypal URL for logging in and authorizing the
  payment.  Redirect the user to this URL.
  
  Note that `amount` should be provided either as a float or as a string with
  exactly two digits after the decimal point.
  
  The dictionary `options` should contain the Paypal API credentials: email,
  username, password, signature, environment.  The environment is 'sandbox'
  or 'production'.
  '''

  client = _setup_patcollins_client(options)
  response = client.set_express_checkout(amt='%.2f' % amount,
    returnurl=return_url, cancelurl=cancel_url,
    paymentaction='Authorization', email=options['email'])
  if not response.success:
    return False

  return _get_authorization_url(options) % response.token

def execute(amount, token, payer_id, options={}):
  '''
  Executes the transaction.  Paypal should give you the payer id and token
  as query string parameters to your return URL.
  
  Returns the response from Paypal in case you want it.
  '''

  client = _setup_patcollins_client(options)

  try:
    response = client.do_express_checkout_payment(token,
      paymentaction='Authorization', payerid=payer_id, amt='%.2f' % amount)
  except:
    return False
  if not response.success:
    return False

  return response

def _setup_patcollins_client(_options):
  options = {'environment': 'sandbox'}
  options.update(_options)

  return patcollins_paypal.PayPalInterface(
    API_USERNAME=options['username'],
    API_PASSWORD=options['password'],
    API_SIGNATURE=options['signature'])

def _get_authorization_url(options):
  if options['environment'] == 'sandbox':
    return ('https://www.sandbox.paypal.com'
            '/webscr?cmd=_express-checkout&token=%s')
  else:
    return ('https://www.paypal.com'
            '/webscr?cmd=_express-checkout&token=%s')
