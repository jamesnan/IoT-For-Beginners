# 存储位置数据

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-12.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。 单击图像可查看更大的版本。

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/23)

## 介绍

在上一课中，您学习了如何使用 GPS 传感器捕获位置数据。 要使用这些数据来可视化装载食物的卡车的位置及其旅程，需要将其发送到云中的物联网服务，然后存储在某个地方。

在本课程中，您将了解存储 IoT 数据的不同方法，并了解如何使用无服务器代码存储来自 IoT 服务的数据。

在本课中，我们将介绍：

* [结构化和非结构化数据](#结构化和非结构化数据)
* [将 GPS 数据发送到 IoT 中心](#send-gps-data-to-an-iot-hub)
* [热、暖和冷路径](#hot-warm-and-cold-paths)
* [使用无服务器代码处理 GPS 事件](#handle-gps-events-using-serverless-code)
* [Azure 存储帐户](#azure-storage-accounts)
* [将您的无服务器代码连接到存储](#connect-your-serverless-code-to-storage)

## 结构化和非结构化数据

计算机系统处理数据，这些数据有各种不同的形状和大小。 它可以是单个数字、大量文本、视频和图像以及物联网数据。 数据通常可以分为两类之一 - *结构化*数据和*非结构化*数据。

* **结构化数据** 是具有明确定义的刚性结构的数据，不会改变，通常映射到具有关系的数据表。 一个例子是一个人的详细信息，包括姓名、出生日期和地址。

* **非结构化数据**是没有明确定义、严格结构的数据，包括可以频繁更改结构的数据。 一个例子是书面文档或电子表格等文档。

✅ 做一些研究：您能想到结构化和非结构化数据的其他一些示例吗？

> 💁 还有一种半结构化数据，它是结构化的，但不适合固定的数据表

物联网数据通常被认为是非结构化数据。

想象一下，您正在将物联网设备添加到大型商业农场的车队中。 您可能希望对不同类型的车辆使用不同的设备。 例如：

* 对于拖拉机等农用车辆，您需要 GPS 数据来确保它们在正确的田地里工作
* 对于将食品运送到仓库的送货卡车，您需要 GPS 数据以及速度和加速度数据，以确保驾驶员安全驾驶，并需要驾驶员身份和启动/停止数据，以确保驾驶遵守当地有关工作时间的法律
* 对于冷藏车，您还需要温度数据，以确保食物在运输过程中不会变得太热或太冷而变质

该数据可能会不断变化。 例如，如果物联网设备位于卡车驾驶室中，那么它发送的数据可能会随着拖车的变化而变化，例如仅在使用冷藏拖车时发送温度数据。

✅ 可能会捕获哪些其他物联网数据？ 考虑卡车可以承载的负载类型以及维护数据。

这些数据因车辆而异，但都会发送到同一物联网服务进行处理。 物联网服务需要能够处理这些非结构化数据，以允许搜索或分析的方式存储它，但可以使用与该数据不同的结构。

### SQL 与 NoSQL 存储

数据库是允许您存储和查询数据的服务。 数据库有两种类型 - SQL 和 NoSQL

#### SQL 数据库

第一个数据库是关系数据库管理系统（RDBMS）或关系数据库。 这些也称为 SQL 数据库，因为使用结构化查询语言 (SQL) 与它们交互以添加、删除、更新或查询数据。 这些数据库由一个模式组成 - 一组明确定义的数据表，类似于电子表格。 每个表都有多个命名列。 插入数据时，会向表中添加一行，并将值放入每一列中。 这使数据保持非常严格的结构 - 尽管您可以将列留空，但如果您想添加新列，则必须在数据库上执行此操作，填充现有行的值。 这些数据库是关系型的——一个表可以与另一个表建立关系。

![一个关系数据库，其中用户表的 ID 与购买表的用户 ID 列相关，产品表的 ID 与购买表的产品 ID 相关](../../../../images/sql-database.png)


例如，如果您将用户的个人详细信息存储在表中，则每个用户都会有某种内部唯一 ID，该 ID 在包含用户姓名和地址的表中的行中使用。 如果您随后想要在另一个表中存储有关该用户的其他详细信息（例如他们的购买情况），则新表中将有一列用于该用户 ID。 当您查找用户时，您可以使用他们的 ID 来获取继承一张桌子上的个人详细信息，以及另一张桌子上的购买情况。

SQL 数据库非常适合存储结构化数据，以及当您想要确保数据与您的架构匹配时。

✅ 如果您以前没有使用过 SQL，请花点时间在 [Wikipedia 上的 SQL 页面](https://wikipedia.org/wiki/SQL) 上阅读它。

一些著名的 SQL 数据库包括 Microsoft SQL Server、MySQL 和 PostgreSQL。

✅ 做一些研究：阅读其中一些 SQL 数据库及其功能。

#### NoSQL 数据库

NoSQL 数据库之所以被称为 NoSQL，是因为它们不具有 SQL 数据库相同的严格结构。 它们也称为文档数据库，因为它们可以存储非结构化数据（例如文档）。

> 💁 尽管名称如此，一些 NoSQL 数据库允许您使用 SQL 来查询数据。

![NoSQL 数据库文件夹中的文档](../../../../images/noqsl-database.png)

NoSQL 数据库没有限制数据存储方式的预定义架构，您可以插入任何非结构化数据，通常使用 JSON 文档。 这些文档可以组织到文件夹中，类似于计算机上的文件。 每个文档可以具有与其他文档不同的字段 - 例如，如果您存储农用车辆的 IoT 数据，有些文档可能包含加速度计和速度数据的字段，其他文档可能包含拖车中温度的字段。 如果您要添加一种新的卡车类型，例如带有内置秤来跟踪所运产品重量的卡车，那么您的物联网设备可以添加这个新字段，并且可以在不更改数据库的情况下存储它。

一些著名的 NoSQL 数据库包括 Azure CosmosDB、MongoDB 和 CouchDB。

✅ 做一些研究：了解其中一些 NoSQL 数据库及其功能。

在本课程中，您将使用 NoSQL 存储来存储 IoT 数据。

## 将 GPS 数据发送到 IoT 中心

在上一课中，您从连接到 IoT 设备的 GPS 传感器捕获了 GPS 数据。 要将这些 IoT 数据存储在云中，您需要将其发送到 IoT 服务。 您将再次使用 Azure IoT 中心，这是您在上一个项目中使用的相同 IoT 云服务。

![将 GPS 遥测数据从 IoT 设备发送到 IoT 中心](../../../../images/gps-telemetry-iot-hub.png)

### 任务 - 将 GPS 数据发送到 IoT 中心

1. 使用免费套餐创建新的 IoT 中心。

     > ⚠️如果需要， 您可以参考 [项目2第4课创建IoT Hub的说明](../../../2-farm/lessons/4-migrate-your-plant-to-the-cloud/README.md#create-an-iot-service-in-the-cloud)。

     请记住创建一个新的资源组。 将新资源组命名为 `gps-sensor ` ，并将新 IoT 中心命名为基于 `gps-sensor ` 的唯一名称，例如 `gps-sensor-<您的名字> ` 。

     > 💁 如果您仍然拥有上一个项目的 IoT 中心，则可以重新使用它。 创建其他服务时，请记住使用此 IoT 中心的名称及其所在的资源组。

1. 将新设备添加到 IoT 中心。 将此设备称为 `gps-sensor ` 。 获取设备的连接字符串。

1. 更新设备代码，以使用上一步中的设备连接字符串将 GPS 数据发送到新的 IoT 中心。

     > ⚠️ 如果需要，您可以参考[项目 2 第 4 课中将设备连接到 IoT 的说明](../../../2-farm/lessons/4-migrate-your-plant-to-the-cloud/README.md#connect-your-device-to-the-iot-service) 

1. 当您发送 GPS 数据时，请按照以下格式将其作为 JSON：

    ```json
    {
        "gps" :
        {
            "lat" : <latitude>,
            "lon" : <longitude>
        }
    }
    ```

1. 每分钟发送一次 GPS 数据，这样您就不会用完每日消息分配。

如果您使用 Wio 终端，请记住添加所有必要的库，并使用 NTP 服务器设置时间。 您的代码还需要确保在使用上一课中的现有代码发送 GPS 位置之前已从串行端口读取了所有数据。 使用以下代码构建 JSON 文档：

```cpp
DynamicJsonDocument doc(1024);
doc["gps"]["lat"] = gps.location.lat();
doc["gps"]["lon"] = gps.location.lng();
```

如果您使用的是虚拟 IoT 设备，请记住使用虚拟环境安装所有所需的库。

对于 Raspberry Pi 和虚拟 IoT 设备，请使用上一课中的现有代码来获取纬度和经度值，然后使用以下代码以正确的 JSON 格式发送它们：

```python
message_json = { "gps" : { "lat":lat, "lon":lon } }
print("Sending telemetry", message_json)
message = Message(json.dumps(message_json))
```

> 💁 您可以在 [code/wio-terminal](../code/wio-terminal)、[code/pi](../code/pi) 或 [code/virtual-device](../code/virtual-device) 文件夹中找到此代码 。

运行设备代码并使用 `az iot hub monitor-events` CLI 命令确保消息流入 IoT 中心。

## 热、暖、冷路径

从物联网设备流向云端的数据并不总是实时处理。 有些数据需要实时处理，其他数据可以稍后处理。 流向在不同时间处理数据的不同服务的数据流被称为热路径、温路径和冷路径。

### 热路径

热路径是指需要实时或近实时处理的数据。 您可以使用热路径数据来发出警报，例如获取车辆正在接近仓库或冷藏车内温度过高的警报。 要使用热路径数据，您的代码将在云服务收到事件后立即响应。

### 暖路径

暖路径是指可以在接收后不久进行处理的数据，例如用于报告或短期分析。 您可以使用前一天收集的数据，将热路径数据用于车辆里程的每日报告。 一旦云服务接收到暖路径数据，就会将其存储在某种可以快速访问的存储中。

### 冷路径

冷路径是指历史数据，长期存储数据以便在需要时进行处理。 例如，您可以使用冷路径获取车辆的年度里程报告，或者对路线进行分析以找到降低燃料成本的最佳路线。

冷路径数据存储在数据仓库中 - 设计用于存储大量永不更改且可以快速轻松查询的数据的数据库。 您的云应用程序中通常会有一项常规作业，每天、每周或每月定期运行，将数据从热路径存储移动到数据仓库。

✅ 思考到目前为止您在这些课程中捕获的数据。 是热路径数据、暖路径数据还是冷路径数据？

## 使用无服务器代码处理 GPS 事件

数据流入 IoT 中心后，您可以编写一些无服务器代码来侦听发布到 Event-Hub 兼容端点的事件。 这是温暖路径 - 该数据将被存储并在下一课中用于报告旅程。

![将 GPS 遥测数据从 IoT 设备发送到 IoT 中心，然后通过事件中心触发器发送到 Azure Functions](../../../../images/gps-telemetry-iot-hub-functions.png)

### 任务 - 使用无服务器代码处理 GPS 事件

1. 使用 Azure Functions CLI 创建 Azure Functions 应用。 使用 Python 运行时，并在名为 `gps-trigger` 的文件夹中创建它，并使用与 Functions App 项目名称相同的名称。 确保创建一个用于此目的的虚拟环境。

     > ⚠️ 如果需要， 您可以参考 [项目2第5课创建Azure Functions项目的说明](../../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#create-a-serverless-application)。

1. 添加使用 IoT 中心的事件中心兼容终结点的 IoT 中心事件触发器。

     > ⚠️如果需要， 您可以参考 [项目2第5课创建IoT Hub事件触发器的说明](../../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#create-an-iot-hub-event-trigger) 。

1. 在 `local.settings.json ` 文件中设置与事件中心兼容的终结点连接字符串，并使用 `function.json ` 文件中该条目的密钥。

1. 使用Azurite应用程序作为本地存储模拟器

1. 运行您的函数应用程序以确保它正在接收来自 GPS 设备的事件。 确保您的 IoT 设备也在运行并发送 GPS 数据。

    ```output
    Python EventHub trigger processed an event: {"gps": {"lat": 47.73481, "lon": -122.25701}}
    ```

## Azure 存储帐户

![Azure 存储徽标](../../../../images/azure-storage-logo.png)

Azure 存储帐户是一种通用存储服务，可以通过多种不同方式存储数据。 您可以将数据同时存储为 blob、队列、表或文件。

### Blob 存储

*Blob* 一词表示二进制大对象，但已成为任何非结构化数据的术语。 您可以在 Blob 存储中存储任何数据，从包含 IoT 数据的 JSON 文档到图像和电影文件。 Blob 存储具有 `容器 ` 的概念，即可以在其中存储数据的命名存储桶，类似于关系数据库中的表。 这些容器可以有一个或多个文件夹来存储 blob，每个文件夹都可以包含其他文件夹，类似于文件在计算机硬盘上的存储方式。

您将在本课程中使用 Blob 存储来存储 IoT 数据。

✅ 做一些研究：阅读 [Azure Blob Storage](https://docs.microsoft.com/azure/storage/blobs/storage-blobs-overview?WT.mc_id=academic-17441-jabenn)

### 表存储

表存储允许您存储半结构化数据。 表存储实际上是一种 NoSQL 数据库，因此不需要预先定义一组表，但它旨在将数据存储在一个或多个表中，并使用唯一键来定义每一行。

✅ 做一些研究：阅读 [Azure 表存储](https://docs.microsoft.com/azure/storage/tables/table-storage-overview?WT.mc_id=academic-17441-jabenn)

### 队列存储

队列存储允许您在队列中存储最大大小为 64KB 的消息。 你可以将消息添加到队列的后面，然后从前面读取它们。 只要还有存储空间，队列就会无限期地存储消息，因此它允许消息长期存储。 然后在需要时读出。 例如，如果您想运行每月作业来处理 GPS 数据，您可以将其每天添加到队列中，持续一个月，然后在月底处理队列中的所有消息。

✅ 做一些研究：阅读 [Azure 队列存储](https://docs.microsoft.com/azure/storage/queues/storage-queues-introduction?WT.mc_id=academic-17441-jabenn)

### 文件存储

文件存储是文件在云端的存储，任何应用程序或设备都可以使用行业标准协议进行连接。 您可以将文件写入文件存储，然后将其作为驱动器安装在 PC 或 Mac 上。

✅ 做一些研究：阅读 [Azure 文件存储](https://docs.microsoft.com/azure/storage/files/storage-files-introduction?WT.mc_id=academic-17441-jabenn)

## 将无服务器代码连接到存储

您的函数应用现在需要连接到 Blob 存储以存储来自 IoT 中心的消息。 有两种方法可以做到这一点：

* 在函数代码中，使用blob存储Python SDK连接到blob存储并将数据写入blob
* 使用输出函数绑定将函数的返回值绑定到blob存储并自动保存blob

在本课程中，您将使用 Python SDK 了解如何与 Blob 存储交互。

![将 GPS 遥测数据从 IoT 设备发送到 IoT 中心，然后通过事件中心触发器发送到 Azure Functions，然后将其保存到 Blob 存储](../../../../images/save-telemetry-to-storage-from-functions.png)


数据将保存为 JSON blob，格式如下：

```json
{
    "device_id": <device_id>,
    "timestamp" : <time>,
    "gps" :
    {
        "lat" : <latitude>,
        "lon" : <longitude>
    }
}
```

### 任务 - 将无服务器代码连接到存储

1. 创建 Azure 存储帐户。 将其命名为 `gps<您的名字>` 。

     > ⚠️如果需要，您可以参考 [项目2第5课创建存储帐户的说明](../../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#task---create-the-cloud-resources) 。

     如果您仍然拥有上一个项目的存储帐户，则可以重新使用它。

     > 💁 在本课程稍后部分中，您将能够使用相同的存储帐户来部署 Azure Functions 应用程序。

1. 运行以下命令获取存储帐户的连接字符串：

    ```sh
    az storage account show-connection-string --output table \
                                              --name <storage_name>
    ```

     将 `<storage_name>` 替换为您在上一步中创建的存储帐户的名称。

1. 使用上一步中的值，将新条目添加到存储帐户连接字符串的 `local.settings.json` 文件中。 将其命名为 `STORAGE_CONNECTION_STRING` 

1. 将以下内容添加到 `requirements.txt` 文件中以安装 Azure 存储 Pip 包：
   
    ```sh
    azure-storage-blob
    ```

     在您的虚拟环境中安装此文件中的软件包。

     > 如果出现错误，请使用以下命令将虚拟环境中的 Pip 版本升级到最新版本，然后重试：
     >
     > ```sh
     > pip install --upgrade pip
     > ```

1. 在 `iot-hub-trigger` 的 `__init__.py` 文件中，添加以下导入语句：

    ```python
    import json
    import os
    import uuid
    from azure.storage.blob import BlobServiceClient, PublicAccess
    ```

     `json` 系统模块将用于读取和写入 JSON，`os` 系统模块将用于读取连接字符串，`uuid` 系统模块将用于生成用于 GPS 读取的唯一 ID。

      `azure.storage.blob ` 包包含用于处理 blob 存储的 Python SDK。

1. 在 `main` 方法之前，添加以下辅助函数：

    ```python
    def get_or_create_container(name):
        connection_str = os.environ['STORAGE_CONNECTION_STRING']
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    
        for container in blob_service_client.list_containers():
            if container.name == name:
                return blob_service_client.get_container_client(container.name)
        
        return blob_service_client.create_container(name, public_access=PublicAccess.Container)
    ```
    
    Python blob SDK 没有用于创建容器（如果容器不存在）的辅助方法。 此代码将从 `local.settings.json` 文件（或部署到云后的应用程序设置）加载连接字符串，然后从中创建一个 `BlobServiceClient` 类以与 blob 存储帐户进行交互。 然后，它会循环访问 Blob 存储帐户的所有容器，查找具有所提供名称的容器 - 如果找到，它将返回一个 `ContainerClient` 类，该类可以与容器交互以创建 Blob。 如果找不到，则创建容器并返回新容器的客户端。

    创建新容器后，将授予公共访问权限以查询容器中的 blob。 这将在下一课中用于在地图上可视化 GPS 数据。

1. 与土壤湿度不同，使用此代码我们希望存储每个事件，因此在 `main` 函数的 `for event in events:` 循环中添加以下代码，位于 `logging` 语句下方：

    ```python
    device_id = event.iothub_metadata['connection-device-id']
    blob_name = f'{device_id}/{str(uuid.uuid1())}.json'
    ```

     此代码从事件元数据中获取设备 ID，然后使用它创建 Blob 名称。 Blob 可以存储在文件夹中，设备 ID 将用作文件夹名称，因此每台设备都将其所有 GPS 事件放在一个文件夹中。 blob名称就是这个文件夹，后面跟一个文档名称，用正斜杠分隔，类似于Linux和macOS路径（也类似于Windows，但Windows使用反斜杠）。 文档名称是使用Python `uuid`模块生成的唯一ID，文件类型为`json`。

     例如，对于 `gps-sensor` 设备 ID，blob 名称可能是 `gps-sensor/a9487ac2-b9cf-11eb-b5cd-1e00621e3648.json` 。

1. 在下面添加以下代码：

    ```python
    container_client = get_or_create_container('gps-data')
    blob = container_client.get_blob_client(blob_name)
    ```

    此代码使用 get_or_create_container 帮助程序类获取容器客户端，然后使用 blob 名称获取 blob 客户端对象。 这些 Blob 客户端可以引用现有的 Blob，或者在本例中引用新的 Blob。

1. 在此之后添加以下代码：

    ```python
    event_body = json.loads(event.get_body().decode('utf-8'))
    blob_body = {
        'device_id' : device_id,
        'timestamp' : event.iothub_metadata['enqueuedtime'],
        'gps': event_body['gps']
    }
    ```

    这将构建将写入 Blob 存储的 Blob 主体。 它是一个 JSON 文档，包含设备 ID、遥测数据发送到 IoT 中心的时间以及遥测数据的 GPS 坐标。

    > 💁 重要的是使用消息的排队时间而不是当前时间来获取消息的发送时间。 如果功能应用程序未运行，它可能会在集线器上停留一段时间，然后再被拿起。

1. 在该代码下方添加以下内容：

    ```python
    logging.info(f'Writing blob to {blob_name} - {blob_body}')
    blob.upload_blob(json.dumps(blob_body).encode('utf-8'))
    ```

    此代码记录即将写入 Blob 及其详细信息，然后上传 Blob 正文作为新 Blob 的内容。

1. 运行功能应用程序。 您将在输出中看到为所有 GPS 事件写入的 blob：

    ```output
    [2021-05-21T01:31:14.325Z] Python EventHub trigger processed an event: {"gps": {"lat": 47.73092, "lon": -122.26206}}
    ...
    [2021-05-21T01:31:14.351Z] Writing blob to gps-sensor/4b6089fe-ba8d-11eb-bc7b-1e00621e3648.json - {'device_id': 'gps-sensor', 'timestamp': '2021-05-21T00:57:53.878Z', 'gps': {'lat': 47.73092, 'lon': -122.26206}}
    ```

     > 💁 确保您没有同时运行 IoT 中心事件监视器。

> 💁 您可以在 [code/functions](../code/functions) 文件夹中找到此代码。

### 任务 - 验证上传的 blob

1. 要查看创建的 blob，您可以使用免费工具 [Azure 存储资源管理器](https://azure.microsoft.com/features/storage-explorer/?WT.mc_id=academic-17441-jabenn) 允许您查看和管理您的存储帐户，或通过 CLI。

    1. 要使用 CLI，首先您需要一个帐户密钥。 运行以下命令来获取此密钥：


        ```sh
        az storage account keys list --output table \
                                     --account-name <storage_name>
        ```

         将 `<storage_name>` 替换为存储帐户的名称。

         复制 `key1` 的值。

    1. 运行以下命令列出容器中的 blob：
     
       ```sh
        az storage blob list --container-name gps-data \
                             --output table \
                             --account-name <storage_name> \
                             --account-key <key1>
        ```

        将 `<storage_name>` 替换为存储帐户的名称，将 `<key1>` 替换为您在上一步中复制的 `key1` 的值。

        这将列出容器中的所有 blob：

        ```output
        Name                                                  Blob Type    Blob Tier    Length    Content Type              Last Modified              Snapshot
        ----------------------------------------------------  -----------  -----------  --------  ------------------------  -------------------------  ----------
        gps-sensor/1810d55e-b9cf-11eb-9f5b-1e00621e3648.json  BlockBlob    Hot          45        application/octet-stream  2021-05-21T00:54:27+00:00
        gps-sensor/18293e46-b9cf-11eb-9f5b-1e00621e3648.json  BlockBlob    Hot          45        application/octet-stream  2021-05-21T00:54:28+00:00
        gps-sensor/1844549c-b9cf-11eb-9f5b-1e00621e3648.json  BlockBlob    Hot          45        application/octet-stream  2021-05-21T00:54:28+00:00
        gps-sensor/1894d714-b9cf-11eb-9f5b-1e00621e3648.json  BlockBlob    Hot          45        application/octet-stream  2021-05-21T00:54:28+00:00
        ```

     1. 使用以下命令下载 Blob 之一：

        ```sh
        az storage blob download --container-name gps-data \
                                 --account-name <storage_name> \
                                 --account-key <key1> \
                                 --name <blob_name> \
                                 --file <file_name>
        ```

        将 `<storage_name>` 替换为存储帐户的名称，将 `<key1>` 替换为您在前面步骤中复制的 `key1` 的值。

        将 `<blob_name>` 替换为上一步输出的 `Name` 列中的全名，包括文件夹名称。 将 `<file_name>` 替换为要保存 blob 的本地文件的名称。

     下载后，您可以在 VS Code 中打开 JSON 文件，您将看到包含 GPS 位置详细信息的 blob：

    ```json
    {"device_id": "gps-sensor", "timestamp": "2021-05-21T00:57:53.878Z", "gps": {"lat": 47.73092, "lon": -122.26206}}
    ```

### 任务 - 将您的 Functions 应用程序部署到云

现在您的 Function 应用程序正在运行，您可以将其部署到云中。

1. 使用之前创建的存储帐户创建新的 Azure Functions 应用程序。 将其命名为 `gps-sensor- ` ，并在末尾添加一个唯一标识符，例如一些随机单词或您的名字。

     > ⚠️ 如果需要， 您可以参考[项目 2 第 5 课创建 Functions 应用程序的说明](../../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#task---create-the-cloud-resources)。

1. 将 `IOT_HUB_CONNECTION_STRING` 和 `STORAGE_CONNECTION_STRING` 值上传到应用程序设置

     > ⚠️如果需要，您可以参考 [项目2第5课上传应用程序设置说明](../../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#task---upload-your-application-settings)。

1. 将本地 Functions 应用部署到云端。

     > ⚠️ 如果需要，您可以参考[项目 2 第 5 课中部署 Functions 应用程序的说明]](../../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#task---deploy-your-functions-app-to-the-cloud)。

---

## 🚀 挑战

GPS 数据并不完全准确，检测到的位置可能会偏差几米，尤其是在隧道和高层建筑区域。

想想卫星导航如何克服这个问题？ 您的卫星导航拥有哪些数据可以使其更好地预测您的位置？

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/24)

## 复习与自学

* 在 [Wikipedia 上的数据模型页面](https://wikipedia.org/wiki/Data_model) 上了解结构化数据
* 在 [Wikipedia 上的半结构化数据页面](https://wikipedia.org/wiki/Semi-structured_data) 上阅读有关半结构化数据的信息
* 在 [Wikipedia 上的非结构化数据页面](https://wikipedia.org/wiki/Unstructured_data) 上了解非结构化数据
* 在 [Azure 存储文档](https://docs.microsoft.com/azure/storage/?WT.mc_id=academic-17441-jabenn) 中了解有关 Azure 存储和不同存储类型的更多信息

## 任务

[研究函数绑定](../assignment.md)
