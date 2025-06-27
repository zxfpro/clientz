# clientz

# 正式启动
<!-- cd src; python -m clientz.server 8008 -->
python -m clientz.server --prod

# 测试启动
python -m src.clientz.server
python -m src.clientz.server --dev

基本只需要修改
core.py 
config.yaml

注意间接导入的faiss
