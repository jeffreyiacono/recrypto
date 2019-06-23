# Recrypto
Recrypto enables submission of market orders via Coinbase Pro (formerly
GDAX) APIs. If you configure this to run periodically, you can easily set up a
dollar cost averaging investment process for a wide varity of crypto assets.

## Background
Coinbase recently posted an artcile titled [When is the “perfect time” to buy
cryptocurrency?](https://blog.coinbase.com/when-is-the-perfect-time-to-buy-cryptocurrency-e583a18f130b)
where the author covers the concept of dollar cost averaging. In a nutshell,
this concept centers around periodic and incremental purchases of an underlying
asset. Coinbase also highlights how you can [get started
today](https://www.coinbase.com/signup?utm_medium=oss&utm_source=recrypto&utm_campaign=recurring_buys),
but I want to share an alternative: you can run your own software to do this for
you (ie. the code found in this repo!). **Disclaimer:** This is not investment
advice. Use this software at your own risk.

Why may you want to do this?
- You can save (a little) money in the long run: Coinbase appears to charge
  $0.99 / recurring buy, while running this script uses Coinbase Pro (formly
  GDAX) so you'll typically only pay fees of [0.05% to
  0.25%](https://support.pro.coinbase.com/customer/en/portal/articles/2945310-fees).
  If you were buying $10.00 USD of BTC per day, that's $0.99 per day in fees vs fees
  that would range from $0.01 to $0.03 in my experience. You do need a computer
  to run this for you, but you can host it somewhere or buy a
  [pi](https://www.raspberrypi.org/) (which is what I've been doing for the past
  few years)
- You'll probably have fun! You'll likely learn something by setting this up and
  running it on your own. You can also help improve it, just send me a pull
  request. This was my first attempt at writing anything in Python, so there is
  probably loads to improve upon.

## Setup
### Coinbase Pro API Access
Assuming you already have a Coinbase account, next you need to set up an API
access.
1. Go to [API settings](https://pro.coinbase.com/profile/api) on Coinbase Pro,
   which is under Account (your name) > API > API Settings
1. Tap on "+ New API Key" and ensure you select the "View" and "Trade"
   permissions

Ensure that you've funded the account, otherwise the script will submit a buy
order, and you'll have no funds to use!

### Get Recrypto Code
```
$ git clone https://github.com/jeffreyiacono/recrypto
```

### Set Up The Virtual Environment & Install Required Packages
```
$ cd recrypto
$ pip3 install virtualenv
$ virtualenv vrecrypto
$ source vrecrypto/bin/activate
$ pip3 install -r requirements.txt
```

### Configure Account Details
When you set up API Access, you were given a passphrase, key, secret, and account ID.
Using `recrypto/accounts/template.yaml` as a starting point, change the filename to to
your name (or whatever you'd like) and enter in your account's details. **DO
NOT SHARE THOSE WITH ANYONE ELSE.**

You can also set up the USD amount you'd like to purchase on each run. It is currently
set to $10.00 USD as that is the minimum order Coinbase Pro will accept as of 2018 (as
far as I recall).

### Test It Out
**Note that running the following, if set up properly, will submit a request to
buy a given coin and will buy the amount you've specified in your account template.**

For example, if you have used `recrypto/accounts/template.yaml` and `cp` it to
`recrypto/accounts/jeff.yaml` and set it up as follows:

```
# recrypto/accounts/jeff.yaml
gdax:
  passphrase: 'some-passphrase'
  key: 'some-key'
  secret: 'some-secret'
  accounts:
    usd_id: 'some-account-usd-id'
trading:
  btc:
    buy_amount_usd: 20
```
and I run:
```
$ python3 market_buyer.py --account=jeff --coin=btc
```
It will kick off a request to Coinbase Pro to purchase $20.00 USD in BTC.

### Set It and Forget It
Lastly, if you want to have this purchase on your behalf, you'll need to instruct
your computer to run this script at whatever time intervals you'd like.

You can use something like `cron` to do this, and there is an example file
provided within the repo called `crontab-example`

# Like This?
Buy me a coffee! Send bitcoin to the following address:
`1AYG93PW5zL7YLyGkevGvPGQHmxYpGnv6m`

Or scan the following QR code if you have a bitcoin wallet on your mobile
device:

![1AYG93PW5zL7YLyGkevGvPGQHmxYpGnv6m](https://raw.githubusercontent.com/jeffreyiacono/penalty-blox/master/images/1AYG93PW5zL7YLyGkevGvPGQHmxYpGnv6m.png)

# MIT License
Copyright (c) 2019 Jeff Iacono

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
