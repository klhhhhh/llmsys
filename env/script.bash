##docker
docker pull nvidia/cuda:11.0.3-cudnn8-devel-centos7
docker run -it -v /home/lk432963/code/:/code --name=centos7-CUDA --gpus all nvidia/cuda:11.0.3-cudnn8-devel-centos7 /bin/bash
docker exec -it centos7-CUDA /bin/bash

##conda
wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
bash Anaconda3-2020.02-Linux-x86_64.sh
export PATH="/root/anaconda3/bin:$PATH"
