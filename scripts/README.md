说明：
1. 请使用python3

操作指南:
1. 进入下载的文件目录(/xxx/xxx/huobi_Python/), 执行:
export PYTHONPATH=$PYTHONPATH:${PWD}

pip install -r requirement

2. 编辑scripts目录下的apikeys.py文件, 编辑配置(其他配置不用管): API_DICT 和 WITHDRAW_ADDRESS
备注:
API_DICT是你的货币账号API TOKEN, 在网页版货币账号的API管理中创建，有效期90天
WITH_ADDRESS 是你的 trc20 usdt的提取目标地址，请务必保证正确性

3. 执行:
python3 scripts/main.py