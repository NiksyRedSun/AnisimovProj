



class DataMixin:
    title_page = None
    extra_context = {}
    cat_selected = None
    tag_selected = None


    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

        if self.tag_selected is not None:
            self.extra_context['tag_selected'] = self.tag_selected


    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context