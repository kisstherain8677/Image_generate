# image generate tool  
 本项目用于学习图像分割、图像生成、风格迁移等技术，将多种方法汇总，尽量做到易用。  
 ![image](https://github.com/kisstherain8677/Image_generate/blob/main/sample.png)
 
一、自动抠图，可选取感兴趣区域，一键扣取前景，可通过标记前景/后景进行迭代微调  
基于https://github.com/zihuaweng/Interactive-image-segmentation-opencv-qt 修改。  
使用方法：  
0、安装requirements.txt文件中的依赖项。  
1、运行app.py。  
2、导入图片。  
3、指定区域。  
4、迭代一次，在输出结果窗口查看结果。  
5、微调，鼠标变成画笔，标记前景和背景，继续点击迭代一次。  
6、效果满意后点击保存。  

二、基于SackGAN++的图片生成  
使用方法：  
0、从 https://github.com/hanzhanggit/StackGAN-v2 下载data和pretrain model 到StackGAN/data StackGAN/models。未提供花朵模型，但是已修改代码使其可以训练花朵模型。  
1、点击生成图片按钮。  
2、选择要生成图片的种类。  
3、输入描述属性，点击生成caption，根据实际情况调整生成的句子。  
4、点击生成图片，等待图片生成。  

三、基于CycleGAN的图像风格迁移  
使用方法：  
0、从 https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix 下载pretrainmodel monet_style等四个画家到CycleGAN/checkpoints。  
1、点击导入图片，选择图片。  
2、点击风格转换，选择你要转换的风格。  
3、等待转换风格后的图片出现在output栏。  
4、点击保存，可以保存转换风格后的图片。  

下一步计划：  
1、加入更多种类图片的生成。  
2、用自己搜集的数据集训练图片生成模型和风格迁移模型。  

