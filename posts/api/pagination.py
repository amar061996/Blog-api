#built-in pagination
from rest_framework.pagination import (
		PageNumberPagination,
		LimitOffsetPagination,

	)

#custom Pagination

class PostListOffsetPagination(LimitOffsetPagination):

	default_limit=2     #default value of limit when not provided as a parameter
	max_limit=10		#max value of limit when not provided as a parameter


class PostPageNumberPagination(PageNumberPagination):

	page_size=2			#number of posts on the list page