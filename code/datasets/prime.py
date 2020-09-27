"""
The code is copyrighted by the authors. Permission to copy and use
this software for noncommercial use is hereby granted provided: (a)
this notice is retained in all copies, (2) the publication describing
the method (indicated below) is clearly cited, and (3) the
distribution from which the code was obtained is clearly cited. For
all other uses, please contact the authors.
 
The software code is provided "as is" with ABSOLUTELY NO WARRANTY
expressed or implied. Use at your own risk.

The code and the pre-trained deep neural network model provided with
this repository allow one to perform vessel detection in ultra-widefield
fundus photography images and to compute various evaluation metrics for 
the detected vessel maps by comparing these against provided ground 
truth. The ralated methodology and metrics are described in the paper:

L. Ding, A. E. Kuriyan, R. S. Ramchandran, C. C. Wykoff, and G. Sharma 
"Weakly-Supervised Vessel Detection in Ultra-Widefield Fundus Photography
Via Iterative Multi-Modal Registration and Learning", 
IEEE Trans. on Medical Imaging, 2020, accepted for publication, to appear.
"""
import os
import glob

import numpy as np
from torch.utils.data import Dataset
from PIL import Image


class PRIME_FP(Dataset):
    def __init__(self,root,include_label=True,transforms=None):
        self.root = os.path.expanduser(root)
        self.transforms = transforms
        self.include_label = include_label

        images_name = os.path.join(self.root,'Images_FP_PRIME-FP20','*tif')
        self.image_filenames = sorted(glob.glob(images_name))
        
        mask_name = os.path.join(self.root,'Masks_FP_PRIME-FP20','*png')
        self.mask_filenames = sorted(glob.glob(mask_name))

        if include_label:
            labels_name = os.path.join(self.root,'Labels_FP_PRIME-FP20','*png')
            self.label_filenames = sorted(glob.glob(labels_name))
             
        self.n_img = len(self.image_filenames)

    def get_filename_from_cross_val_id(self,target_id):
        target_id = '{:02d}'.format(target_id)
        image_filename = [f for f in self.image_filenames if "ImgFP"+target_id in f][0]
        mask_filename = [f for f in self.mask_filenames if "MaskFP"+target_id in f][0] 
        if self.include_label:
            label_filename = [f for f in self.label_filenames if "LabelFP"+target_id in f][0]
            return image_filename,mask_filename,label_filename
        else:
            return image_filename,mask_filename,None
            
    def get_image_from_cross_val_id(self,target_id):
        image_filename, mask_filename, label_filename = self.get_filename_from_cross_val_id(target_id)
        image = Image.open(image_filename).convert('RGB')
        mask = Image.open(mask_filename).convert('L')
        if self.include_label:
            label = Image.open(label_filename).cconvert('L')
        else:
            label = Image.new('L',image.size)

        sample = {'i':image,'l':label,'m':mask}
        if self.transforms:
            sample = self.transforms(sample) 
        return sample        
            
        
    def __getitem__(self,index):
        image = Image.open(self.image_filenames[index]).convert('RGB')
        mask = Image.open(self.mask_filenames[index]).convert('L')
        if self.include_label:
            label = Image.open(self.label_filenames[index]).convert('L')
        else:
            label = Image.new('L',image.size) # will not be used
        
        sample = {'i':image,'l':label,'m':mask}
        if self.transforms:
            sample = self.transforms(sample) 
        return sample        
        
    def __len__(self):
        return self.n_img
    

