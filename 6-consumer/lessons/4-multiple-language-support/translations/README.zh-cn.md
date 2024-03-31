
# 支持多种语言

![本课的 sketchnote 概述](../../../../sketchnotes/lesson-24.jpg)

> [Nitya Narasimhan](https://github.com/nitya) 的草图笔记。单击图像查看放大版本。

本视频概述了 Azure 语音服务，涵盖了早期课程中的语音转文本和文本转语音，以及翻译语音（本课程涵盖的主题）：

[![使用 Microsoft Build 2020 中的几行 Python 识别语音](https://img.youtube.com/vi/h6xbpMPSGEA/0.jpg)](https://www.youtube.com/watch?v =h6xbpMPSGEA)

> 🎥 点击上图观看视频

## 课前测验

[课前测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/47)

## 介绍

在过去 3 节课程中，您学习了有关将语音转换为文本、语言理解以及将文本转换为语音的知识，所有这些都由 AI 提供支持。人工智能可以帮助人类交流的另一个领域是语言翻译——从一种语言转换为另一种语言，例如从英语转换为法语。

在本课程中，您将学习如何使用人工智能翻译文本，使您的智能计时器能够与多种语言的用户交互。

在本课中，我们将介绍：

* [翻译文本](#translate-text)
* [翻译服务](#translation-services)
* [创建翻译资源](#create-a-translator-resource)
* [在带有翻译的应用程序中支持多种语言](#support-multiple-linguals-in-applications-with-translations)
* [使用 AI 服务翻译文本](#translate-text-using-an-ai-service)

> 🗑 这是本项目的最后一课，因此完成本课和作业后，不要忘记清理您的云服务。您将需要服务来完成任务，因此请务必先完成任务。
>
> 如有必要，请参阅[清理项目指南](../../../../clean-up.md)，了解如何执行此操作的说明。

## 翻译文本

文本翻译是一个计算机科学问题，已经研究了 70 多年，直到现在，由于人工智能和计算机能力的进步，文本翻译才接近得到解决，达到几乎与人类翻译一样好的程度。

> 💁 起源可以追溯到 [Al-Kindi](https://wikipedia.org/wiki/Al-Kindi)，一位 9 世纪的阿拉伯密码学家，他开发了语言翻译技术

### 机器翻译

文本翻译最初是一种称为机器翻译 (MT) 的技术，可以在不同语言对之间进行翻译。机器翻译的工作原理是用一种语言中的单词替换另一种语言中的单词，并在简单的逐字翻译没有意义时添加技术来选择翻译短语或句子部分的正确方式。

> 🎓 当翻译器支持一种语言和另一种语言之间的翻译时，这些被称为*语言对*。不同的工具支持不同的语言对，并且这些可能并不完整。例如，翻译器可能支持英语到西班牙语作为语言对，以及西班牙语到意大利语作为语言对，但不支持英语到意大利语。

例如，将`Hello world`从英语翻译成法语可以通过替换`Bonjour`代替`Hello`，`le monde`代替`world`，从而得到`Bonjour le monde`的正确翻译。

当不同的语言使用不同的方式表达同一事物时，替换就不起作用。例如，英语句子`我的名字是吉姆`在法语中翻译为`Je m'appelle Jim` - 字面意思是`我称自己为吉姆`。 `Je`是法语`I`的意思，`moi`是我，但与动词连接在一起，因为它以元音开头，所以变成`m'`，`appelle`是呼叫，而`Jim`不是翻译时它是一个名字，而不是一个可以翻译的单词。词序也成为一个问题 - 将`Je m'appelle Jim`简单替换为`我自己叫 Jim`，其词序与英语不同。

> 💁 有些单词永远不会被翻译 - 无论使用哪种语言来介绍我，我的名字是吉姆。当翻译成使用不同字母表的语言，或者使用不同字母表示不同发音时，单词可以被`音译`，即选择给出适当发音的字母或字符，使其听起来与给定单词相同。

习语也是翻译的一个问题。这些短语具有不同于直接解释单词的含义。例如，在英语中，`I’ve got ants in my panties`这个习语的字面意思并不是指衣服里有蚂蚁，而是指焦躁不安。如果你把它翻译成德语，你最终会让听众感到困惑，因为德语版本是`我的底部有大黄蜂`。

> 💁 不同的地区会增加不同的复杂性。用成语`ants in your panties`来说，美式英语中`pants`指的是外衣，英式英语中`pants`指的是内衣。

✅ 如果您会说多种语言，请考虑一些不能直接翻译的短语

机器翻译系统依赖于描述如何翻译某些短语和习语的大型规则数据库，以及从可能的选项中选择适当翻译的统计方法。这些统计方法使用人类翻译成多种语言的庞大作品数据库来选择最可能的翻译，这种技术称为`统计机器翻译`。其中许多使用语言的中间表示，允许将一种语言翻译为中间语言，然后从中间语言翻译为另一种语言。通过这种方式添加更多语言涉及到中间语言的翻译，而不是所有其他语言的翻译。

### 神经翻译

神经翻译涉及利用人工智能的力量进行翻译，通常使用一种模型翻译整个句子。这些模型接受人工翻译的庞大数据集的训练，例如网页、书籍和联合国文件。

由于不需要庞大的短语和习语数据库，神经翻译模型通常比机器翻译模型小。提供翻译的现代人工智能服务通常混合多种技术，混合统计机器翻译和神经翻译

任何语言对都不存在 1:1 的翻译。根据用于训练模型的数据，不同的翻译模型会产生略有不同的结果。翻译并不总是对称的 - 如果您将一个句子从一种语言翻译成另一种语言，然后再翻译回第一种语言，您可能会看到结果略有不同的句子。

✅ 尝试不同的在线翻译器，例如 [Bing Translate](https://www.bing.com/translator)、[Google Translate](https://translate.google.com) 或 Apple 翻译应用程序。比较几个句子的翻译版本。也可以尝试翻译一种语言，然后再翻译回另一种语言。

## 翻译服务

您的应用程序可以使用许多人工智能服务来翻译语音和文本。

### 认知服务 语音服务

![语音服务徽标](../../../../images/azure-speech-logo.png)

您在过去几节课中使用的语音服务具有语音识别翻译功能。当您识别语音时，您不仅可以请求同一语言的语音文本，还可以请求其他语言的语音文本。

> 💁 这只能通过语音 SDK 获得，REST API 没有内置翻译。

### 认知服务 翻译服务

![翻译服务徽标](../../../../images/azure-translator-logo.png)

翻译服务是一项专用翻译服务，可以将文本从一种语言翻译为一种或多种目标语言。除了翻译之外，它还支持多种额外功能，包括屏蔽脏话。它还允许您为特定单词或句子提供特定翻译，处理您不想翻译的术语，或者拥有特定的众所周知的翻译。

例如，当将句子`I have a Raspberry Pi`（指的是单板计算机）翻译成另一种语言（例如法语）时，您可能希望保留名称`Raspberry Pi`，而不是翻译它，给出`J'ai un Raspberry Pi`而不是`J'ai une pi aux framboises`。

## 创建翻译资源

对于本课程，您将需要翻译资源。您将使用 REST API 翻译文本。

### 任务 - 创建翻译资源

1. 从终端或命令提示符运行以下命令，在`smart-timer`资源组中创建翻译器资源。

    ```sh
    az cognitiveservices account create --name smart-timer-translator \
                                        --resource-group smart-timer \
                                        --kind TextTranslation \
                                        --sku F0 \
                                        --yes \
                                        --location <location>
    ```

    替换 `<location>` 为您在创建资源组时使用的位置。

1. 获取翻译服务密钥：

    ```sh
    az cognitiveservices account keys list --name smart-timer-translator \
                                           --resource-group smart-timer \
                                           --output table
    ```

    获取其中一把钥匙的副本。

## 在带有翻译的应用程序中支持多种语言

在理想的世界中，您的整个应用程序应该理解尽可能多的不同语言，从聆听语音到语言理解，再到用语音进行响应。这是一项繁重的工作，因此翻译服务可以加快您的申请的交付时间。

![将日语翻译成英语、用英语处理然后翻译回日语的智能定时器架构](../../../../images/translated-smart-timer.png)

想象一下，您正在构建一个端到端使用英语的智能计时器，理解英语口语并将其转换为文本，以英语运行语言理解，建立英语响应并用英语语音进行回复。如果您想添加对日语的支持，您可以从将日语口语翻译为英语文本开始，然后保持应用程序的核心相同，然后在说出响应之前将响应文本翻译为日语。这将允许您快速添加日语支持，并且您可以稍后扩展以提供完整的端到端日语支持。

> 💁 依赖机器翻译的缺点是，不同的语言和文化对相同事物有不同的表达方式，因此翻译可能与您期望的表达不匹配。

机器翻译还为应用程序和设备提供了可能性，这些应用程序和设备可以在创建用户创建的内容时对其进行翻译。科幻小说经常以`通用翻译器`为特色，这种设备可以将外星语言翻译成（通常是）美式英语。如果你忽略外星人的部分，这些设备不再是科幻小说，而是更多的科学事实。已经有应用程序和设备使用语音和翻译服务的组合来提供语音和书面文本的实时翻译。

一个示例是 [Microsoft Translator](https://www.microsoft.com/translator/apps/?WT.mc_id=academic-17441-jabenn) 手机应用程序，如本视频所示：

[![微软翻译实时功能正在运行](https://img.youtube.com/vi/16yAGeP2FuM/0.jpg)](https://www.youtube.com/watch?v=16yAGeP2FuM)

> 🎥 点击上图观看视频

想象一下，您可以使用这样的设备，尤其是在旅行或与您不懂语言的人互动时。在机场或医院配备自动翻译设备将提供急需的无障碍改进。

✅ 做一些研究：是否有商用翻译物联网设备？智能设备内置的翻译功能怎么样？

> 👽 虽然没有真正的通用翻译器可以让我们与外星人交谈，但[微软翻译器确实支持克林贡语](https://www.microsoft.com/translator/blog/2013/05/14/announcing-klingon-for-bing-translator/?WT.mc_id=academic-17441-jabenn)。卡普拉！

## 使用 AI 服务翻译文本

您可以使用人工智能服务将此翻译功能添加到您的智能计时器中。

### 任务 - 使用 AI 服务翻译文本

按照相关指南在 IoT 设备上转换翻译文本：

* [Arduino - Wio 终端](../wio-terminal-translate-speech.md)
* [单板机-Raspberry Pi](../pi-translate-speech.md)
* [单板机-虚拟设备](../virtual-device-translate-speech.md)

---

## 🚀 挑战

机器翻译如何使智能设备以外的其他物联网应用受益？想想翻译可以提供帮助的不同方式，不仅是口语，还有文本。

## 课后测验

[课后测验](https://black-meadow-040d15503.1.azurestaticapps.net/quiz/48)

## 复习与自学

* 在[维基百科上的机器翻译页面](https://wikipedia.org/wiki/Machine_translation) 上了解有关机器翻译的更多信息
* 在 [维基百科上的神经机器翻译页面](https://wikipedia.org/wiki/Neural_machine_translation) 上了解有关神经机器翻译的更多信息
* 查看 [Microsoft Docs 上语音服务文档的语言和语音支持](https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support?WT.mc_id=academic-17441-jabenn) 

## 任务

[构建通用翻译器](../assignment.md)

    
   