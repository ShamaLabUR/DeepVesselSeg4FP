#!/bin/bash

# Root directory to dataset 
DATA_PATH='../data/datasets/sample_images_from_PRIME-FP20'

# Directory to pretrained model
PRETRAINED_DIR='../data/pretrained_models/'
PRETRAINED_ID=4

# Directory to results folder. Automatically generated if it doesn't exist
SAVE_DIR='../results'

# Batch size
BATCH_SIZE=16

python detect_FP_vessels_w_DNN.py -d ${DATA_PATH} -p ${PRETRAINED_DIR} -i ${PRETRAINED_ID} -s ${SAVE_DIR} -b ${BATCH_SIZE}
