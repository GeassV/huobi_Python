# coding: utf-8
# map of username: ["api_key", "secret_key"]
# username不重要，仅用于帮助个人记忆
# api_key和secret_key请保证正确有效和具有相关操作的权限
API_DICT = {
    # "username1": ["api_key1", "secret_key1"],
    # "username2": ["api_key2", "secret_key2"],
}

# usdt Trc20提现地址，请务必确保正确
WITHDRAW_ADDRESS = ""

# 默认提现配置, 不用管
"""
"""
DEFAULT_WITHDROW_CONFIG = {
    "usdt": {
        "address": "",
        "amount": 50.0,
        "currency": "usdt",
        "chain": "trc20usdt",
        "fee": 0,
        "left_amount": 0,
    },
    "ht": {
        "address": "",
        "amount": 40.0,
        "currency": "ht",
        "chain": "",
        "fee": 0,
        "left_amount": 0,
    }
}