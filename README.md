# MOSS

## 使用方法

- 克隆仓库

    ```shell
    git clone git@github.com:zhuxihuaizuo/MOSS.git
    ```

- 使用pycharm创建python虚拟环境，并安装依赖

    ```shell
    pip install -r requirements.txt
    ```

- 配置env环境

    - 去除文件.env.template的.template后缀，得到.env文件
    - 填入自己的api key等相关配置信息
    - 注意代理端口的配置根据需要进行
    - 可以通过注释代码中`set_xxx_proxy()`函数来取消某些接口的代理

- 运行main.py以测试项目运行结果，可以适当修改输入测试不同的AI功能

- 运行app.py运行api接口服务



## 接口说明

- 本项目接口依赖fastapi库进行开发

1. 与travel master聊天

    路由：/chat

    方法：post

    参数：

    | 参数         | 说明                                                         |
    | ------------ | ------------------------------------------------------------ |
    | chat_id      | 创建新的聊天时，chat_id置为空字符串<br />希望在同一次聊天中多轮对话，需要前端在创建聊天后保存chai_id，在请求时将chat_id置为保存的值 |
    | query        | 用户的提问                                                   |
    | current_time | 现在的时间（目前这个值由后端自行生成不需要传入）             |
    | position     | 用户的位置，用地址描述用户的位置                             |

    返回值

    - 返回值的统一格式如下

        ```
        {
        	"action": string, \\ 动作提示，标记返回值的含义
            "action_input": string, \\ 返回值
        }
        ```

    - 不同action的含义

        | action       | 含义                                              | 流式返回 |
        | ------------ | ------------------------------------------------- | -------- |
        | Final Answer | 最终提交给用户的回答                              | 是       |
        | New Question | 根据用户的问题提出的新的相关问题，每次交互返回3个 | 否       |
        | 其他         | AI调用工具的应答信息                              | 否       |

        > 流式返回：action_input每次只携带一个token，所有的token组后后是完整的回答
        >
        > 非流式返回：action_input携带完整的信息

    - 示例

        ```
        问题：天安门附近的饭店
        返回值（实际的输出没有换行和注释，这里方便阅读进行了处理）：
        // AI调用Sight Search工具搜索‘天安门附近的饭店’
        {"action": "Sight Search", "action_input": "天安门附近的饭店"}
        // AI给出答复
        {"action": "Final Answer", "action_input": "以下"}
        {"action": "Final Answer", "action_input": "是"}
        {"action": "Final Answer", "action_input": "天"}
        {"action": "Final Answer", "action_input": "安"}
        {"action": "Final Answer", "action_input": "门"}
        {"action": "Final Answer", "action_input": "附"}
        {"action": "Final Answer", "action_input": "近"}
        {"action": "Final Answer", "action_input": "的"}
        {"action": "Final Answer", "action_input": "饭"}
        {"action": "Final Answer", "action_input": "店"}
        {"action": "Final Answer", "action_input": "列表"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "\n"}
        {"action": "Final Answer", "action_input": "1"}
        {"action": "Final Answer", "action_input": "."}
        {"action": "Final Answer", "action_input": "名称"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "程"}
        {"action": "Final Answer", "action_input": "府"}
        {"action": "Final Answer", "action_input": "宴"}
        {"action": "Final Answer", "action_input": "("}
        {"action": "Final Answer", "action_input": "南"}
        {"action": "Final Answer", "action_input": "长"}
        {"action": "Final Answer", "action_input": "街"}
        {"action": "Final Answer", "action_input": "店"}
        {"action": "Final Answer", "action_input": ")"}
        {"action": "Final Answer", "action_input": " 地"}
        {"action": "Final Answer", "action_input": "址"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "北京"}
        {"action": "Final Answer", "action_input": "市"}
        {"action": "Final Answer", "action_input": "西"}
        {"action": "Final Answer", "action_input": "城"}
        {"action": "Final Answer", "action_input": "区"}
        {"action": "Final Answer", "action_input": "南"}
        {"action": "Final Answer", "action_input": "长"}
        {"action": "Final Answer", "action_input": "街"}
        {"action": "Final Answer", "action_input": "38"}
        {"action": "Final Answer", "action_input": "号"}
        {"action": "Final Answer", "action_input": "\n"}
        {"action": "Final Answer", "action_input": "2"}
        {"action": "Final Answer", "action_input": "."}
        {"action": "Final Answer", "action_input": "名称"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "东"}
        {"action": "Final Answer", "action_input": "门"}
        {"action": "Final Answer", "action_input": "烤"}
        {"action": "Final Answer", "action_input": "鸭"}
        {"action": "Final Answer", "action_input": "店"}
        {"action": "Final Answer", "action_input": "("}
        {"action": "Final Answer", "action_input": "东"}
        {"action": "Final Answer", "action_input": "华"}
        {"action": "Final Answer", "action_input": "门"}
        {"action": "Final Answer", "action_input": "店"}
        {"action": "Final Answer", "action_input": ")"}
        {"action": "Final Answer", "action_input": " 地"}
        {"action": "Final Answer", "action_input": "址"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "北京"}
        {"action": "Final Answer", "action_input": "市"}
        {"action": "Final Answer", "action_input": "东"}
        {"action": "Final Answer", "action_input": "城"}
        {"action": "Final Answer", "action_input": "区"}
        {"action": "Final Answer", "action_input": "东"}
        {"action": "Final Answer", "action_input": "华"}
        {"action": "Final Answer", "action_input": "门"}
        {"action": "Final Answer", "action_input": "大"}
        {"action": "Final Answer", "action_input": "街"}
        {"action": "Final Answer", "action_input": "56"}
        {"action": "Final Answer", "action_input": "号"}
        {"action": "Final Answer", "action_input": "\n"}
        {"action": "Final Answer", "action_input": "3"}
        {"action": "Final Answer", "action_input": "."}
        {"action": "Final Answer", "action_input": "名称"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "全"}
        {"action": "Final Answer", "action_input": "聚"}
        {"action": "Final Answer", "action_input": "德"}
        {"action": "Final Answer", "action_input": "("}
        {"action": "Final Answer", "action_input": "天"}
        {"action": "Final Answer", "action_input": "安"}
        {"action": "Final Answer", "action_input": "门"}
        {"action": "Final Answer", "action_input": "店"}
        {"action": "Final Answer", "action_input": ")"}
        {"action": "Final Answer", "action_input": " 地"}
        {"action": "Final Answer", "action_input": "址"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "北京"}
        {"action": "Final Answer", "action_input": "市"}
        {"action": "Final Answer", "action_input": "东"}
        {"action": "Final Answer", "action_input": "城"}
        {"action": "Final Answer", "action_input": "区"}
        {"action": "Final Answer", "action_input": "东"}
        {"action": "Final Answer", "action_input": "交"}
        {"action": "Final Answer", "action_input": "民"}
        {"action": "Final Answer", "action_input": "巷"}
        {"action": "Final Answer", "action_input": "44"}
        {"action": "Final Answer", "action_input": "号"}
        {"action": "Final Answer", "action_input": "国"}
        {"action": "Final Answer", "action_input": "家"}
        {"action": "Final Answer", "action_input": "博"}
        {"action": "Final Answer", "action_input": "物"}
        {"action": "Final Answer", "action_input": "馆"}
        {"action": "Final Answer", "action_input": "前"}
        {"action": "Final Answer", "action_input": "\n"}
        {"action": "Final Answer", "action_input": "4"}
        {"action": "Final Answer", "action_input": "."}
        {"action": "Final Answer", "action_input": "名称"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "厚"}
        {"action": "Final Answer", "action_input": "榭"}
        {"action": "Final Answer", "action_input": "潮"}
        {"action": "Final Answer", "action_input": "汕"}
        {"action": "Final Answer", "action_input": "菜"}
        {"action": "Final Answer", "action_input": " 地"}
        {"action": "Final Answer", "action_input": "址"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "北京"}
        {"action": "Final Answer", "action_input": "市"}
        {"action": "Final Answer", "action_input": "东"}
        {"action": "Final Answer", "action_input": "城"}
        {"action": "Final Answer", "action_input": "区"}
        {"action": "Final Answer", "action_input": "南"}
        {"action": "Final Answer", "action_input": "河"}
        {"action": "Final Answer", "action_input": "沿"}
        {"action": "Final Answer", "action_input": "大"}
        {"action": "Final Answer", "action_input": "街"}
        {"action": "Final Answer", "action_input": "99"}
        {"action": "Final Answer", "action_input": "号"}
        {"action": "Final Answer", "action_input": "\n"}
        {"action": "Final Answer", "action_input": "5"}
        {"action": "Final Answer", "action_input": "."}
        {"action": "Final Answer", "action_input": "名称"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "泽"}
        {"action": "Final Answer", "action_input": "园"}
        {"action": "Final Answer", "action_input": "酒"}
        {"action": "Final Answer", "action_input": "家"}
        {"action": "Final Answer", "action_input": "("}
        {"action": "Final Answer", "action_input": "南"}
        {"action": "Final Answer", "action_input": "长"}
        {"action": "Final Answer", "action_input": "街"}
        {"action": "Final Answer", "action_input": "店"}
        {"action": "Final Answer", "action_input": ")"}
        {"action": "Final Answer", "action_input": " 地"}
        {"action": "Final Answer", "action_input": "址"}
        {"action": "Final Answer", "action_input": "："}
        {"action": "Final Answer", "action_input": "北京"}
        {"action": "Final Answer", "action_input": "市"}
        {"action": "Final Answer", "action_input": "西"}
        {"action": "Final Answer", "action_input": "城"}
        {"action": "Final Answer", "action_input": "区"}
        {"action": "Final Answer", "action_input": "南"}
        {"action": "Final Answer", "action_input": "长"}
        {"action": "Final Answer", "action_input": "街"}
        {"action": "Final Answer", "action_input": "20"}
        {"action": "Final Answer", "action_input": "号"}
        {"action": "Final Answer", "action_input": "\n"}
        // AI根据用户提问给出的相关问题
        {"action": "New Questions", "action_input": "天安门附近有哪些知名的饭店？"}
        {"action": "New Questions", "action_input": "天安门附近的饭店大致价格水平是怎样的？"}
        {"action": "New Questions", "action_input": "天安门附近有哪些值得推荐的特色小吃店？"}
        ```

2. 删除对话

    路由：/chat

    方法：delete

    参数：

    | 参数    | 说明                    |
    | ------- | ----------------------- |
    | chat_id | 希望删除的聊天的chat_id |

    返回值：

    - 这里不需要关注返回值，需要注意状态码（200删除成功）

## 提交规范

### 模板

```
[<type>](<scope>): <subject>

<body>
```

- type 有下面几类
    - `feature` 新功能
    - `fix` 修补bug（在 `<body>` 里面加对应的 Issue ID）
    - `test` 测试相关
    - `style` 代码风格变化（不影响运行）
    - `refactor` 重构（没有新增功能或修复 BUG）
    - `perf` 性能优化
    - `chore` 构建过程变动（包括构建工具/CI等）
    - `doc`文档变动
- scope（可选）：影响的模块
- subject：主题（一句话简要描述）
- body（可选）：详细描述，包括相关的 issue、bug 以及具体变动等，可以有多行

### 例子

```
[feat](账号模块): 增加微信登录验证
[fix](管理员 UI): Safari 下界面适配

1. xxx 元素 yyyy
2. aaa 页面 bbbb

Issue: #3
[refactor](招聘信息接口): xxx 接口更新
[style]: 格式规范更改，重新格式化
```

