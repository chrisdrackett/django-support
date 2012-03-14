def process_form(request, form_class, save_args=None, *a, **kw):
    '''
        Optional:
        =========
        
        You can pass args to the form save function in a 'save_args' dict.
        
        
        Example Usage:
        ==============
        
        success, form = process_form(request, DiscussionForm, initial={
            'category':Category.objects.all()[0].id,
        })
        if success:
            return form # this is the return from the forms save method.
        
        return template(request, 'talk/create_discussion.html', {
            'categories': Category.objects.all(),
            'form': form
        })
    '''
    
    form = form_class(request.POST or None, *a, **kw)
    
    if request.method == 'POST':
        if form.is_valid():
            if not save_args:
                save_args = {}
            results = form.save(request, **save_args)
            return (True, results)
    return (False, form)