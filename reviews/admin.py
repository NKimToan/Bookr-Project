from django.contrib import admin
# from django.contrib.admin import AdminSite
# username: bookradmin
# email: bookradmin@example.com
# pass: Bookrv123
from reviews.models import (Publisher, Contributor, Book, BookContributor, Review)


# Register your models here.
# tạo lớp BookAdmin kế thừa lớp ModelAdmin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn13', 'has_isbn')
    list_filter = ('publisher', 'publication_date')
    date_hierarchy = 'publication_date'
    search_fields = ('title', 'isbn')

    # Phải bấm vào cột tiêu đề mới sắp xếp được
    @admin.display(ordering='isbn', description='ISBN-13', empty_value='-/-')
    def isbn13(self, obj):
        return "{}-{}-{}-{}-{}".format(obj.isbn[0:3], obj.isbn[3:4], obj.isbn[4:6], obj.isbn[6:12], obj.isbn[12:13])

    @admin.display(boolean=True, description='Has ISBN', )
    def has_isbn(self, obj):
        return bool(obj.isbn)


admin.site.register(Book, BookAdmin)


class ReviewAdmin(admin.ModelAdmin):
    # exclude = ('date_edited',)
    # fields = ('content', 'rating', 'creator', 'book')
    #     Dùng cách nào cũng được
    fieldsets = (
        ("Linkage", {"fields": ("creator", "book")}),
        ("Review content", {"fields": ("content", "rating")}),
    )


admin.site.register(Review, ReviewAdmin)


#
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_names', 'first_names')
    search_fields = ('last_names__startswith', 'first_names')
    list_filter = ['last_names']

    @admin.display(ordering='last_names')
    def last_names(self, obj):
        return obj.last_names

    @admin.display(ordering='first_names')
    def last_names(self, obj):
        return obj.first_names


admin.site.register(Contributor, ContributorAdmin)
# admin.site.register(Contributor)
admin.site.register(Publisher)
admin.site.register(BookContributor)
