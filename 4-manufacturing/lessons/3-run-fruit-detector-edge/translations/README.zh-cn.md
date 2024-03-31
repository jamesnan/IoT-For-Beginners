# 在边缘运行水果探测器

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-17.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。 单击图像可查看更大的版本。

本视频概述了在物联网设备上运行图像分类器，这是本课程涵盖的主题。

[![Azure IoT Edge 上的自定义视觉 AI](https://img.youtube.com/vi/_K5fqGLO8us/0.jpg)](https://www.youtube.com/watch?v=_K5fqGLO8us)

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/33)

## 介绍

在上一课中，您使用图像分类器对成熟和未成熟的水果进行分类，并将物联网设备上的摄像头捕获的图像通过互联网发送到云服务。 这些调用需要时间、成本，并且根据您使用的图像数据的类型，可能会产生隐私问题。

在本课程中，您将了解如何在边缘运行机器学习 (ML) 模型 - 在您自己的网络而不是云中运行的 IoT 设备上。 您将了解边缘计算与云计算的优缺点、如何将 AI 模型部署到边缘以及如何从 IoT 设备访问它。

在本课中，我们将介绍：

* [边缘计算](#edge-computing)
* [Azure IoT Edge](#Azure-IoT-Edge)
* [注册 IoT Edge 设备](#register-an-iot-edge-device)
* [设置 IoT Edge 设备](#set-up-an-iot-edge-device)
* [导出您的模型](#export-your-model)
* [准备容器以进行部署](#prepare-your-container-for-deployment)
* [部署你的容器](#deploy-your-container)
* [使用您的 IoT Edge 设备](#use-your-iot-edge-device)

## 边缘计算

边缘计算涉及让处理物联网数据的计算机尽可能靠近数据生成的地方。 该处理不是在云中进行，而是转移到云的边缘 - 您的内部网络。

![显示云中互联网服务和本地网络上物联网设备的架构图](../../../../images/cloud-without-edge.png)

在到目前为止的课程中，您已经让设备收集数据并将数据发送到云进行分析，在云中运行无服务器功能或 AI 模型。

![显示本地网络上的物联网设备连接到边缘设备以及这些边缘设备连接到云端的架构图](../../../../images/cloud-with-edge.png)

边缘计算涉及将一些云服务从云端移至与物联网设备在同一网络上运行的计算机上，仅在需要时与云进行通信。 例如，您可以在边缘设备上运行人工智能模型来分析水果的成熟度，并且仅将分析结果发送回云端，例如成熟水果的数量与未成熟水果的数量。

✅ 考虑一下您迄今为止构建的 IoT 应用程序。 其中哪些部分可以移动到边缘。

### 优点

边缘计算的优点是：

1. **速度** - 边缘计算非常适合时间敏感的数据，因为操作是在与设备相同的网络上完成的，而不是通过互联网进行调用。 这可以实现更高的速度，因为内部网络的运行速度比互联网连接快得多，数据传输的距离也短得多。

     > 💁 尽管光缆用于互联网连接，允许数据以光速传输，但数据可能需要时间才能在世界各地传输到云提供商。 例如，如果您要将数据从欧洲发送到美国的云服务，则数据通过光缆穿越大西洋至少需要 28 毫秒，并且忽略将数据传输到跨大西洋电缆所需的时间，将 从电信号到光信号，再返回另一侧，然后从光缆到云提供商。

     边缘计算还需要更少的网络流量，从而降低由于互联网连接可用的有限带宽拥塞而导致数据速度减慢的风险。

1. **远程访问** - 当连接有限或没有连接，或者连接过于昂贵而无法持续使用时，边缘计算可以发挥作用。 例如，在基础设施有限的人道主义灾难地区或发展中国家工作时。

1. **降低成本** - 在边缘设备上执行数据收集、存储、分析和触发操作可以减少云服务的使用，从而降低物联网应用程序的总体成本。 最近，专为边缘计算设计的设备有所增加，例如人工智能加速器板，例如 [NVIDIA 的 Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)，它可以 在成本低于 100 美元的设备上使用基于 GPU 的硬件运行 AI 工作负载。

1. **隐私和安全** - 通过边缘计算，数据保留在您的网络上，不会上传到云端。 对于敏感和个人身份信息，这通常是首选，特别是因为数据在分析后不需要存储，这极大地减少了数据的存储量。降低数据泄露的风险。 示例包括医疗数据和安全摄像机镜头。

1. **处理不安全设备** - 如果您的设备存在已知安全缺陷，并且您不想直接连接到您的网络或 Internet，则可以将它们连接到网关 IoT Edge 设备的单独网络。 然后，该边缘设备还可以连接到更广泛的网络或互联网，并管理来回的数据流。

1. **支持不兼容的设备** - 如果您有无法连接到 IoT 中心的设备，例如只能使用 HTTP 连接的设备或只能使用蓝牙连接的设备，您可以使用 IoT 边缘设备作为 网关设备，将消息转发到 IoT 中心。

✅ 做一些研究：边缘计算还有哪些其他优势？

### 缺点

边缘计算也有缺点，而云可能是首选：

1. **规模和灵活性** - 云计算可以通过添加或减少服务器和其他资源来实时调整网络和数据需求。 要添加更多边缘计算机，需要手动添加更多设备。

1. **可靠性和弹性** - 云计算通常在多个位置提供多个服务器，以实现冗余和灾难恢复。 要在边缘拥有相同级别的冗余，需要大量投资和大量配置工作。

1. **维护** - 云服务提供商提供系统维护和更新。

✅ 做一些研究：边缘计算可能还有哪些其他缺点？

其缺点实际上与使用云的优点相反——您必须自己构建和管理这些设备，而不是依赖云提供商的专业知识和规模。

边缘计算的本质缓解了一些风险。 例如，如果您有一个在工厂中运行的边缘设备从机器收集数据，则无需考虑某些灾难恢复场景。 如果工厂断电，那么您就不需要备份边缘设备，因为生成边缘设备处理的数据的机器也将断电。

对于物联网系统，您通常需要云计算和边缘计算的混合，根据系统、客户和维护人员的需求利用每项服务。

## Azure 物联网边缘

![Azure IoT Edge 徽标](../../../../images/azure-iot-edge-logo.png)

Azure IoT Edge 是一项可以帮助你将工作负载从云端移至边缘的服务。 您将设备设置为边缘设备，然后可以从云端将代码部署到该边缘设备。 这使您可以混合云和边缘的功能。

> 🎓 *工作负载* 是一个术语，指的是执行某种工作的任何服务，例如 AI 模型、应用程序或无服务器功能。

例如，您可以在云中训练图像分类器，然后从云将其部署到边缘设备。 然后，您的 IoT 设备将图像发送到边缘设备进行分类，而不是通过互联网发送图像。 如果需要部署模型的新迭代，可以在云中对其进行训练，并使用 IoT Edge 将边缘设备上的模型更新为新迭代。

> 🎓 部署到 IoT Edge 的软件称为*模块*。 默认情况下，IoT Edge 运行与 IoT 中心通信的模块，例如`edgeAgent`和`edgeHub`模块。 当您部署图像分类器时，它将作为附加模块进行部署。

IoT Edge 内置于 IoT 中心，因此您可以使用与管理 IoT 设备相同的服务来管理边缘设备，并具有相同的安全级别。

IoT Edge 从`容器`运行代码 - 自包含应用程序，与计算机上的其他应用程序隔离运行。 当您运行容器时，它就像一台在您的计算机内运行的独立计算机，运行着自己的软件、服务和应用程序。 大多数情况下，容器无法访问计算机上的任何内容，除非您选择与容器共享文件夹等内容。 然后，容器通过开放端口公开服务，您可以连接到或公开到您的网络。

![重定向到容器的 Web 请求](../../../../images/container-web-browser.png)

例如，您可以拥有一个在端口 80（默认 HTTP 端口）上运行网站的容器，然后您也可以在端口 80 上从您的计算机公开该网站。

✅ 做一些研究：阅读有关容器和服务的内容，例如 Docker 或 Moby。

您可以使用自定义视觉下载图像分类器并将其部署为容器，直接运行到设备或通过 IoT Edge 部署。 一旦它们在容器中运行，就可以使用与云版本相同的 REST API 来访问它们，但端点指向运行容器的边缘设备。

## 注册 IoT Edge 设备

要使用 IoT Edge 设备，需要在 IoT 中心注册。

### 任务 - 注册 IoT Edge 设备

1. 在 `fruit-quality- detector` 资源组中创建一个 IoT 中心。 给它一个基于`水果质量检测器`的独特名称。

1. 在 IoT 中心注册一个名为`fruit-quality- detector-edge`的 IoT Edge 设备。 执行此操作的命令类似于用于注册非边缘设备的命令，只不过您传递了`--edge-enabled`标志。

    ```sh
    az iot hub device-identity create --edge-enabled \
                                      --device-id fruit-quality-detector-edge \
                                      --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为 IoT 中心的名称。

1. 使用以下命令获取设备的连接字符串：

    ```sh
    az iot hub device-identity connection-string show --device-id fruit-quality-detector-edge \
                                                      --output table \
                                                      --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为 IoT 中心的名称。

     获取输出中显示的连接字符串的副本。

## 设置 IoT Edge 设备

在 IoT 中心创建边缘设备注册后，您就可以设置边缘设备。

### 任务 - 安装并启动 IoT Edge 运行时

**IoT Edge 运行时仅运行 Linux 容器。**它可以在 Linux 上运行，也可以使用 Linux 虚拟机在 Windows 上运行。

* 如果您使用 Raspberry Pi 作为 IoT 设备，则它运行受支持的 Linux 版本，并且可以托管 IoT Edge 运行时。 按照 [Microsoft 文档上的安装适用于 Linux 的 Azure IoT Edge 指南](https://docs.microsoft.com/azure/iot-edge/how-to-install-iot-edge?WT.mc_id=academic-17441-jabenn ) 安装 IoT Edge 并设置连接字符串。

     > 💁 请记住，Raspberry Pi OS 是 Debian Linux 的变体。

* 如果您没有使用 Raspberry Pi，但拥有 Linux 计算机，则可以运行 IoT Edge 运行时。 按照 [Microsoft 文档上的安装适用于 Linux 的 Azure IoT Edge 指南](https://docs.microsoft.com/azure/iot-edge/how-to-install-iot-edge?WT.mc_id=academic-17441-jabenn) 安装 IoT Edge 并设置连接字符串。

* 如果您使用的是 Windows，则可以按照 [Microsoft 文档上的将第一个 IoT Edge 模块部署到 Windows 设备快速入门的安装并启动 IoT Edge 运行时部分](https://docs.microsoft.com/azure/iot-edge/quickstart?WT.mc_id=academic-17441-jabenn#install-and-start-the-iot-edge-runtime)。 当您到达*部署模块*部分时，您可以停止。

* 如果您使用的是 macOS，则可以在云中创建虚拟机 (VM) 以用于 IoT Edge 设备。 您可以在云中创建并通过互联网访问这些计算机。 您可以创建安装了 IoT Edge 的 Linux VM。 请按照[创建运行 IoT Edge 的虚拟机指南](../vm-iotedge.md) 获取有关如何执行此操作的说明。

## 导出你的模型

要在边缘运行分类器，需要从 Custom Vision 导出它。 Custom Vision 可以生成两种类型的模型 - 标准模型和紧凑模型。 紧凑模型使用各种技术来减小模型的大小，使其足够小，可以下载并部署在物联网设备上。

创建图像分类器时，您使用了 *Food* 域，这是针对食物图像训练而优化的模型版本。 在自定义视觉中，您可以更改项目的领域，使用训练数据来训练具有新领域的新模型。 Custom Vision 支持的所有领域均可作为标准和紧凑型提供。

### 任务 - 使用 Food（紧凑）域训练您的模型

1. 在 [CustomVision.ai](https://customvision.ai) 上启动 Custom Vision 门户，如果尚未打开，请登录。 然后打开您的`水果质量检测器`项目。

1. 选择 **设置** 按钮（⚙ 图标）

1. 在*域*列表中，选择*食品（紧凑）*

1. 在*导出功能*下，确保选择*基本平台（Tensorflow、CoreML、ONNX，...）*。

1. 在`设置`页面底部，选择`**保存更改**`。

1. 使用 **训练** 按钮重新训练模型，选择 *快速训练*。

### 任务 - 导出你的模型

模型训练完成后，需要将其导出为容器。

1. 选择 **性能** 选项卡，然后找到使用紧凑域训练的最新迭代。

1. 选择顶部的 **导出** 按钮。

1. 选择 **DockerFile**，然后选择与您的边缘设备匹配的版本：

     * 如果您在 Linux 计算机、Windows 计算机或虚拟机上运行 IoT Edge，请选择 *Linux* 版本。
     * 如果您在 Raspberry Pi 上运行 IoT Edge，请选择 *ARM (Raspberry Pi 3)* 版本。

     > 🎓 Docker 是最流行的容器管理工具之一，DockerFile 是一组有关如何设置容器的指令。

1. 选择 **导出** 以让 Custom Vision 创建相关文件，然后选择 **下载** 以 zip 文件形式下载它们。

1. 将文件保存到您的计算机，然后解压缩文件夹。

## 准备用于部署的容器

![构建容器，然后推送到容器注册表，然后使用 IoT Edge 从容器注册表部署到边缘设备](../../../../images/container-edge-flow.png)

下载模型后，需要将其构建到容器中，然后推送到容器注册表 - 一个可以存储容器的在线位置。 然后，IoT Edge 可以从注册表下载容器并将其推送到您的设备。

![Azure 容器注册表徽标](../../../../images/azure-container-registry-logo.png)

本课程将使用的容器注册表是 Azure 容器注册表。 这不是免费服务，因此为了省钱，请确保在完成后[清理您的项目](../../../../clean-up.md)。

> 💁 您可以在[Azure 容器注册表定价页面](https://azure.microsoft.com/pricing/details/container-registry/?WT.mc_id=academic-17441-jabenn) 中查看使用 Azure 容器注册表的费用

### 任务 - 安装 Docker

要构建和部署分类器分类器，您可能需要安装[Docker](https://www.docker.com/)。

仅当您计划从安装 IoT Edge 的另一台设备构建容器时，才需要执行此操作 - 作为安装 IoT Edge 的一部分，会为您安装 Docker。

1. 如果在与 IoT Edge 设备不同的设备上构建 docker 容器，请按照 [Docker 安装页面](https://www.docker.com/products/docker-desktop) 上的 Docker 安装说明安装 Docker 桌面或 Docker 引擎。 确保安装后正在运行。

### 任务 - 创建容器注册表资源

1. 从终端或命令提示符运行以下命令来创建 Azure 容器注册表资源：
    
    ```sh
    az acr create --resource-group fruit-quality-detector \
                  --sku Basic \
                  --name <Container registry name>
    ```

     将`<容器注册表名称>`替换为容器注册表的唯一名称，仅使用字母和数字。 其基础是`水果质量检测器`。 该名称成为访问容器注册表的 URL 的一部分，因此需要全局唯一。

1. 使用以下命令登录 Azure 容器注册表：

    ```sh
    az acr login --name <Container registry name>
    ```

     将`<容器注册表名称>`替换为您用于容器注册表的名称。

1. 将容器注册表设置为管理模式，以便您可以使用以下命令生成密码：

    ```sh
    az acr update --admin-enabled true \
                 --name <Container registry name>
    ```

     将`<容器注册表名称>`替换为您用于容器注册表的名称。

1. 使用以下命令为容器注册表生成密码：

    ```sh
     az acr credential renew --password-name password \
                             --output table \
                             --name <Container registry name>
    ```

     将`<容器注册表名称>`替换为您用于容器注册表的名称。

     复制`PASSWORD`的值，稍后您将需要它。

### 任务 - 构建你的容器

您从 Custom Vision 下载的是一个 DockerFile，其中包含有关如何构建容器的说明，以及将在容器内运行以托管自定义视觉模型的应用程序代码，以及用于调用它的 REST API。 您可以使用 Docker 从 DockerFile 构建标记容器，然后将其推送到容器注册表。

> 🎓 容器被赋予一个标签，用于定义它们的名称和版本。 当您需要更新容器时，您可以使用相同的标签但更新的版本来构建它。

1. 打开终端或命令提示符并导航到从 Custom Vision 下载的解压模型。

1. 运行以下命令来构建并标记镜像：

    ```sh
    docker build --platform <platform> -t <Container registry name>.azurecr.io/classifier:v1 .
    ```

     将 `<platform>` 替换为该容器将运行的平台。 如果您在 Raspberry Pi 上运行 IoT Edge，请将其设置为`linux/armhf`，否则将其设置为`linux/amd64`。

     > 💁 如果您从运行 IoT Edge 的设备运行此命令，例如从 Raspberry Pi 运行此命令，则可以省略 `--platform <platform>` 部分，因为它默认为当前平台。

     将`<容器注册表名称>`替换为您用于容器注册表的名称。

     > 💁 如果您在 Linux 或 Raspberry Pi 操作系统上运行，您可能需要使用 `sudo` 来运行此命令。

     Docker 将构建镜像，配置所有需要的软件。 然后该图像将被标记为`classifier:v1`。

   ```output
    ➜  d4ccc45da0bb478bad287128e1274c3c.DockerFile.Linux docker build --platform linux/amd64 -t  fruitqualitydetectorjimb.azurecr.io/classifier:v1 .
    [+] Building 102.4s (11/11) FINISHED
     => [internal] load build definition from Dockerfile
     => => transferring dockerfile: 131B
     => [internal] load .dockerignore
     => => transferring context: 2B
     => [internal] load metadata for docker.io/library/python:3.7-slim
     => [internal] load build context
     => => transferring context: 905B
     => [1/6] FROM docker.io/library/python:3.7-slim@sha256:b21b91c9618e951a8cbca5b696424fa5e820800a88b7e7afd66bba0441a764d6
     => => resolve docker.io/library/python:3.7-slim@sha256:b21b91c9618e951a8cbca5b696424fa5e820800a88b7e7afd66bba0441a764d6
     => => sha256:b4d181a07f8025e00e0cb28f1cc14613da2ce26450b80c54aea537fa93cf3bda 27.15MB / 27.15MB
     => => sha256:de8ecf497b753094723ccf9cea8a46076e7cb845f333df99a6f4f397c93c6ea9 2.77MB / 2.77MB
     => => sha256:707b80804672b7c5d8f21e37c8396f319151e1298d976186b4f3b76ead9f10c8 10.06MB / 10.06MB
     => => sha256:b21b91c9618e951a8cbca5b696424fa5e820800a88b7e7afd66bba0441a764d6 1.86kB / 1.86kB
     => => sha256:44073386687709c437586676b572ff45128ff1f1570153c2f727140d4a9accad 1.37kB / 1.37kB
     => => sha256:3d94f0f2ca798607808b771a7766f47ae62a26f820e871dd488baeccc69838d1 8.31kB / 8.31kB
     => => sha256:283715715396fd56d0e90355125fd4ec57b4f0773f306fcd5fa353b998beeb41 233B / 233B
     => => sha256:8353afd48f6b84c3603ea49d204bdcf2a1daada15f5d6cad9cc916e186610a9f 2.64MB / 2.64MB
     => => extracting sha256:b4d181a07f8025e00e0cb28f1cc14613da2ce26450b80c54aea537fa93cf3bda
     => => extracting sha256:de8ecf497b753094723ccf9cea8a46076e7cb845f333df99a6f4f397c93c6ea9
     => => extracting sha256:707b80804672b7c5d8f21e37c8396f319151e1298d976186b4f3b76ead9f10c8
     => => extracting sha256:283715715396fd56d0e90355125fd4ec57b4f0773f306fcd5fa353b998beeb41
     => => extracting sha256:8353afd48f6b84c3603ea49d204bdcf2a1daada15f5d6cad9cc916e186610a9f
     => [2/6] RUN pip install -U pip
     => [3/6] RUN pip install --no-cache-dir numpy~=1.17.5 tensorflow~=2.0.2 flask~=1.1.2 pillow~=7.2.0
     => [4/6] RUN pip install --no-cache-dir mscviplib==2.200731.16
     => [5/6] COPY app /app
     => [6/6] WORKDIR /app
     => exporting to image
     => => exporting layers
     => => writing image sha256:1846b6f134431f78507ba7c079358ed66d944c0e185ab53428276bd822400386
     => => naming to fruitqualitydetectorjimb.azurecr.io/classifier:v1
    ```
### 任务 - 将容器推送到容器注册表

1. 使用以下命令将容器推送到容器注册表：

    ```sh
    docker push <Container registry name>.azurecr.io/classifier:v1
    ```

     将`<容器注册表名称>`替换为您用于容器注册表的名称。

     > 💁 如果您运行的是 Linux，则可能需要使用 `sudo` 来运行此命令。

     容器将被推送到容器注册表。

    ```output
    ➜  d4ccc45da0bb478bad287128e1274c3c.DockerFile.Linux docker push fruitqualitydetectorjimb.azurecr.io/classifier:v1
    The push refers to repository [fruitqualitydetectorjimb.azurecr.io/classifier]
    5f70bf18a086: Pushed 
    8a1ba9294a22: Pushed 
    56cf27184a76: Pushed 
    b32154f3f5dd: Pushed 
    36103e9a3104: Pushed 
    e2abb3cacca0: Pushed 
    4213fd357bbe: Pushed 
    7ea163ba4dce: Pushed 
    537313a13d90: Pushed 
    764055ebc9a7: Pushed 
    v1: digest: sha256:ea7894652e610de83a5a9e429618e763b8904284253f4fa0c9f65f0df3a5ded8 size: 2423
    ```

1. 要验证推送，您可以使用以下命令列出注册表中的容器：

    ```sh
    az acr repository list --output table \
                           --name <Container registry name> 
    ```

     将`<容器注册表名称>`替换为您用于容器注册表的名称。

    ```output
    ➜  d4ccc45da0bb478bad287128e1274c3c.DockerFile.Linux az acr repository list --name fruitqualitydetectorjimb --output table
    Result
    ----------
    classifier

     您将看到输出中列出了您的分类器。

## 部署你的容器

现在可以将容器部署到 IoT Edge 设备。 要进行部署，您需要定义一个部署清单 - 一个 JSON 文档，其中列出了将部署到边缘设备的模块。

### 任务 - 创建部署清单

1. 在计算机上的某个位置创建一个名为`deployment.json`的新文件。

1. 将以下内容添加到该文件中：

    ```json
    {
        "content": {
            "modulesContent": {
                "$edgeAgent": {
                    "properties.desired": {
                        "schemaVersion": "1.1",
                        "runtime": {
                            "type": "docker",
                            "settings": {
                                "minDockerVersion": "v1.25",
                                "loggingOptions": "",
                                "registryCredentials": {
                                    "ClassifierRegistry": {
                                        "username": "<Container registry name>",
                                        "password": "<Container registry password>",
                                        "address": "<Container registry name>.azurecr.io"
                                      }
                                }
                            }
                        },
                        "systemModules": {
                            "edgeAgent": {
                                "type": "docker",
                                "settings": {
                                    "image": "mcr.microsoft.com/azureiotedge-agent:1.1",
                                    "createOptions": "{}"
                                }
                            },
                            "edgeHub": {
                                "type": "docker",
                                "status": "running",
                                "restartPolicy": "always",
                                "settings": {
                                    "image": "mcr.microsoft.com/azureiotedge-hub:1.1",
                                    "createOptions": "{\"HostConfig\":{\"PortBindings\":{\"5671/tcp\":[{\"HostPort\":\"5671\"}],\"8883/tcp\":[{\"HostPort\":\"8883\"}],\"443/tcp\":[{\"HostPort\":\"443\"}]}}}"
                                }
                            }
                        },
                        "modules": {
                            "ImageClassifier": {
                                "version": "1.0",
                                "type": "docker",
                                "status": "running",
                                "restartPolicy": "always",
                                "settings": {
                                    "image": "<Container registry name>.azurecr.io/classifier:v1",
                                    "createOptions": "{\"ExposedPorts\": {\"80/tcp\": {}},\"HostConfig\": {\"PortBindings\": {\"80/tcp\": [{\"HostPort\": \"80\"}]}}}"
                                }
                            }
                        }
                    }
                },
                "$edgeHub": {
                    "properties.desired": {
                        "schemaVersion": "1.1",
                        "routes": {
                            "upstream": "FROM /messages/* INTO $upstream"
                        },
                        "storeAndForwardConfiguration": {
                            "timeToLiveSecs": 7200
                        }
                    }
                }
            }
        }
    }
    ```
     > 💁 您可以在 [code-deployment/deployment](code-deployment/deployment) 文件夹中找到该文件。

     将`<容器注册表名称>`的三个实例替换为您用于容器注册表的名称。 一个位于`ImageClassifier`模块部分，另外两个位于`registryCredentials`部分。

     将`registryCredentials`部分中的`<容器注册表密码>`替换为您的容器注册表密码。

1. 从包含部署清单的文件夹中，运行以下命令：

    ```sh
    az iot edge set-modules --device-id fruit-quality-detector-edge \
                            --content deployment.json \
                            --hub-name <hub_name>
    ```

     将 `<hub_name>` 替换为 IoT 中心的名称。

     图像分类器模块将部署到您的边缘设备。

### 任务 - 验证分类器正在运行

1. 连接物联网边缘设备：

     * 如果您使用 Raspberry Pi 运行 IoT Edge，请从终端或通过 VS Code 中的远程 SSH 会话使用 ssh 进行连接
     * 如果您在 Windows 上的 Linux 容器中运行 IoT Edge，请按照[验证成功配置指南](https://docs.microsoft.com/azure/iot-edge/how-to-install-iot-edge-on-windows?WT.mc_id=academic-17441-jabenn&view=iotedge-2018-06&tabs=powershell#verify-successful-configuration) 连接到 IoT Edge 设备。
     * 如果在虚拟机上运行 IoT Edge，则可以使用创建 VM 时设置的`adminUsername`和`password`以及 IP 地址或 DNS 名称通过 SSH 登录到计算机：

        ```sh
        ssh <adminUsername>@<IP address>
        ```

         或者：

        ```sh
        ssh <adminUsername>@<DNS Name>
        ```

         出现提示时输入您的密码

1. 连接后，运行以下命令以获取 IoT Edge 模块列表：

    ```sh
    iotedge list
    ```

     > 💁 您可能需要使用 `sudo` 来运行此命令。

     您将看到正在运行的模块：

    ```output
    jim@fruit-quality-detector-jimb:~$ iotedge list
    NAME             STATUS           DESCRIPTION      CONFIG
    ImageClassifier  running          Up 42 minutes    fruitqualitydetectorjimb.azurecr.io/classifier:v1
    edgeAgent        running          Up 42 minutes    mcr.microsoft.com/azureiotedge-agent:1.1
    edgeHub          running          Up 42 minutes    mcr.microsoft.com/azureiotedge-hub:1.1
    ```

1. 使用以下命令检查图像分类器模块的日志：

    ```sh
    iotedge logs ImageClassifier
    ```

     > 💁 您可能需要使用 `sudo` 来运行此命令。

    ```output
    jim@fruit-quality-detector-jimb:~$ iotedge logs ImageClassifier
    2021-07-05 20:30:15.387144: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
    2021-07-05 20:30:15.392185: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 2394450000 Hz
    2021-07-05 20:30:15.392712: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x55ed9ac83470 executing computations on platform Host. Devices:
    2021-07-05 20:30:15.392806: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): Host, Default Version
    Loading model...Success!
    Loading labels...2 found. Success!
     * Serving Flask app "app" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
    ```

### 任务 - 测试图像分类器

1. 可以使用 CURL 使用运行 IoT Edge 代理的计算机的 IP 地址或主机名来测试图像分类器。 查找IP地址：

     * 如果您与 IoT Edge 运行在同一台计算机上，则可以使用`localhost`作为主机名。
     * 如果您使用的是 VM，则可以使用 VM 的 IP 地址或 DNS 名称
     * 否则，您可以获得运行 IoT Edge 的计算机的 IP 地址：
       * 在 Windows 10 上，请按照[查找您的 IP 地址指南](https://support.microsoft.com/windows/find-your-ip-address-f21a9bbc-c582-55cd-35e0-73431160a1b9?WT.mc_id=academic-17441-jabenn)
       * 在 macOS 上，请按照[如何在 Mac 上查找 IP 地址指南](https://www.hellotech.com/guide/for/how-to-find-ip-address-on-mac)
       * 在 Linux 上，请按照 [如何在 Linux 中查找 IP 地址指南](https://opensource.com/article/18/5/how-find-ip-address-linux) 中查找您的私有 IP 地址的部分进行操作 ）

1. 您可以通过运行以下curl命令使用本地文件测试容器：

    ```sh
    curl --location \
         --request POST 'http://<IP address or name>/image' \
         --header 'Content-Type: image/png' \
         --data-binary '@<file_Name>' 
    ```

     将`<IP 地址或名称>`替换为运行 IoT Edge 的计算机的 IP 地址或主机名。 将 `<file_Name>` 替换为要测试的文件的名称。

     您将在输出中看到预测结果：

    ```output
    {
        "created": "2021-07-05T21:44:39.573181",
        "id": "",
        "iteration": "",
        "predictions": [
            {
                "boundingBox": null,
                "probability": 0.9995615482330322,
                "tagId": "",
                "tagName": "ripe"
            },
            {
                "boundingBox": null,
                "probability": 0.0004384400090202689,
                "tagId": "",
                "tagName": "unripe"
            }
        ],
        "project": ""
    }
    ```
     > 💁 此处无需提供预测密钥，因为这不使用 Azure 资源。 相反，安全性将根据内部安全需求在内部网络上配置，而不是依赖公共端点和 API 密钥。

## 使用您的 IoT Edge 设备

现在，图像分类器已部署到 IoT Edge 设备，您可以从 IoT 设备使用它。

### 任务 - 使用 IoT Edge 设备

完成相关指南以使用 IoT Edge 分类器对图像进行分类：

* [Arduino - Wio 终端](../wio-terminal.md)
* [单板计算机-Raspberry Pi/虚拟物联网设备](../single-board-computer.md)

### 模型再训练

在 IoT Edge 上运行图像分类器的缺点之一是它们未连接到自定义视觉项目。 如果您查看自定义视觉中的 **预测** 选项卡，您将看不到使用基于边缘的分类器分类的图像。

这是预期的行为 - 图像不会发送到云进行分类，因此它们在云中不可用。 使用 IoT Edge 的优点之一是隐私，确保图像不会离开网络，另一个优点是能够离线工作，因此在设备没有互联网连接时无需依赖上传图像。 缺点是改进模型 - 您需要实现另一种存储图像的方法，可以手动重新分类以改进和重新训练图像分类器。

✅ 考虑如何上传图像来重新训练分类器。

---

## 🚀 挑战

在边缘设备上运行人工智能模型比在云中运行速度更快——网络跳数更短。 它们也可能会更慢，因为运行模型的硬件可能不如云强大。

进行一些计时并比较对边缘设备的调用是否比对云的调用更快或更慢？ 想想原因o 解释差异或缺乏差异。 研究使用专用硬件在边缘更快运行人工智能模型的方法。

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/34)

## 复习与自学

* 在 [Wikipedia 上的操作系统级虚拟化页面](https://wikipedia.org/wiki/OS-level_virtualization) 上了解有关容器的更多信息
* 阅读有关边缘计算的更多内容，重点是 5G 如何帮助扩展边缘计算 [什么是边缘计算以及它为何重要？ 关于 NetworkWorld 的文章](https://www.networkworld.com/article/3224893/what-is-edge-computing-and-how-it-s-changing-the-network.html)
* 通过观看  [Microsoft Channel9 上的 Learn Live 节目](https://channel9.msdn.com/Shows/Learn-Live/Sharpen-Your-AI-Edge-Skills-Episode-4-Learn-How-to-Use-Azure-IoT-Edge-on-Pre-Built-AI-Service-on-t?WT.mc_id=academic-17441-jabenn)，了解有关在 IoT Edge 中运行 AI 服务的更多信息

## 任务

[在边缘运行其他服务](../assignment.md)