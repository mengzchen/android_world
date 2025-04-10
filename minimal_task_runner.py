# Copyright 2024 The android_world Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# 你不能在未遵守许可证的情况下使用此文件。
# 你可以在以下地址获取许可证：
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# 除非适用法律要求或书面同意，否则根据许可证分发的软件是“按原样”分发的，
# 不附带任何明示或暗示的保证或条件。
# 有关许可证下的权限和限制的更多详细信息，请参阅许可证。

"""运行单个任务。

minimal_run.py 模块用于运行单个任务，是 run.py 模块的简化版本。
可以指定一个任务，否则会随机选择一个任务。
"""

from collections.abc import Sequence
import os
import random
from typing import Type

from absl import app
from absl import flags
from absl import logging
from android_world import registry
from android_world.agents import infer
from android_world.agents import t3a
from android_world.env import env_launcher
from android_world.task_evals import task_eval

# 设置日志级别为警告
logging.set_verbosity(logging.WARNING)

# 设置 gRPC 环境变量以减少日志输出
os.environ['GRPC_VERBOSITY'] = 'ERROR'  # 仅显示错误
os.environ['GRPC_TRACE'] = 'none'  # 禁用跟踪

# 定义一个函数查找 adb 工具的路径
def _find_adb_directory() -> str:
  """返回 adb 所在的目录。"""
  potential_paths = [
      os.path.expanduser('~/Library/Android/sdk/platform-tools/adb'),
      os.path.expanduser('~/Android/Sdk/platform-tools/adb'),
      os.path.expanduser('~/AppData/Local/Android/Sdk/platform-tools/adb'),
      # os.path.expanduser(r'C:\Users\v-mengzchen\AppData\Local\Android\Sdk\platform-tools\adb.exe'),
      os.path.expanduser('C:/Users/v-mengzchen/AppData/Local/Android/Sdk/platform-tools/adb.exe')
  ]
  for path in potential_paths:
    if os.path.isfile(path):
      return path
  raise EnvironmentError(
      '未在常见的 Android SDK 路径中找到 adb。请安装 Android SDK 并确保 adb 位于预期目录之一。'
      '如果已安装，请指向已安装的位置。'
  )

# 定义命令行标志，用于指定 adb 路径
_ADB_PATH = flags.DEFINE_string(
    'adb_path',
    _find_adb_directory(),
    'adb 的路径。如果未通过 SDK 安装，请设置此路径。',
)

# 定义命令行标志，用于是否执行模拟器设置
_EMULATOR_SETUP = flags.DEFINE_boolean(
    'perform_emulator_setup',
    False,
    '是否执行模拟器设置。此操作必须在运行 Android World 之前执行一次且仅执行一次。'
    '设置完成后，此标志应始终为 False。',
)

# 定义命令行标志，用于指定设备控制台端口
_DEVICE_CONSOLE_PORT = flags.DEFINE_integer(
    'console_port',
    5554,
    '运行中的 Android 设备的控制台端口。通常可以通过 `adb devices` 的输出获取。'
    '一般来说，第一个连接的设备端口为 5554，第二个为 5556，以此类推。',
)

# 定义命令行标志，用于指定要运行的任务
_TASK = flags.DEFINE_string(
    'task',
    None,
    '要运行的特定任务。',
)

# 主函数，运行单个任务
def _main() -> None:
  """运行单个任务。"""
  # 加载并设置环境
  # print env info
  print(f"console_port: {_DEVICE_CONSOLE_PORT.value}")
  print(f"emulator_setup: {_EMULATOR_SETUP.value}")
  print(f"adb_path: {_ADB_PATH.value}")

  env = env_launcher.load_and_setup_env(
      console_port=_DEVICE_CONSOLE_PORT.value,
      emulator_setup=_EMULATOR_SETUP.value,
      adb_path=_ADB_PATH.value,
  )

  env.reset(go_home=True)  # 重置环境并返回主屏幕
  task_registry = registry.TaskRegistry()  # 获取任务注册表
  aw_registry = task_registry.get_registry(task_registry.ANDROID_WORLD_FAMILY)  # 获取 Android World 任务注册表

  # 如果指定了任务，则检查任务是否存在
  if _TASK.value:
    if _TASK.value not in aw_registry:
      raise ValueError('任务 {} 未在注册表中找到。'.format(_TASK.value))
    task_type: Type[task_eval.TaskEval] = aw_registry[_TASK.value]
  else:
    # 如果未指定任务，则随机选择一个任务
    task_type: Type[task_eval.TaskEval] = random.choice(
        list(aw_registry.values())
    )
  
  # 生成任务参数并初始化任务
  params = task_type.generate_random_params()
  task = task_type(params)
  task.initialize_task(env)

  # 创建智能体（Agent）
  # agent = t3a.T3A(env, infer.Gpt4Wrapper('gpt-4-turbo-2024-04-09'))
  agent = t3a.T3A(env, infer.Gpt4Wrapper('gpt-4-turbo-20240409'))  # 使用 GPT-4 模型

  print('目标: ' + str(task.goal))  # 打印任务目标
  is_done = False
  # 根据任务复杂度执行智能体的步骤
  for _ in range(int(task.complexity * 10)):
    response = agent.step(task.goal)
    if response.done:
      is_done = True
      break

  # 检查任务是否成功
  agent_successful = is_done and task.is_successful(env) == 1
  print(
      f'{"任务成功 ✅" if agent_successful else "任务失败 ❌"};'
      f' {task.goal}'
  )
  env.close()  # 关闭环境

# 主入口函数
def main(argv: Sequence[str]) -> None:
  del argv  # 删除未使用的参数
  _main()

# 如果作为脚本运行，则调用主函数
if __name__ == '__main__':
  app.run(main)
