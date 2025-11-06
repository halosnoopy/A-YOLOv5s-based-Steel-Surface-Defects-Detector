
import subprocess

subprocess.run(['python', 'xml2txt.py'])


print('Data Spliting Start!')
seed = 42
ratio = 0.9
subprocess.run(['python', 'train_val_split.py', '--random_seed=' + str(seed), '--train_ratio=' + str(ratio)])

print('Data for YOLO Gnerated!')





