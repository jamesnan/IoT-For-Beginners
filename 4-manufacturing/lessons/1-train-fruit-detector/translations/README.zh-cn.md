# 训练水果品质检测器

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-15.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。 单击图像可查看更大的版本。

本视频概述了 Azure 自定义视觉服务，该服务将在本课程中介绍。

[![自定义视觉 – 机器学习变得简单 | Xamarin 秀](https://img.youtube.com/vi/TETcDLJlWR4/0.jpg)](https://www.youtube.com/watch?v=TETcDLJlWR4)

> 🎥 点击上图观看视频

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/29)

## 介绍

最近人工智能 (AI) 和机器学习 (ML) 的兴起为当今的开发人员提供了广泛的功能。 机器学习模型可以经过训练来识别图像中的不同物体，包括未成熟的水果，这可以在物联网设备中使用，以帮助在收获时或在工厂或仓库加工过程中对农产品进行分类。

在本课程中，您将学习图像分类 - 使用机器学习模型来区分不同事物的图像。 您将学习如何训练图像分类器来区分好水果和坏水果（未熟或过熟、碰伤或腐烂）。

在本课中，我们将介绍：

* [使用人工智能和机器学习对食物进行分类](#using-ai-and-ml-to-sort-food)
* [通过机器学习进行图像分类](#image-classification-via-machine-learning)
* [训练图像分类器](#train-an-image-classifier)
* [测试你的图像分类器](#test-your-image-classifier)
* [重新训练你的图像分类器](#retrain-your-image-classifier)

## 使用人工智能和机器学习对食物进行分类

养活全球人口是很困难的，尤其是在价格让所有人都能负担得起的情况下。 最大的成本之一是劳动力，因此农民越来越多地转向自动化和物联网等工具来降低劳动力成本。 手工收割是劳动密集型的（而且通常是辛苦的工作），并且正在被机械所取代，特别是在富裕国家。 尽管使用机械收割可以节省成本，但也有一个缺点——无法在收割时对食物进行分类。

并非所有农作物都能均匀成熟。 例如，当大多数西红柿准备好收获时，藤上仍然可以结出一些绿色水果。 尽管提早收割这些作物是一种浪费，但对于农民来说，使用机械收割所有东西并稍后处理未成熟的农产品更便宜且更容易。

✅ 看看不同的水果或蔬菜，无论是在您附近的农场、花园还是商店中生长的，它们的成熟度是否都相同，或者您是否看到差异？

自动化收割的兴起将农产品的分类从收割转移到了工厂。 食物会在长长的传送带上传送，由一群人挑选产品，去除任何不符合质量标准的东西。 由于有了机械，收割变得更便宜，但手动分类食物仍然有成本。

![如果检测到红色番茄，它会不间断地继续其旅程。 如果检测到绿色番茄，则会通过杠杆将其弹入垃圾桶](../../../../images/optical-tomato-sorting.png)

下一步的发展是使用机器进行分类，要么内置于收割机中，要么内置于加工厂中。 第一代机器使用光学传感器来检测颜色，控制执行器使用杠杆或喷气将绿色西红柿推入垃圾桶，而红色西红柿则继续在传送带网络上运行。

在这段视频中，当西红柿从一条传送带落到另一条传送带时，绿色西红柿会被检测到并使用杠杆弹入垃圾箱。

✅ 在工厂或现场，这些光学传感器需要什么条件才能正常工作？

这些分拣机的最新发展利用了人工智能和机器学习，使用经过训练的模型来区分好产品和坏产品，不仅通过明显的颜色差异（例如绿色西红柿与红色西红柿），还通过外观上更细微的差异（可以表明疾病或瘀伤） 。

## 通过机器学习进行图像分类

传统编程是获取数据、对数据应用算法并获得输出。 例如，在上一个项目中，您获取了 GPS 坐标和地理围栏，应用了 Azure Maps 提供的算法，并返回了该点是否位于地理围栏内部或外部的结果。 输入更多数据，就会得到更多输出。

![传统开发需要输入和算法并给出输出。 机器学习使用输入和输出数据来训练模型，并且该模型可以采用新的输入数据来生成新的输出](../../../../images/traditional-vs-ml.png)

机器学习扭转了这一局面——从数据和已知输出开始，机器学习算法从数据中学习。 然后，您可以采用经过训练的算法（称为`机器学习模型`或`模型`），并输入新数据并获得新输出。

> 🎓 机器的流程从数据中学习的学习算法称为`训练`。 输入和已知输出称为`训练数据`。

例如，您可以为模型提供数百万张未成熟香蕉的图片作为输入训练数据，训练输出设置为`未成熟`，以及数百万张成熟香蕉图片作为训练数据，输出设置为`成熟`。 然后，机器学习算法将根据这些数据创建一个模型。 然后，你给这个模型一张香蕉的新图片，它会预测新图片是成熟的香蕉还是未成熟的香蕉。

> 🎓 ML 模型的结果称为*预测*

![2根香蕉，一根成熟的香蕉，预测成熟度为99.7%，未成熟的0.3%，一根未成熟的香蕉，预测成熟度为1.4%，未成熟的98.6%](../../../../images//bananas-ripe-vs-unripe-predictions.png)


机器学习模型不会给出二元答案，而是给出概率。 例如，模型可能会得到一张香蕉的图片，并预测成熟`为 99.7%，`未成熟`为 0.3%。 然后，您的代码将选择最佳预测并确定香蕉成熟了。

用于检测此类图像的 ML 模型称为`图像分类器`——它会给出带标签的图像，然后根据这些标签对新图像进行分类。

> 💁 这是一种过度简化，还有许多其他方法来训练并不总是需要标记输出的模型，例如无监督学习。 如果您想了解有关 ML 的更多信息，请查看 [ML 初学者，关于机器学习的 24 课课程](https://aka.ms/ML-beginners)。

## 训练图像分类器

要成功训练图像分类器，您需要数百万张图像。 事实证明，一旦你有了一个在数百万或数十亿张分类图像上训练的图像分类器，你就可以重复使用它，并使用一小组图像重新训练它，并使用称为`迁移学习`的过程获得很好的结果 。

> 🎓 迁移学习是将现有机器学习模型的学习迁移到基于新数据的新模型。

一旦图像分类器接受了各种图像的训练，它的内部结构就非常擅长识别形状、颜色和图案。 迁移学习允许模型利用在识别图像部分时已经学到的知识，并用它来识别新图像。

![一旦您能够识别形状，就可以将它们放入不同的配置中以制作船或猫](../../../../images/shapes-to-images.png)

你可以把它想象成有点像儿童形状书，一旦你能认出半圆、长方形和三角形，你就能根据这些形状的配置认出帆船或猫。 图像分类器可以识别形状，迁移学习可以教会它什么组合可以构成船或猫，或者成熟的香蕉。

有多种工具可以帮助您做到这一点，包括基于云的服务，可以帮助您训练模型，然后通过 Web API 使用它。

> 💁 训练这些模型需要大量的计算机能力，通常通过图形处理单元或 GPU。 使 Xbox 上的游戏看起来很棒的专用硬件也可用于训练机器学习模型。 通过使用云，您可以在配备 GPU 的强大计算机上租用时间来训练这些模型，从而在需要时获得所需的计算能力。

## 自定义视觉

Custom Vision 是一种基于云的工具，用于训练图像分类器。 它允许您仅使用少量图像来训练分类器。 您可以通过门户网站、Web API 或 SDK 上传图像，为每个图像提供一个具有该图像分类的*标签*。 然后，您训练模型并对其进行测试以查看其性能如何。 一旦您对模型感到满意，您就可以发布可通过 Web API 或 SDK 访问的版本。

![Azure 自定义视觉徽标](../../../../images/custom-vision-logo.png)

> 💁 您可以使用每个分类最少 5 个图像来训练自定义视觉模型，但越多越好。 至少使用 30 张图像可以获得更好的结果。

自定义视觉是微软称为认知服务的一系列人工智能工具的一部分。 这些人工智能工具无需任何培训或只需少量培训即可使用。 它们包括语音识别和翻译、语言理解和图像分析。 这些可作为 Azure 中的免费服务使用。

> 💁 免费套餐足以创建模型、训练模型，然后将其用于开发工作。 您可以在 [Microsoft 文档上的自定义视觉限制和配额页面](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/limits-and-quotas?WT.mc_id=academic-17441-jabenn) 上了解免费套餐。

### 任务 - 创建认知服务资源

要使用自定义视觉，首先需要使用 Azure CLI 在 Azure 中创建两个认知服务资源，一个用于自定义视觉训练，一个用于自定义视觉预测。

1.为此项目创建一个名为`fruit-quality- detector`的资源组

1. 使用以下命令可创建免费的自定义视觉培训资源：

    ```sh
    az cognitiveservices account create --name fruit-quality-detector-training \
                                        --resource-group fruit-quality-detector \
                                        --kind CustomVision.Training \
                                        --sku F0 \
                                        --yes \
                                        --location <location>
    ```

     将 `<location>` 替换为您在创建资源组时使用的位置。

     这将在您的资源组中创建自定义视觉培训资源。 它将被称为`fruit-quality- detector-training`并使用`F0` sku，即免费套餐。 `--yes`选项表示您同意认知服务的条款和条件。

> 💁 如果您已经拥有使用任何认知服务的免费帐户，请使用`S0` sku。

1. 使用以下命令创建免费的自定义视觉预测资源：

    ```sh
    az cognitiveservices account create --name fruit-quality-detector-prediction \
                                        --resource-group fruit-quality-detector \
                                        --kind CustomVision.Prediction \
                                        --sku F0 \
                                        --yes \
                                        --location <location>
    ```

     将 `<location>` 替换为您在创建资源组时使用的位置。

     这将在您的资源组中创建自定义视觉预测资源。 它将被称为`fruit-quality- detector-prediction`并使用`F0` sku，这是免费套餐。 `--yes`选项表示您同意认知服务的条款和条件。

### 任务 - 创建图像分类器项目

1. 通过 [CustomVision.ai](https://customvision.ai) 启动自定义视觉门户，然后使用您用于 Azure 帐户的 Microsoft 帐户登录。

1. 按照 [Microsoft 文档上构建分类器快速入门的创建新项目部分](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier?WT.mc_id=academic-17441-jabenn#create-a-new-project) 创建一个新的自定义视觉项目。 用户界面可能会发生变化，这些文档始终是最新的参考。

     将您的项目命名为`水果质量检测器`。

     创建项目时，请确保使用之前创建的`fruit-quality- detector-training`资源。 使用 *Classification* 项目类型、*Multiclass* 分类类型和 *Food* 域。

     ![自定义视觉项目的设置，名称设置为fruit-quality- detector，无描述，资源设置为fruit-quality- detector-training，项目类型设置为classification，分类类型设置为multi class， 域设置为食物](../../../../images/custom-vision-create-project.png)

✅ 花一些时间探索图像分类器的自定义视觉 UI。

### 任务 - 训练你的图像分类器项目

要训练图像分类器，您需要多张水果图片（质量好坏）来标记好坏，例如成熟的香蕉和过熟的香蕉。

> 💁 这些分类器可以对任何东西的图像进行分类，所以如果你手头没有不同质量的水果，你可以使用两种不同类型的水果，或者猫和狗！

理想情况下，每张图片应该只是水果，具有一致的背景或多种背景。 确保背景中没有任何特定于成熟和未成熟水果的内容。

> 💁 重要的是不要有特定的背景，或者每个标签的与要分类的事物不相关的特定项目，否则分类器可能只是根据背景进行分类。 有一个皮肤癌分类器，针对正常和癌变的痣进行了训练，并且癌变的痣都有标尺来测量它们的大小。 事实证明，分类器在识别图片中的标尺而不是癌性痣方面几乎 100% 准确。

图像分类器以非常低的分辨率运行。 例如，Custom Vision 可以采用高达 10240x10240 的训练和预测图像，但可以在 227x227 的图像上训练和运行模型。 较大的图像会缩小到此大小，因此请确保您要分类的内容占据图像的很大一部分，否则在分类器使用的较小图像中它可能太小。

1. 收集分类器的图片。 每个标签至少需要 5 张图片来训练分类器，但越多越好。 您还需要一些额外的图像来测试分类器。 这些图像应该都是同一事物的不同图像。 例如：

     * 使用 2 个成熟的香蕉，从几个不同的角度为每一个拍摄一些照片，至少拍摄 7 张照片（5 张用于训练，2 张用于测试），但最好更多。

         ![2 个不同香蕉的照片](../../../../images/banana-training-images.png)

     * 使用 2 根未成熟的香蕉重复相同的过程

     您应该有至少 10 个训练图像，其中至少 5 个成熟图像和 5 个未成熟图像，以及 4 个测试图像，其中 2 个成熟图像，2 个未成熟图像。 您的图像应该是 png 或 jpeg，小于 6MB。 例如，如果您使用 iPhone 创建它们，它们可能是高分辨率 HEIC 图像，因此需要转换并可能缩小。 图像越多越好，并且成熟和未成熟的图像数量应该相似。

     如果你没有成熟和未成熟的水果，你可以使用不同的水果，或你现有的任何两种物体。 您还可以在 [images](./images) 文件夹中找到一些可以使用的成熟和未成熟香蕉的示例图像。

1. 按照 Microsoft 文档上构建分类器快速入门的[上传和标记图像部分](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier?WT.mc_id=academic-17441-jabenn#upload-and-tag-images) 上传您的训练图像。 将成熟的果实标记为`成熟`，将未成熟的果实标记为`未成熟`。

     ![显示上传成熟和未成熟香蕉图片的上传对话框](../../../../images/image-upload-bananas.png)

1. 按照 [Microsoft 文档上构建分类器快速入门的训练分类器部分](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier?WT.mc_id=academic-17441-jabenn#train-the-classifier) 在您上传的图像上训练图像分类器。

     您将可以选择培训类型。 选择**快速训练**。

然后分类器将进行训练。 培训需要几分钟才能完成。

> 🍌 如果您决定在分类器训练时吃水果，请确保您有足够的图像来首先进行测试！

## 测试你的图像分类器

分类器训练完成后，您可以通过给它一个新图像进行分类来测试它。

### 任务 - 测试你的图像分类器

1. 按照[在 Microsoft 文档上测试您的模型文档](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/test-your-model?WT.mc_id=academic-17441-jabenn#test-your-model) 来测试您的图像分类器。 使用您之前创建的测试图像，而不是用于训练的任何图像。

     ![未成熟的香蕉被预测为未成熟的概率为 98.9%，成熟的概率为 1.1%](../../../../images/banana-unripe-quick-test-prediction.png)

1. 尝试您可以访问的所有测试图像并观察概率。

## 重新训练你的图像分类器

当您测试分类器时，它可能不会给出您期望的结果。 图像分类器使用机器学习根据图像的特定特征与特定标签匹配的概率来预测图像中的内容。 它不理解图像中的内容 - 它不知道香蕉是什么，也不理解是什么使香蕉成为香蕉而不是船。 您可以通过使用错误的图像重新训练分类器来改进分类器。

每次使用快速测试选项进行预测时，都会存储图像和结果。 您可以使用这些图像来重新训练您的模型。

### 任务 - 重新训练你的图像分类器

1. 按照 [使用 Microsoft 文档上的预测图像作为培训文档](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/test-your-model?WT.mc_id=academic-17441-jabenn#use-the-predicted-image-for-training) 重新训练模型，为每个图像使用正确的标签。

1. 模型重新训练后，在新图像上进行测试。

---

## 🚀 挑战

如果你使用一张草莓的照片和一个接受过香蕉训练的模型，或者一张充气香蕉的照片，或者一个穿着香蕉套装的人的照片，甚至是一个像《辛普森一家》中的黄色卡通人物那样的黄色卡通人物，你认为会发生什么？

尝试一下，看看预测是什么。 您可以使用 [Bing 图像搜索](https://www.bing.com/images/trending) 查找要尝试使用的图像。

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/30)

## 复习与自学

* 当您训练分类器时，您会看到 *Precision*、*Recall* 和 *AP* 的值，这些值对所创建的模型进行评级。 阅读这些值的用途 [Microsoft 文档上构建分类器快速入门的评估分类器部分](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier?WT.mc_id=academic-17441-jabenn#evaluate-the-classifier)
* 从 [Microsoft 文档中如何改进自定义视觉模型](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/getting-started-improving-your-classifier?WT.mc_id=academic-17441-jabenn)  中了解如何改进分类器 -改进你的分类器？

## 任务

[训练多种水果和蔬菜的分类器](../assignment.md)