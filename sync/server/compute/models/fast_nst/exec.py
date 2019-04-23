import numpy as np 
import torch
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms
import torch.onnx

import utils
from transformer_net import TransformerNet
from vgg import Vgg16
import re
from PIL import Image 
import time 
import os 
import re
import matplotlib.pyplot as plt

class NeuralStyleTransfer:
	'''Class containing implementation of Neural Style Transfer Algorithm'''

	def __init__(self):
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")	

	def run(self,content_img_arr,saved_style_model_path):

		'''
		Implmentation of Fast Neural Style Transfer Algorithm.Takes Style Image (numpy array with shape (h,w,3)) & 
		Trained Model weights for a particular Style (.pth file) & return output image as a numpy array of shape (3,h,w)
		'''
		
		content_image=Image.fromarray(np.uint8(content_img_arr))
		content_transform = transforms.Compose([
			transforms.ToTensor(),
			transforms.Lambda(lambda x: x.mul(255))
		])
		content_image = content_transform(content_image)
		content_image = content_image.unsqueeze(0).to(self.device)

		with torch.no_grad():
			style_model = TransformerNet()
			state_dict = torch.load(saved_style_model_path)
			# remove saved deprecated running_* keys in InstanceNorm from the checkpoint
			for k in list(state_dict.keys()):
				if re.search(r'in\d+\.running_(mean|var)$', k):
					del state_dict[k]
			style_model.load_state_dict(state_dict)
			style_model.to(self.device)
			output = style_model(content_image).cpu()
		return(output.numpy()[0])


'''
# Testing model

nst=NeuralStyleTransfer()
content_img_arr = np.asarray(Image.open(<ADD IMAGE>))
res=nst.run(content_img_arr,'/Models/candy.pth')
print(res)
'''