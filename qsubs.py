import os
from argparse import ArgumentParser
arg = ArgumentParser(description='Batch submit job scripts - BLOSCAU')

arg.add_argument('-p','--path',default='',help='PBS Folder Location')

args = arg.parse_args()
path = args.path

for filename in os.listdir(os.path.join(os.getcwd(),path)):
    if not filename.endswith('.pbs'):
        continue
    # print(filename)
    os.system(f'dos2unix {filename} 1>&- 2>/dev/null')
    os.system(f'qsub {os.path.join(os.getcwd(),path,filename)}')