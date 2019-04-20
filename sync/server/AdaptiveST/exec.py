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



class RealTimeArbitararyNstWithAdaIn:
	''' Real Time Arbitrary Style Transfer with Adaptive Instance Normalization '''

	def __init__(self,content_imgs=None,style_imgs=None,content_size=512,style_size=512,output_img=None,alpha=1.0,preserve_color=True,):

		self.content_imgs = content_imgs	# list of content image paths
		self.style_imgs = style_imgs		# list of Style image paths
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

	def run(self,alpha=1.0):
		''' Style Transfer Algorithm'''
		
		content_tf = self.test_transform(self.content_size,self.crop)	
		style_tf = self.test_transform(self.style_size,self.crop)

		for content_path in self.content_imgs:
			for style_path in self.style_imgs:
				content = content_tf(Image.open(content_path))
				style = style_tf(Image.open(style_path))
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
				output_name = '{:s}/{:s}_stylized_{:s}{:s}'.format(self.output_img, splitext(basename(content_path))[0],splitext(basename(style_path))[0],'.jpg')
				save_image(output, output_name)	
				return(output.numpy()[0]) #shape (3, 512, 512)
	

# Runnning Testing & Training


adain=RealTimeArbitararyNstWithAdaIn(content_imgs=['/home/ashik/Desktop/hbp.jpg'],
	style_imgs=['/home/ashik/Desktop/jap.jpg'],
	output_img='/home/ashik/Desktop/',preserve_color=False)
adain.run()
