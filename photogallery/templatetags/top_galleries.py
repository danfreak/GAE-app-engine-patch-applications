from photogallery.models import Gallery, Photo
from django import template
register = template.Library()

def latest_galleries(parser, token):
    return LatestGalleriesNode

class LatestGalleriesNode(template.Node):
    def render(self, context):
      gall = Gallery.all()
      gall.filter("published = ", True)
      gall.order('-created')
      context['latest_galleries'] = gall
      return ''

registertag('top_galleries', latest_galleries)