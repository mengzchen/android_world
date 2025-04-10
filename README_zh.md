# AndroidWorld

[![单元测试](https://github.com/google-research/android_world/actions/workflows/pytest.yml/badge.svg)](https://github.com/google-research/android_world/actions/workflows/pytest.yml)

<p align="center">
<a href="https://google-research.github.io/android_world/">官网</a> •
<a href="https://arxiv.org/pdf/2405.14573">论文</a> •
<a href="https://google-research.github.io/android_world/task_list.html">任务列表</a> •
<a href="https://docs.google.com/spreadsheets/d/1cchzP9dlTZ3WXQTfYNhh3avxoLipqHN75v1Tb86uhHo/edit?gid=0#gid=0">排行榜</a>
</p>

![概览图](assets/overview.png)

**AndroidWorld** 是一个用于构建和评估自主计算机控制代理的环境。

它运行在实时Android模拟器上，包含20个应用中116个手工制作任务的高度可复现基准测试，这些任务通过随机生成的参数动态实例化，可创建数百万种独特任务变体。

除内置任务外，AndroidWorld还支持来自[Liu等人](http://arxiv.org/abs/1802.08802)的流行网页基准测试MiniWoB++。

AndroidWorld的核心特性包括：

* 📝 **116个多样化任务** 覆盖20个真实应用
* 🎲 **动态任务实例化** 生成数百万独特变体
* 🏆 **持久奖励信号** 确保可靠评估
* 🌐 **开放环境** 支持数百万Android应用和网站
* 💾 **轻量级占用** (2GB内存，8GB磁盘)
* 🔧 **可扩展设计** 轻松添加新任务和基准
* 🖥️ **MiniWoB++集成** 支持网页任务

演示视频请见[官网](https://google-research.github.io/android_world/)。

## 安装指南

1. 配置Android模拟器
   1. 下载[Android Studio](https://developer.android.com/studio?gad_source=1&gclid=Cj0KCQjw3ZayBhDRARIsAPWzx8oLcadBD0vAq8xmUutaunLGSzhgEtLz4xVZ_SpV4G0xJazS7LxQkDsaAuveEALw_wcB&gclsrc=aw.ds)
   2. 按说明创建Android虚拟设备(AVD)：硬件选择**Pixel 6**，系统镜像选择**Tiramisu, API Level 33**，AVD名称设为**AndroidWorldAvd**。[观看设置视频](https://github.com/google-research/android_world/assets/162379927/efc33980-8b36-44be-bb2b-a92d4c334a50)

1. 通过命令行启动模拟器

    必须使用`-grpc 8554`参数启动（用于无障碍服务通信），不要通过Android Studio界面启动：
    ```bash
    # 通常路径为 ~/Android/Sdk/emulator/emulator 或
    # ~/Library/Android/sdk/emulator/emulator
    EMULATOR_NAME=AndroidWorldAvd # 上一步设置的名称
    ~/Library/Android/sdk/emulator/emulator -avd $EMULATOR_NAME -no-snapshot -grpc 8554
    ```

1. [可选] 推荐使用`conda`，可从[此处](https://docs.anaconda.com/free/miniconda/miniconda-install/)下载：
    ```
    conda create -n android_world python=3.11.8
    # windows need 3.12
    conda create -n android_world python=3.12
    conda activate android_world
    ```

1. 安装最新版[AndroidEnv](https://github.com/google-deepmind/android_env)：
    ```python
    git clone https://github.com/google-deepmind/android_env.git
    cd android_env
    python setup.py install
    ```

    Windows系统不能直接用master branch，需要用这个PR的版本：
    ```bash
    git fetch origin pull/265/head:pr-265
    git checkout pr-265
    ```
    然后再安装 `python setup.py install`

1. 安装AndroidWorld（*注意：需要Python 3.11及以上版本*）：
    ```python
    git clone https://github.com/google-research/android_world.git
    cd ./android_world
    pip install -r requirements.txt
    python setup.py install
    ```

1. 设置模型供应商API环境变量：
    ```bash
    # 加入.bashrc
    export OPENAI_API_KEY=你的密钥
    export GCP_API_KEY=你的密钥
    ```

1. 安装`ffmpeg`（如未安装）：
    ```bash
    # Linux (Ubuntu/Debian)
    # sudo apt update && sudo apt install ffmpeg

    # macOS
    brew install ffmpeg

    # Windows
    choco install ffmpeg
    ```

### 已知问题

**Protobuf版本兼容性**

运行`android_world`时若出现如下错误：
```bash
ImportError: cannot import name 'runtime_version' from 'google.protobuf'
```
可通过安装特定版本解决：
```bash
pip install protobuf==5.29.0
```
这是AndroidEnv与其他包依赖冲突的临时解决方案。完整版本要求参见[`.github/pytest.yml`](https://github.com/google-research/android_world/tree/main/.github/workflows)。

## 快速开始

运行`minimal_task_runner.py`脚本了解基础运行机制。该脚本会初始化环境、设置任务并运行默认代理M3A：
```bash
python minimal_task_runner.py --task=ContactsAddContact
```
不指定任务时将随机选择任务。*注意：如需测试开源应用（非Android系统自带），请在下述脚本中添加`--perform_emulator_setup`参数。*

## 运行基准测试

注意：**任务步数限制更新**  
截至2024年11月18日，各任务的max_steps/step_budget已调整为**人类平均完成时间的2倍**，确保代理有充足时间完成任务，同时减少基准测试开销。[具体调整](https://docs.google.com/spreadsheets/d/1KF-vY0Uy47o0mnursvs-HmS6hreU6U3rPrAjgEfjMK4/edit?usp=sharing)

```bash
python run.py \
  --suite_family=android_world \
  --agent_name=t3a_gpt4 \
  --perform_emulator_setup \
  --tasks=ContactsAddContact,ClockStopWatchRunning \  # 可选：指定子集任务
```

```bash
python run.py --suite_family=android_world --agent_name=t3a_gpt4 --perform_emulator_setup --tasks=ContactsAddContact,ClockStopWatchRunning
```

首次运行必须添加`--perform_emulator_setup`参数来安装必要应用和设置权限（一次性操作，耗时取决于网络速度）。

`n_task_combinations`参数指定每个任务使用的参数排列数量。例如短信任务会对应不同的电话号码/消息组合。

若运行中途失败，可通过`--checkpoint_dir`指向原输出目录来恢复运行。

## 运行MiniWoB++任务

在AndroidWorld中运行MiniWoB++网页任务只需设置：
```bash
--suite_family=miniwob --perform_emulator_setup
```
关键优势在于常见输入元素会渲染为Android原生控件（而非HTML），因此代理必须学会使用通用组件如时间/日期选择器：

<p align="center">
   <img src="assets/miniwob.png" style="width:30%">
</p>

## 创建自定义代理

除[现有代理](https://github.com/google-research/android_world/tree/main/android_world/agents)外，您可轻松创建自定义代理：

1. 继承[EnvironmentInteractingAgent](https://github.com/google-research/android_world/blob/6e4feb00702735c9a7485f4ae714528a058cb2b7/android_world/agents/base_agent.py#L39C1-L39C44)类并实现[step](https://github.com/google-research/android_world/blob/6e4feb00702735c9a7485f4ae714528a058cb2b7/android_world/agents/base_agent.py#L116)方法。典型流程包括：通过AndroidEnv获取屏幕截图/UI元素 → 选择[支持的操作](https://github.com/google-research/android_world/blob/main/android_world/env/json_action.py) → 返回[AgentInteractionResult](https://github.com/google-research/android_world/blob/6e4feb00702735c9a7485f4ae714528a058cb2b7/android_world/agents/base_agent.py#L26)（设置`done=True`表示任务完成）

2. 在[run.py](https://github.com/google-research/android_world/blob/main/run.py)中导入代理，并在[_get_agent](https://github.com/google-research/android_world/blob/15471441ac306ff08bca87454b1b546ae81db7af/run.py#L147)方法中添加代理名映射

3. 使用`--agent_name=你的代理名`运行基准测试

## 添加新任务

请参考[任务添加指南](https://github.com/google-research/android_world/blob/main/docs/tasks_guide.md)

## 引用

若使用本环境或数据，请引用论文：
```
@misc{rawles2024androidworlddynamicbenchmarkingenvironment,
      title={AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents},
      author={Christopher Rawles and Sarah Clinckemaillie and Yifan Chang and Jonathan Waltz and Gabrielle Lau and Marybeth Fair and Alice Li and William Bishop and Wei Li and Folawiyo Campbell-Ajala and Daniel Toyama and Robert Berry and Divya Tyamagundlu and Timothy Lillicrap and Oriana Riva},
      year={2024},
      eprint={2405.14573},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2405.14573},
}
```

*非Google官方支持产品*
