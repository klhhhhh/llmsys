##docker
docker pull nvidia/cuda:12.3.2-devel-centos7
docker run -it -v /home/lk432963/code/llmsys:/llmsys --name=centos7-CUDA --gpus all nvidia/cuda:12.3.2-devel-centos7 /bin/bash
docker exec -it centos7-CUDA /bin/bash

##conda
wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh