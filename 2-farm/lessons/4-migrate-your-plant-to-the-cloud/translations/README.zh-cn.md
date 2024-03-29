
# 将你的植物迁移到云端

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-8.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。单击图像可查看更大的版本。

本课程是 [Microsoft Reactor](https://developer.microsoft.com/reactor/?WT.mc_id=academic-17441-jabenn)) 的 [IoT 初学者项目 2 - 数字农业系列](https://youtube.com/playlist?list=PLmsFUfdnGr3yCutmcVg6eAUEfsGiFXgcx) 的一部分。

[![使用 Azure IoT 中心将您的设备连接到云](https://img.youtube.com/vi/bNxjopXkhvk/0.jpg)](https://youtu.be/bNxjopXkhvk)

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/15)

＃＃ 介绍

在上一课中，您学习了如何将工厂连接到 MQTT 代理并通过本地运行的某些服务器代码控制中继。这构成了连接互联网的自动浇水系统的核心，从家庭的个体植物到商业农场都可以使用该系统。

IoT 设备与公共 MQTT 代理进行通信作为演示原理的一种方式，但这并不是最可靠或最安全的方式。在本课程中，您将了解云以及公共云服务提供的物联网功能。您还将了解如何将您的工厂从公共 MQTT 代理迁移到这些云服务之一。

在本课中，我们将介绍：

* [什么是云？](#what-is-the-cloud)
* [创建云订阅](#create-a-cloud-subscription)
* [云物联网服务](#cloud-iot-services)
* [在云端创建 IoT 服务](#create-an-iot-service-in-the-cloud)
* [与 IoT 中心通信](#communicate-with-iot-hub)
* [将您的设备连接到 IoT 服务](#connect-your-device-to-the-iot-service)

## 什么是云？

在云出现之前，当一家公司想要向其员工（例如数据库或文件存储）或公众（例如网站）提供服务时，他们会构建并运行数据中心。其范围从具有少量计算机的房间到具有许多计算机的建筑物。该公司将管理一切，包括：

* 购买电脑
* 硬件维护
* 电源和冷却
* 联网
* 安全性，包括保护建筑物和计算机上软件的安全
* 软件安装和更新

这可能非常昂贵，需要大量熟练的员工，并且在需要时改变非常缓慢。例如，如果一家在线商店需要为繁忙的假期做好计划，他们需要提前几个月计划购买更多硬件，配置它，安装它并安装软件来运行他们的销售流程。假期结束后，销量回落，他们花钱购买的电脑将闲置到下一个旺季。

✅ 您认为这会让公司迅速采取行动吗？如果一家在线服装零售商因为名人穿着衣服而突然走红，他们是否能够足够快地提高计算能力来支持突然涌入的订单？

### 别人的电脑

云经常被戏称为`别人的计算机`  。最初的想法很简单——您不用购买计算机，而是租用别人的计算机。其他人（云计算提供商）将管理巨大的数据中心。他们将负责购买和安装硬件、管理电源和冷却、网络、建筑安全、硬件和软件更新等一切。作为客户，您可以租用所需的计算机，随着需求激增而租用更多计算机，然后在需求下降时减少租用数量。这些云数据中心遍布世界各地。

![Microsoft 云数据中心](../../../../images/azure-region-existing.png)
![微软云数据中心计划扩建](../../../../images/azure-region-planned-expansion.png)

这些数据中心的规模可能有数平方公里。上面的图片是几年前在 Microsoft 云数据中心拍摄的，显示了初始大小以及计划的扩展。扩建清理面积超过5平方公里。

> 💁 这些数据中心需要大量电力，以至于有些数据中心拥有自己的发电站。由于它们的规模和云提供商的投资水平，它们通常非常环保。它们比大量的小型数据中心更有效率，它们主要依靠可再生能源运行，云提供商努力减少浪费，减少用水量，并重新种植森林，以弥补为建设数据中心提供空间而砍伐的森林。您可以在 [Azure 可持续发展网站](https://azure.microsoft.com/global-infrastruct/sustainability/?WT.mc_id=academic-17441-jabenn) 上详细了解云提供商如何致力于可持续发展。

✅ 做一些研究：阅读主要云，例如 [Microsoft 的 Azure](https://azure.microsoft.com/?WT.mc_id=academic-17441-jabenn) 或 [Google 的 GCP](https://cloud.google.com)。他们有多少个数据中心？它们位于世界何处？

使用云可以降低公司的成本，并使他们能够专注于自己最擅长的事情，从而将云计算专业知识交到提供商手中。公司不再需要租用或购买数据中心空间、向不同的提供商支付连接和电力费用或聘请专家。相反，他们可以每月向云提供商支付一份账单，以解决一切问题。

然后，云提供商可以利用规模经济来降低成本，以较低的成本批量购买计算机，投资工具以减少维护工作量，甚至设计和构建自己的硬件来改进其云产品。

### 微软 Azure

Azure 是 Microsoft 的开发者云，您将在这些课程中使用它。下面的视频简要概述了 Azure：

[![Azure 视频概述](../../../../images/what-is-azure-video-thumbnail.png)](https://www.microsoft.com/videoplayer/embed/RE4Ibng?WT.mc_id=academic-17441-jabenn)


## 创建云订阅

要使用云中的服务，您需要向云提供商注册订阅。在本课程中，您将注册 Microsoft Azure 订阅。如果你已经有 Azure 订阅，则可以跳过此任务。此处描述的订阅详细信息在撰写本文时正确无误，但可能会发生变化。

> 💁 如果您通过学校访问这些课程，您可能已经有可用的 Azure 订阅。请咨询你的老师。

您可以注册两种不同类型的免费 Azure 订阅：

* **Azure for Students** - 这是专为 18 岁以上学生设计的订阅。您不需要信用卡即可注册，并且可以使用学校电子邮件地址来验证您是学生。注册后，您将获得 100 美元用于购买云资源，以及免费服务，包括免费版本的 IoT 服务。有效期为 12 个月，您可以在学生身份期间每年续签。

* **Azure 免费订阅** - 这是面向非学生的任何人的订阅。您需要一张信用卡来注册订阅，但您的卡不会被计费，这只是用来验证您是一个真正的人，而不是机器人。您将获得 200 美元的积分，可在前 30 天内使用任何服务，以及免费的 Azure 服务。一旦您的信用额度用完，除非您转换为现收现付订阅，否则不会从您的卡中扣费。

> 💁 Microsoft 确实为 18 岁以下的学生提供 Azure for Students Starter 订阅，但在撰写本文时，它不支持任何 IoT 服务。

### 任务 - 注册免费云订阅

如果你是 18 岁以上的学生，则可以注册 Azure 学生版订阅。您需要使用学校电子邮件地址进行验证。您可以通过以下两种方式之一执行此操作：

* 在 [education.github.com/pack](https://education.github.com/pack) 注册 GitHub 学生开发包。这使您可以访问一系列工具和产品，包括 GitHub 和 Microsoft Azure。注册开发人员包后，您就可以激活面向学生的 Azure 优惠。

* 直接在 [azure.microsoft.com/free/students](https://azure.microsoft.com/free/students/?WT.mc_id=academic-17441-jabenn) 注册 Azure for Students 帐户。

> ⚠️ 如果您的学校电子邮件地址无法识别，请在此存储库中 [提出问题](https://github.com/Microsoft/IoT-For-Beginners/issues)，我们将查看是否可以将其添加到Azure 学生允许列表。

如果你不是学生，或者没有有效的学校电子邮件地址，则可以注册 Azure 免费订阅。

* 在 [azure.microsoft.com/free](https://azure.microsoft.com/free/?WT.mc_id=academic-17441-jabenn) 注册 Azure 免费订阅

## 云物联网服务

您一直在使用的公共测试 MQTT 代理在学习时是一个很好的工具，但作为在商业环境中使用的工具有许多缺点：

* 可靠性 - 这是一项免费服务，没有任何保证，并且可以随时关闭
* 安全性 - 它是公开的，因此任何人都可以监听您的遥测或发送命令来控制您的硬件
* 性能 - 它仅针对少量测试消息而设计，因此无法应对发送的大量消息
* 发现 - 无法知道连接了哪些设备

云中的物联网服务解决了这些问题。它们由大型云提供商维护，他们在可靠性方面投入巨资，并随时解决可能出现的任何问题。它们具有内置的安全功能，可以阻止黑客读取您的数据或发送恶意命令。它们还具有高性能，每天能够处理数百万条消息，并利用云根据需要进行扩展。

> 💁 尽管您需要按月付费才能获得这些好处，但大多数云提供商都提供免费版本的物联网服务，每天的消息数量或可连接的设备数量有限。这个免费版本通常足以让开发人员了解该服务。在本课程中，您将使用免费版本。

IoT 设备使用设备 SDK（提供使用服务功能的代码的库）或直接通过 MQTT 或 HTTP 等通信协议连接到云服务。设备 SDK 通常是最简单的途径，因为它会为您处理所有事情，例如了解要发布或订阅哪些主题以及如何处理安全性。

![设备使用设备 SDK 连接到服务。服务器代码还通过 SDK 连接到服务](../../../../images/iot-service-connectivity.png)

然后，您的设备通过此服务与应用程序的其他部分进行通信 - 类似于通过 MQTT 发送遥测数据和接收命令的方式。这通常使用服务 SDK 或类似的库。消息从您的设备发送到服务，然后应用程序的其他组件可以读取它们，然后消息可以发送回您的设备。

![没有有效密钥的设备无法连接到 IoT 服务](../../../../images/iot-service-allowed-denied-connection.png)

这些服务通过了解可以连接和发送数据的所有设备来实现安全性，方法是让设备预先注册到服务，或者向设备提供可用于首次向服务注册的设备密钥或证书。他们连接。未知设备无法连接，如果它们尝试，服务会拒绝连接并忽略它们发送的消息。

✅ 做一些研究：拥有任何设备或代码都可以连接的开放物联网服务有什么缺点？您能找到黑客利用这一点的具体例子吗？

应用程序的其他组件可以连接到 IoT 服务并了解所有连接或注册的设备，并直接批量或单独与它们通信。

> 💁 物联网服务还实现了额外的功能，并且云提供商拥有可以连接到该服务的额外服务和应用程序。例如，如果您想要将所有设备发送的所有遥测消息存储在数据库中，通常只需在云提供商的配置工具中单击几下即可将服务连接到数据库并将数据流式传输。

## 在云端创建 IoT 服务

现在您已拥有 Azure 订阅，您可以注册 IoT 服务。 Microsoft 的 IoT 服务称为 Azure IoT Hub。

![Azure IoT 中心徽标](../../../../images/azure-iot-hub-logo.png)

下面的视频简要概述了 Azure IoT 中心：

[![Azure IoT 中心视频概述](https://img.youtube.com/vi/smuZaZZXKsU/0.jpg)](https://www.youtube.com/watch?v=smuZaZZXKsU)

> 🎥 点击上图观看视频

✅ 花点时间做一些研究并阅读 [Microsoft IoT 中心文档](https://docs.microsoft.com/azure/iot-hub/about-iot-hub?WT.mc_id=学术-17441-jabenn)。

Azure 中提供的云服务可以通过基于 Web 的门户或命令行界面 (CLI) 进行配置。对于此任务，您将使用 CLI。

### 任务 - 安装 Azure CLI

要使用 Azure CLI，首先必须将其安装在 PC 或 Mac 上。

1. 按照 [Azure CLI 文档](https://docs.microsoft.com/cli/azure/install-azure-cli?WT.mc_id=academic-17441-jabenn) 中的说明安装 CLI。

1. Azure CLI 支持许多扩展，这些扩展增加了管理各种 Azure 服务的功能。通过从命令行或终端运行以下命令来安装 IoT 扩展：

    ```sh
    az extension add --name azure-iot
    ```

1. 在命令行或终端中，运行以下命令以从 Azure CLI 登录到 Azure 订阅。

    ```sh
    az login
    ```

    将在您的默认浏览器中启动一个网页。使用用于注册 Azure 订阅的帐户登录。登录后，您可以关闭浏览器选项卡。

1. 如果您有多个 Azure 订阅（例如学校提供的订阅）和您自己的 Azure for Students 订阅，则需要选择要使用的订阅。运行以下命令列出您有权访问的所有订阅：
    
    ```sh
    az account list --output table
    ```

    在输出中，您将看到每个订阅的名称及其 `SubscriptionId`。

    ```output
    ➜  ~ az account list --output table
    Name                    CloudName    SubscriptionId                        State    IsDefault
    ----------------------  -----------  ------------------------------------  -------  -----------
    School-subscription     AzureCloud   cb30cde9-814a-42f0-a111-754cb788e4e1  Enabled  True
    Azure for Students      AzureCloud   fa51c31b-162c-4599-add6-781def2e1fbf  Enabled  False
    ```

    要选择您要使用的订阅，请使用以下命令：

    ```sh
    az account set --subscription <SubscriptionId>
    ```

    替换 `SubscriptionID`  为您要使用的订阅的 ID。运行此命令后，重新运行该命令以列出您的帐户。您将看到您刚刚设置的订阅的 `IsDefault`  列将被标记为`True`  。

### 任务 - 创建资源组

Azure 服务（例如 IoT 中心实例、虚拟机、数据库或 AI 服务）被称为**资源**。每个资源都必须位于**资源组**内，即一个或多个资源的逻辑分组。

> 💁 使用资源组意味着您可以同时管理多个服务。例如，当您完成该项目的所有课程后，您可以删除该资源组，其中的所有资源将被自动删除。

1. 全球有多个Azure数据中心，分为多个区域。创建 Azure 资源或资源组时，必须指定创建位置。运行以下命令以获取位置列表：

    ```sh
    az account list-locations --output table
    ```

    您将看到位置列表。这个清单会很长。

    > 💁 在撰写本文时，您可以部署到 65 个位置。

    ```output
        ➜  ~ az account list-locations --output table
    DisplayName               Name                 RegionalDisplayName
    ------------------------  -------------------  -------------------------------------
    East US                   eastus               (US) East US
    East US 2                 eastus2              (US) East US 2
    South Central US          southcentralus       (US) South Central US
    ...
    ```

    记下离您最近的区域的`Name`  列中的值。您可以在 [Azure 地理页面](https://azure.microsoft.com/global-infrastruct/geographies/?WT.mc_id=academic-17441-jabenn) 上的地图上找到这些区域。

1. 运行以下命令创建名为 `soil-moisture-sensor`  的资源组。资源组名称在您的订阅中必须是唯一的。

     ```sh
    az group create --name soil-moisture-sensor \
                    --location <location>
    ```

    替换 `loction`  为您在上一步中选择的位置。

### 任务 - 创建 IoT 中心

现在，您可以在资源组中创建 IoT 中心资源。

1. 使用以下命令创建 IoT 中心资源：

    ```sh
    az iot hub create --resource-group soil-moisture-sensor \
                      --sku F1 \
                      --partition-count 2 \
                      --name <hub_name>
    ```

     将 `<hub_name>` 替换为您的集线器的名称。 该名称必须是全局唯一的 - 即任何人创建的其他 IoT 中心都不能具有相同的名称。 此名称在指向中心的 URL 中使用，因此需要是唯一的。 使用`soil-moisture-sensor`  之类的东西，并在末尾添加一个唯一的标识符，例如一些随机单词或您的名字。

     `--sku F1` 选项告诉它使用免费套餐。 免费套餐每天支持 8,000 条消息以及全价套餐的大部分功能。

     > 🎓 Azure 服务的不同定价级别称为层级。 每个层都有不同的成本并提供不同的功能或数据量。

     > 💁 如果您想了解更多定价信息，可以查看 [Azure IoT Hub定价指南](https://azure.microsoft.com/pricing/details/iot-hub/?WT.mc_id=academic-17441-jabenn).

     `--partition-count 2` 选项定义了 IoT 中心支持多少个数据流，更多的分区可以减少多个事物从 IoT 中心读写时的数据阻塞。 分区不在这些课程的范围内，但需要设置此值才能创建免费层 IoT 中心。

     > 💁 每个订阅只能拥有一个免费的 IoT 中心。

将创建 IoT 中心。 这需要一分钟左右才能完成。

## 与 IoT 中心通信

在上一课中，您使用了 MQTT 并就不同的主题来回发送消息，不同的主题有不同的用途。 IoT 中心不是通过不同的主题发送消息，而是为设备与集线器通信或集线器与设备通信提供了多种定义的方式。

> 💁 在底层，IoT 中心和您的设备之间的通信可以使用 MQTT、HTTPS 或 AMQP。

* 设备到云 (D2C) 消息 - 这些是从设备发送到 IoT 中心的消息，例如遥测。 然后，您的应用程序代码可以从 IoT 中心读取它们。

     > 🎓 在底层，IoT 中心使用名为 [事件中心](https://docs.microsoft.com/azure/event-hubs/?WT.mc_id=academic-17441-jabenn) 的 Azure 服务。 当您编写代码来读取发送到集线器的消息时，这些消息通常称为事件。

* 云到设备 (C2D) 消息 - 这些是从应用程序代码通过 IoT 中心发送到 IoT 设备的消息

* 直接方法请求 - 这些是从应用程序代码通过 IoT 中心发送到 IoT 设备的消息，以请求设备执行某些操作，例如控制执行器。 这些消息需要响应，以便您的应用程序代码可以判断是否已成功处理。

* 设备孪生 - 这些是在设备和 IoT 中心之间保持同步的 JSON 文档，用于存储设备报告的设置或其他属性，或者应由 IoT 中心在设备上设置（称为所需）。

IoT 中心可以在可配置的时间段（默认为一天）内存储消息和直接方法请求，因此，如果设备或应用程序代码失去连接，它在重新连接后仍然可以检索离线时发送的消息。 设备孪生永久保存在 IoT 中心，因此设备可以随时重新连接并获取最新的设备孪生。

✅ 做一些研究：在 IoT 中心文档中阅读有关这些消息类型的更多信息: [设备到云通信指南](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-d2c-guidance?WT.mc_id=academic-17441-jabenn)，以及[云到设备通信指南](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-c2d-guidance?WT.mc_id=academic-17441-jabenn) 。

## 将您的设备连接到 IoT 服务

创建中心后，您的 IoT 设备就可以连接到它。 只有注册的设备才能连接到服务，因此您需要先注册您的设备。 注册时，您可以获得设备可用于连接的连接字符串。 此连接字符串是设备特定的，包含有关 IoT 中心、设备以及允许该设备连接的密钥的信息。

> 🎓 连接字符串是包含连接详细信息的一段文本的通用术语。 这些在连接到 IoT 中心、数据库和许多其他服务时使用。 它们通常由服务标识符（例如 URL）和安全信息（例如密钥）组成。 这些将传递给 SDK 以连接到服务。

> ⚠️ 连接字符串应保持安全！ 安全性将在以后的课程中更详细地介绍。

### 任务 - 注册您的 IoT 设备

可以使用 Azure CLI 向 IoT 中心注册 IoT 设备。

1. 运行以下命令注册设备：

    ```sh
    az iot hub device-identity create --device-id soil-moisture-sensor \
                                      --hub-name <hub_name>
    ```

    将 `<hub_name>` 替换为您用于 IoT 中心的名称。

    这将创建一个 ID 为`soil-moisture-sensor`  的设备。

1. 当您的 IoT 设备使用 SDK 连接到 IoT 中心时，它需要使用提供中心 URL 的连接字符串以及密钥。 运行以下命令获取连接字符串：

    ```sh
    az iot hub device-identity connection-string show --device-id soil-moisture-sensor \
                                                      --output table \
                                                      --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为您用于 IoT 中心的名称。

1. 存储输出中显示的连接字符串，稍后您将需要它。

### 任务 - 将您的 IoT 设备连接到云端

完成相关指南将您的 IoT 设备连接到云：

* [Arduino - Wio 终端](../wio-terminal-connect-hub.md)
* [单板计算机-Raspberry Pi/虚拟物联网设备](../single-board-computer-connect-hub.md)

### 任务 - 监视事件

目前，您不会更新服务器代码。 相反，您可以使用 Azure CLI 来监视来自 IoT 设备的事件。

1. 确保您的物联网设备正在运行并发送土壤湿度遥测值

1. 在命令提示符或终端中运行以下命令来监控发送到 IoT 中心的消息：

    ```sh
    az iot hub monitor-events --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为您用于 IoT 中心的名称。

     您将看到由 IoT 设备发送的消息出现在控制台输出中。

    ```output
    Starting event monitor, use ctrl-c to stop...
    {
        "event": {
            "origin": "soil-moisture-sensor",
            "module": "",
            "interface": "",
            "component": "",
            "payload": "{\"soil_moisture\": 376}"
        }
    },
    {
        "event": {
            "origin": "soil-moisture-sensor",
            "module": "",
            "interface": "",
            "component": "",
            "payload": "{\"soil_moisture\": 381}"
        }
    }
    ```

     `payload`  的内容将与您的 IoT 设备发送的消息匹配。

     > 在撰写本文时，`az iot`  扩展尚未在 Apple Silicon 上完全运行。 如果您使用的是 Apple Silicon 设备，则需要以不同的方式监视消息，例如使用 [适用于 Visual Studio Code 的 Azure IoT 工具](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-vscode-iot-toolkit-cloud-device-messaging)。


1. 这些消息自动附加了许多属性，例如发送的时间戳。 这些被称为*注释*。 要查看所有消息注释，请使用以下命令：

    ```sh
    az iot hub monitor-events --properties anno --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为您用于 IoT 中心的名称。

     您将看到由 IoT 设备发送的消息出现在控制台输出中。

    ```output
    Starting event monitor, use ctrl-c to stop...
    {
        "event": {
            "origin": "soil-moisture-sensor",
            "module": "",
            "interface": "",
            "component": "",
            "properties": {},
            "annotations": {
                "iothub-connection-device-id": "soil-moisture-sensor",
                "iothub-connection-auth-method": "{\"scope\":\"device\",\"type\":\"sas\",\"issuer\":\"iothub\",\"acceptingIpFilterRule\":null}",
                "iothub-connection-auth-generation-id": "637553997165220462",
                "iothub-enqueuedtime": 1619976150288,
                "iothub-message-source": "Telemetry",
                "x-opt-sequence-number": 1379,
                "x-opt-offset": "550576",
                "x-opt-enqueued-time": 1619976150277
            },
            "payload": "{\"soil_moisture\": 381}"
        }
    }
    ```

     注释中的时间值采用 [UNIX 时间](https://wikipedia.org/wiki/Unix_time)，表示自 1970 年 1 月 1 日午夜以来的秒数。

     完成后退出事件监视器。

### 任务 - 控制您的 IoT 设备

你还可以使用 Azure CLI 调用 IoT 设备上的直接方法。

1. 在命令提示符或终端中运行以下命令以调用 IoT 设备上的 `relay_on` 方法：

    ```sh
    az iot hub invoke-device-method --device-id soil-moisture-sensor \
                                    --method-name relay_on \
                                    --method-payload '{}' \
                                    --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为您用于 IoT 中心的名称。

     这会发送对`method-name`  指定的方法的直接方法请求。 直接方法可以采用包含该方法数据的有效负载，并且可以在`method-payload`  参数中将其指定为 JSON。

     您将看到继电器打开，以及 IoT 设备的相应输出：

    ```output
    Direct method received -  relay_on
    ```

1. 重复上述步骤，但将 `--method-name` 设置为 `relay_off`。 您将看到继电器关闭以及 IoT 设备的相应输出。

---

## 🚀 挑战

IoT 中心的免费套餐每天允许发送 8,000 条消息。 您编写的代码每 10 秒发送一次遥测消息。 每 10 秒一条消息每天有多少条消息？

考虑一下土壤湿度测量结果应该多久发送一次？ 如何更改代码以保持在免费套餐内并根据需要经常检查但又不过于频繁？ 如果您想添加第二台设备怎么办？

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/16)

## 复习与自学

IoT 中心 SDK 对于 Arduino 和 Python 都是开源的。 在 GitHub 上的代码存储库中，有许多示例展示了如何使用不同的 IoT 中心功能。

* 如果您使用的是 Wio 终端，请查看 [GitHub 上的 Arduino 示例](https://github.com/Azure/azure-iot-pal-arduino/tree/master/pal/samples)
* 如果您使用的是 Raspberry Pi 或虚拟设备，请查看 GitHub 上的 [Python 示例](https://github.com/Azure/azure-iot-sdk-python/tree/master/azure-iot-hub/samples)

##  任务

[了解云服务](../assignment.md)
           
          
         
        
       
      
     
    
   