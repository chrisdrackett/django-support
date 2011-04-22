import re, logging
from copy import copy

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import truncate_html_words
from django.template.defaulttags import url as url_tag
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

log = logging.getLogger('helper.interface_tags')

##################
#  Active Items  #
##################

@register.tag
def active(parser, token):
    """ tag to determine if a link is to the current page, and if it is, sets 'link_active'
        to True in the context.
        
        Use:
            {% active path view strict[True,False] arg1 arg2 arg3 %}
            
            path:   the path to check. Generally this is just 'request.path'
            view:   the view that you want to check against the path. (uses reverse)
            strict: if strict is true, then the two paths need to be exactly the same.
                    if strict is false, then a path of /some/path/ and a view with the url
                    /some/ will match.
            args:   args needed by the given view to get its path using reverse.
        
        Example:
            {% active request.path "settings" True %}
            <a href="{% url settings %}" class="{% if link_active %} active{% endif %}">
        
        """
    args = token.split_contents()
    path = args[1]
    view = args[2].replace('"', '').replace("'", '')
    strict = args[3].replace('"', '').replace("'", '')

    arg1 = None; arg2 = None; arg3 = None
    if len(args) > 4:
        arg1 = args[4]
    if len(args) > 5:
        arg2 = args[5]
    if len(args) > 6:
        arg3 = args[6]
    if not view:
        raise template.TemplateSyntaxError, "%r tag requires at least one view argument" % token.contents.split()[0]
    return ActiveTag(view, path, strict, arg1, arg2, arg3)

class ActiveTag(template.Node):
    def __init__(self, view, path, strict, arg1, arg2, arg3):
        self.view = view
        self.path = template.Variable(path)
        self.strict = template.Variable(strict) if strict else True
        self.arg1 = template.Variable(arg1) if arg1 else None
        self.arg2 = template.Variable(arg2) if arg2 else None
        self.arg3 = template.Variable(arg3) if arg3 else None
        self.context_var = 'link_active'
    
    def render(self, context):
        views = self.view.split(',')
        path = self.path.resolve(context)
        strict = str(self.strict) == 'True'
        pattern = None
        
        args = []
        if self.arg1:
            args.append(self.arg1.resolve(context))
        if self.arg2:
            args.append(self.arg2.resolve(context))
        if self.arg3:
            args.append(self.arg3.resolve(context))
        
        # Loop through any views we accept and try to find a matching one
        for view in views:
            #log.debug("Trying view %s " % view)
            try:
                pattern = reverse(view, args=args)
            except NoReverseMatch:
                try:
                    project_name = settings.SETTINGS_MODULE.split('.')[0]
                    pattern = reverse(project_name + '.' +  view, args=args)
                except NoReverseMatch:
                    pass
            if pattern:
                #log.debug("MATCHED pattern %s" % pattern)
                break
        
        # If we came out of the loop with no pattern matching, we're done
        if not pattern:
            context[self.context_var] = False
            return ''
        
        pattern = '^' + pattern
        
        if strict:
            pattern = pattern + '$'
        log.debug('checking to see if %s matches %s...' % (pattern, path))
        context[self.context_var] = re.search(pattern, path)
        return ''

#####################
#  Text Formatting  #
#####################

class TruncateNode(template.Node):
    def __init__(self, count, nodelist, nodelist_more):
        self.count, self.nodelist, self.nodelist_more = count, nodelist, nodelist_more
    
    def render(self, context):
        content_original = self.nodelist.render(context)
        content_truncated = truncate_html_words(content_original, self.count, end_text='')
        if self.nodelist_more and (content_original != content_truncated ):
            more = self.nodelist_more.render(context)
        else:
            more = u''
        
        return mark_safe(content_truncated + more)

@register.tag(name='truncate')
def do_truncate(parser, token):
    """
    Truncates given text (html-aware)
    Sample usage::
    
        {% truncate 60 %}
             {{ some_text }}
        {% more %}
             <a href="asdasd">Read more..</a>
        {% endtruncate %}
    """
    _, count = token.split_contents()
    
    nodelist = parser.parse(('more', 'endtruncate',))
    token = parser.next_token()
    if token.contents == 'more':
        nodelist_more = parser.parse(('endtruncate',))
        parser.delete_first_token()
    else:
        nodelist_more = None
    return TruncateNode(count, nodelist, nodelist_more)

#########
#  SVG  #
#########

@register.inclusion_tag('support/full_width_svg.html')
def full_width_svg(name, width, height, alt_text=None):
    ''' Helper to render an SVG that will size to fill
        its element while keeping its dimentions.
        
        '''
    
    return {
        'ratio': str((float(height)/float(width))*100)[:2],
        'url': "%s/svg/%s" % (settings.MEDIA_URL.rstrip('/'), name),
        'alt_text': alt_text
    }