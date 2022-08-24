# template

存放openfaas函数部署的定制化模板，模板存放在`template`中，包括python3-logger和python3-dynamic

## python3-logger

该模板给用户函数提供了日志输出的功能，用户应该在`handler.py`中定义如下的函数：

```python
def handle(req, logger):
    """handle a request to the function
    Args:
        req (str): request body
        logger: print log into stderr
    """
    logger.info("started")
    logger.info("invoke function1")
    return req
```

- 其中req表示通过http接收的参数
- logger为模板提供的日志输出工具，通过`logger.info("message")`进行日志输出

## python3-dynamic

该模板给用户提供了基于函数列表文件以及流程配置文件来构建openfaas函数的功能。在`handler.py`中定义函数列表，在`process-cfg.json`中定义函数工作流程。

`handler.py`中定义的函数应该具有如下的格式：

```python
from function import globalFlag


def function1(args):
    args['res'] = args['std_in']
    return args


def function2(args):
    # ...
    return args


```

- `from function import globalFlag`为必须引入的模块，不可修改
- 每个函数都只有一个参数args，为一个dict字典
- 每个函数的返回值也是dict字典
- 通过http获取的函数输入参数存放在`args['std_in']`中
- 需要最终返回的结果应该存放在`args['res']`中

`process-cfg.json`中定义的流程配置应该具有如下的格式：

```json
{
  "name": "paralleltest",
  "global": [],
  "extra_threads": ["thread1"],
  "thread_process": {
    "main": [
      {
        "func_name": "join",
        "type": "order",
        "wait_threads": [
          "thread2",
          "thread3"
        ],
        "condition": "",
        "next_func_true": "function2",
        "next_func_false": ""
      },
      {
        "func_name": "function2",
        "type": "order",
        "condition": "",
        "next_func_true": "",
        "next_func_false": ""
      }
    ],
    "thread1": [
      {
        "func_name": "function1",
        "type": "order",
        "condition": "",
        "next_func_true": "",
        "next_func_false": ""
      }
    ]
  }
}
```
- `name`字段中定义在openfaas平台部署的函数名称，为一个字符串

- `global`字段中定义全局布尔变量，通过一个二维列表分别定义名称和初始值

- 流程配置一共提供四类流程：并行、顺序、分支和循环

- 并行的实现通过`extra_threads`来定义，这是一个列表，其中定义了需要额外启动的线程名称

- 在`thread_process`中定义了各个线程的执行流程。这是一个字典，Key为线程名称，Value为线程执行流程。其中必须有一个`main`线程；而如果配置了`extra_threads`，则对应在该字典中要定义相应的Key

- 每个线程对应的执行流程，通过一个列表来定义，列表中每个元素又是一个字典，格式如下：

  ```json
  {
      "func_name": "",
      "type": "",
      "condition": "",
      "next_func_true": "",
      "next_func_false": ""
  }
  ```

  - `func_name`表示当前运行函数的名称，也可以设置为join。如果设置为join，则表示线程之间的同步关系，需要同时设置`wait_threads`字段
  - `type`表示函数流程的类型，可选项为`order,loop,branch`，分别代表顺序、循环和分支结构
  - `condition`在循环和分支类型下有效，并且值需要出现在全局布尔变量列表中
  - 在顺序结构下，通过`next_func_true`指定下个运行的函数
  - 在循环和分支结构下，通过`next_func_true`和`next_func_false`来指定不同情况下运行的函数

# example

在example中，分别列举了不同运行流程的具体配置参考。其中order、branch、loop都采用单线程配置，parallel采用多线程配置

## order

在order例子中，主线程依次运行function1、function2、function3、function4、function5

## branch

在branch例子中，主线程先运行function1，然后通过flag1的值来判断下一个函数是运行function2还是function3

## loop

在loop例子中，主线程先运行function1，然后循环运行function2，通过flag1的值来判断是否退出循环，退出循环后运行function3

## parallel

在parallel例子中，需要额外启动三个线程，分别为thread1、thread2和thread3

主线程等待thread2和thread3的运行完成，然后运行function4

thread1无需等待任何线程的运行，直接运行function1

thread2需要等待thread1的运行，然后循环运行function2

thread3需要等待thread1的运行，然后分支运行function3或者function5

# openfaas平台部署

在openfaas平台上的部署操作如下

```shell
faas-cli new xxx --lang python3-dynamic -p yyy

...修改对应文件夹中的handler.py文件和process-cfg.json配置文件

faas-cli build -f ./xxx.yml

docker push yyy/xxx

faas-cli deploy -f xxx.yml 

```
在最后deploy阶段可以通过`-e`选项来指定环境变量，如`-e write_debug=true`,`-e read_timeout=100`,`-e write_timeout=100`等。具体环境变量可以参考openfaas中of-watchdog。

