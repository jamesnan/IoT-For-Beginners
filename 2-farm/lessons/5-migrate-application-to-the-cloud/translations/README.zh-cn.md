
# 将应用程序逻辑迁移到云端

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-9.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。单击图像可查看更大的版本。


本课程是 [Microsoft Reactor](https://developer.microsoft.com/reactor/?WT.mc_id=academic-17441-jabenn) 的 [IoT 初学者项目 2 - 数字农业系列](https://youtube.com/playlist?list=PLmsFUfdnGr3yCutmcVg6eAUEfsGiFXgcx) 的一部分。

[![使用无服务器代码控制您的 IoT 设备](https://img.youtube.com/vi/VVZDcs5u1_I/0.jpg)](https://youtu.be/VVZDcs5u1_I)

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/17)

## 介绍

在上一课中，您学习了如何将植物土壤湿度监测和继电器控制连接到基于云的物联网服务。下一步是将控制中继时间的服务器代码移至云端。在本课程中，您将学习如何使用无服务器函数来执行此操作。

在本课中，我们将介绍：

* [什么是无服务器？](#什么是无服务器)
* [创建无服务器应用程序](#create-a-serverless-application)
* [创建 IoT 中心事件触发器](#create-an-iot-hub-event-trigger)
* [从无服务器代码发送直接方法请求](#send-direct-method-requests-from-serverless-code)
* [将您的无服务器代码部署到云](#deploy-your-serverless-code-to-the-cloud)

## 什么是无服务器？

无服务器或无服务器计算涉及创建在云中运行以响应不同类型事件的小代码块。当事件发生时，您的代码将运行，并且会传递有关该事件的数据。这些事件可以来自许多不同的事物，包括 Web 请求、放入队列的消息、数据库中数据的更改或 IoT 设备发送到 IoT 服务的消息。

![从 IoT 服务发送到无服务器服务的事件，所有事件都由正在运行的多个函数同时处理](../../../../images/iot-messages-to-serverless.png)

> 💁 如果您以前使用过数据库触发器，您可以将其视为同一件事，代码由插入行等事件触发。

![当同时发送许多事件时，无服务器服务会扩展以同时运行所有事件](../../../../images/serverless-scaling.png)

您的代码仅在事件发生时运行，没有任何东西可以让您的代码在其他时间保持活动状态。事件发生后，您的代码将被加载并运行。这使得无服务器非常具有可扩展性——如果许多事件同时发生，云提供商可以在他们拥有的任何服务器上根据需要同时运行您的函数多次。这样做的缺点是，如果您需要在事件之间共享信息，则需要将其保存在数据库之类的地方，而不是将其存储在内存中。

您的代码被编写为一个函数，该函数将有关事件的详细信息作为参数。您可以使用多种编程语言来编写这些无服务器函数。

> 🎓 无服务器也称为函数即服务 (FaaS)，因为每个事件触发器都是作为代码中的函数实现的。

尽管有这个名字，无服务器实际上确实使用服务器。命名是因为您作为开发人员不关心运行代码所需的服务器，您只关心代码是为了响应事件而运行的。云提供商有一个无服务器*运行时*，用于管理分配服务器、网络、存储、CPU、内存以及运行代码所需的所有其他内容。这种模式意味着您无法为每台服务器付费，因为没有服务器。相反，您需要为代码运行的时间和使用的内存量付费。

> 💰 无服务器是在云中运行代码最便宜的方式之一。例如，在撰写本文时，一家云提供商允许您的所有无服务器功能每月执行总计 1,000,000 次，然后开始向您收费，之后每 1,000,000 次执行收取 0.20 美元。当您的代码未运行时，您无需付费。

作为物联网开发人员，无服务器模型是理想的。您可以编写一个函数，调用该函数来响应从连接到云托管 IoT 服务的任何 IoT 设备发送的消息。您的代码将处理发送的所有消息，但仅在需要时运行。

✅ 回顾一下您编写的通过 MQTT 监听消息的服务器代码的代码。如何使用无服务器在云中运行？您认为如何更改代码以支持无服务器计算？

> 💁 除了运行代码之外，无服务器模型正在迁移到其他云服务。例如，无服务器数据库可以使用无服务器定价模型在云中使用，您可以根据针对数据库发出的请求（例如查询或插入）付费，通常根据为请求提供服务所需的工作量来定价。例如，针对主键单次选择一行的成本低于连接许多表并返回数千行的复杂操作。

## 创建无服务器应用程序

Microsoft 的无服务器计算服务称为 Azure Functions。

![Azure Functions 徽标](../../../../images/azure-functions-logo.png)

下面的简短视频概述了 Azure Functions

[![Azure Functions 概述视频](https://img.youtube.com/vi/8-jz5f_JyEQ/0.jpg)](https://www.youtube.com/watch?v=8-jz5f_JyEQ)

> 🎥 点击上图观看视频

✅ 花点时间做一些研究并阅读 [Microsoft Azure Functions 文档](https://docs.microsoft.com/azure/azure-functions/functions-overview?WT.mc_id=academic-17441-jabenn)。

要编写 Azure Functions，请从使用您选择的语言的 Azure Functions 应用开始。开箱即用的 Azure Functions 支持 Python、JavaScript、TypeScript、C#、F#、Java 和 Powershell。在本课程中，您将学习如何使用 Python 编写 Azure Functions 应用程序。

> 💁 Azure Functions 还支持自定义处理程序，因此您可以使用支持 HTTP 请求的任何语言编写函数，包括 COBOL 等较旧的语言。

函数应用程序由一个或多个 `触发器` 组成 - 响应事件的函数。您可以在一个函数应用内拥有多个触发器，所有触发器都共享通用配置。例如，在 Functions 应用程序的配置文件中，您可以拥有 IoT 中心的连接详细信息，并且应用程序中的所有函数都可以使用它来连接和侦听事件。

### 任务 - 安装 Azure Functions 工具

> 在撰写本文时，Azure Functions 代码工具尚未完全适用于带有 Python 项目的 Apple Silicon。您需要使用基于 Intel 的 Mac、Windows PC 或 Linux PC。

Azure Functions 的一大功能是可以在本地运行它们。在云中使用的相同运行时可以在您的计算机上运行，​​允许您编写响应 IoT 消息的代码并在本地运行。您甚至可以在处理事件时调试代码。一旦您对代码感到满意，就可以将其部署到云中。

Azure Functions 工具以 CLI 形式提供，称为 Azure Functions 核心工具。

1. 按照 [Azure Functions 核心工具文档](https://docs.microsoft.com/azure/azure-functions/functions-run-local?WT.mc_id=academic-17441-jabenn)
   
1. 安装 VS Code 的 Azure Functions 扩展。此扩展提供对创建、调试和部署 Azure 函数的支持。有关在 VS Code 中安装此扩展的说明，请参阅 [Azure Functions 扩展文档](https://marketplace.visualstudio.com/items?WT.mc_id=academic-17441-jabenn&itemName=ms-azuretools.vscode-azurefunctions)。

将 Azure Functions 应用程序部署到云时，它需要使用少量云存储来存储应用程序文件和日志文件等内容。当您在本地运行 Functions 应用程序时，您仍然需要连接到云存储，但您可以使用名为 [Azurite](https://github.com/Azure/Azurite) 的存储模拟器，而不是使用实际的云存储。它在本地运行，但作用类似于云存储。

> 🎓 在 Azure 中，Azure Functions 使用的存储是 Azure 存储帐户。这些帐户可以存储文件、blob、表中的数据或队列中的数据。您可以在多个应用程序（例如 Functions 应用程序和 Web 应用程序）之间共享一个存储帐户。

1. Azurite 是一个 Node.js 应用程序，因此您需要安装 Node.js。您可以在 [Node.js网站](https://nodejs.org/) 上找到下载和安装说明。如果您使用的是 Mac，还可以从 [Homebrew](https://formulae.brew.sh/formula/node) 安装它。

1. 使用以下命令安装 Azurite（`npm` 是安装 Node.js 时安装的工具）：

    ```sh
    npm install -g azurite
    ```

1. 创建一个名为 `azurite` 的文件夹，供 Azurite 用于存储数据：

    ```sh
    mkdir azurite
    ```

1. 运行 Azurite，并将其传递给这个新文件夹：

    ```sh
    azurite --location azurite
    ```

    Azurite 存储模拟器将启动并准备好本地 Functions 运行时的连接。

    ```output
    ➜  ~ azurite --location azurite  
    Azurite Blob service is starting at http://127.0.0.1:10000
    Azurite Blob service is successfully listening at http://127.0.0.1:10000
    Azurite Queue service is starting at http://127.0.0.1:10001
    Azurite Queue service is successfully listening at http://127.0.0.1:10001
    Azurite Table service is starting at http://127.0.0.1:10002
    Azurite Table service is successfully listening at http://127.0.0.1:10002
    ````

### 任务 - 创建 Azure Functions 项目

Azure Functions CLI 可用于创建新的 Functions 应用程序。

1. 为您的 Functions 应用程序创建一个文件夹并导航到该文件夹​​。称之为 `soil-moisture-trigger`
    
    ```sh
    mkdir soil-moisture-trigger
    cd soil-moisture-trigger
    ```

1. 在此文件夹内创建Python虚拟环境：

    ```sh
    python3 -m venv .venv
    ```

1.  激活虚拟环境：

    * 在 Windows 上：
        * 如果您使用命令提示符或通过 Windows 终端使用命令提示符，请运行：
            
            ```cmd
            .venv\Scripts\activate.bat
            ```

        * 如果您使用 PowerShell，请运行：
            
            ```powershell
            .\.venv\Scripts\Activate.ps1
            ```

    * 在 macOS 或 Linux 上，运行：

        ```cmd
        source ./.venv/bin/activate
        ```

    > 💁 这些命令应该从运行创建虚拟环境的命令的同一位置运行。您永远不需要导航到 `.venv `文件夹，您应该始终运行 activate 命令和任何命令来安装软件包或运行创建虚拟环境时所在文件夹中的代码。

1. 运行以下命令在此文件夹中创建 Functions 应用程序：

    ```sh
    func init --worker-runtime python soil-moisture-trigger
    ```

    这将在当前文件夹中创建三个文件：

    * `host.json` - 此 JSON 文档包含 Functions 应用程序的设置。您不需要修改这些设置。
    * `local.settings.json` - 此 JSON 文档包含您的应用程序在本地运行时将使用的设置，例如 IoT 中心的连接字符串。这些设置仅是本地的，不应添加到源代码控制中。当您将应用程序部署到云时，不会部署这些设置，而是从应用程序设置加载您的设置。本课稍后将对此进行介绍。
    * `requirements.txt` - 这是一个 [Pip 要求文件](https://pip.pypa.io/en/stable/user_guide/#requirements-files)，其中包含运行 Functions 应用程序所需的 Pip 包。

1. `local.settings.json` 文件具有 Functions 应用程序将使用的存储帐户的设置。默认为空设置，因此需要设置。要连接到 Azurite 本地存储模拟器，请将此值设置为以下值：

    ```json
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    ````

1. 使用需求文件安装必要的 Pip 包：

    ```sh
    pip install -r requirements.txt
    ```

    > 💁 所需的 Pip 包需要位于此文件中，以便当 Functions 应用部署到云端时，运行时可以确保它安装正确的包。

1. 要测试一切是否正常工作，您可以启动 Functions 运行时。运行以下命令来执行此操作：
    
    ```sh
    func start
    ```

    您将看到运行时启动并报告它尚未找到任何作业功能（触发器）。

    ```output
    (.venv) ➜  soil-moisture-trigger func start
    Found Python version 3.9.1 (python3).
    
    Azure Functions Core Tools
    Core Tools Version:       3.0.3442 Commit hash: 6bfab24b2743f8421475d996402c398d2fe4a9e0  (64-bit)
    Function Runtime Version: 3.0.15417.0
    
    [2021-05-05T01:24:46.795Z] No job functions found.
    ```

    > ⚠️ 如果您收到防火墙通知，请授予访问权限，因为 `func` 应用程序需要能够读取和写入您的网络。

    > ⚠️ 如果您使用的是 macOS，输出中可能会出现警告：
    >
    > ```输出
    > (.venv) ➜ 土壤湿度触发函数启动
    > 找到Python 版本3.9.1 (python3)。
    >
    > Azure Functions 核心工具
    > 核心工具版本：3.0.3442 提交哈希：6bfab24b2743f8421475d996402c398d2fe4a9e0（64 位）
    > 函数运行版本：3.0.15417.0
    >
    > [2021-06-16T08:18:28.315Z] 无法创建共享内存使用目录：/dev/shm/AzureFunctions
    > [2021-06-16T08:18:28.316Z] System.IO.FileSystem：对路径 `/dev/shm/AzureFunctions `的访问被拒绝。不允许操作。
    > [2021-06-16T08:18:30.361Z] 未找到工作职能。
    > ```
    >
    > 只要 Functions 应用程序正确启动并列出正在运行的函数，您就可以忽略这些。正如[Microsoft 文档问答中的这个问题](https://docs.microsoft.com/answers/questions/396617/azure-functions-core-tools-error-osx-devshmazurefu.html?WT.mc_id=academic-17441-jabenn) 可以忽略。

1. 按 `ctrl+c` 停止 Functions 应用程序。

1. 打开 VS Code 中的当前文件夹，方法是打开 VS Code，然后打开此文件夹，或者运行以下命令：

   ```sh
    code .
    ```

    VS Code 将检测您的 Functions 项目并显示一条通知：

    ```output
    Detected an Azure Functions Project in folder "soil-moisture-trigger" that may have been created outside of
    VS Code. Initialize for optimal use with VS Code?
    ```

    ![通知](../../../../images/vscode-azure-functions-init-notification.png)

    从此通知中选择**是**。

1. 确保 VS Code 终端中正在运行 Python 虚拟环境。终止它并在必要时重新启动它。

## 创建 IoT 中心事件触发器

Functions 应用程序是无服务器代码的外壳。要响应 IoT 中心事件，您可以向此应用添加 IoT 中心触发器。此触发器需要连接到发送到 IoT 中心的消息流并对其做出响应。要获取此消息流，您的触发器需要连接到 IoT 中心*事件中心兼容端点*。

IoT 中心基于另一项名为 Azure 事件中心的 Azure 服务。事件中心是一项允许您发送和接收消息的服务，IoT 中心对此进行了扩展，为 IoT 设备添加了功能。连接以从 IoT 中心读取消息的方式与使用事件中心时的方式相同。

✅ 做一些研究：阅读 [Azure 事件中心文档](https://docs.microsoft.com/azure/event-hubs/event-hubs-about?WT.mc_id=academic-17441-jabenn)。基本功能与 IoT Hub 相比如何？

对于要连接到 IoT 中心的 IoT 设备，它必须使用密钥来确保只有允许的设备才能连接。连接以读取消息时也是如此，您的代码将需要一个包含密钥的连接字符串以及 IoT 中心的详细信息。

> 💁 您获得的默认连接字符串具有 **iothubowner** 权限，这为任何使用它的代码提供了 IoT 中心的完全权限。理想情况下，您应该使用所需的最低级别的权限进行连接。这将在下一课中介绍。

连接触发器后，将针对发送到 IoT 中心的每条消息调用函数内的代码，无论发送的是哪个设备。触发器将把消息作为参数传递。

### 任务 - 获取事件中心兼容的终结点连接字符串

1. 从 VS Code 终端运行以下命令以获取 IoT 中心事件中心兼容终结点的连接字符串：

    ```sh
    az iot hub connection-string show --default-eventhub \
                                      --output table \
                                      --hub-name <hub_name>
    ```

    替换 `<connection string>` 为您用于 IoT 中心的名称。

1. 在 VS Code 中，打开 `local.settings.json` 文件。在 `Values`部分添加以下附加值：

    ```json
    "IOT_HUB_CONNECTION_STRING": "<connection string>"
    ```

    使用上一步中的值 替换 `<connection string>` 。您需要在上面的行后面添加一个逗号才能使此 JSON 有效。

### 任务 - 创建事件触发器

您现在已准备好创建事件触发器。

1. 在 VS Code 终端的 `soil-moisture-trigger` 文件夹中运行以下命令：

   ```sh
    func new --name iot-hub-trigger --template "Azure Event Hub trigger"
    ```

    这将创建一个名为 `iot-hub-trigger` 的新函数。该触发器将连接到 IoT 中心上与事件中心兼容的终结点，因此您可以使用事件中心触发器。没有特定的 IoT 中心触发器。

这将在 `soil-moisture-trigger` 文件夹中创建一个名为 `iot-hub-trigger` 的文件夹，其中包含此函数。该文件夹中将包含以下文件：

* `__init__.py` - 这是包含触发器的Python代码文件，使用标准Python文件名约定将此文件夹转换为Python模块。

    该文件将包含以下代码：

    ```python
    import logging

    import azure.functions as func


    def main(event: func.EventHubEvent):
        logging.info('Python EventHub trigger processed an event: %s',
                    event.get_body().decode('utf-8'))
    ```

    触发器的核心是 `main` 函数。来自 IoT 中心的事件会调用此函数。该函数有一个名为 `event `的参数，其中包含 `EventHubEvent` 。每次将消息发送到 IoT 中心时，都会调用此函数，将该消息作为 `事件` 以及与您在上一课中看到的注释相同的属性传递。

    该函数的核心是记录事件。

* `function.json` - 这包含触发器的配置。主要配置位于名为 `bindings` 的部分中。绑定是指 Azure Functions 与其他 Azure 服务之间的连接的术语。此函数具有到事件中心的输入绑定 - 它连接到事件中心并接收数据。

    > 💁 您还可以拥有输出绑定，以便将函数的输出发送到另一个服务。例如，您可以将输出绑定添加到数据库并从函数返回 IoT 中心事件，它将自动插入到数据库中。

    ✅ 做一些研究：阅读 [Azure Functions 触发器和绑定概念文档](https://docs.microsoft.com/azure/azure-functions/functions-triggers-bindings?WT.mc_id=academic-17441-jabenn&tabs=python)。

     `bindings` 部分包含绑定的配置。感兴趣的值是：

  * `"type": "eventHubTrigger"` - 这告诉函数需要监听来自事件中心的事件
  * `"name": "events"` - 这是用于事件中心事件的参数名称。这与 Python 代码中 `main` 函数中的参数名称相匹配。
  * `"direction": "in"` - 这是一个输入绑定，来自事件中心的数据进入函数
  * `"connection": ""` - 这定义了从中读取连接字符串的设置的名称。在本地运行时，这将从 `local.settings.json `文件中读取此设置。

    > 💁 连接字符串不能存储在 `function.json` 文件中，必须从设置中读取。这是为了防止您意外暴露连接字符串。

1. 由于[Azure Functions 模板中的错误](https://github.com/Azure/azure-functions-templates/issues/1250)， `function.json `的 `基数` 值不正确场地。将此字段从 `many` 更新为 `one`：

    ```json
    "cardinality": "one",
    ```

1. 更新 `function.json` 文件中 `connection` 的值，使其指向您添加到 `local.settings.json` 文件中的新值：

    ```json
    "connection": "IOT_HUB_CONNECTION_STRING",
    ```

    > 💁 请记住 - 这需要指向设置，而不包含实际的连接字符串。

1. 连接字符串包含 `eventHubName` 值，因此需要清除 `function.json` 文件中的该值。将此值更新为空字符串：

    ```json
    "eventHubName": "",
    ```

### 任务 - 运行事件触发器

1. 确保您没有运行 IoT 中心事件监视器。如果它与函数应用程序同时运行，函数应用程序将无法连接和使用事件。

    > 💁 多个应用程序可以使用不同的*消费者组*连接到 IoT 中心端点。这些将在后面的课程中介绍。

1. 要运行 Functions 应用程序，请从 VS Code 终端运行以下命令

    ```sh
    func start
    ```

    Functions 应用程序将启动，并会发现 `iot-hub-trigger` 函数。然后，它将处理过去一天已发送到 IoT 中心的所有事件。

    ```output
    (.venv) ➜  soil-moisture-trigger func start
    Found Python version 3.9.1 (python3).
    
    Azure Functions Core Tools
    Core Tools Version:       3.0.3442 Commit hash: 6bfab24b2743f8421475d996402c398d2fe4a9e0  (64-bit)
    Function Runtime Version: 3.0.15417.0
    
    Functions:
    
            iot-hub-trigger: eventHubTrigger
    
    For detailed output, run func with --verbose flag.
    [2021-05-05T02:44:07.517Z] Worker process started and initialized.
    [2021-05-05T02:44:09.202Z] Executing 'Functions.iot-hub-trigger' (Reason='(null)', Id=802803a5-eae9-4401-a1f4-176631456ce4)
    [2021-05-05T02:44:09.205Z] Trigger Details: PartitionId: 0, Offset: 1011240-1011632, EnqueueTimeUtc: 2021-05-04T19:04:04.2030000Z-2021-05-04T19:04:04.3900000Z, SequenceNumber: 2546-2547, Count: 2
    [2021-05-05T02:44:09.352Z] Python EventHub trigger processed an event: {"soil_moisture":628}
    [2021-05-05T02:44:09.354Z] Python EventHub trigger processed an event: {"soil_moisture":624}
    [2021-05-05T02:44:09.395Z] Executed 'Functions.iot-hub-trigger' (Succeeded, Id=802803a5-eae9-4401-a1f4-176631456ce4, Duration=245ms)
    ```

    对函数的每次调用都会被输出中的 `Executing 'Functions.iot-hub-trigger`/ `Executed 'Functions.iot-hub-trigger`块包围，因此您可以知道每个调用中处理了多少条消息函数调用。

1. 确保您的物联网设备正在运行，您将看到功能应用程序中出现新的土壤湿度消息。

1. 停止并重新启动 Functions 应用程序。您将看到它不会再次处理以前的消息，它只会处理新消息。

> 💁 VS Code 还支持调试您的函数。您可以通过单击每行代码开头的边框，或将光标放在一行代码上并选择 `运行` -> `切换断点` 或按 `F9` 来设置断点。您可以通过选择 *运行 -> 开始调试*，按 `F5`，或选择 *运行和调试* 窗格并选择 **开始调试** 按钮来启动调试器。通过执行此操作，您可以查看正在处理的事件的详细信息。

#### 故障排除

* 如果您收到以下错误：

    ```output
    The listener for function 'Functions.iot-hub-trigger' was unable to start. Microsoft.WindowsAzure.Storage: Connection refused. System.Net.Http: Connection refused. System.Private.CoreLib: Connection refused.
    ```

    检查 Azurite 是否正在运行，并且您已将 `local.settings.json` 文件中的 `AzureWebJobsStorage` 设置为 `UseDevelopmentStorage=true`。

* 如果您收到以下错误：

    ```output
    Azure.Messaging.EventHubs: The path to an Event Hub may be specified as part of the connection string or as a separate value, but not both.  Please verify that your connection string does not have the `EntityPath` token if you are passing an explicit Event Hub name. (Parameter 'connectionString').
    ```

    检查您是否已将 `function.json` 文件中的 `cardinality`设置为 `one`。

* 如果您收到以下错误：

    ```output
    Azure.Messaging.EventHubs: The path to an Event Hub may be specified as part of the connection string or as a separate value, but not both.  Please verify that your connection string does not have the `EntityPath` token if you are passing an explicit Event Hub name. (Parameter 'connectionString').
    ```

    检查您是否已将 `function.json` 文件中的 `eventHubName` 设置为空字符串。

## 从无服务器代码发送直接方法请求

到目前为止，您的 Functions 应用程序正在使用事件中心兼容端点侦听来自 IoT 中心的消息。您现在需要向 IoT 设备发送命令。这是通过*注册表管理器*使用与 IoT 中心的不同连接来完成的。注册表管理器是一个工具，可让您查看哪些设备已在 IoT 中心注册，并通过发送云到设备消息、直接方法请求或更新设备孪生来与这些设备进行通信。您还可以使用它从 IoT 中心注册、更新或删除 IoT 设备。

要连接到注册表管理器，您需要一个连接字符串。

### 任务 - 获取注册表管理器连接字符串

1. 要获取连接字符串，请运行以下命令：

    ```sh
    az iot hub connection-string show --policy-name service \
                                      --output table \
                                      --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为您用于 IoT 中心的名称。

     使用 `--policy-name service` 参数为 *ServiceConnect* 策略请求连接字符串。 当您请求连接字符串时，您可以指定该连接字符串允许的权限。 ServiceConnect 策略允许您的代码连接 IoT 设备并向其发送消息。

     ✅ 做一些研究：阅读 [IoT 中心权限文档](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-security#iot-hub-permissions?WT.mc_id=academic-17441-jabenn)

1. 在 VS Code 中，打开 `local.settings.json` 文件。 在 `Values` 部分添加以下附加值：

    ```json
    "REGISTRY_MANAGER_CONNECTION_STRING": "<connection string>"
    ```

     将 `<connection string>`替换为上一步中的值。 您需要在上面的行后面添加一个逗号才能使此 JSON 有效。

### 任务 - 向设备发送直接方法请求

1. 注册表管理器的 SDK 可通过 Pip 包获取。 将以下行添加到 `requirements.txt` 文件中以添加对此包的依赖项：

    ```sh
    azure-iot-hub
    ```

1. 确保 VS Code 终端已激活虚拟环境，然后运行以下命令安装 Pip 包：

    ```sh
    pip install -r requirements.txt
    ```

1. 将以下导入添加到 `__init__.py` 文件中：

    ```python
    body = json.loads(event.get_body().decode('utf-8'))
    device_id = event.iothub_metadata['connection-device-id']

    logging.info(f'Received message: {body} from {device_id}')
    ```

     这会导入一些系统库，以及与注册表管理器交互并发送直接方法请求的库。

1. 从`main` 方法中删除代码，但保留方法本身。

1. 在`main`方法中，添加以下代码：

    ```python
    body = json.loads(event.get_body().decode('utf-8'))
    device_id = event.iothub_metadata['connection-device-id']

    logging.info(f'Received message: {body} from {device_id}')
    ```

     此代码提取事件正文，其中包含 IoT 设备发送的 JSON 消息。

     然后，它从随消息传递的注释中获取设备 ID。 事件正文包含作为遥测发送的消息， `iothub_metadata `字典包含 IoT 中心设置的属性，例如发送者的设备 ID 以及发送消息的时间。

     然后记录该信息。 当您在本地运行 Function 应用程序时，您将在终端中看到此日志记录。

1. 在此下方添加以下代码：

    ```python
    soil_moisture = body['soil_moisture']

    if soil_moisture > 450:
        direct_method = CloudToDeviceMethod(method_name='relay_on', payload='{}')
    else:
        direct_method = CloudToDeviceMethod(method_name='relay_off', payload='{}')
    ```

     此代码从消息中获取土壤湿度。 然后，它检查土壤湿度，并根据该值，为 `relay_on` 或 `relay_off `直接方法的直接方法请求创建一个辅助类。 该方法请求不需要有效负载，因此会发送一个空的 JSON 文档。

1. 在此下方添加以下代码：

    ```python
    logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')

    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
    ```

     此代码从 `local.settings.json` 文件加载 `REGISTRY_MANAGER_CONNECTION_STRING`。 该文件中的值可用作环境变量，可以使用 `os.environ` 函数读取这些值，该函数返回所有环境变量的字典。

     > 💁 当此代码部署到云端时， `local.settings.json` 文件中的值将被设置为 *Application Settings*，并且可以从环境变量中读取这些值。

     然后，代码使用连接字符串创建注册表管理器帮助程序类的实例。

1. 在此下方添加以下代码：

    ```python
    registry_manager.invoke_device_method(device_id, direct_method)

    logging.info('Direct method request sent!')
    ```

     此代码告诉注册表管理器将直接方法请求发送到发送遥测数据的设备。

     > 💁 在您在之前的课程中使用 MQTT 创建的应用程序版本中，继电器控制命令被发送到所有设备。 该代码假设您只有一台设备。 此版本的代码将方法请求发送到单个设备，因此如果您有多个湿度传感器和继电器设置，则可以将正确的直接方法请求发送到正确的设备。

1. 运行 Functions 应用程序，并确保您的 IoT 设备正在发送数据。 您将看到正在处理的消息以及正在发送的直接方法请求。 将土壤湿度传感器移入和移出土壤，查看数值变化以及继电器的打开和关闭

> 💁 您可以在 [code/functions](../code/functions) 文件夹中找到此代码。

## 将您的无服务器代码部署到云端

您的代码现在可以在本地运行，因此下一步是将 Functions App 部署到云。

### 任务 - 创建云资源

您的 Functions 应用程序需要部署到 Azure 中的 Functions 应用程序资源，位于您为 IoT 中心创建的资源组内。 您还需要在 Azure 中创建一个存储帐户来替换您在本地运行的模拟帐户。

1. 运行以下命令创建存储帐户：

    ```sh
    az storage account create --resource-group soil-moisture-sensor \
                              --sku Standard_LRS \
                              --name <storage_name> 
    ```

     将 `<storage_name>` 替换为您的存储帐户的名称。 这需要是全局唯一的，因为它构成用于访问存储帐户的 URL 的一部分。 该名称只能使用小写字母和数字，不能使用其他字符，且长度不得超过 24 个字符。 使用 `sms `之类的内容并在末尾添加唯一标识符，例如一些随机单词或您的名字。

     `--sku Standard_LRS` 选择定价层，选择成本最低的通用帐户。 没有免费的存储层，您需要按使用量付费。 成本相对较低，最昂贵的存储每月每 GB 存储费用不到 0.05 美元。

     ✅ 在 [Azure 存储帐户定价页面](https://azure.microsoft.com/pricing/details/storage/?WT.mc_id=academic-17441-jabenn) 上了解定价信息

1. 运行以下命令创建Function App：

    ```sh
    az functionapp create --resource-group soil-moisture-sensor \
                          --runtime python \
                          --functions-version 3 \
                          --os-type Linux \
                          --consumption-plan-location <location> \
                          --storage-account <storage_name> \
                          --name <functions_app_name>
    ```

     将 `<location>` 替换为您在上一课中创建资源组时使用的位置。

     将 `<storage_name>` 替换为您在上一步中创建的存储帐户的名称。

     将 `<functions_app_name>` 替换为 Functions 应用程序的唯一名称。 这需要是全局唯一的，因为它构成可用于访问 Functions App 的 URL 的一部分。 使用 `土壤湿度传感器-` 之类的东西，并在末尾添加一个唯一的标识符，例如一些随机单词或您的名字。

      `--functions-version 3` 选项设置要使用的 Azure Functions 版本。 版本 3 是最新版本。

     `--os-type Linux` 告诉 Functions 运行时使用 Linux 作为托管这些函数的操作系统。 函数可以托管在 Linux 或 Windows 上，具体取决于所使用的编程语言。 Python 应用程序仅在 Linux 上受支持。

### 任务 - 上传您的应用程序设置

当您开发 Functions 应用程序时，您在 `local.settings.json` 文件中存储了 IoT 中心连接字符串的一些设置。 这些需要写入 Azure 中的 Function App 中的应用程序设置，以便您的代码可以使用它们。

> 🎓 `local.settings.json` 文件仅用于本地开发设置，不应将这些设置签入源代码控制，例如 GitHub。 部署到云时，将使用应用程序设置。 应用程序设置是托管在云中的键/值对，可以从代码中的环境变量中读取，也可以在将代码连接到 IoT 中心时由运行时读取。

1. 运行以下命令以在 Functions App 应用程序设置中设置 `IOT_HUB_CONNECTION_STRING` 设置：

    ```sh
    az functionapp config appsettings set --resource-group soil-moisture-sensor \
                                          --name <functions_app_name> \
                                          --settings "IOT_HUB_CONNECTION_STRING=<connection string>"
    ```

     将 `<functions_app_name>` 替换为您用于 Functions 应用程序的名称。

     将 `<connection string>` 替换为 `local.settings.json` 文件中 `IOT_HUB_CONNECTION_STRING` 的值。

1. 重复上述步骤，但将 `REGISTRY_MANAGER_CONNECTION_STRING` 的值设置为 `local.settings.json` 文件中的相应值。

当您运行这些命令时，它们还将输出函数应用的所有应用程序设置的列表。 您可以使用它来检查您的值设置是否正确。

> 💁 您将看到已经为 `AzureWebJobsStorage` 设置了一个值。 在 `local.settings.json` 文件中，将其设置为使用本地存储模拟器的值。 创建 Functions App 时，您将存储帐户作为参数传递，并在此设置中自动设置。

### 任务 - 将您的 Functions 应用程序部署到云

现在 Functions App 已准备就绪，可以部署您的代码了。

1. 从 VS Code 终端运行以下命令来发布您的 Functions App：

    ```sh
    func azure functionapp publish <functions_app_name>
    ```

     将 `<functions_app_name>` 替换为您用于 Functions 应用程序的名称。

代码将被打包并发送给 Functions App，在那里代码将被部署和启动。 将有大量控制台输出，以确认部署和已部署功能列表结束。 在这种情况下，列表将仅包含触发器。

```output
Deployment successful.
Remote build succeeded!
Syncing triggers...
Functions in soil-moisture-sensor:
    iot-hub-trigger - [eventHubTrigger]
```

确保您的 IoT 设备正在运行。 通过调整土壤湿度或将传感器移入和移出土壤来改变湿度水平。 您将看到继电器随着土壤湿度的变化而打开和关闭。

---


## 🚀 挑战 

在上一课中，您通过在中继开启时以及中继关闭后的一小段时间内取消订阅 MQTT 消息来管理中继的时间。您不能在此处使用此方法 - 您无法取消订阅 IoT 中心触发器。考虑在 Functions 应用程序中处理此问题的不同方法。

## 课后测验 
[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/18) 

## 复习和自学 

* 阅读无服务器计算的 [Wikipedia 页面](https://wikipedia.org/wiki/Serverless_computing)
* 了解如何在 Azure 中使用无服务器，包括 [采用无服务器技术来满足您的 IoT 需求 Azure 博客文章](https://azure.microsoft.com/blog/go-serverless-for-your-iot-needs/?WT.mc_id=academic-17441-jabenn)
* 在 [Azure Functions YouTube 频道](https://www.youtube.com/c/AzureFunctions) 上了解有关 Azure Functions 的更多信息。 

## 作业
[添加手动继电器控制](../assignment.md)
                        
                       
                      
                     
                    
                   
                  
                 
                
               
              
             
            
           
          
         
        
       
      
     
    
   