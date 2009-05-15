from __future__ import division
from google.appengine.api import images

def flickr_thumb(file,size):
  """ 
  returns squared cropped thumbnail
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
    
  file = images.im_feeling_lucky(file, images.JPEG)
  return file

def resize_to_max(file, max_w, max_h):
  """ 
  rezizes an image in order to fit max dimensions keeping proportions
  NO crop
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
  file = images.im_feeling_lucky(file, images.JPEG)
  return file


def resize_to(file, w, h):

  """ 
  rezizes an image to given dimensions
  cropping it in order to keep proportions
  """
  width, height = getImageInfo(file)
  #ratio = width/height
  #ratio_n = w/h
  #ratio_new = ratio/ratio_n
  w_new = height * (w/h)
  h_new = width / (w/h)
  #cut width
  if w_new < width:
    
    cropoff =  (abs(width  -  w_new)*.5)/width
    file =  images.crop(file,top_y=0.0, bottom_y=1.0,left_x=cropoff,right_x=1.0  - cropoff)
    file = images.resize(file, height= h)
  #cut height
  elif h_new < height:
    
    #print h_new
    cropoff =  (abs(height  -  h_new)*.5)/height
    file =  images.crop(file,top_y=cropoff, bottom_y=1.0 - cropoff,left_x=0.0,right_x=1.0 )
    file = images.resize(file, width= w)
  else:
    file = images.resize(file, width = w, height= h)
    
  file = images.im_feeling_lucky(file, images.JPEG)
  return file
  
def getImageInfo(file):
  """ 
  returns image dimensions
  """
  img = images.Image(file)
  width = img.width
  height = img.height
  return width, height