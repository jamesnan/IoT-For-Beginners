# 地理围栏

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-14.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。 单击图像可查看更大的版本。

本视频概述了地理围栏以及如何在 Azure Maps 中使用它们，本课程将介绍这些主题：

[![Microsoft 开发者物联网展示中的 Azure Maps 地理围栏](https://img.youtube.com/vi/nsrgYhaYNVY/0.jpg)](https://www.youtube.com/watch?v=nsrgYhaYNVY ）

> 🎥 点击上图观看视频

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/27)

＃＃ 介绍

在过去 3 节课程中，您使用 IoT 来定位将农产品从农场运送到加工中心的卡车。 您已捕获 GPS 数据，将其发送到云端进行存储，并在地图上将其可视化。 提高供应链效率的下一步是在卡车即将到达处理中心时收到警报，以便需要卸货的人员在车辆到达后立即准备好叉车和其他设备。 这样他们就可以快速卸货，而且您无需支付卡车和司机的费用来等待。

在本课程中，您将了解地理围栏 - 定义的地理空间区域，例如处理中心 2 公里分钟车程内的区域，以及如何测试 GPS 坐标是在地理围栏内部还是外部，以便您可以查看 GPS 传感器是否已到达 或离开一个区域。

在本课中，我们将介绍：

* [什么是地理围栏](#what-are-geofences)
* [定义地理围栏](#defining-a-geofence)
* [针对地理围栏的测试点](#testing-points-against-a-geofence)
* [使用无服务器代码中的地理围栏](#use-geofences-from-serverless-code)

> 🗑 这是本项目的最后一课，因此完成本课和作业后，不要忘记清理您的云服务。 您将需要服务来完成任务，因此请务必先完成任务。
>
> 如有必要，请参阅[清理项目指南](../../../../clean-up.md)，了解如何执行此操作的说明。

## 什么是地理围栏

地理围栏是现实世界地理区域的虚拟边界。 地理围栏可以是定义为点和半径的圆（例如围绕建筑物周围 100m 宽的圆），也可以是覆盖学区、城市范围、大学或办公园区等区域的多边形。

![一些地理围栏示例显示了 Microsoft 公司商店周围的圆形地理围栏和 Microsoft 西园区周围的多边形地理围栏](../../../../images/geofence-examples.png)

> 💁 您可能在不知情的情况下已经使用过地理围栏。 如果您使用 iOS 提醒应用或 Google Keep 根据位置设置了提醒，则您已经使用了地理围栏。 这些应用程序将根据给定的位置设置地理围栏，并在您的手机进入地理围栏时提醒您。

您想知道车辆位于地理围栏内部还是外部的原因有很多：

* 卸货准备 - 收到车辆已到达现场的通知，工作人员可以准备卸货，减少车辆等待时间。 这可以让司机在一天内完成更多的送货任务，同时减少等待时间。
* 税收合规性 - 一些国家（例如新西兰）仅根据在公共道路上行驶时的车辆重量对柴油车征收道路税。 使用地理围栏可以让您跟踪在公共道路上行驶的里程，而不是在农场或伐木区等地点的私人道路上行驶的里程。
* 监控盗窃 - 如果车辆只应留在某个区域（例如农场），并且离开了地理围栏，则它可能已被盗。
* 地点合规性 - 工作场所、农场或工厂的某些地方可能禁止某些车辆通行，例如使运载人造肥料和农药的车辆远离种植有机农产品的田地。 如果进入地理围栏，则车辆不合规，并且可以通知驾驶员。

✅ 你能想到地理围栏的其他用途吗？

Azure Maps 是您在上一课中用于可视化 GPS 数据的服务，它允许您定义地理围栏，然后测试某个点是在地理围栏内部还是外部。

## 定义地理围栏

地理围栏是使用 GeoJSON 定义的，与上一课中添加到地图中的点相同。 在这种情况下，它不是包含`Point` 值的 `FeatureCollection`，而是包含 `Polygon` 的 `FeatureCollection`。


```json
{
   "type": "FeatureCollection",
   "features": [
     {
       "type": "Feature",
       "geometry": {
         "type": "Polygon",
         "coordinates": [
           [
             [
               -122.13393688201903,
               47.63829579223815
             ],
             [
               -122.13389128446579,
               47.63782047131512
             ],
             [
               -122.13240802288054,
               47.63783312249837
             ],
             [
               -122.13238388299942,
               47.63829037035086
             ],
             [
               -122.13393688201903,
               47.63829579223815
             ]
           ]
         ]
       },
       "properties": {
         "geometryId": "1"
       }
     }
   ]
}
```

多边形上的每个点都被定义为数组中的经度、纬度对，这些点位于被设置为 `坐标` 的数组中。 在上一课的 `点` 中，`坐标` 是一个包含 2 个值（纬度和经度）的数组，对于`多边形`来说，它是一个包含 2 个值（经度、纬度）的数组。

> 💁 请记住，GeoJSON 使用`经度，纬度`作为点，而不是`纬度，经度`

多边形坐标数组始终比多边形上的点数多 1 个条目，最后一个条目与第一个条目相同，从而闭合多边形。 例如，对于一个矩形，将有 5 个点。

![带有坐标的矩形](../../../../images/polygon-points.png)

在上图中，有一个矩形。 多边形坐标从左上角 47,-122 开始，然后向右移动到 47,-121，然后向下移动到 46,-121，然后向右移动到 46,-122，然后返回到起点 47, -122。 这为多边形提供了 5 个点 - 左上角、右上角、右下角、左下角，然后是左上角以将其封闭。

✅ 尝试在您的家或学校周围创建一个 GeoJSON 多边形。 使用 [GeoJSON.io](https://geojson.io/) 等工具。

### 任务 - 定义地理围栏

要在 Azure 地图中使用地理围栏，首先必须将其上传到您的 Azure Maps 帐户。 上传后，您将获得一个唯一的 ID，可用于根据地理围栏测试点。 要将地理围栏上传到 Azure Maps，您需要使用地图 Web API。 您可以使用名为 [curl](https://curl.se) 的工具调用 Azure Maps Web API。

> 🎓 Curl 是一个命令行工具，用于向 Web 端点发出请求

1. 如果您使用的是 Linux、macOS 或最新版本的 Windows 10，您可能已经安装了curl。 从终端或命令行运行以下命令进行检查：

    ```sh
    curl --version
    ```

     如果您没有看到curl的版本信息，则需要从[curl下载页面](https://curl.se/download.html)安装它。

     > 💁 如果您有使用 Postman 的经验，那么您可以根据需要使用它。

1. 创建包含多边形的 GeoJSON 文件。 您将使用 GPS 传感器对此进行测试，因此在当前位置周围创建一个多边形。 您可以通过编辑上面给出的 GeoJSON 示例来手动创建一个，也可以使用 [GeoJSON.io](https://geojson.io/) 等工具。

     GeoJSON 需要包含一个`FeatureCollection`，其中包含一个`Feature`和`Polygon`类型的`geometry`。

     您**必须**还添加一个与`geometry`元素处于同一级别的`properties`元素，并且它必须包含一个`geometryId`：

    ```json
    "properties": {
        "geometryId": "1"
    }
    ```

     如果您使用 [GeoJSON.io](https://geojson.io/)，那么您必须在下载 JSON 文件后或在 JSON 编辑器中手动将此项目添加到空的`properties`元素中。 应用程序。

     此`geometryId`在此文件中必须是唯一的。 您可以将多个地理围栏作为同一 GeoJSON 文件中`FeatureCollection`中的多个`Features`上传，只要每个地理围栏具有不同的`geometryId`即可。 如果多边形是在不同时间从不同文件上传的，则它们可以具有相同的`geometryId`。

1. 将此文件另存为`geofence.json`，然后导航到终端或控制台中保存该文件的位置。

1. 运行以下curl命令创建地理围栏：

    ```sh
    curl --request POST 'https://atlas.microsoft.com/mapData/upload?api-version=1.0&dataFormat=geojson&subscription-key=<subscription_key>' \
         --header 'Content-Type: application/json' \
         --include \
         --data @geofence.json
    ```

     将 URL 中的`<subscription_key>`替换为 Azure Maps 帐户的 API 密钥。

     该 URL 用于通过`https://atlas.microsoft.com/mapData/upload` API 上传地图数据。 该调用包含一个`api-version`参数来指定要使用哪个 Azure Maps API，这是为了允许 API 随着时间的推移而更改，但保持向后兼容性。 上传的数据格式设置为`geojson`。

     这将运行对上传 API 的 POST 请求并返回响应标头列表，其中包括名为`location`的标头

    ```output
    content-type: application/json
    location: https://us.atlas.microsoft.com/mapData/operations/1560ced6-3a80-46f2-84b2-5b1531820eab?api-version=1.0
    x-ms-azuremaps-region: West US 2
    x-content-type-options: nosniff
    strict-transport-security: max-age=31536000; includeSubDomains
    x-cache: CONFIG_NOCACHE
    date: Sat, 22 May 2021 21:34:57 GMT
    content-length: 0
    ````

     > 🎓 调用 Web 端点时，您可以通过添加`?`后跟键值对（如`key=value`）向调用传递参数，并用`&`分隔键值对。

1. Azure Maps 不处理立即执行此操作，因此您需要使用`location`标头中给出的 URL 检查上传请求是否已完成。 向此位置发出 GET 请求以查看状态。 您需要将订阅密钥添加到`location` URL 的末尾，方法是在末尾添加`&subscription-key=<subscription_key>`，并将`<subscription_key>`替换为您的 Azure Maps 帐户的 API 密钥。 运行以下命令：

    ```sh
    curl --request GET '<location>&subscription-key=<subscription_key>'
    ```

     将`<location>`替换为`location`标头的值，将`<subscription_key>`替换为 Azure Maps 帐户的 API 密钥。

1. 检查响应中`status`的值。 如果不是`Succeeded`，则稍等一下，然后重试。

1. 状态返回为`Succeeded`后，查看响应中的`resourceLocation`。 其中包含有关 GeoJSON 对象的唯一 ID（称为 UDID）的详细信息。 UDID 是`metadata/`之后的值，不包括`api-version`。 例如，如果`resourceLocation`是：

    ```json
    {
      "resourceLocation": "https://us.atlas.microsoft.com/mapData/metadata/7c3776eb-da87-4c52-ae83-caadf980323a?api-version=1.0"
    }
    ```

     那么 UDID 将为`7c3776eb-da87-4c52-ae83-caadf980323a`。

     保留此 UDID 的副本，因为您将需要它来测试地理围栏。

## 针对地理围栏的测试点

将多边形上传到 Azure Maps 后，您可以测试某个点以查看它是在地理围栏内部还是外部。 您可以通过发出 Web API 请求、传入地理围栏的 UDID 以及要测试的点的纬度和经度来完成此操作。

当您发出此请求时，您还可以传递一个名为`searchBuffer`的值。 这告诉 Maps API 返回结果时的准确度。 其原因是 GPS 并不完全准确，有时位置可能会相差数米（甚至更多）。 搜索缓冲区的默认值为 50m，但您可以将值设置为 0m 到 500m。

当从 API 调用返回结果时，结果的一部分是测量到地理围栏边缘最近点的`距离`，如果该点位于地理围栏外部，则值为正值；如果位于地理围栏内部，则为负值 地理围栏。 如果该距离小于搜索缓冲区，则返回实际距离（以米为单位），否则该值为 999 或 -999。 999 表示该点在地理围栏之外超出搜索缓冲区，-999 表示该点在地理围栏内部超出搜索缓冲区。

![周围有 50m 搜索缓冲区的地理围栏](../../../../images/search-buffer-and-distance.png)

在上图中，地理围栏有 50m 的搜索缓冲区。

* 地理围栏中心、搜索缓冲区内的某个点的距离为 **-999**
* 搜索缓冲区之外的点的距离为 **999**
* 地理围栏内和搜索缓冲区内的点，距离地理围栏 6m，距离为 **6m**
* 地理围栏外、搜索缓冲区内的点，距离地理围栏 39m，距离为 **39m**

了解到地理围栏边缘的距离非常重要，并在根据车辆位置做出决策时将其与其他信息（例如其他 GPS 读数、速度和道路数据）结合起来。

例如，想象一下 GPS 读数显示一辆车辆正在沿着一条道路行驶，最终跑到了地理围栏旁边。 如果单个 GPS 值不准确，并且将车辆置于地理围栏内，尽管没有车辆通行，则可以忽略它。

![GPS 轨迹显示一辆车辆在 520 上经过 Microsoft 园区，沿路有 GPS 读数，园区内的 GPS 读数除外，在地理围栏内](../../../../images/geofence-crossing-inaccurate-gps.png)

在上图中，微软园区的部分区域有地理围栏。 红线显示一辆卡车沿着 520 公路行驶，圆圈显示 GPS 读数。 其中大多数读数都是准确的，并且沿着 520 号线，只有一个在地理围栏内的读数不准确。 读数不可能是正确的 - 卡车没有道路可以突然从 520 转向校园，然后返回 520。检查此地理围栏的代码需要在执行操作之前考虑之前的读数。 地理围栏测试的结果。

✅ 您还需要检查哪些额外数据才能确定 GPS 读数是否正确？

### 任务 - 针对地理围栏的测试点

1. 首先构建 Web API 查询的 URL。 格式为：
    
    ```output
    https://atlas.microsoft.com/spatial/geofence/json?api-version=1.0&deviceId=gps-sensor&subscription-key=<subscription-key>&udid=<UDID>&lat=<lat>&lon=<lon>
    ```

     将`<subscription_key>`替换为 Azure Maps 帐户的 API 密钥。

     将`<UDID>`替换为上一个任务中地理围栏的 UDID。

     将 `<lat>` 和 `<lon>` 替换为您要测试的纬度和经度。

     此 URL 使用`https://atlas.microsoft.com/spatial/geofence/json` API 用于查询使用 GeoJSON 定义的地理围栏 。 它的目标是`1.0` API 版本。 `deviceId` 参数是必需的，并且应该是纬度和经度来自的设备的名称。

     默认搜索缓冲区为 50m，您可以通过传递附加参数`searchBuffer=<distance>`来更改此设置，将`<distance>`设置为搜索缓冲区距离（以米为单位），范围为 0 到 500。

1. 使用curl 向此URL 发出GET 请求：

    ```sh
    curl --request GET '<URL>'
    ```

    > 💁 如果您收到`BadRequest`的响应代码，错误为：
    >
    > ```output
    > Invalid GeoJSON: All feature properties should contain a geometryId, which is used for identifying the geofence.
    > ```
    >
    > 那么您的 GeoJSON 缺少包含`geometryId`的`properties`部分。 您需要修复 GeoJSON，然后重复上述步骤重新上传并获取新的 UDID。

1. 响应将包含一系列`几何图形`，一个对应于用于创建地理围栏的 GeoJSON 中定义的每个多边形。 每个几何图形都有 3 个感兴趣的字段：`distance`、`nearestLat`和`nearestLon`。

    ```output
    {
        "geometries": [
            {
                "deviceId": "gps-sensor",
                "udId": "7c3776eb-da87-4c52-ae83-caadf980323a",
                "geometryId": "1",
                "distance": 999.0,
                "nearestLat": 47.645875,
                "nearestLon": -122.142713
            }
        ],
        "expiredGeofenceGeometryId": [],
        "invalidPeriodGeofenceGeometryId": []
    }
    ```

     * `nearestLat` 和 `nearestLon` 是地理围栏边缘最接近测试位置的点的纬度和经度。

     *`距离`是从正在测试的位置到地理围栏边缘最近点的距离。 负数表示地理围栏内部，正数表示外部。 该值将小于 50（默认搜索缓冲区）或 999。

1. 对地理围栏内外的位置重复此操作多次。

## 使用无服务器代码中的地理围栏

现在，您可以向 Functions 应用添加新触发器，以根据地理围栏测试 IoT 中心 GPS 事件数据。

### 消费者群体

正如您在之前的课程中所记得的那样，IoT 中心将允许您重播中心已接收但未处理的事件。 但如果连接多个触发器会发生什么？ 它如何知道哪一个处理了哪些事件。

答案是不可以！ 相反，您可以定义多个单独的连接来读取事件，每个连接都可以管理未读消息的重播。 这些被称为`消费者群体`。 当您连接到端点时，您可以指定要连接到哪个消费者组。 应用程序的每个组件将连接到不同的消费者组

![一个 IoT 中心包含 3 个消费者组，将相同的消息分发到 3 个不同的功能应用程序](../../../../images/consumer-groups.png)

理论上每个消费者组最多可以有 5 个应用程序连接，并且它们到达时都会收到消息。 最佳实践是仅让一个应用程序访问每个使用者组，以避免重复的消息处理，并确保重新启动时正确处理所有排队的消息。 例如，如果您在本地启动 Functions 应用程序并在云中运行它，它们都会处理消息，从而导致存储帐户中存储重复的 blob。

如果您查看在前面的课程中创建的 IoT 中心触发器的`function.json`文件，您将在事件中心触发器绑定部分中看到使用者组：

```json
"consumerGroup": "$Default"
```

创建 IoT 中心时，您将获得默认创建的`$Default`使用者组。 如果您想添加额外的触发器，可以使用新的消费者组来添加它。

> 💁 在本课程中，您将使用与用于存储 GPS 数据的函数不同的函数来测试地理围栏。 这是为了展示如何使用消费者组并分离代码以使其更易于阅读和理解。 在生产应用程序中，您可以通过多种方式构建此功能 - 将两者放在一个函数上，使用存储帐户上的触发器来运行函数来检查地理围栏，或使用多个函数。 没有`正确的方法`，这取决于您的应用程序的其余部分和您的需求。

### 任务 - 创建一个新的消费者组

1. 运行以下命令为您的 IoT 中心创建一个名为`geofence`的新使用者组：

    ```sh
    az iot hub consumer-group create --name geofence \
                                     --hub-name <hub_name>
    ```

    将 `<hub_name>` 替换为您用于 IoT 中心的名称。

1. 如果要查看 IoT 中心的所有使用者组，请运行以下命令：

    ```sh
    az iot hub consumer-group list --output table \
                                   --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为您用于 IoT 中心的名称。 蒂s 将列出所有消费者组。

    ```output
    Name      ResourceGroup
    --------  ---------------
    $Default  gps-sensor
    geofence  gps-sensor
    ```

> 💁 当您在前面的课程中运行 IoT 中心事件监视器时，它连接到 `$Default` 使用者组。 这就是您无法运行事件监视器和事件触发器的原因。 如果您想同时运行两者，那么您可以为所有函数应用程序使用其他使用者组，并为事件监视器保留`$Default`。

### 任务 - 创建新的 IoT 中心触发器

1. 将新的 IoT 中心事件触发器添加到您在前面的课程中创建的`gps-trigger`函数应用。 将此函数称为`geofence-trigger`。

     > ⚠️ 如果需要，您可以参考 [项目 2 第 5 课创建 IoT Hub 事件触发器的说明](../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#create-an-iot-hub-event-trigger).
。

1. 在 `function.json` 文件中配置 IoT 中心连接字符串。 `local.settings.json` 在 Function App 中的所有触发器之间共享。

1. 更新 `function.json` 文件中 `consumerGroup` 的值以引用新的 `geofence` 消费者组：

    ```json
    "consumerGroup": "geofence"
    ```

1. 您将需要在此触发器中使用 Azure Maps 帐户的订阅密钥，因此请在名为`MAPS_KEY`的`local.settings.json`文件中添加一个新条目。

1. 运行 Functions App 以确保其正在连接和处理消息。 前面课程中的`iot-hub-trigger`也将运行并将 blob 上传到存储。

    > 为了避免 blob 存储中出现重复的 GPS 读数，您可以停止在云中运行的 Functions 应用程序。 为此，请使用以下命令：
    >
    > ```sh
    > az functionapp stop --resource-group gps-sensor \
    >                     --name <functions_app_name>
    > ```
    >
    > 将 `<functions_app_name>` 替换为您用于 Functions 应用程序的名称。
    >
    > 您可以稍后使用以下命令重新启动它：
    >
    > ```sh
    > az functionapp start --resource-group gps-sensor \
    >                     --name <functions_app_name>
    > ```
    >
    > 将 `<functions_app_name>` 替换为您用于 Functions 应用程序的名称。

### 任务 - 通过触发器测试地理围栏

在本课程的前面部分，您使用curl 来查询地理围栏以查看某个点是位于内部还是外部。 您可以从触发器内部发出类似的网络请求。

1. 查询地理围栏需要地理围栏的UDID。 使用此值将一个名为`GEOFENCE_UDID`的新条目添加到`local.settings.json`文件中。

1. 从新的`geofence-trigger`触发器中打开`__init__.py`文件。

1. 将以下导入添加到文件顶部：

    ```python
    import json
    import os
    import requests
    ```

     `requests`包允许您进行 Web API 调用。 Azure Maps 没有 Python SDK，您需要进行 Web API 调用才能从 Python 代码中使用它。

1. 将以下两行添加到`main`方法的开头以获取地图订阅密钥：

    ```python
    maps_key = os.environ['MAPS_KEY']
    geofence_udid = os.environ['GEOFENCE_UDID']    
    ```

1. 在`for event in events`循环中，添加以下内容以获取每个事件的纬度和经度：

    ```python
    event_body = json.loads(event.get_body().decode('utf-8'))
    lat = event_body['gps']['lat']
    lon = event_body['gps']['lon']
    ```

     此代码将事件正文中的 JSON 转换为字典，然后从`gps`字段中提取`lat`和`lon`。

1. 使用`requests`时，您可以仅使用 URL 部分并将参数作为字典传递，而不是像使用curl 那样构建长 URL。 添加以下代码定义调用的URL并配置参数：

    ```python
    url = 'https://atlas.microsoft.com/spatial/geofence/json'

    params = {
        'api-version': 1.0,
        'deviceId': 'gps-sensor',
        'subscription-key': maps_key,
        'udid' : geofence_udid,
        'lat' : lat,
        'lon' : lon
    }
    ```

     `params`字典中的项目将与您通过curl调用Web API时使用的键值对匹配。

1. 添加以下代码行来调用Web API：

    ```python
    response = requests.get(url, params=params)
    response_body = json.loads(response.text)
    ```

     这将调用带有参数的 URL，并返回一个响应对象。

1. 在下面添加以下代码：

    ```python
    distance = response_body['geometries'][0]['distance']

    if distance == 999:
        logging.info('Point is outside geofence')
    elif distance > 0:
        logging.info(f'Point is just outside geofence by a distance of {distance}m')
    elif distance == -999:
        logging.info(f'Point is inside geofence')
    else:
        logging.info(f'Point is just inside geofence by a distance of {distance}m')
    ```

     此代码假设 1 个几何图形，并从该单个几何图形中提取距离。 然后它记录根据距离不同的消息。

1. 运行此代码。 您将在日志记录输出中看到 GPS 坐标是在地理围栏内部还是外部，如果该点在 50m 以内，则会看到距离。 根据 GPS 传感器的位置使用不同的地理围栏尝试此代码，尝试移动传感器（例如从手机连接到 WiFi，或使用虚拟 IoT 设备上的不同坐标）以查看此更改。

1. 准备好后，将此代码部署到云中的 Functions 应用程序。 不要忘记部署新的应用程序设置。

     > ⚠️ 如果需要，您可以参考[从项目2第5课上传应用程序设置的说明](../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#task---upload-your-application-settings)。

     > ⚠️ 如果需要，您可以参考[项目 2 第 5 课中部署 Functions 应用程序的说明](../../../2-farm/lessons/5-migrate-application-to-the-cloud/README.md#task---deploy-your-functions-app-to-the-cloud)。

> 💁 您可以在 [code/functions](../code/functions) 文件夹中找到此代码。

---

## 🚀 挑战

在本课程中，您使用具有单个多边形的 GeoJSON 文件添加了一个地理围栏。 您可以同时上传多个多边形，只要它们在`属性`部分具有不同的`geometryId`值即可。

尝试上传包含多个多边形的 GeoJSON 文件，并调整代码以查找 GPS 坐标最接近或位于哪个多边形。

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/28)

## 复习与自学

* 在 [Wikipedia 上的地理围栏页面](https://en.wikipedia.org/wiki/Geo-fence) 上了解有关地理围栏及其一些用例的更多信息。
* 在 [Microsoft Azure Maps Spatial - 获取地理围栏文档](https://docs.microsoft.com/rest/api/maps/spatial/getgeofence?WT.mc_id=academic-17441-jabenn) 上了解有关 Azure Maps 地理围栏 API 的更多信息 ）。
* 有关使用者组的更多信息，请参阅 [Azure 事件中心的功能和术语 - Microsoft 文档上的事件使用者文档](https://docs.microsoft.com/azure/event-hubs/event-hubs-features?WT.mc_id=academic-17441-jabenn#event-consumers)


## 任务

[使用 Twilio 发送通知](../assignment.md)