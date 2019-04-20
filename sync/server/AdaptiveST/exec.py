import os

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
from torchvision import transforms
from torchvision.utils import save_image


from PIL import Image
from PIL import ImageFile

from os.path import basename
from os.path import splitext


from tqdm import tqdm
from tensorboardX import SummaryWriter

import net
from function import adaptive_instance_normalization
from function import coral
from sampler import InfiniteSamplerWrapper
import numpy as np 



class RealTimeArbitararyNstWithAdaIn:
	''' Real Time Arbitrary Style Transfer with Adaptive Instance Normalization '''

	def __init__(self,content_size=512,style_size=512,output_img=None,alpha=1.0,preserve_color=True,):

		self.content_size = content_size	# New (minimum) size for the style image,keeping the original size if set to 0
		self.style_size = style_size		# New (minimum) size for the style image,keeping the original size if set to 0
		self.output_img = output_img		# Output image path
		self.alpha=alpha 					# The weight that controls the degree of stylization. Should be between 0 and 1
		self.crop = False
		self.preserve_color=preserve_color
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
		self.decoder_path = 'models/decoder.pth'
		self.vgg_normalised_path = 'models/vgg_normalised.pth'

		self.decoder=net.decoder
		self.vgg=net.vgg
		self.decoder.eval()
		self.vgg.eval()

		self.decoder.load_state_dict(torch.load(self.decoder_path))
		self.vgg.load_state_dict(torch.load(self.vgg_normalised_path))
		self.vgg = nn.Sequential(*list(self.vgg.children())[:31])

		self.vgg.to(self.device)
		self.decoder.to(self.device)



	def test_transform(self,size,crop):
		transform_list = []
		if size != 0:
			transform_list.append(transforms.Resize(size))
		if crop:
			transform_list.append(transforms.CenterCrop(size))
		transform_list.append(transforms.ToTensor())
		transform = transforms.Compose(transform_list)
		return transform

	def run(self,content_img,style_img,alpha=1.0):
		
		''' Style Transfer Algorithm.Takes Style Image (numpy array with shape (h,w,3)) & Content Image
			with shape (numpy array with shape (h,w,3)) & return output image as a numpy array of shape (3,h,h)
		 '''
		
		content_tf = self.test_transform(self.content_size,self.crop)	
		style_tf = self.test_transform(self.style_size,self.crop)

		content = content_tf(Image.fromarray(np.uint8(content_img)))
		style = style_tf(Image.fromarray(np.uint8(style_img)))

		if self.preserve_color:
			style = coral(style, content)
		style = style.to(self.device).unsqueeze(0)
		content = content.to(self.device).unsqueeze(0)
		with torch.no_grad():
			content_f = self.vgg(content)
			style_f = self.vgg(style)
			feat = adaptive_instance_normalization(content_f, style_f)
			feat = feat * alpha + content_f * (1 - alpha)
			output = self.decoder(feat)
		output = output.cpu()
		#output_name = '{:s}/{:s}_stylized_{:s}{:s}'.format(self.output_img, splitext(basename('content_img'))[0],splitext(basename('style_img'))[0],'.jpg')
		#save_image(output, output_name)	
		return(output.numpy()[0]) #shape (3, 512, 512)
	

# Runnning Testing & Training


adain=RealTimeArbitararyNstWithAdaIn(output_img='/home/ashik/Desktop/',preserve_color=False)

content_img = np.asarray(Image.open('/home/ashik/Desktop/hbp.jpg'))
style_img =  np.asarray(Image.open('/home/ashik/Desktop/jap.jpg'))
print(style_img.shape)
res=adain.run(content_img,style_img)
