# Tensorflow2.0rc1
Building Tensorflow 2.0 RC 1 from source

## Purpose of Building from source
When a version of tensorflow is released, you can easily do a **pip3 install tensorflow-gpu==2.0.0rc1** to install the latest software. However, there is no source codes required, it's just a module install.  When Source codes of tensorflow is required, for example, the need to access TFliteconverter etc or when you need to have a better understanding of tensorflow codes, you might need to build from source.  However, it is very timeconsuming.  And after many hours, it might fail on some conditions. I am building this, because a foot note from tensorflow says if you want to delve into Converter Python converter, you need to [build from source](https://www.tensorflow.org/lite/convert/python_api#build_from_source_code_).

Last week, Tensorflow released 2.0 RC1.  Here's my environment

![NVIDIA version](nvidia-smi.png)
![OS](system.png)

## Building steps

### 1. Download BAZEL version 0.25 for build.  

```
cd ~/Downloads
wget https://github.com/bazelbuild/bazel/tags download bazel-0.25.2-installer-linux-x86_64.sh
./bazel-0.25.2-installer-linux-x86_64.sh --user

WARNING: --batch mode is deprecated. Please instead explicitly shut down your Bazel server using the command "bazel shutdown".
Build label: 0.25.2
Build target: bazel-out/k8-opt/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer_deploy.jar
Build time: Fri May 10 20:47:48 2019 (1557521268)
Build timestamp: 1557521268
Build timestamp as int: 1557521268

```

Notes:  
1.  I normally go to ~/Downloads and do this wget. Then, when I am done with the file, I can remove them
2.  The latest version of BAZEL might not work.  The latest **doesn't** mean the greatest.  
3.  Specifically for 2.0rc1, I tested with **0.25.2** 

### 2. Install all pre-requisites

```
sudo apt-get install python-numpy [**not sure if I needed to do this or is pip3 install numpy good enough**]
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
```

Notes:
1.  numpy caused me some problems with .local version, pip3 install numpy version and this sudo apt-get install python-numpy
2.  In the end, my pip3 has numpy version **1.17.2** 
3.  Most of these packages have an init.py, which needed to be in PYTHONPATH.  So, place the right numpy path for python in the earlier sequence for the PYTHONPATH variable which I set in ~/.bashrc
4.  Another trick I do is this, get into python command line, do an **import numpy**, then check **numpy.__file__** which will display the path of the numpy used.  If import numpy hits a problem, don't proceed to bazel build as it will surely abend after step 11,000+

### 3. Download tf2 source codes

There are 2 methods of doing this. But do checkout the [latest release](https://github.com/tensorflow/tensorflow/releases) Then, go to the bottom of the [link](https://github.com/tensorflow/tensorflow/releases/tag/v2.0.0-rc1) and you can see the link to either the 



https://github.com/tensorflow/tensorflow/archive/v2.0.0-rc1.tar.gz


```
