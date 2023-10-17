

# 使用 JupyterLab 和 Docker 增强 AI/ML 开发



[JupyterLab](https://github.com/jupyterlab/jupyterlab)是一个围绕计算笔记本文档概念构建的开源应用程序。它支持共享和执行代码、数据处理、可视化，并提供一系列用于创建图形的交互功能。 

最新版本[JupyterLab 4.0](https://jupyterlab.readthedocs.io/en/stable/getting_started/changelog.html)已于 6 月初发布。与之前的版本相比，该版本具有更快的 Web UI、改进的编辑器性能、新的[扩展管理](https://jupyterlab.readthedocs.io/en/latest/user/extensions.html)器和实时协作。

如果您已经安装了独立的 3.x 版本，评估新功能将需要重写您当前的环境，这可能是劳动密集型且有风险的。但是，在 Docker 运行的环境中，例如[Docker Desktop](https://www.docker.com/products/docker-desktop/)，您可以在容器中启动隔离的 JupyterLab 4.0，而不会影响已安装的 JupyterLab 环境。当然，您可以在不影响现有环境的情况下运行它们并在不同的端口上访问它们。 

在本文中，我们将展示如何在 Docker Desktop 上使用[Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/)快速评估 JupyterLab 4.0 的新功能，而不影响主机 PC 端。

 ![Docker 和 jupyter 徽标显示在浅蓝色背景上，并带有相交的深蓝色线条](https://www.docker.com/wp-content/uploads/2023/07/banner_supercharging-ai-ml-development-with-jupyterlab-and-docker-1110x583.png)

## 为什么要对 JupyterLab 进行容器化？

-   容器化可确保您的 JupyterLab 环境在不同部署中保持一致。
    -   无论您是在本地计算机、开发环境还是生产集群中运行 JupyterLab，使用相同的容器映像都可以保证一致的设置。此方法有助于消除兼容性问题，并确保您的笔记本电脑在不同环境中的行为方式相同。

-   将 JupyterLab 打包在容器中使您可以轻松地与其他人共享您的笔记本环境，无论他们的操作系统或设置如何。
    -   这消除了手动安装依赖项和配置环境的需要，从而更容易协作和共享可重复的研究或工作流程。这在人工智能/机器学习项目中特别有用，因为在这些项目中，可重复性至关重要。

-   容器支持可扩展性，允许您根据工作负载要求扩展 JupyterLab 环境。
    -   您可以轻松启动多个运行 JupyterLab 实例的容器、分配工作负载，并利用 Kubernetes 等容器编排平台进行高效的资源管理。这在 AI/ML 开发中变得越来越重要，因为资源密集型任务很常见。


## 入门

要在计算机上使用 JupyterLab，一种选择是使用 JupyterLab 桌面应用程序。它基于 Electron，因此可以在 Windows、macOS 和 Linux 上使用 GUI 运行。事实上，使用 JupyterLab Desktop 使安装过程相当简单。然而，在 Windows 环境中，您还需要单独设置 Python 语言，并且为了扩展功能，您需要使用 pip 来设置包。

尽管这样的桌面解决方案可能比从头开始构建更简单，但我们认为 Docker Desktop 和 Docker Stacks 的组合仍然是更直接的选择。使用 JupyterLab Desktop，您无法混合多个版本或在评估后轻松删除它们。最重要的是，它无法在 Windows、macOS 和 Linux 上提供一致的用户体验。

在 Windows 命令提示符下，执行以下命令来启动基本笔记本： 

```
docker container run -it --rm -p 10000:8888 jupyter/base-notebook
```

该命令利用`jupyter/base-notebook`Docker 镜像，将主机的端口映射`10000`到容器的端口`8888`，并启用命令输入和伪终端。此外，还添加了一个选项，用于在该过程完成后删除容器。

等待 Docker 镜像下载后，命令提示符上将显示访问权限和令牌信息，如下所示。`http://127.0.0.1:8888`在这里，重写URL `http://127.0.0.1:10000`，然后将令牌附加到该 URL 的末尾。在此示例中，输出将如下所示：

-   屏幕上显示：[http://127.0.0.1:8888/ lab?token=6e302b2c99d56f1562e082091f4a3236051fb0a4135e10bb](http://127.0.0.1:8888/lab?token=6e302b2c99d56f1562e082091f4a3236051fb0a4135e10bb)
-   在浏览器中输入地址：[http://127.0.0.1:10000 /lab?token=6e302b2c99d56f1562e082091f4a3236051fb0a4135e10bb](http://127.0.0.1:10000/lab?token=6e302b2c99d56f1562e082091f4a3236051fb0a4135e10bb)

请注意，此令牌特定于我的环境，因此复制它对您不起作用。您应该将其替换为命令提示符上实际显示的内容。

然后，稍等片刻后，JupyterLab 将启动（图 1）。从这里，您可以启动 Notebook、访问 Python 的控制台环境或利用其他工作环境。

 ![jupyterlab 页面的屏幕截图，显示文件列表、笔记本、Python 控制台和其他启动选项。](https://www.docker.com/wp-content/uploads/2023/07/F1-.JupyterLab-token-1110x812.png)

**图 1.**输入 JupyterLab 令牌后的页面。左侧是文件列表，右侧可以打开Notebook创建、Python控制台等。

主机端的10000端口映射到容器内部的8888端口，如图2所示。

 ![显示主机端口 10000 映射到容器端口 8888 的屏幕截图。](https://www.docker.com/wp-content/uploads/2023/07/F2-host-mapping-1110x117.png)

**图 2.**主机端口 10000 映射到容器内的端口 8888。

在屏幕上的“**密码或令牌**`token=`输入”表单中，输入命令行或容器日志中显示的令牌（后面的字符串），然后选择**“登录”**，如图3所示。

 ![显示令牌身份验证设置的屏幕截图。](https://www.docker.com/wp-content/uploads/2023/07/F3-Jupyter-authentication-1110x724.png)

图 3. 输入容器日志中显示的令牌。

顺便说一句，在这种环境下，当容器停止时数据将被删除。如果您想在停止容器后重用数据，请`-v`在启动 Docker 容器时添加该选项来创建卷。

要停止此容器环境，请单击`CTRL-C`命令提示符，然后响应 Jupyter 服务器的提示`Shutdown this Jupyter server (y/[n])?`并按`y`Enter 键。如果您使用的是 Docker Desktop，请从容器中停止目标容器。

```
Shutdown this Jupyter server (y/[n])? y
[C 2023-06-26 01:39:52.997 ServerApp] Shutdown confirmed
[I 2023-06-26 01:39:52.998 ServerApp] Shutting down 5 extensions
[I 2023-06-26 01:39:52.998 ServerApp] Shutting down 1 kernel
[I 2023-06-26 01:39:52.998 ServerApp] Kernel shutdown: 653f7c27-03ff-4604-a06c-2cb4630c098d
```

一旦显示发生如下变化，容器就会被终止，数据也会被删除。

容器运行时，数据保存在`/home/jovyan/work/`容器内的目录中。您可以将其绑定安装为卷，也可以在启动容器时将其分配为卷。通过这样做，即使停止容器，重新启动容器时也可以再次使用相同的数据：

```
docker container run -it -p 10000:8888  -v "%cd%":/home/jovyan/work  jupyter/base-notebook
```

**注意：**该`\`符号表示命令行在命令提示符下继续。您也可以将命令写在一行中而不使用符号`\`。但是，在 Windows 命令提示符的情况下，您需要使用该`^`符号。

通过此设置，启动时，JupyterLab 容器会将目录安装到执行命令的`/work/`文件夹。`docker container run`由于即使容器停止，数据仍然存在，因此当您再次启动容器时，您可以继续使用 Notebook 数据。

`!pip`请注意，每次都使用命令添加模块可能会很麻烦。幸运的是，您可以通过以下方式添加模块：

-   通过创建专用的 Dockerfile
-   通过使用名为 Jupyter Docker Stacks 的现有映像组

## 方法一、从base-notebook构建 Docker 镜像

如果您熟悉 Dockerfile 和构建映像，那么这个五步方法很简单。此外，这种方法可以帮助控制 Docker 镜像的大小。 

### 步骤1. 创建目录

要构建 Docker 映像，第一步是创建并导航到放置 Dockerfile 和上下文的目录：

```
mkdir myjupyter && cd myjupyter
```

### 步骤2. 创建requirements.txt文件

创建一个`requirements.txt`文件并列出要使用以下`pip`命令添加的 Python 模块：

### 步骤3. 编写 Dockerfile

```
FROM jupyter/base-notebook
WORKDIR /home/jovyan/work
COPY ./requirements.txt /home/jovyan/work
RUN python -m pip install --no-cache -r requirements.txt
```

该 Dockerfile 指定一个基础镜像，将文件从本地目录`jupyter/base-notebook`复制到容器内部，然后运行命令来安装文件中列出的 Python 包。`requirements.txt``/home/jovyan/work directory``pip install``requirements.txt`

### 步骤 4. 构建 Docker 镜像

```
docker image build -t myjupyter
```

### 步骤 5. 启动容器

```
docker container run -it -p 10000:8888 -v "%cd%":/home/jovyan/work myjupyter
```

以下是该命令各部分的作用：

-   该`docker run`命令指示 Docker 运行容器。
-   该`-it`  选项将交互式终端附加到容器。
-   将`-p 10000:8888`主机上的端口 10000 映射到容器内的端口 8888。`http://localhost:10000`这允许您通过Web 浏览器访问在容器中运行的 Jupyter Notebook 。
-   将主机上的`-v "%cd%":/home/jovyan/work`当前目录挂载到容器内的目录。这使得主机和 Jupyter Notebook 之间可以共享文件。`%cd%``/home/jovyan/work`

## 方法二、如何使用 Jupyter Docker Stacks 的镜像

[`jupyter/scipy-notebook`](https://hub.docker.com/r/jupyter/scipy-notebook)为了执行 JupyterLab 环境，我们将利用从[Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/)调用的 Docker 映像。请注意，正在运行的笔记本将被终止。`Ctrl-C`在命令提示符下输入后，输入`y`并指定正在运行的容器。

然后，输入以下命令来运行新容器：

```
docker container run -it -p 10000:8888  -v “%cd%”:/home/jovyan/work jupyter/scipy-notebook
```

此命令将使用该映像运行一个容器`jupyter/scipy-notebook`，该容器提供带有附加科学库的 Jupyter Notebook 环境。 

以下是该命令的详细说明：

-   该`docker run`命令启动一个新容器。
-   该`-it`选项将交互式终端附加到容器。
-   将`-p 10000:8888`主机上的端口 10000 映射到容器内的端口 8888，从而允许通过[http://localhost:10000](http://localhost:10000/)访问 Jupyter Notebook 。
-   将主机上的`-v "$(pwd)":/home/jovyan/work`当前目录 载到容器内的目录。这使得主机和 Jupyter Notebook 之间可以共享文件。`$(pwd)``/home/jovyan/work`
-   这`jupyter/scipy-notebook`是用于容器的 Docker 映像的名称。确保您的系统上有此映像。

## 结论

通过使用 Docker 将 JupyterLab 容器化，AI/ML 开发人员获得了众多优势，包括一致性、轻松共享和协作以及可扩展性。它可以有效管理 AI/ML 开发工作流程，从而更轻松地在不同环境中进行实验、协作和重现结果。借助 JupyterLab 4.0 和 Docker，增强 AI/ML 开发的可能性是无限的。那为什么还要等呢？拥抱容器化并在您的 AI/ML 项目中体验 JupyterLab 的真正力量。
