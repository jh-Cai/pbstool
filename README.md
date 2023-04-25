PBS-Tools 
----
适用于 PBS/Torque 作业调度系统 作业脚本批量生成与提交工具。


## 使用方法

### PBS_tool 批量作业脚本生成

```shell
# 帮助信息
python pbstool.py -h

# 快速开始
python pbstool.py -c cmd.txt --name test --queue cu --ppn 1

-c      # 命令脚本
--name  # 作业名称
--env   # 调用Conda环境
--queue # 目标计算队列
--node  # 所需节点数量，默认1
--ppn   # 所需每节点计算核心数目，默认1
```

### qsubs  批量作业提交

```shell
# 默认提交当前目录下全部作业脚本
python qsubs.py

# 指定作业脚本所在目录进行批量提交
python qsubs.py -p /home/test/pbsfiles

```


## 其他

建议使用 pyinstaller 程序将此脚本进行编译后放置在系统环境变量的目录中，方便批量生成命令脚本后直接调用

----
Author：wangzt (interestingcn01@gmail.com)
华南农业大学生物信息学实验室