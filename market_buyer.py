import gdax
import yaml
import sys
import os
import argparse
from time import sleep


def to_usd(val):
    return '${:,.2f} USD'.format(float(val))


parser = argparse.ArgumentParser()
parser.add_argument('--account', required=True, help='Specify which account to use')
parser.add_argument('--coin', choices=['btc', 'bch', 'ltc', 'eth'], required=True, help='Specify which coin to buy')
args = parser.parse_args()

account = yaml.load(open(os.path.dirname(os.path.abspath(__file__)) + '/accounts/' + args.account + '.yaml', 'r'),
                    Loader=yaml.BaseLoader)

coin = args.coin.lower()
try:
    coin_buy_amount_usd = account['trading'][coin]['buy_amount_usd']
except KeyError:
    print("{} is not specified in accounts/{}.yaml.".format(coin, args.account))
    print("Exiting without buying anything.")
    sys.exit()

gdax_credentials = account['gdax']
auth_client = gdax.AuthenticatedClient(gdax_credentials['key'],
                                       gdax_credentials['secret'],
                                       gdax_credentials['passphrase'])

usd_account = auth_client.get_account(account_id=account['gdax']['accounts']['usd_id'])
if 'message' in usd_account.keys():
    print("Coinbase Pro authentication hit an error: {}".format(usd_account['message']))
    print("Exiting without buying anything.")
    sys.exit()

if float(usd_account['available']) >= float(coin_buy_amount_usd):
    print("Sufficient funds: want to buy {} of {}, have {} available.".format(to_usd(coin_buy_amount_usd),
                                                                              coin,
                                                                              to_usd(usd_account['available'])))
else:
    print("Insufficient funds: want to buy {} of {}, but only have {} available.".format(to_usd(coin_buy_amount_usd),
                                                                                         coin,
                                                                                         to_usd(usd_account['available'])))
    print("Exiting without buying anything.")
    sys.exit()

order = auth_client.buy(type='market',
                        funds=str(coin_buy_amount_usd),
                        product_id="{}-USD".format(coin.upper()))

if 'id' in order.keys():
    print("Order {} submitted for {} of {}, status is {}".format(order['id'],
                                                                 to_usd(order['specified_funds']),
                                                                 coin,
                                                                 order['status']))
    order_done = False
    seconds_to_wait_between_checks = 5
    times_to_check = 5
    times_checked = 0
    while not order_done and times_checked < times_to_check:
        sleep(seconds_to_wait_between_checks)
        print("Checking the status of order {} ...".format(order['id']))
        updated_order = auth_client.get_order(order['id'])
        times_checked += 1
        if updated_order['status'] == 'done':
            print("Order {} settled and done. {} of {} bought ({} fees paid).".format(order['id'],
                                                                                      to_usd(float(updated_order['funds'])),
                                                                                      order['product_id'],
                                                                                      to_usd(float(updated_order['specified_funds']) - float(updated_order['funds']))))
            order_done = True
        elif updated_order['status'] == 'pending':
            print("Order is {}. Let's check again in {} seconds. I'll try this {} more time{}".format(updated_order['status'],
                                                                                                      seconds_to_wait_between_checks,
                                                                                                      times_to_check - times_checked,
                                                                                                      '' if times_to_check - times_checked == 1 else 's'))
    if order_done:
        print("All done. Have a nice day.")
    else:
        print("Could not determine if the order was completed or not. Please check manually.")
else:
    print("Something went wrong.")
