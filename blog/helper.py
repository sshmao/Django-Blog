from django.views.generic import ListView

class ListViewPage(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # paginator = context.get('paginator')
        # page = context.get('page_obj')
        # is_paginated = context.get('is_paginated')
        # pagination_data = pagination_datas(context)

        # context.update(pagination_data)
        return self.pagination_data(context)

    def pagination_data(self, context):

        paginator = context.get('paginator')

        page = context.get('page_obj')

        is_paginated = context.get('is_paginated')

        if not is_paginated:
            return {}
        # 当前页左边连续的页码号, 初始值为空
        left = []
        # 当前页右边连续的页码号, 初始值为空
        right = []
        # 标示第一页页码后是否需要显示省略号
        left_has_more = False
        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        first = False
        # 标示是否需要显示最后一页的页码号
        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages -1 :
                right_has_more = True


            if right[-1] < total_pages :
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number -1]


            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:

            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number -1]
            right = page_range[page_number:page_number + 2]


            if right[-1] < total_pages - 1 :
                right_has_more = True

            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        context.update(data)
        return context
