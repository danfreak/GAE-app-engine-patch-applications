def flickr_thumb(file,size):
  from google.appengine.api import images
  from mycommon.getimageinfo import getImageInfo
  type,width,height = getImageInfo(file)
  if width < height:
    file = images.resize(file,width=size)
    type,width,height =  getImageInfo(file)
    cropoff  = ((height  - size)*.5)/height
    file =  images.crop(file,top_y=cropoff, bottom_y=1.0  - cropoff,left_x=0.0,right_x=1.0)
  else:
    file  =  images.resize(file,height=size)
    type,width,height =  getImageInfo(file)
    cropoff =  ((width  -  size)*.5)/width
    file  = images.crop(file,left_x=cropoff, right_x=1.0 - cropoff,top_y=0.0,bottom_y=1.0) 
  return file