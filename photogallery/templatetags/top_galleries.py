from django.template import Library, Node
from django.db.models import get_model
from ragendja.dbutils import get_object_list
     
register = Library()
     
class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = int(num), varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        #items = self.model._default_manager.all().order('-created').filter("published = ", True)#[:self.num]
        #items = get_object_list(self.model, "published = ", True).order('-created').fetch(self.num)
        items = get_object_list(self.model).fetch()
        n = 1
        newlist[]
        for i in len(items):
          newlist[n].append(i)
          if n % 3:
            n += 1
        context[self.varname] = newlist
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
    
get_latest = register.tag(get_latest)