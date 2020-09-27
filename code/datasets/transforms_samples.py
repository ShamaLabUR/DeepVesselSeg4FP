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
import numpy as np
from PIL import Image
from torchvision.transforms import functional as F


class ToTensorSample(object):
    def __call__(self,sample):
        image,label,mask = sample['i'],sample['l'],sample['m']
        image = F.to_tensor(image)
        label = F.to_tensor(label)
        mask = F.to_tensor(mask)
        return {'i':image,'l':label,'m':mask}


class GreenChannel(object):
    def __init__(self,n_out_ch=3):
        self.n_out_ch = n_out_ch
    def __call__(self,sample):
        image,label,mask = sample['i'],sample['l'],sample['m']
        image_np = np.array(image)
        green_ch_np = image_np[:,:,1]
        if self.n_out_ch == 1:
            green_ch = Image.fromarray(green_ch_np).convert('L')
        if self.n_out_ch == 3:
            green_ch_np = np.array(green_ch_np,dtype=np.uint8)
            green_ch_np = np.dstack([green_ch_np,green_ch_np,green_ch_np])
            green_ch = Image.fromarray(green_ch_np,'RGB')
        return {'i':green_ch,'l':label,'m':mask}
