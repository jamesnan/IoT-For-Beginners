# 可视化位置数据

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-13.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。 单击图像可查看更大的版本。

本视频概述了 Azure Maps with IoT，这是本课程将介绍的一项服务。

[![Azure Maps - Microsoft Azure 企业定位平台](https://img.youtube.com/vi/P5i2GFTtb2s/0.jpg)](https://www.youtube.com/watch?v=P5i2GFTtb2s)

> 🎥 点击上图观看视频

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/25)

## 介绍

在上一课中，您学习了如何使用无服务器代码从传感器获取 GPS 数据，并将其保存到云存储容器中。 现在您将了解如何在 Azure 地图上可视化这些点。 您将学习如何在网页上创建地图、了解 GeoJSON 数据格式以及如何使用它在地图上绘制所有捕获的 GPS 点。

在本课中，我们将介绍：

* [什么是数据可视化](#什么是数据可视化)
* [地图服务](#map-services)
* [创建 Azure Maps 资源](#create-an-azure-maps-resource)
* [在网页上显示地图](#show-a-map-on-a-web-page)
* [GeoJSON 格式](#the-geojson-format)
* [使用 GeoJSON 在地图上绘制 GPS 数据](#plot-gps-data-on-a-map-using-geojson)

> 💁 本课将涉及少量 HTML 和 JavaScript。 如果您想了解有关使用 HTML 和 JavaScript 进行 Web 开发的更多信息，请查看[初学者 Web 开发](https://github.com/microsoft/Web-Dev-For-Beginners)。

## 什么是数据可视化

数据可视化，顾名思义，就是以更易于人类理解的方式将数据可视化。 它通常与图表和图形相关，但是以图形方式表示数据的任何方式，以帮助人们不仅更好地理解数据，而且帮助他们做出决策。

举一个简单的例子 - 回到农场项目中，您捕获了土壤湿度设置。 2021 年 6 月 1 日每小时捕获的土壤湿度数据表可能如下所示：

| Date             | Reading |
| ---------------- | ------: |
| 01/06/2021 00:00 |     257 |
| 01/06/2021 01:00 |     268 |
| 01/06/2021 02:00 |     295 |
| 01/06/2021 03:00 |     305 |
| 01/06/2021 04:00 |     325 |
| 01/06/2021 05:00 |     359 |
| 01/06/2021 06:00 |     398 |
| 01/06/2021 07:00 |     410 |
| 01/06/2021 08:00 |     429 |
| 01/06/2021 09:00 |     451 |
| 01/06/2021 10:00 |     460 |
| 01/06/2021 11:00 |     452 |
| 01/06/2021 12:00 |     420 |
| 01/06/2021 13:00 |     408 |
| 01/06/2021 14:00 |     431 |
| 01/06/2021 15:00 |     462 |
| 01/06/2021 16:00 |     432 |
| 01/06/2021 17:00 |     402 |
| 01/06/2021 18:00 |     387 |
| 01/06/2021 19:00 |     360 |
| 01/06/2021 20:00 |     358 |
| 01/06/2021 21:00 |     354 |
| 01/06/2021 22:00 |     356 |
| 01/06/2021 23:00 |     362 |


作为人类，理解数据可能很困难。 这是一堵没有任何意义的数字墙。 作为可视化此数据的第一步，可以将其绘制在折线图上：

![上述数据的折线图](../../../../images/chart-soil-moisture.png)

通过添加一行来指示自动浇水系统何时在土壤湿度读数为 450 时打开，可以进一步增强此功能：

![450 处的土壤湿度折线图](../../../../images/chart-soil-moisture-relay.png)

该图表不仅可以快速显示土壤湿度水平，还可以显示浇水系统打开的点。

图表并不是可视化数据的唯一工具。 跟踪天气的物联网设备可以拥有使用符号可视化天气状况的网络应用程序或移动应用程序，例如表示阴天的云符号、表示雨天的雨云符号等。 可视化数据的方法有很多种，有很多很严肃，也有一些很有趣。

✅ 想想您所看到的数据可视化的方式。 哪些方法最清晰并且可以让您最快地做出决策？

最好的可视化可以让人类快速做出决策。 例如，有一堵仪表墙显示工业机械的各种读数很难处理，但是当出现问题时闪烁的红灯可以让人们做出决定。 有时最好的可视化是闪烁的灯光！

使用 GPS 数据时，最清晰的可视化是将数据绘制在地图上。 例如，显示送货卡车的地图可以帮助加工厂的工人了解卡车何时到达。 如果这张地图不仅显示了卡车当前位置的图片，而且还提供了卡车内货物的概念，那么工厂的工人就可以做出相应的计划 - 如果他们看到附近有一辆冷藏卡车，他们就知道要准备空间 冰箱。

## 地图服务

使用地图是一项有趣的练习，有很多地图可供选择，例如 Bing 地图、Leaflet、Open Street Maps 和 Google 地图。 在本课中，您将学到有关 [Azure 地图](https://azure.microsoft.com/services/azure-maps/?WT.mc_id=academic-17441-jabenn) 以及它们如何显示您的 GPS 数据。

![Azure Maps 徽标](../../../../images/azure-maps-logo.png)

Azure Maps 是“地理空间服务和 SDK 的集合，它们使用新的地图数据为 Web 和移动应用程序提供地理上下文。” 开发人员可以使用工具来创建精美的交互式地图，这些地图可以提供推荐的交通路线、提供有关交通事件的信息、室内导航、搜索功能、海拔信息、天气服务等。

✅ 尝试一些[映射代码示例](https://docs.microsoft.com/samples/browse?WT.mc_id=academic-17441-jabenn&products=azure-maps)

您可以将地图显示为空白画布、图块、卫星图像、叠加道路的卫星图像、各种类型的灰度地图、带有阴影浮雕的地图以显示高程、夜景地图和高对比度地图。 您可以通过将地图与 [Azure 事件网格](https://azure.microsoft.com/services/event-grid/?WT.mc_id=academic-17441-jabenn) 集成来获取地图的实时更新。 您可以通过启用各种控件来控制地图的行为和外观，以使地图能够对捏合、拖动和单击等事件做出反应。 要控制地图的外观，您可以添加包含气泡、线条、多边形、热图等的图层。 您实现哪种风格的地图取决于您选择的 SDK。

您可以通过 [REST API](https://docs.microsoft.com/javascript/api/azure-maps-rest/?WT.mc_id=academic-17441-jabenn&view=azure-maps-typescript-latest) 及其 [Web SDK](https://docs.microsoft.com/azure/azure-maps/how-to-use-map-control?WT.mc_id=academic-17441-jabenn) 来访问 Azure Maps API。如果您正在构建一个移动应用程序，Z则利用 [Android SDK](https://docs.microsoft.com/azure/azure-maps/how-to-use-android-map-control-library?WT.mc_id=academic-17441-jabenn&pivots=programming-language-java-android)。


在本课程中，您将使用 Web SDK 绘制地图并显示传感器的 GPS 位置路径。

## 创建 Azure Maps 资源

第一步是创建 Azure Maps 帐户。

### 任务 - 创建 Azure Maps 资源

1. 从终端或命令提示符运行以下命令，在“gps-sensor”资源组中创建 Azure Maps 资源：

    ```sh
    az maps account create --name gps-sensor \
                           --resource-group gps-sensor \
                           --accept-tos \
                           --sku S1
    ```

     这将创建一个名为“gps-sensor”的 Azure Maps 资源。 所使用的级别是“S1”，这是一个付费级别，包含一系列功能，但有大量免费通话。

     > 💁 要查看使用 Azure Maps 的费用，请查看 [Azure Maps 定价页面](https://azure.microsoft.com/pricing/details/azure-maps/?WT.mc_id=academic-17441-jabenn) 。

1. 您需要地图资源的 API 密钥。 使用以下命令获取此密钥：

    ```sh
    az maps account keys list --name gps-sensor \
                              --resource-group gps-sensor \
                              --output table
    ```

     获取“PrimaryKey”值的副本。

## 在网页上显示地图

现在您可以采取下一步，即在网页上显示地图。 我们将只为您的小型 Web 应用程序使用一个“html”文件； 请记住，在生产或团队环境中，您的 Web 应用程序很可能会有更多移动部件！

### 任务 - 在网页上显示地图

1. 在本地计算机上的某个文件夹中创建一个名为index.html 的文件。 添加 HTML 标记来保存地图：

    ```html
    <html>
    <head>
        <style>
            #myMap {
                width:100%;
                height:100%;
            }
        </style>
    </head>
    
    <body onload="init()">
        <div id="myMap"></div>
    </body>
    </html>
    ```

     地图将加载到 `myMap` `div` 中。 一些样式允许它跨越页面的宽度和高度。

     > 🎓 `div` 是网页中可以命名和设置样式的部分。

1. 在开始的 `<head>` 标签下，添加外部样式表来控制地图显示，并添加来自 Web SDK 的外部脚本来管理其行为：

     ````html
     <link rel="stylesheet" href="https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.css" type="text/css" />
     <script src="https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.js"></script>
     ````

     该样式表包含地图外观的设置，脚本文件包含加载地图的代码。 添加此代码类似于包含 C++ 头文件或导入 Python 模块。

1. 在该脚本下，添加脚本块以启动地图。

    ```javascript
    <script type='text/javascript'>
        function init() {
            var map = new atlas.Map('myMap', {
                center: [-122.26473, 47.73444],
                zoom: 12,
                authOptions: {
                    authType: "subscriptionKey",
                    subscriptionKey: "<subscription_key>",

                }
            });
        }
    </script>
    ```

    将 `<subscription_key>` 替换为 Azure Maps 帐户的 API 密钥。

    如果您在网络浏览器中打开 `index.html` 页面，您应该会看到加载的地图，并且重点关注西雅图地区。

    ![显示美国华盛顿州西雅图市的地图](../../../../images/map-image.png)

    ✅ 尝试使用缩放和中心参数来更改地图显示。 您可以添加与数据的纬度和经度相对应的不同坐标，以重新居中地图。

> 💁 在本地使用 Web 应用程序的更好方法是安装 [http-server](https://www.npmjs.com/package/http-server)。 在使用此工具之前，您需要安装 [node.js](https://nodejs.org/) 和 [npm](https://www.npmjs.com/)。 安装这些工具后，您可以导航到“index.html”文件的位置并输入“http-server”。 该网络应用程序将在本地网络服务器 [http://127.0.0.1:8080/](http://127.0.0.1:8080/) 上打开。

## GeoJSON 格式

现在您已经有了可以显示地图的 Web 应用程序，您需要从存储帐户中提取 GPS 数据并将其显示在地图顶部的标记层中。 在此之前，让我们先了解一下 Azure Maps 所需的 [GeoJSON](https://wikipedia.org/wiki/GeoJSON) 格式。

[GeoJSON](https://geojson.org/) 是一种开放标准 JSON 规范，具有特殊格式，旨在处理特定于地理的数据。 您可以通过使用 [geojson.io](https://geojson.io) 测试示例数据来了解它，这也是调试 GeoJSON 文件的有用工具。

示例 GeoJSON 数据如下所示：

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -2.10237979888916,
          57.164918677004714
        ]
      }
    }
  ]
}
```

特别有趣的是数据作为 `Feature` 嵌套在 `FeatureCollection` 中的方式。 在该对象中可以找到“几何图形”，其中“坐标”表示纬度和经度。

✅ 构建 geoJSON 时，请注意对象中 `纬度` 和 `经度` 的顺序，否则您的点将不会出现在应有的位置！ GeoJSON 期望数据点的顺序为 `lon,lat`，而不是 `lat,lon`。

`几何图形` 可以有不同的类型，例如单个点或多边形。 在此示例中，它是指定了两个坐标的点：经度和纬度。

✅ Azure Maps 支持标准 GeoJSON 以及一些[增强功能](https://docs.microsoft.com/azure/azure-maps/extend-geojson?WT.mc_id=academic-17441-jabenn)，包括绘制圆圈和 其他几何形状。

## 使用 GeoJSON 在地图上绘制 GPS 数据

现在您已准备好使用在上一课程中构建的存储中的数据。 提醒一下，它作为多个文件存储在 Blob 存储中，因此您需要检索文件并解析它们，以便 Azure Maps 可以使用这些数据。

### 任务 - 配置可从网页访问的存储

如果您调用存储来获取数据，您可能会惊讶地发现浏览器控制台中出现错误。 这是因为您需要为此存储设置 [CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS) 权限，以允许外部 Web 应用程序读取其数据。

> 🎓 CORS 代表“跨源资源共享”，出于安全原因通常需要在 Azure 中明确设置。 它会阻止您不期望的网站访问您的数据。

1. 运行以下命令启用 CORS：
   
    ```sh
    az storage cors add --methods GET \
                        --origins "*" \
                        --services b \
                        --account-name <storage_name> \
                        --account-key <key1>
    ```


    将 `<storage_name>` 替换为您的存储帐户的名称。 将 `<key1>` 替换为您的存储帐户的帐户密钥。

    此命令允许任何网站（通配符“*”表示任意）发出 *GET* 请求，即从您的存储帐户获取数据。 `--services b` 表示仅将此设置应用于 blob。

### 任务 - 从存储加载 GPS 数据

1. 将 `init` 函数的全部内容替换为以下代码：

    ```javascript
    fetch("https://<storage_name>.blob.core.windows.net/gps-data/?restype=container&comp=list")
        .then(response => response.text())
        .then(str => new window.DOMParser().parseFromString(str, "text/xml"))
        .then(xml => {
            let blobList = Array.from(xml.querySelectorAll("Url"));
                blobList.forEach(async blobUrl => {
                    loadJSON(blobUrl.innerHTML)                
        });
    })
    .then( response => {
        map = new atlas.Map('myMap', {
            center: [-122.26473, 47.73444],
            zoom: 14,
            authOptions: {
                authType: "subscriptionKey",
                subscriptionKey: "<subscription_key>",
    
            }
        });
        map.events.add('ready', function () {
            var source = new atlas.source.DataSource();
            map.sources.add(source);
            map.layers.add(new atlas.layer.BubbleLayer(source));
            source.add(features);
        })
    })
    ```

     将 `<storage_name>` 替换为您的存储帐户的名称。 将 `<subscription_key>` 替换为 Azure Maps 帐户的 API 密钥。

     这里发生了几件事。 首先，代码使用使用存储帐户名称构建的 URL 终结点从 Blob 容器中获取 GPS 数据。 此 URL 从 `gps-data` 检索，指示资源类型是容器 (`restype=container`)，并列出有关所有 Blob 的信息。 此列表不会返回 blob 本身，但会返回每个 blob 的 URL，可用于加载 blob 数据。

     > 💁 您可以将此 URL 放入浏览器中以查看容器中所有 Blob 的详细信息。 每个项目都有一个 `Url` 属性，您也可以在浏览器中加载该属性以查看 blob 的内容。

     然后，此代码加载每个 blob，调用接下来将创建的 `loadJSON` 函数。 然后，它创建地图控件，并将代码添加到“ready”事件中。 当地图显示在网页上时调用此事件。

     就绪事件创建一个 Azure Maps 数据源 - 一个包含稍后将填充的 GeoJSON 数据的容器。 然后使用该数据源创建一个气泡层 - 这是地图上以 GeoJSON 中的每个点为中心的一组圆圈。

1. 将 `loadJSON` 函数添加到脚本块中，位于 `init` 函数下方：

    ```javascript
    var map, features;

    function loadJSON(file) {
        var xhr = new XMLHttpRequest();
        features = [];
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    gps = JSON.parse(xhr.responseText)
                    features.push(
                        new atlas.data.Feature(new atlas.data.Point([parseFloat(gps.gps.lon), parseFloat(gps.gps.lat)]))
                    )
                }
            }
        };
        xhr.open("GET", file, true);
        xhr.send();
    }    
    ```

    该函数由 fetch 例程调用，以解析 JSON 数据并将其转换为以 geoJSON 形式读取的经度和纬度坐标。解析后，数据将被设置为 geoJSON“特征”的一部分。 地图将被初始化，并且数据绘制的路径周围将出现小气泡：

1. 在浏览器中加载 HTML 页面。 它将加载地图，然后从存储中加载所有 GPS 数据并将其绘制在地图上。

     ![西雅图附近的圣爱德华州立公园地图，圆圈显示公园边缘的路径](../../../../images/map-path.png)

> 💁 您可以在 [code](..//code) 文件夹中找到此代码。

---

## 🚀 挑战

能够在地图上将静态数据显示为标记真是太好了。 您能否使用带时间戳的 json 文件增强此 Web 应用程序以添加动画并显示标记随时间变化的路径？ 以下是在地图中使用动画的[一些示例](https://azuremapscodesamples.azurewebsites.net/)。

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/26)

## 复习与自学

Azure Maps 对于使用 IoT 设备特别有用。

* 研究 [Microsoft 文档上的 Azure Maps 文档](https://docs.microsoft.com/azure/azure-maps/tutorial-iot-hub-maps?WT.mc_id=academic-17441-jabenn)。
* 通过 [使用 Microsoft Learn 上的 Azure Maps 自助学习模块创建您的第一个路线查找应用程序](https://docs.microsoft.com/learn/modules/create-your-first-app-with-azure-maps/?WT.mc_id=academic-17441-jabenn)。

## 任务

[部署您的应用程序](../assignment.md)                 