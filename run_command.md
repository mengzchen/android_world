

```bash
conda activate android_world

C:\Users\v-mengzchen\AppData\Local\Android\Sdk\emulator\emulator -avd AndroidWorldAvd -no-snapshot -grpc 8554
```

```bash
export OPENAI_API_KEY="xxx"
export OPENAI_BASE_URL="http://127.0.0.1:8000"
```

Powershell：
```shell
$env:OPENAI_API_KEY="xxx"
$env:OPENAI_BASE_URL="http://127.0.0.1:8000"
```

Quick Start:

运行`minimal_task_runner.py`脚本了解基础运行机制。该脚本会初始化环境、设置任务并运行默认代理M3A：

```bash
python minimal_task_runner.py --task=ContactsAddContact
```