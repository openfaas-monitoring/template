# template
openfaas函数部署的定制化模板

在template文件夹下的python3-logger模板提供日志输出和记录服务
- 允许记录函数开始节点，使用`logger.info(started)`
- 允许记录函数调用节点，使用`logger.info(invoke function_name)`
