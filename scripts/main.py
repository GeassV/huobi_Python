from huobi.client.account import AccountClient
from huobi.constant import *
from huobi.utils import LogInfo
from huobi.client.generic import *
from huobi.client.market import *
from huobi.client.trade import *
from huobi.client.wallet import WalletClient
from huobi.constant import *
from huobi.utils import *
from huobi.client.account import AccountClient
from huobi.client.trade import TradeClient
from huobi.utils import *
import datetime
from scripts.apikeys import API_DICT, WITHDRAW_ADDRESS

# Create generic client instance and get the timestamp
generic_client = GenericClient()
ts = generic_client.get_exchange_timestamp()
timearray = time.localtime(ts / 1000)
localtime = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
print("server time:%s" % localtime)
# 获得当前时间时间戳
now = int(time.time())
# 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
timeArray = time.localtime(now)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print("local time:%s" % otherStyleTime)


def run():
    funcs = """
功能列表:
1.显示余额
2.usdt提现
3.设置交易(暂未支持) 
请选择(1 or 2): """
    func = int(input(funcs))
    if func > 2 or func < 1:
        print("不支持的功能选项")
        return

    if func == 1:
        operate_accounts([], 1)
    if func == 2:
        amount = float(input("usdt提现数额:"))
        print("提现地址: " + WITHDRAW_ADDRESS)
        addr_check = (input("请确认以上提现地址(y/n): "))
        if addr_check != "y":
            return
        operate_accounts([], 2, amount)


def operate_accounts(api_dict_all, func, amount=10):
    if len(api_dict_all) == 0:
        api_dict_all = API_DICT
    count = 0
    # 展示余额
    for i in api_dict_all.keys():
        count += 1
        print("------------------------第%s个账号：%s操作详情-------------------" % (count, i))
        ak = api_dict_all[i][0]
        sk = api_dict_all[i][1]
        if func == 1:
            show_account_balance(ak, sk)
        elif func == 2:
            withdraw_balance(ak, sk, amount)


"""
查看账户的余额
memo:
format of accounts_data: 
{'id': 36318210, 'type': 'point', 'state': 'working', 'subtype': ''}
{'id': 36456129, 'type': 'spot', 'state': 'working', 'subtype': ''}
format of balance coins:
{'currency': 'ht', 'type': 'trade', 'balance': '301.396'}
{'currency': 'ht', 'type': 'frozen', 'balance': '0'}
{'currency': 'usdt', 'type': 'trade', 'balance': '198.1875156811188'}
{'currency': 'usdt', 'type': 'frozen', 'balance': '0'}
"""


def show_account_balance(ak="", sk=""):
    if ak == "" or sk == "":
        print("获取余额失败: 账号或秘钥缺失")
    account_client = AccountClient(api_key=ak, secret_key=sk)
    try:
        # 千万不要用get_account_balance 方法, 低效且容易触发频控
        # account_balance_list = account_client.get_account_balance()
        # get_account: return the list of accounts data
        accounts_data = account_client.get_accounts()
        for data in accounts_data:
            if data.id and data.type == "spot":
                all_coins = account_client.get_balance(account_id=data.id)
                available_coins = []
                for coin in all_coins:
                    if coin.balance != '0':
                        available_coins.append(coin)
                # coin数量排序
                available_coins = sorted(available_coins, key=lambda item: item.balance, reverse=True)
                for coin in available_coins:
                    print(coin.currency + ":" + coin.balance)
    except Exception as err:
        print("获取余额失败:" + str(err))


# 账户提现
def withdraw_balance(ak="", sk="", amount=10):
    if ak == "" or sk == "":
        print("提现失败: 账号或秘钥缺失")
    account_client = AccountClient(api_key=ak, secret_key=sk)
    try:
        # 千万不要用get_account_balance 方法, 低效且容易触发频控
        # account_balance_list = account_client.get_account_balance()
        # get_account: return the list of accounts data
        accounts_data = account_client.get_accounts()
        for data in accounts_data:
            if data.id and data.type == "spot":
                all_coins = account_client.get_balance(account_id=data.id)
                for coin in all_coins:
                    # 提币规则：提USDT 而且余额大于52U就提币
                    if coin.currency == "usdt" and coin.balance != '0' and float(coin.balance) > 52:
                        print(coin.currency + ":" + coin.balance)
                        wallet_client = WalletClient(api_key=ak, secret_key=sk)
                        withdraw_id = wallet_client.post_create_withdraw(
                            address=WITHDRAW_ADDRESS,  # 提币地址需要在交易所提前存好
                            amount=amount,  # 提币数量
                            currency="usdt",
                            fee=0,  # amount提币数量，fee trc20usdt可以填0
                            chain="trc20usdt",
                            address_tag=None
                        )  # chain就是提币方式

    except Exception as err:
        print("提现失败:" + str(err))
    else:
        print("提现申请提交成功,请查看账号")


## TODO: to implement
def trade_application(api_dict_all):
    # Create generic client instance and get the timestamp
    generic_client = GenericClient()
    ts = generic_client.get_exchange_timestamp()
    timearray = time.localtime(ts / 1000)
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
    print("server time:%s" % localtime)
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print("local time:%s" % otherStyleTime)

    g_account_id_list = []
    count = 0
    for i in api_dict_all.keys():
        count += 1
        g_api_key = api_dict_all[i][0]
        g_secret_key = api_dict_all[i][1]
        print("------------------------第%s个账号：%s账号详情-------------------" % (count, i))
        try:
            trade_client = TradeClient(api_key=g_api_key, secret_key=g_secret_key)
            account_client = AccountClient(api_key=g_api_key, secret_key=g_secret_key)
            # 千万不要用get account balance！！！！！！！！！！
            # account_balance_list = account_client.get_account_balance()
            list_obj = account_client.get_accounts()
            for new in list_obj:
                if new.type == "spot":
                    print(new.id)
                    symbol_test = "erthausdt"  # 交易对名
                    account_id = new.id
                    order_id = trade_client.create_order(symbol=symbol_test, account_id=account_id,
                                                         order_type=OrderType.SELL_MARKET, source=OrderSource.API,
                                                         # order_type这边是市价卖出
                                                         amount=205.52,  # 交易量
                                                         price=None)  # 市价可以不填price
                    LogInfo.output("created order id : {id}".format(id=order_id))

        except Exception as e:
            print(e)


# def tryTradeOrder(account_client):
#     try:
#         list_obj = account_client.get_accounts()
#     except Exception as e:
#         print(e)
#
#     for new in list_obj:
#         if new.id:
#             g_account_id_list.append(new.id)
#             g_account_id1 = g_account_id_list[-1]
#             list_obj = account_client.get_balance(account_id=g_account_id1)
#         if new.type == "spot":
#             print(new.id)
#             symbol_test = "diousdt"
#             account_id = new.id
#             order_id = trade_client.create_order(symbol=symbol_test, account_id=account_id,
#                                                  order_type=OrderType.SELL_MARKET, source=OrderSource.API,
#                                                  amount=63.01,
#                                                  price=None)
#             LogInfo.output("created order id : {id}".format(id=order_id))


#                for x in list_obj:
# if x.type=='trade' and x.currency=='usdt' and float(x.balance) >50 and
#                    if float(x.balance)!=0:
#                        print(x.currency+":"+x.balance)
#                        wallet_client = WalletClient(api_key=g_api_key, secret_key=g_secret_key)
#                        for d in wallet_client.get_account_deposit_address(currency='usdt'):
#                            if d.chain=='hrc20usdt':
#                                print(d.address)

#    LogInfo.output("====== (SDK encapsulated api) not recommend for low performance and frequence limitation ======")


# if x.balance != "0" and x.currency == "usdt":
#     print(x.currency + ":" + x.balance)
#     currency = x.balance
#     fixed_currency = str(round(float(currency), 2) - 0.01)
#     print(fixed_currency)
#     """
#
#     """
#     try:
#         wallet_client = WalletClient(api_key=g_api_key, secret_key=g_secret_key)
#         withdraw_id = wallet_client.post_create_withdraw(address="TLxeqa52MGHDHiFSwjCVrhuiiVqyqDP2pc",
#                                                          amount=fixed_currency, currency="usdt", fee=0,
#                                                          chain="trc20usdt", address_tag=None)
#     except Exception as e:
#         print(e)
"""
#    withdraw_id_ret = wallet_client.post_cancel_withdraw(withdraw_id=withdraw_id)
#    LogInfo.output("Cancel Withdraw {withdraw_id}, {response_id}".format(withdraw_id=withdraw_id, response_id=withdraw_id_ret))

"""
# 列表对象里才是数据需要过一个循环然后去找model里面的数据
# 下单功能
if __name__ == '__main__':
    run()
