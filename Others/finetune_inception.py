# -*- coding: utf-8 -*-

import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

# Inception-v3模型瓶颈层的节点个数
BOTTLENECK_TENSOR_SIZE = 2048
# Inception-v3模型中代表瓶颈层结果的张量名称
BOTTLENECK_TENSOR_NAME = "pool_3/_reshape:0"
# 图像输入张量所对应的名称
JPEG_DATA_TENSOR_NAME = "DecodeJpeg/contents:0"
# 下载模型所在路径
MODEL_DIR = "E:/Work/PyCharm/TF_LEARN/model/"
# 下载的模型文件名
MODEL_FILE = "tensorflow_inception_graph.pb"
# 因为一个训练数据会被使用多次，所以可以将原始图像通过Inception-v3模型计算得到的特征向量保存在文件中，
# 免去重复的计算
CACHE_DIR = "E:/Work/PyCharm/TF_LEARN/model/tmp/bottle"
# 图片数据文件夹。在这个文件夹中，每一个子文件夹代表一个类别
INPUT_DATA = "E:/Work/PyCharm/TF_LEARN/data/flower_photos"
# 验证数据所占百分比
VALIDATION_PERCENTAGE = 10
# 测试数据所占百分比
TEST_PERCENTAGE = 10
# 神经网络的设置
LEARNING_RATE = 0.01
STEPS = 4000
BATCH = 100

# 从数据文件夹中读取所有的图片列表并按训练、验证、测试数据集分开
def create_img_lists(testing_percentage,validation_percentage):
    # 得到的所有图片都存在字典result中，其key为类别的名称，其value也是字典，存储所有图片的名称
    result = {}
    # 获取当前目录下所有的子目录
    sub_dirs = [x[0] for x in os.walk(INPUT_DATA)]
    # 得到的第一个目录是当前目录，不需要考虑
    is_root_dir = True
    for sub_dir in sub_dirs:
        if is_root_dir:
            is_root_dir=False
            continue
        # 获取当前目录下所有的有效图片文件
        extensions = ["jpg","jpeg","JPG","JPEG"]
        file_list =[]
        dir_name = os.path.basename(sub_dir)
        for extension in extensions:
            file_glob = os.path.join(INPUT_DATA,dir_name,'*.'+extension)
            file_list.extend(glob.glob(file_glob))
        if not file_list:
            continue
        # 通过目录名获取类别的名称
        label_name = dir_name.lower()
        # 初始化当前类别的训练集、验证集、测试集
        training_images = []
        testing_images = []
        validation_images = []
        for file_name in file_list:
            base_name = os.path.basename(file_name)
            # 随机将数据分到训练集、验证集、测试集
            chance =np.random.randint(100)
            if chance < validation_percentage:
                validation_images.append(base_name)
            elif chance < (testing_percentage+validation_percentage):
                testing_images.append(base_name)
            else:
                training_images.append(base_name)
        # 将当前类别的数据放入结果字典
        result[label_name]={"dir":dir_name,
                            "training":training_images,
                            "testing":testing_images,
                            "validation":validation_images,}
    # 返回整理好的所有数据
    return result

# 通过类别名称、所属数据集和图片编号获取一张图片的地址
# img_lists: 所有图片信息
# img_dir: 根目录。存放图片数据的根目录与存放图像特征向量的根目录地址不同
# label_name: 类别的名称
# index: 获取的图片的编号
# category: 指定需要获取的图片是在训练集、验证集、测试集
def get_img_path(img_lists,img_dir,label_name,index,category):
    # 获取给定类别中所有图片的信息
    label_lists = img_lists[label_name]
    # 根据所属数据集的名称获取集合中的全部图片信息
    category_lists = label_lists[category]
    mod_index = index % len(category_lists)
    # 获取图片的文件名
    base_name = category_lists[mod_index]
    sub_dir = label_lists["dir"]
    # 最终的地址为目录地址加上类别文件夹加上图片名称
    full_path = os.path.join(img_dir,sub_dir,base_name)
    return full_path

# 通过类别名称、所属数据集和图片编号经过Inception-v3模型处理后的特征向量文件地址
def get_bottleneck_path(img_lists,label_name,index,category):
    return get_img_path(img_lists,CACHE_DIR,label_name,index,category)+".txt"

# 使用加载好的训练好的Inception-v3模型处理一张图片，得到这个图片的特征向量
def run_bottleneck_on_img(sess,img_data,img_data_tensor,bottleneck_tensor):
    # 这个过程实际上是将当前图片作为输入计算瓶颈张量的值。这个瓶颈张量的值即这张图片的新的特征向量
    bottleneck_values = sess.run(bottleneck_tensor,{img_data_tensor:img_data})
    # 经过CNN处理，得到一个四维数组，需要将此结果压缩为特征向量（一维数组）
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values

# 获取一张图片经过Inception-v3模型处理后的特征向量。该函数先会试图寻找已经计算并且保存下来的特征向量
# 如果找不到，则先计算该特征向量，然后保存
def get_or_create_bottleneck(sess,img_lists,label_name,index,category,jpeg_data_tensor,bottleneck_tensor):
    # 获取一张图片对应的特征向量文件的绝对路径
    label_lists = img_lists[label_name]
    sub_dir = label_lists["dir"]
    sub_dir_path = os.path.join(CACHE_DIR,sub_dir)
    if not os.path.exists(sub_dir_path):
        os.makedirs(sub_dir_path)
    bottleneck_path = get_bottleneck_path(img_lists,label_name,index,category)
    # 如果该特征向量文件不存在，则通过Inception-v3计算特征向量，并对计算结果进行保存
    if not os.path.exists(bottleneck_path):
        # 原始的图片路径
        img_path = get_img_path(img_lists,INPUT_DATA,label_name,index,category)
        # 获取图片内容
        img_data = gfile.FastGFile(img_path,'rb').read()
        # 通过Inception-v3计算特征向量
        bottleneck_values = run_bottleneck_on_img(sess,img_data,jpeg_data_tensor,bottleneck_tensor)
        # 将计算的特征向量保存
        bottleneck_string = ','.join(str(x) for x in bottleneck_values)
        with open(bottleneck_path,'w') as bottleneck_file:
            bottleneck_file.write(bottleneck_string)
    else:
        # 直接从文件中获取图片相应的特征向量
        with open(bottleneck_path,'r') as bottleneck_file:
            bottleneck_string = bottleneck_file.read()
        bottleneck_values = [float(x) for x in bottleneck_string.split(",")]
    # 返回得到的特征向量
    return bottleneck_values

# 随机获取一个batch的图片作为训练数据
def get_random_cached_bottlenecks(sess,n_classes,img_lists,how_many,category,jpeg_data_tensor,bottleneck_tensor):
    bottlenecks = []
    ground_truths = []
    for _ in range(how_many):
        # 随机将一个类别和图片的编号加入当前的训练数据
        label_index = random.randrange(n_classes)
        label_name = list(img_lists.keys())[label_index]
        img_index = random.randrange(65536)
        bottleneck = get_or_create_bottleneck(sess,img_lists,label_name,img_index,category,jpeg_data_tensor,bottleneck_tensor)
        ground_truth = np.zeros(n_classes,dtype=np.float32)
        ground_truth[label_index] = 1.0
        bottlenecks.append(bottleneck)
        ground_truths.append(ground_truth)

    return bottlenecks,ground_truths

# 获取全部的测试数据。最终测试时，需要在所有的测试集上计算正确率
def get_test_bottlenecks(sess,img_lists,n_classes,jpeg_data_tensor,bottleneck_tensor):
    bottlenecks = []
    ground_truths = []
    label_name_list = list(img_lists.keys())
    # 枚举所有的类别和每个类别中的测试图片
    for label_index,label_name in enumerate(label_name_list):
        category = "testing"
        for index,unused_base_name in enumerate(img_lists[label_name][category]):
            # 通过Inception-v3计算图片对应的特征向量，并将其加入最终数据的列表
            bottleneck = get_or_create_bottleneck(sess,img_lists,label_name,index,category,jpeg_data_tensor,bottleneck_tensor)
            ground_truth = np.zeros(n_classes,dtype=np.float32)
            ground_truth[label_index] = 1.0
            bottlenecks.append(bottleneck)
            ground_truths.append(ground_truth)

    return bottlenecks,ground_truths

def main(_):
    # 读取所有图片
    img_lists=create_img_lists(TEST_PERCENTAGE,VALIDATION_PERCENTAGE)
    n_classes = len(img_lists.keys())
    # 读取已经训练好的Inception-v3模型。Google训练好的模型保存在GraphDef Protocol Buffer中，
    # 里面保存了每一个节点取值的计算方法以及变量的取值。具体参见模型持久化
    with gfile.FastGFile(os.path.join(MODEL_DIR,MODEL_FILE),'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    # 加载读取的Inception-v3模型，并返回数据输入所对应的张量以及计算瓶颈层结果所对应的张量
    bottleneck_tensor,jpeg_data_tensor = tf.import_graph_def(graph_def,return_elements=[BOTTLENECK_TENSOR_NAME,JPEG_DATA_TENSOR_NAME])
    # 定义新的神经网络输入，此输入即新的图片经过Inception-v3模型前向传播到达瓶颈层时的节点取值。
    # 此过程可理解为特征提取
    bottleneck_input = tf.placeholder(tf.float32,[None,BOTTLENECK_TENSOR_SIZE],name="BottleneckInputPlaceholder")
    # 定义新的标准答案输入
    ground_truth_input = tf.placeholder(tf.float32,[None,n_classes],name="GroundTruthInput")
    # 定义一层新的全连接层来解决新的图片分类问题。因为训练好的Inception-v3模型已经将原始的
    # 图片抽象为更加容易的特征向量，所以不必再从头训练如此复杂的神经网络来完成新的分类任务
    with tf.name_scope("final_training_ops"):
        weights = tf.Variable(tf.truncated_normal([BOTTLENECK_TENSOR_SIZE,n_classes],stddev=0.001))
        biases = tf.Variable(tf.zeros([n_classes]))
        logits = tf.matmul(bottleneck_input,weights)+biases
        final_tensor = tf.nn.softmax(logits)
    # 定义交叉熵损失函数
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=ground_truth_input)
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cross_entropy_mean)
    # 计算正确率
    with tf.name_scope("evalulation"):
        correct_prediction = tf.equal(tf.argmax(final_tensor,1),tf.argmax(ground_truth_input,1))
        evaluation_step = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    saver =tf.train.Saver()
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        # 训练过程
        for i in range(STEPS):
            # 每次获取一个batch的训练数据
            train_bottlenecks,train_ground_truth = get_random_cached_bottlenecks(sess,n_classes,img_lists,BATCH,"training",jpeg_data_tensor,bottleneck_tensor)
            sess.run(train_step,feed_dict={bottleneck_input:train_bottlenecks,ground_truth_input:train_ground_truth})
            # 在验证数据集上测试正确率
            if i % 100 ==0 or i+1 == STEPS:
                validation_bottlenecks,validation_gound_truth = get_random_cached_bottlenecks(sess,n_classes,img_lists,BATCH,"validation",jpeg_data_tensor,bottleneck_tensor)
                validation_accuracy = sess.run(evaluation_step,feed_dict={bottleneck_input:validation_bottlenecks,ground_truth_input:validation_gound_truth})
                print("Step %d: Validation accuracy on random sampled %d examples = %.1f%%" % (i,BATCH,validation_accuracy*100))
            # 在最后的测试数据集上测试正确率
            if i % 1000 == 0 or i+1 == STEPS:
                saver.save(sess, os.path.join(MODEL_DIR, "flower.ckpt"))
                print("model has saved!")
        test_bottlenecks, test_ground_truth = get_test_bottlenecks(sess, img_lists, n_classes, jpeg_data_tensor,bottleneck_tensor)
        test_accuracy = sess.run(evaluation_step, feed_dict={bottleneck_input: test_bottlenecks,ground_truth_input: test_ground_truth})
        print("Final test accuracy = %.1f%%" % (test_accuracy * 100))

if __name__=="__main__":
    tf.app.run()















