from __future__ import division
from google.appengine.api import images

def flickr_thumb(file,size):
  """ 
  returns squared thumbnail
  """
  width,height =  getImageInfo(file)
  
  if width < height:
    file = images.resize(file,width=size)
    width,height =  getImageInfo(file)
    cropoff  = ((height  - size)*.5)/height
    file =  images.crop(file,top_y=cropoff, bottom_y=1.0  - cropoff,left_x=0.0,right_x=1.0)
  else:
    file  =  images.resize(file,height=size)
    width,height =  getImageInfo(file)
    cropoff =  ((width  -  size)*.5)/width
    file  = images.crop(file,left_x=cropoff, right_x=1.0 - cropoff,top_y=0.0,bottom_y=1.0) 
  return file

def resize_to_max(file, max_w, max_h):
  """ 
  rezizes an image in order to fit max dimensions keeping proportions
  """
  
  width, height = getImageInfo(file)
  
  ratio_w = width/max_w
  ratio_h = height/max_h
  ratio_new = ratio_w/ratio_h
  ratio = width/height
  new_w = int(width)
  new_h = int(height)
  #too large
  if (ratio_new > 1 and width > max_w):
    new_w = max_w
    new_h = int(round(max_h / ratio))
  #too heigh
  elif (ratio_new < 1 and height > max_h):
    new_w = int(round(max_w * ratio))
    new_h = max_h
  elif (ratio_new == 1 and width > max_w):
    new_w = max_w
    new_h = max_h
  
  file = images.resize(file, new_w, new_h)
  return file
  
def getImageInfo(file):
  """ 
  returns image dimensions
  """
  img = images.Image(file)
  width = img.width
  height = img.height
  return width, height