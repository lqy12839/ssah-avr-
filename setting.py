import numpy as np
import scipy.io
from load_data import loading_data_zyf
# from load_data1 import loading_data_zyf
from load_data import split_data


# environmental setting: setting the following parameters based on your experimental environment.
select_gpu = '3'
per_process_gpu_memory_fraction = 0.9

# Initialize data loader
MODEL_DIR = './data/imagenet-vgg-f.mat'
DATA_DIR = './data/FLICKR-25K.mat'

phase = 'train'
checkpoint_dir = './checkpoint'
Savecode = './Savecode'
dataset_dir = 'Flickr'
netStr = 'alex'

have_weight = True

SEMANTIC_EMBED = 512
MAX_ITER = 100
batch_size = 2
image_size = 224


#data = scipy.io.loadmat(MODEL_DIR)
#print data
#mean = data['meta']['normalization'][0][0][0]

images, tags, labels = loading_data_zyf(DATA_DIR)
dimTxt = tags.shape[1]
dimLab = labels.shape[1]

# DATABASE_SIZE = 18015
# TRAINING_SIZE = 10000
# QUERY_SIZE = 2000
DATABASE_SIZE = 3633
TRAINING_SIZE = 2000
QUERY_SIZE = 400
VERIFICATION_SIZE = 200

X, Y, L = split_data(images, tags, labels, QUERY_SIZE, TRAINING_SIZE, DATABASE_SIZE)
train_L = L['train']
train_x = X['train']
train_y = Y['train']

query_L = L['query']
query_x = X['query']
query_y = Y['query']

retrieval_L = L['retrieval']
retrieval_x = X['retrieval']
retrieval_y = Y['retrieval']

num_train = train_x.shape[0]
numClass = train_L.shape[1]
dimText = train_y.shape[1]

Sim = (np.dot(train_L, train_L.transpose()) > 0).astype(int)*0.999

data = scipy.io.loadmat(MODEL_DIR)
#print data['meta']['normalization'][0][0][0][0][2]
mean = data['meta']['normalization'][0][0][0][0][2]
#mean = data['normalization'][0][0][0]
#mean = [0.485, 0.456, 0.406]

Epoch = 100
k_lab_net = 10
k_img_net = 15
k_txt_net = 15
k_dis_net = 1
save_freq = 1

bit = 16
alpha = 1
gamma = 1
beta = 1
eta = 1
delta = 1

# Learning rate
lr_lab = [np.power(0.1, x) for x in np.arange(2.0, MAX_ITER, 0.5)]
lr_img = [np.power(0.1, x) for x in np.arange(4.5, MAX_ITER, 0.5)]
lr_txt = [np.power(0.1, x) for x in np.arange(3.5, MAX_ITER, 0.5)]
lr_dis = [np.power(0.1, x) for x in np.arange(3.0, MAX_ITER, 0.5)]
