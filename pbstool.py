import os
from argparse import ArgumentParser
'''
用于快速将多条命令分配到多个pbs脚本中，提升任务完成效率
wangzt
2022.12.23
'''
welcome = '''  ____  ____ ____    _____           _           ____  _     ___  ____   ____    _   _   _ 
 |  _ \| __ ) ___|  |_   _|__   ___ | |         | __ )| |   / _ \/ ___| / ___|  / \ | | | |
 | |_) |  _ \___ \    | |/ _ \ / _ \| |  _____  |  _ \| |  | | | \___ \| |     / _ \| | | |
 |  __/| |_) |__) |   | | (_) | (_) | | |_____| | |_) | |__| |_| |___) | |___ / ___ \ |_| |
 |_|   |____/____/    |_|\___/ \___/|_|         |____/|_____\___/|____/ \____/_/   \_\___/ 
                            
                            PBS Script Tool - BLOSCAU                         
                PBS任务作业脚本批量生成工具 - 华南农业大学生物信息学实验室      
-------------------------------------------------------------------------------------------------------'''
print(welcome)

arg = ArgumentParser(description='PBS Script generator tools - BLOSCAU')

arg.add_argument("-c",
                 "--cmd",
                 required=True,
                 help="input cmd file path")

arg.add_argument("--name",
                 default='Job',
                 help="Job name")

arg.add_argument("--env",
                 default=False,
                 help="Conda environments name")

arg.add_argument("--queue",
                 default='cu',
                 help="Target computing cluster")

arg.add_argument("--node",
                 type=int,
                 default=1,
                 help="Number of calculation nodes")

arg.add_argument("--ppn",
                 type=int,
                 default=1,
                 help="Calculate the number of cores")

arg.add_argument("--walltime",
                 default=10000,
                 help="Maximum running time (hour)")

arg.add_argument("--output",
                 help="output file path")

args = arg.parse_args()

# 命令列表
cmd_list = args.cmd
# 任务名称
job_name = args.name
# Conda 环境 如没有conda则false
conda_env = args.env
# 目标集群
job_queue = args.queue
# 节点数目
job_nodes = args.node
# 节点使用核心数
job_ppn = args.ppn
# 最大等待时间（小时）
job_walltime_hour = args.walltime
# 生成pbs脚本目录
pbs_files_path = args.output
# 正常信息输出
job_info_log = 'pbs_info.log'
# 错误信息输出
job_error_log = 'pbs_error.log'


if pbs_files_path == None:
    pbs_files_path = job_name + '-pbsFiles'

# 导入命令列表
with open(cmd_list,'r',encoding='utf8') as file:
    cmd_list = file.read().splitlines()
if not os.path.exists(pbs_files_path):
    os.mkdir(pbs_files_path)

# conda 环境
if conda_env == False or conda_env == None or conda_env == '':
    conda_activate = ''
    conda_env = 'Undefined'
else:
    conda_activate = 'source activate ' + conda_env

num = 0
for cmd in cmd_list:
    if cmd == '':
        continue
    num += 1
    # print('正在创建：' + f'{pbs_files_path}/{job_name}_{num}.pbs')
    with open(f'{pbs_files_path}/{job_name}_{num}.pbs','w',encoding='utf8') as  file:
        pbs_txt = f'''#!/bin/sh
# Bioinformatics Laboratory of South China Agricultural University
#PBS -N {job_name}_{num}
#PBS -q {job_queue}
#PBS -l nodes={job_nodes}:ppn={job_ppn}
#PBS -l walltime={job_walltime_hour}:00:00
#PBS -o {job_name}_{num}_{job_info_log}
#PBS -e {job_name}_{num}_{job_error_log}
#PBS -V
#PBS -S /bin/bash
cat $PBS_NODEFILE > /tmp/nodefile.$$
echo "========================================-"
echo "[作业详情] "
echo '作业标识: '$PBS_JOBID - $PBS_JOBNAME
echo '作业队列: '$PBS_QUEUE
echo 'Conda 环境： {conda_env}' 
echo "作业命令: {cmd} "
echo '开始时间: ';date
echo "========================================-"
echo "[任务开始时间] "
date
echo "========================================-"
echo "[ 工作目录 ] "
cd $PBS_O_WORKDIR;pwd
echo "========================================-"
{conda_activate}
{cmd}
echo "========================================-"
echo "[任务结束时间] "
date
echo "========================================-"
rm -rf /tmp/nodefile.$$
rm -rf /tmp/nodes.$$
'''
        file.write(pbs_txt)
    file.close()
print(f'[Success] - Total {num} Jobs >> '+ os.path.join(os.getcwd(),pbs_files_path))
