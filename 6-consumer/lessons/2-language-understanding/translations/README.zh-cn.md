# 理解语言

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-22.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。 单击图像查看放大版本。

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/43)

## 介绍

在上一课中，您将语音转换为文本。 为了使用它来编程智能计时器，您的代码需要了解所说的内容。 您可以假设用户会说一个固定的短语，例如`设置 3 分钟计时器`，并解析该表达式以获取计时器应该有多长，但这对用户来说不太友好。 如果用户说`设置 3 分钟的计时器`，您或我会理解他们的意思，但您的代码不会，它会期待一个固定的短语。

这就是语言理解的用武之地，使用 AI 模型解释文本并返回所需的详细信息，例如能够同时接受`设置 3 分钟计时器`和`设置 3 分钟计时器`，并理解 定时器需要3分钟。

在本课程中，您将学习语言理解模型、如何创建它们、训练它们以及在代码中使用它们。

在本课中，我们将介绍：

* [语言理解](#language-understanding)
* [创建语言理解模型](#create-a-language-understanding-model)
* [意图和实体](#intents-and-entities)
* [使用语言理解模型](#use-the-language-understanding-model)

## 语言理解

人类使用语言进行交流已有数十万年的历史。 我们通过言语、声音或动作进行交流，并理解所说的内容，包括言语、声音或动作的含义，以及它们的上下文。 我们理解真诚和讽刺，根据我们语气的不同，相同的词语可以表达不同的含义。

✅ 回想一下您最近进行的一些对话。 有多少对话内容对于计算机来说是难以理解的，因为它需要上下文？

语言理解，也称为自然语言理解，是称为自然语言处理（NLP）的人工智能领域的一部分，涉及阅读理解，试图理解单词或句子的细节。 如果您使用 Alexa 或 Siri 等语音助手，则您已经使用了语言理解服务。 这些幕后人工智能服务将`Alexa，播放泰勒·斯威夫特的最新专辑`转换成我女儿在客厅里随着她最喜欢的音乐跳舞。

> 💁 计算机尽管取得了诸多进步，但要真正理解文本还有很长的路要走。 当我们提到计算机的语言理解时，我们并不是指任何像人类交流那样先进的东西，而是指提取一些单词并提取关键细节。

作为人类，我们不需要真正思考就可以理解语言。 如果我让另一个人`播放泰勒·斯威夫特的最新专辑`，那么他们会本能地知道我的意思。 对于计算机来说，这更困难。 它必须将单词从语音转换为文本，并计算出以下信息：

* 需要播放音乐
* 音乐由艺术家泰勒·斯威夫特创作
* 具体音乐为多首曲目按顺序排列的整张专辑
* Taylor Swift 有很多专辑，因此需要按时间顺序排序，最新发布的就是所需的

✅ 想一想您在提出请求时说过的其他一些句子，例如点咖啡或要求家人给您递东西。 尝试将其分解为计算机需要提取以理解该句子的信息片段。

语言理解模型是一种人工智能模型，经过训练可以从语言中提取某些细节，然后使用迁移学习针对特定任务进行训练，就像使用一小组图像训练自定义视觉模型一样。 您可以采用一个模型，然后使用您希望其理解的文本对其进行训练。

## 创建语言理解模型

![LUIS 徽标](../../../../images/luis-logo.png)

您可以使用 LUIS 创建语言理解模型，LUIS 是 Microsoft 提供的语言理解服务，属于认知服务的一部分。

### 任务 - 创建创作资源

要使用 LUIS，您需要创建创作资源。

1. 使用以下命令在`smart-timer`资源组中创建创作资源：

    ```python
    az cognitiveservices account create --name smart-timer-luis-authoring \
                                        --resource-group smart-timer \
                                        --kind LUIS.Authoring \
                                        --sku F0 \
                                        --yes \
                                        --location <location>
    ```

    将 `<location>` 替换为您在创建资源组时使用的位置。

    > ⚠️ LUIS 不适用于所有 regions，因此如果您收到以下错误：
    >
    > ```output
    > Inval
    >
    > pick a different region.

    这将创建免费层 LUIS 创作资源。

### 任务 - 创建一个语言理解应用程序

1. 在浏览器中打开 [luis.ai](https://luis.ai?WT.mc_id=academic-17441-jabenn) 上的 LUIS 门户，然后使用用于 Azure 的同一帐户登录。

1. 按照对话框中的说明选择 Azure 订阅，然后选择刚刚创建的`smart-timer-luis-authoring`资源。

1. 从*对话应用程序*列表中，选择**新建应用程序**按钮以创建新应用程序。 将新应用程序命名为`smart-timer`，并将*文化*设置为您的语言。

     > 💁 有一个预测资源字段。 您可以创建第二个资源仅用于预测，但免费创作资源每月允许 1,000 个预测，这对于开发来说应该足够了，因此您可以将此留空。

1. 通读创建应用程序后出现的指南，了解训练语言理解模型所需的步骤。 完成后关闭本指南。

## 意图和实体

语言理解基于*意图*和*实体*。 意图是单词的意图，例如播放音乐、设置计时器或点餐。 实体是意图所指的内容，例如专辑、计时器的长度或食物的类型。 模型解释的每个句子应该至少有一个意图，并且可以选择一个或多个实体。

一些例子：

| Sentence                                            | Intent           | Entities                                   |
| --------------------------------------------------- | ---------------- | ------------------------------------------ |
| "Play the latest album by Taylor Swift"             | *play music*     | *the latest album by Taylor Swift*         |
| "Set a 3 minute timer"                              | *set a timer*    | *3 minutes*                                |
| "Cancel my timer"                                   | *cancel a timer* | None                                       |
| "Order 3 large pineapple pizzas and a caesar salad" | *order food*     | *3 large pineapple pizzas*, *caesar salad* |

✅ 对于您之前想到的句子，该句子的意图和实体是什么？

要训练 LUIS，首先要设置实体。 这些可以是固定的术语列表，也可以是从文本中学到的。 例如，您可以提供菜单中可用食物的固定列表，其中包含每个单词的变体（或同义词），例如 *egg plant* 和 *aubergine* 作为 *aubergine* 的变体。 LUIS 还具有可供使用的预构建实体，例如号码和位置。

为了设置计时器，您可以让一个实体使用预先构建的数字实体来表示时间，而另一个实体则用于表示单位，例如分钟和秒。 每个单位都有多种变体来涵盖单数和复数形式 - 例如分钟和分钟。

一旦定义了实体，您就可以创建意图。 这些是模型根据您提供的例句（称为话语）学习的。 例如，对于*设置计时器*意图，您可以提供以下句子：

* `设置 1 秒定时器`
* `设置一个1分12秒的计时器`
*`设置3分钟的计时器`
* `设置一个 9 分 30 秒的计时器`

然后，您告诉 LUIS 这些句子的哪些部分映射到实体：

![该句子设置了一个计时器，1分12秒分解为实体](../../../../images/sentence-as-intent-entities.png)

`设置计时器为 1 分 12 秒`这句话具有`设置计时器`的意图。 它还具有 2 个实体，每个实体有 2 个值：

| | 时间 | 单位|
| ---------- | ---: | ------ |
| 1 分钟 | 1 | 分钟|
| 12 秒 | 12 | 12 第二 |

为了训练一个好的模型，您需要一系列不同的例句来涵盖某人可能要求同一件事的多种不同方式。

> 💁 与任何人工智能模型一样，用于训练的数据越多且越准确，模型就越好。

✅ 考虑一下您可能会问同一件事并期望人们理解的不同方式。

### 任务 - 将实体添加到语言理解模型中

对于计时器，您需要添加 2 个实体 - 一个用于时间单位（分钟或秒），另一个用于分钟或秒数。

您可以在 [快速入门：在 Microsoft 文档上的 LUIS 门户文档中构建应用程序](https://docs.microsoft.com/azure/cognitive-services/luis/luis-get-started-create-app?WT.mc_id=academic-17441-jabenn)。

1. 在 LUIS 门户中，选择`*实体*`选项卡，然后通过选择`**添加预构建实体**`按钮，然后从列表中选择`数字`来添加`数字`预构建实体。

1. 为t创建一个新实体使用 **创建** 按钮创建时间单位。 将实体命名为`时间单位`并将类型设置为*List*。 将`分钟`和`秒`的值添加到*标准化值*列表，将单数和复数形式添加到*同义词*列表。 添加每个同义词后按`返回`将其添加到列表中。

     | 标准化值 | 同义词 |
     | ---------------- | ---------------- |
     | 分钟| 分钟，分钟|
     | 第二 | 第二，秒 |

### 任务 - 将意图添加到语言理解模型中

1. 从*意图*选项卡中，选择**创建**按钮以创建新意图。 将此意图命名为`设置计时器`。

1. 在示例中，输入使用分钟、秒以及分钟和秒组合设置计时器的不同方法。 例子可以是：

     * `设置 1 秒定时器`
     * `设置 4 分钟计时器`
     * `设置一个四分六秒的计时器`
     * `设置一个 9 分 30 秒的计时器`
     * `设置一个1分12秒的计时器`
     *`设置3分钟的计时器`
     * `设置计时器 3 分 1 秒`
     * `设置一个三分一秒的计时器`
     * `设置一个1分1秒的计时器`
     * `设置30秒的计时器`
     * `设置一个1秒的计时器`

     将数字混合为单词和数字，以便模型学习处理两者。

1. 当您输入每个示例时，LUIS 将开始检测实体，并对找到的任何实体添加下划线和标签。

     ![带有 LUIS 下划线的数字和时间单位的示例](../../../../images/luis-intent-examples.png)

### 任务 - 训练和测试模型

1. 配置实体和意图后，您可以使用顶部菜单上的 **Train** 按钮来训练模型。 选择此按钮，模型将在几秒钟内完成训练。 该按钮在训练时将显示为灰色，并在完成后重新启用。

1. 从顶部菜单中选择`**测试**`按钮来测试语言理解模型。 输入文本，例如`设置 5 分 4 秒的计时器`，然后按回车键。 该句子将出现在您输入该句子的文本框下方的框中，并且这将是*顶级意图*，或以最高概率检测到的意图。 这应该是`设置计时器`。 意图名称后面将跟有检测到的意图正确的概率。

1. 选择 **检查** 选项以查看结果的详细信息。 您将看到得分最高的意图及其百分比概率，以及检测到的实体列表。

1. 完成测试后，关闭*测试*窗格。

### 任务 - 发布模型

要通过代码使用此模型，您需要发布它。 从 LUIS 发布时，您可以发布到暂存环境以进行测试，也可以发布到产品环境以进行完整发布。 在本课程中，暂存环境就很好。

1. 在 LUIS 门户中，从顶部菜单中选择 **发布** 按钮。

1. 确保选择*暂存槽*，然后选择**完成**。 发布应用程序时您将看到一条通知。

1. 您可以使用curl 进行测试。 要构建curl命令，您需要三个值——端点、应用程序ID（App ID）和API密钥。 可以从顶部菜单中选择的`**管理**`选项卡访问这些内容。

     1. 从*设置*部分，复制应用程序 ID

     1. 从 *Azure 资源* 部分，选择 *创作资源*，然后复制 *主键* 和 *端点 URL*

1. 在命令提示符或终端中运行以下curl 命令：
   
    ```sh
    curl "<endpoint url>/luis/prediction/v3.0/apps/<app id>/slots/staging/predict" \
          --request GET \
          --get \
          --data "subscription-key=<primary key>" \
          --data "verbose=false" \
          --data "show-all-intents=true" \
          --data-urlencode "query=<sentence>"
    ```

     将`<端点 url>`替换为 *Azure 资源* 部分中的端点 URL。

     将 `<app id>` 替换为 *Settings* 部分中的应用程序 ID。

     将`<主键>`替换为 *Azure 资源* 部分中的主键。

     将 `<sentence>` 替换为您要测试的句子。

2. 此调用的输出将是一个 JSON 文档，其中详细说明了查询、首要意图以及按类型细分的实体列表。

    ```JSON
    {
        "query": "set a timer for 45 minutes and 12 seconds",
        "prediction": {
            "topIntent": "set timer",
            "intents": {
                "set timer": {
                    "score": 0.97031575
                },
                "None": {
                    "score": 0.02205793
                }
            },
            "entities": {
                "number": [
                    45,
                    12
                ],
                "time-unit": [
                    [
                        "minute"
                    ],
                    [
                        "second"
                    ]
                ]
            }
        }
    }
    ```

     上面的 JSON 来自`设置 45 英里的计时器`的查询坚果和 12 秒`：

     * `设置计时器`是最重要的意图，概率为 97%。
     * 检测到两个 *number* 实体，`45`和`12`。
     * 检测到两个`时间单位`实体，`分钟`和`秒`。

## 使用语言理解模型

发布后，可以从代码调用 LUIS 模型。 在之前的课程中，您已使用 IoT 中心来处理与云服务的通信、发送遥测数据和侦听命令。 这是非常异步的 - 一旦发送遥测数据，您的代码就不会等待响应，并且如果云服务关闭，您也不会知道。

对于智能定时器，我们希望立即得到响应，这样我们就可以告诉用户定时器已设置，或者提醒他们云服务不可用。 为此，我们的 IoT 设备将直接调用 Web 端点，而不是依赖 IoT 中心。

您可以将无服务器代码与不同类型的触发器（HTTP 触发器）结合使用，而不是从 IoT 设备调用 LUIS。 这允许您的函数应用侦听 REST 请求并响应它们。 此函数将是您的设备可以调用的 REST 端点。

> 💁 虽然您可以直接从 IoT 设备调用 LUIS，但最好使用无服务器代码之类的东西。 这样，当您想要更改调用的 LUIS 应用程序时，例如，当您训练更好的模型或用不同的语言训练模型时，您只需更新云代码，而无需重新部署代码到潜在的数千或数百万 物联网设备。

### 任务 - 创建一个无服务器函数应用程序

1. 创建一个名为`smart-timer-trigger`的 Azure Functions 应用程序，并在 VS Code 中打开它

1. 在 VS Code 终端内使用以下命令向此应用添加一个名为`speech-trigger`的 HTTP 触发器：

    ```sh
    func new --name text-to-timer --template "HTTP trigger"
    ```

     这将创建一个名为`text-to-timer`的 HTTP 触发器。

1. 通过运行函数应用程序来测试 HTTP 触发器。 当它运行时，您将看到输出中列出的端点：

    ```output
    Functions:
    
            text-to-timer: [GET,POST] http://localhost:7071/api/text-to-timer
    ```

     通过在浏览器中加载 [http://localhost:7071/api/text-to-timer](http://localhost:7071/api/text-to-timer) URL 进行测试。

    ```output
    This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.
    ```

### 任务 - 使用语言理解模型

1. LUIS 的 SDK 可通过 Pip 包获取。 将以下行添加到`requirements.txt`文件中以添加对此包的依赖项：

    ```sh
    azure-cognitiveservices-language-luis
    ```

1. 确保 VS Code 终端已激活虚拟环境，然后运行以下命令安装 Pip 包：

    ```sh
    pip install -r requirements.txt
    ```

    > 💁 如果出现错误，您可能需要使用以下命令升级 pip：
    >
    > ```sh
    > pip install --upgrade pip
    > ````

1. 从 LUIS 门户的 **MANAGE** 选项卡将新条目添加到 LUIS API 密钥、端点 URL 和应用程序 ID 的`local.settings.json`文件中：

    ```JSON
    "LUIS_KEY": "<primary key>",
    "LUIS_ENDPOINT_URL": "<endpoint url>",
    "LUIS_APP_ID": "<app id>"
    ```

     将`<端点 url>`替换为 **管理** 选项卡的 *Azure 资源* 部分中的端点 URL。 这将是`https://<location>.api.cognitive.microsoft.com/`。

     将 `<app id>` 替换为 **MANAGE** 选项卡的 *Settings* 部分中的应用程序 ID。

     将`<主键>`替换为`管理`选项卡的`Azure 资源`部分中的主键。

1. 将以下导入添加到 `__init__.py` 文件中：

    ```python
    import json
    import os
    from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
    from msrest.authentication import CognitiveServicesCredentials
    ```

     这会导入一些系统库以及与 LUIS 交互的库。

1. 删除 `main` 函数中的内容，添加如下代码：

    ```python
    luis_key = os.environ['LUIS_KEY']
    endpoint_url = os.environ['LUIS_ENDPOINT_URL']
    app_id = os.environ['LUIS_APP_ID']
    
    credentials = CognitiveServicesCredentials(luis_key)
    client = LUISRuntimeClient(endpoint=endpoint_url, credentials=credentials)
    ```

    这将加载您添加到 LUIS 应用的`local.settings.json`文件中的值，使用您的 API 密钥创建凭据对象，然后创建 LUIS 客户端对象以与您的 LUIS 应用交互。

1. 此 HTTP 触发器将被称为传递文本以理解为 JSON，文本位于名为`text`的属性中。 以下代码从 HTTP 请求正文中提取值，并将其记录到控制台。 将此代码添加到`main`函数中：

    ```python
    req_body = req.get_json()
    text = req_body['text']
    logging.info(f'Request - {text}')
    ```

1. 通过发送 LUIS 请求预测

预测请求 - 包含要预测的文本的 JSON 文档。 使用以下代码创建它：

    ```python
    prediction_request = { 'query' : text }
    ```

1. 然后可以使用您的应用程序发布到的暂存槽将该请求发送到 LUIS：

    ```python
    prediction_response = client.prediction.get_slot_prediction(app_id, 'Staging', prediction_request)
    ```

1. 预测响应包含最高意图 - 具有最高预测分数的意图以及实体。 如果顶部意图是`设置计时器`，则可以读取实体以获取计时器所需的时间：
   
    ```python
    if prediction_response.prediction.top_intent == 'set timer':
        numbers = prediction_response.prediction.entities['number']
        time_units = prediction_response.prediction.entities['time unit']
        total_seconds = 0
    ```

     `number`实体将是一个数字数组。 例如，如果您说`设置一个 4 分 17 秒的计时器。`*，那么 `number` 数组将包含 2 个整数 - 4 和 17。

     `时间单位`实体将是一个字符串数组的数组，每个时间单位都是数组内的一个字符串数组。 例如，如果您说`设置一个 4 分 17 秒的计时器。`*，那么`时间单位`数组将包含 2 个数组，每个数组都有单个值 -`['分钟']`和`['秒']` 。

     *`设置 4 分 17 秒计时器`* 的这些实体的 JSON 版本是：

    ```json
    {
        "number": [4, 17],
        "time unit": [
            ["minute"],
            ["second"]
        ]
    }
    ```

     此代码还定义了计时器总时间（以秒为单位）的计数。 这将由实体的值填充。

2. 实体之间没有联系，但我们可以对它们做出一些假设。 它们将按说出的顺序排列，因此数组中的位置可用于确定哪个数字与哪个时间单位匹配。 例如：

     * *`设置 30 秒计时器`* - 这将有一个数字`30`和一个时间单位`秒`，因此单个数字将与单个时间单位匹配。
     * *`设置 2 分 30 秒计时器`* - 这将有两个数字`2`和`30`，以及两个时间单位`分钟`和`秒`，因此第一个数字将是第一次 单位（2 分钟），第二个数字表示第二时间单位（30 秒）。

     以下代码获取数字实体中的项目计数，并使用它从每个数组中提取第一项，然后提取第二项，依此类推。 将其添加到`if`块内。

    ```python
    for i in range(0, len(numbers)):
        number = numbers[i]
        time_unit = time_units[i][0]
    ```

     对于*`设置 4 分 17 秒的计时器。`*，这将循环两次，给出以下值：

    | loop count | `number` | `time_unit` |
    | ---------: | -------: | ----------- |
    | 0          | 4        | minute      |
    | 1          | 17       | second      |

3. 在此循环内，使用数字和时间单位计算计时器的总时间，每分钟添加 60 秒，任意秒添加秒数。

    ```python
    if time_unit == 'minute':
        total_seconds += number * 60
    else:
        total_seconds += number
    ```

4. 在实体循环之外，记录计时器的总时间：

    ```python
    logging.info(f'Timer required for {total_seconds} seconds')
    ```

5. 函数需要作为 HTTP 响应返回的秒数。 在`if`块的末尾添加以下内容：

    ```python
    payload = {
        'seconds': total_seconds
    }
    return func.HttpResponse(json.dumps(payload), status_code=200)
    ```

     此代码创建一个包含计时器总秒数的有效负载，将其转换为 JSON 字符串，并将其作为 HTTP 结果返回，状态代码为 200，这意味着调用成功。

6. 最后，在`if`块之外，通过返回错误代码来处理意图未被识别的情况：

    ```python
    return func.HttpResponse(status_code=404)
    ```

     404 是`未找到`的状态代码。

7. 运行函数应用程序并使用curl 进行测试。

    ```sh
    curl --request POST 'http://localhost:7071/api/text-to-timer' \
         --header 'Content-Type: application/json' \
         --include \
         --data '{"text":"<text>"}'
    ```

     将 `<text>` 替换为您的请求文本，例如`设置 2 分 27 秒计时器`。

     您将看到函数应用程序的以下输出：

    ```output
    Functions:

            text-to-timer: [GET,POST] http://localhost:7071/api/text-to-timer
    
    For detailed output, run func with --verbose flag.
    [2021-06-26T19:45:14.502Z] Worker process started and initialized.
    [2021-06-26T19:45:19.338Z] Host lock lease acquired by instance ID '000000000000000000000000951CAE4E'.
    [2021-06-26T19:45:52.059Z] Executing 'Functions.text-to-timer' (Reason='This function was programmatically called via the host APIs.', Id=f68bfb90-30e4-47a5-99da-126b66218e81)
    [2021-06-26T19:45:53.577Z] Timer required for 147 seconds
    [2021-06-26T19:45:53.746Z] Executed 'Functions.text-to-timer' (Succeeded, Id=f68bfb90-30e4-47a5-99da-126b66218e81, Duration=1750ms)
    ```

     对curl 的调用将返回以下内容：

    ```output
    HTTP/1.1 200 OK
    Date: Tue, 29 Jun 2021 01:14:11 GMT
    Content-Type: text/plain; charset=utf-8
    Server: Kestrel
    Transfer-Encoding: chunked
    
    {"seconds": 147}
    ```

     计时器的秒数位于`秒`值中。

> 💁 您可以在 [code/functions](../code/functions) 文件夹中找到此代码。


### 任务 - 使您的功能可用于您的 IoT 设备

1. 为了让 IoT 设备调用 REST 端点，它需要知道 URL。 当您之前访问它时，您使用了`localhost`，这是访问本地计算机上的 REST 端点的快捷方式。 为了让您的 IoT 设备能够访问，您需要发布到云端，或者获取您的 IP 地址以在本地访问它。

     > ⚠️ 如果您使用 Wio 终端，则在本地运行函数应用程序会更容易，因为对库的依赖性意味着您无法像以前那样部署函数应用程序。 在本地运行函数应用程序并通过计算机 IP 地址访问它。 如果您确实想要部署到云，稍后的课程将提供有关执行此操作的方法的信息。

     * 发布 Functions 应用程序 - 按照前面课程中的说明将函数应用程序发布到云。 发布后，URL 将为`https://<APP_NAME>.azurewebsites.net/api/text-to-timer`，其中`<APP_NAME>`将是函数应用的名称。 请务必同时发布您的本地设置。

       使用 HTTP 触发器时，默认情况下使用功能应用程序密钥来保护它们。 要获取此密钥，请运行以下命令：

      ```sh
      az functionapp keys list --resource-group smart-timer \
                               --name <APP_NAME>                               
      ```

      从 `functionKeys` 复制 `default` 条目的值。

      ```output
      {
        "functionKeys": {
          "default": "sQO1LQaeK9N1qYD6SXeb/TctCmwQEkToLJU6Dw8TthNeUH8VA45hlA=="
        },
        "masterKey": "RSKOAIlyvvQEQt9dfpabJT018scaLpQu9p1poHIMCxx5LYrIQZyQ/g==",
        "systemKeys": {}
      }
      ```

    需要将此密钥作为查询参数添加到 URL，因此最终 URL 将为`https://<APP_NAME>.azurewebsites.net/api/text-to-timer?code=<FUNCTION_KEY>`，其中 `<APP_NAME>` 将是您的功能应用程序的名称，而 `<FUNCTION_KEY>` 将是您的默认功能键。

    > 💁 您可以使用 `function.json` 文件中的 `authlevel` 设置来更改 HTTP 触发器的授权类型。 您可以参考 [Microsoft 文档上的 Azure Functions HTTP 触发器文档的配置部分](https://docs.microsoft.com/azure/azure-functions/functions-bindings-http-webhook-trigger?WT.mc_id=academic-17441-jabenn&tabs=python#configuration)

       * 在本地运行函数应用程序，并使用 IP 地址进行访问 - 您可以获取本地网络上计算机的 IP 地址，并使用它来构建 URL。

       查找您的 IP 地址：

       * 在 Windows 10 上，请按照 [查找您的 IP 地址指南](https://support.microsoft.com/windows/find-your-ip-address-f21a9bbc-c582-55cd-35e0-73431160a1b9?WT.mc_id=academic-17441-jabenn)
       * 
       * 在 macOS 上，请按照[如何在 Mac 上查找 IP 地址指南](https://www.hellotech.com/guide/for/how-to-find-ip-address-on-mac)
       * 在 Linux 上，请按照 [如何在 Linux 中查找 IP 地址指南](https://opensource.com/article/18/5/how-find-ip-address-linux) 中查找您的私有 IP 地址的部分进行操作 ）

       获得 IP 地址后，您将可以通过`http://<IP_ADDRESS>:7071/api/text-to-timer`访问该功能，其中`<IP_ADDRESS>`将是您的 IP 地址，例如` http://192.168.1.10:7071/api/text-to-timer`。

       > 💁 并不是说它使用端口 7071，所以在 IP 地址后面您需要有 `:7071`。

       > 💁 仅当您的 IoT 设备与计算机位于同一网络时，此功能才有效。

1. 使用curl 访问端点来测试端点。

---

## 🚀 挑战

请求同一件事的方法有很多种，例如设置计时器。 想出不同的方法来执行此操作，并将它们用作 LUIS 应用中的示例。 对这些进行测试，看看您的模型能够如何很好地处理多种请求计时器的方式。

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/44)

## 复习与自学

* 有关 LUIS 及其功能的更多信息，请访问 [Microsoft 文档上的语言理解 (LUIS) 文档页面](https://docs.microsoft.com/azure/cognitive-services/luis/?WT.mc_id=academic-17441-jabenn)
* 在 [Wikipe 上的自然语言理解页面](https://wikipedia.org/wiki/Natural-language_understanding) 上了解有关语言理解的更多信息
* 有关 HTTP 触发器的更多信息，请参阅 [Microsoft 文档上的 Azure Functions HTTP 触发器文档](https://docs.microsoft.com/azure/azure-functions/functions-bindings-http-webhook-trigger?WT.mc_id=academic-17441-jabenn&tabs=python)

## 任务

[取消定时器](../assignment.md)