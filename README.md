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

There are 2 methods of doing this. But do checkout the [latest release](https://github.com/tensorflow/tensorflow/releases) Then, go to the bottom of the [link](https://github.com/tensorflow/tensorflow/releases/tag/v2.0.0-rc1) and you can see the link to either source codes ( zip or tar.gz ) version.  I prefer to download the tar.gz version but either is fine

![Assets](Assets.jpg)

```
cd ~/Downloads
wget https://github.com/tensorflow/tensorflow/archive/v2.0.0-rc1.tar.gz
tar -xvf v2*.gz
[move the tensorflow directory to ~/]
```
Alternatively, you can **git clone https://github.com/tensorflow/tensorflow.git ** and do a **git checkout xxxxx** But then again, you will need to know the version to checkout.


### 4.  Configure

```
cd ~/tensorflow
./configure
```

Notes:
1.  set up python bin as **/usr/bin/python3**
2.  set up python library as **/usr/lib/python3.7** This step is very very important to get right. Otherwise, after the last step, import tensorflow as tf will just be silent.
3.  select **CUDA** - Then we will get a GPU built tensorflow


### 5.  Start the BUILD
```
bazel build --verbose_failures --config=cuda //tensorflow/tools/pip_package:build_pip_package &

INFO: Elapsed time: 28929.331s, Critical Path: 473.63s
INFO: 25004 processes: 25004 local.
INFO: Build completed successfully, 34536 total actions
```

Notes:
1.   The **&** generates a background job
2.   Wait for a long time till you see 34536 actions finnished.  It took around 5-6 hours 

### 6.   Convert into a WHL file  
```
./bazel-bin/tensorflow/tools/pip_package/build_pip_package tensorflow_pkg

Sat Sep 14 14:35:17 +08 2019 : === Preparing sources in dir: /tmp/tmp.vJA9nY1r7W
~/tensorflow ~/tensorflow
~/tensorflow
/tmp/tmp.vJA9nY1r7W/tensorflow/include ~/tensorflow
~/tensorflow
Sat Sep 14 14:35:32 +08 2019 : === Building wheel
warning: no files found matching '*.pyd' under directory '*'
warning: no files found matching '*.pd' under directory '*'
warning: no files found matching '*.dylib' under directory '*'
warning: no files found matching '*.dll' under directory '*'
warning: no files found matching '*.lib' under directory '*'
warning: no files found matching '*.csv' under directory '*'
warning: no files found matching '*.h' under directory 'tensorflow_core/include/tensorflow'
warning: no files found matching '*' under directory 'tensorflow_core/include/third_party'
Sat Sep 14 14:36:12 +08 2019 : === Output wheel file is in: /home/keng/tensorflow/tensorflow_pkg

```
Notes:
1.   This conversion is very fast, taking 2 minutes.

### 7.  pip3 install whl
```
pip3 install tensorflow_pkg/tensorflow*

Requirement already satisfied: tensorflow==2.0.0rc1 from file:///home/keng/tensorflow/tensorflow_pkg/tensorflow-2.0.0rc1-cp37-cp37m-linux_x86_64.whl in /home/keng/.local/lib/python3.7/site-packages (2.0.0rc1)
Requirement already satisfied: six>=1.10.0 in /usr/lib/python3/dist-packages (from tensorflow==2.0.0rc1) (1.12.0)
Requirement already satisfied: termcolor>=1.1.0 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (1.1.0)
Requirement already satisfied: grpcio>=1.8.6 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (1.22.0)
Collecting wrapt>=1.11.1 (from tensorflow==2.0.0rc1)
  Downloading https://files.pythonhosted.org/packages/23/84/323c2415280bc4fc880ac5050dddfb3c8062c2552b34c2e512eb4aa68f79/wrapt-1.11.2.tar.gz
Requirement already satisfied: keras-applications>=1.0.8 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (1.0.8)
Requirement already satisfied: gast==0.2.2 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (0.2.2)
Requirement already satisfied: tf-estimator-nightly<1.14.0.dev2019080602,>=1.14.0.dev2019080601 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (1.14.0.dev2019080601)
Requirement already satisfied: astor>=0.6.0 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (0.8.0)
Requirement already satisfied: absl-py>=0.7.0 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (0.7.1)
Requirement already satisfied: opt-einsum>=2.3.2 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (3.0.1)
Requirement already satisfied: keras-preprocessing>=1.0.5 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (1.1.0)
Requirement already satisfied: numpy<2.0,>=1.16.0 in /usr/lib/python3/dist-packages (from tensorflow==2.0.0rc1) (1.16.2)
Requirement already satisfied: wheel>=0.26 in /usr/lib/python3/dist-packages (from tensorflow==2.0.0rc1) (0.32.3)
Requirement already satisfied: protobuf>=3.6.1 in /usr/lib/python3/dist-packages (from tensorflow==2.0.0rc1) (3.6.1)
Requirement already satisfied: google-pasta>=0.1.6 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (0.1.7)
Requirement already satisfied: tb-nightly<1.15.0a20190807,>=1.15.0a20190806 in /home/keng/.local/lib/python3.7/site-packages (from tensorflow==2.0.0rc1) (1.15.0a20190806)
Requirement already satisfied: h5py in /home/keng/.local/lib/python3.7/site-packages (from keras-applications>=1.0.8->tensorflow==2.0.0rc1) (2.9.0)
Requirement already satisfied: werkzeug>=0.11.15 in /home/keng/.local/lib/python3.7/site-packages (from tb-nightly<1.15.0a20190807,>=1.15.0a20190806->tensorflow==2.0.0rc1) (0.15.5)
Collecting setuptools>=41.0.0 (from tb-nightly<1.15.0a20190807,>=1.15.0a20190806->tensorflow==2.0.0rc1)
  Downloading https://files.pythonhosted.org/packages/b2/86/095d2f7829badc207c893dd4ac767e871f6cd547145df797ea26baea4e2e/setuptools-41.2.0-py2.py3-none-any.whl (576kB)
    100% |████████████████████████████████| 583kB 2.8MB/s 
Requirement already satisfied: markdown>=2.6.8 in /home/keng/.local/lib/python3.7/site-packages (from tb-nightly<1.15.0a20190807,>=1.15.0a20190806->tensorflow==2.0.0rc1) (3.1.1)
Building wheels for collected packages: wrapt
  Running setup.py bdist_wheel for wrapt ... done
  Stored in directory: /home/keng/.cache/pip/wheels/d7/de/2e/efa132238792efb6459a96e85916ef8597fcb3d2ae51590dfd
Successfully built wrapt
launchpadlib 1.10.6 requires testresources, which is not installed.
pycocotools 2.0 requires cython>=0.27.3, which is not installed.
Installing collected packages: wrapt, setuptools
Successfully installed setuptools-41.2.0 wrapt-1.11.2
```
### 8. Test out the sample code

