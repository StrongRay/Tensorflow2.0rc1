# Tensorflow2.0rc1
Building Tensorflow 2.0 RC 1 from source

## Purpose of Building from source
When a version of tensorflow is released, you can easily do a **pip3 install tensorflow-gpu==2.0.0rc1** to install the latest software. However, there is no source codes required, it's just a module install.  When Source codes of tensorflow is required, for example, the need to access TFliteconverter etc or when you need to have a better understanding of tensorflow codes, you might need to build from source.  However, it is very timeconsuming.  And after many hours, it might fail on some conditions.

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

