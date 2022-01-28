from django.utils.safestring import mark_safe
import copy

class Pagination(object):
    def __init__(self, request, query_set, page_size = 10, page_param='page', plus=5):
        try: 
            page_id = int(request.GET.get(page_param, 1))
        except:
            page_id = 1

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param

        # if page_id.isdecimal():
        #     page_id = int(page_id)
        # else:
        #     page_id = 1

        self.page_id = page_id
        self.page_size = page_size
        self.data_start = (page_id-1) * page_size
        self.data_end = page_id * page_size

        total_cnt = query_set.count()
        num_page, div = divmod(total_cnt, page_size)
        if div:
            num_page += 1
        self.num_page = num_page

        self.query_set = query_set[self.data_start:self.data_end]
        self.plus = plus

    def html(self):
        if self.num_page <= 2*self.plus + 1:
            start_page = 1
            end_page = self.num_page
        else:
            if self.page_id <= self.plus:
                start_page = 1
                end_page = 2*self.plus+1
            else:
                if (self.page_id + self.plus) > self.num_page:
                    start_page = self.num_page - 2*self.plus
                    end_page = self.num_page
                else:
                    start_page = self.page_id - self.plus
                    end_page = self.page_id + self.plus

        page_str_list = []
        # First Page
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('''
            <li class="page-item"><a class="page-link" href="?{}">First Page</a></li>
            '''.format(self.query_dict.urlencode()))

        # Prev. Page
        if self.page_id == 1:
            self.query_dict.setlist(self.page_param, [1])
            prev = '''
                <li class="page-item"><a class="page-link" href="?{}">Previous</a></li>
                '''.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page_id-1])

            prev = '''
                <li class="page-item"><a class="page-link" href="?{}">Previous</a></li>
                '''.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page+1):
            if i == self.page_id:
                self.query_dict.setlist(self.page_param, [i])

                ele = '<li class="page-item active"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])

                ele = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # next page
        if self.page_id == self.num_page:
            self.query_dict.setlist(self.page_param, [self.num_page])

            next = '''
                <li class="page-item"><a class="page-link" href="?{}">Next</a></li>
                '''.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page_id+1])

            next = '''
                <li class="page-item"><a class="page-link" href="?{}">Next</a></li>
                '''.format(self.query_dict.urlencode())
        page_str_list.append(next)

        # Last page
        self.query_dict.setlist(self.page_param, [self.num_page])

        page_str_list.append('''
            <li class="page-item"><a class="page-link" href="?{}">Last Page</a></li>
            '''.format(self.query_dict.urlencode()))

        # Search
        search_str = '''
        <li>
            <form style="float: left;margin-left: -1px" method="get">
                <input name="page"
                    style="postion: relative;float:left;display: inline-block;width: 100px;border-radius: 0;"
                    type="text" class="form-control" placeholder="Page">
                <button type="submit" class="btn btn-primary">Jump</button>
            </form>
        </li>
        '''
        page_str_list.append(search_str)

        page_string = '<nav aria-label="Page navigation example"> <ul class="pagination justify-content-center">'\
            + ("".join(page_str_list))+\
                '</ul> </nav>'

        page_string = mark_safe(page_string)

        return page_string
