import yaml

# 读取 YAML 配置文件
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

print(type(config))

# 打印读取后的内容
print(config.keys())
print(config['workspace'].keys())
print(config['workspace']['test_key'])
print(config['workspace']['test_list'])

print(config['graph_name'])

print(type(config['stage']), len(config['stage']))
print(config['stage'][0])

# python parse_yaml.py 
# 输出：
# <class 'dict'>
# dict_keys(['workspace', 'graph_name', 'stage', 'data_configs'])
# dict_keys(['test_key', 'test_list', 'pythonpath', 'pip'])
# test_value
# [1, 2, 3]
# LayerPdGraphPool
# <class 'list'> 4
# [{'name': 'PdDpbagExtractorNode'}]
