from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Contributor, Review, Publisher
from .utils import average_rating
from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm
from django.contrib import messages
from django.utils import timezone
from PIL import Image
from django.conf import settings
# from django.contrib.auth.decorators import permission_required #Cách 1
# from django.contrib.auth.decorators import user_passes_test #Cách 2
from django.contrib.auth.decorators import (login_required, user_passes_test)
from django.core.exceptions import PermissionDenied
# thư viện dùng để link các trang bằng id
# Create your views here.


def index(request):
    return render(request, 'base.html')


def book_search(request):
    search_text = request.GET.get("search")
    form = SearchForm(request.GET)
    books_list = []
    if request.method == "GET":
        if form.is_valid() and form.cleaned_data["search"]:
            search = form.cleaned_data["search"]
            search_in = form.cleaned_data["search_in"]
            # Lấy session
            if request.user.is_authenticated:
                search_histories = request.session.get("search_histories", [])
                search_history = [search, search_in]
                if search_history in search_histories:
                    search_histories.pop(search_histories.index(search_history))
                search_histories.insert(0, search_history)
                request.session['search_histories'] = search_histories

            if search_in == "title":
                book_list = Book.objects.filter(title__icontains=search)
                for book in book_list:
                    books_list.append(book)
            else:
                firstnames = Contributor.objects.filter(first_names__icontains=search)
                for contributor in firstnames:
                    for book in contributor.book_set.all():  # Truy vấn ngược các book có kết nối với contributor thông qua bảng trung gian, thuộc tính contributor xuất hiện trong bảng book
                        books_list.append(book)

                lastnames = Contributor.objects.filter(last_names__icontains=search)
                for contributor in lastnames:
                    for book in contributor.book_set.all():
                        books_list.append(book)
    return render(request, "reviews/search-results.html",
                  {"search_text": search_text, "form": form, "books_list": books_list})


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews is not None:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book,
                          'book_rating': book_rating,
                          'number_of_reviews': number_of_reviews})
        context = {
            'book_list': book_list
        }
    # Cách để xác định tên truy vấn ngược với _set
    # related_name = Review._meta.get_field('book').related_query_name()
    # print("Tên quan hệ:", related_name)
    return render(request, 'reviews/book_list.html', context)


def book_detail(request, id):
    book = get_object_or_404(Book, id=id) #Lấy thẳng đối tượng Book có id bằng id truyền vào in type ra sẽ thấy rõ hơn
    # books = Book.objects.filter(id=id) #Lấy đối tượng Book có id bằng id được truyền vào nhưng sẽ chuyển vào 1 query set
    reviews = book.review_set.all()
    if reviews is not None:
        book_rating = average_rating([rev.rating for rev in reviews])
        context = {'book': book, 'book_rating': book_rating, 'reviews': reviews}
    else:
        context = {'book': book, 'book_rating': None, 'reviews': reviews}

    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get("viewed_books", [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session["viewed_books"] = viewed_books
    return render(request, 'reviews/review_detail.html', context)

# @permission_required('edit_publisher') #Cách 1


def is_staff_user(user): #Cách 2
    return user.is_staff


@user_passes_test(is_staff_user)
def publisher_edit(request, pk=None):
    if pk:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            # Nếu publisher đã tồn tại thực hiện save tương đương với cập nhật thông tin mới
            # Nếu publisher chưa tồn tại thực hiện save sẽ tạo ra 1 bản ghi mới và trả về đường dẫn ở redirect khi đó publisher_edit lại dc chạy 1 lần nữa
            if publisher is None:
                messages.success(request, "Publisher {} was created.".format(updated_publisher))
            else:
                messages.success(request, "Publisher {} was updated.".format(updated_publisher))
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    instance = publisher
    model_type = "Publisher"
    return render(request, "instance-form.html", {"form": form, "instance": instance, "model_type": model_type})


@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)
# Tham số False ngăn lưu trực tiếp vào database mà chỉ tạo ra 1 đối tượng updated_review.
# Vì ở bước này các nội dung nhập cần phải đi qua các điều kiện để xem thử là thêm mới hay là cập nhật
            updated_review.book = book
# gán book trong bảng review bằng đối tượng book có trùng id dù là cập nhật hay thêm mới review cũng đã có 1 đối tượng book đã được xác định
            if review:
                updated_review.date_edited = timezone.now() #Gán thời gian update bằng thời gian hiện tại
                messages.success(request, "Review for {} was updated.".format(updated_review.book))
            else:
                messages.success(request, "Review for {} was created.".format(updated_review.book))
            updated_review.save()
# Cần phải gọi phương thức save 1 lần nữa để lưu dữ liệu vào database
            return redirect("book_detail", book_pk)
# Thêm mới hay cập nhật review thành công đều trả về trang book_detail
    else:
        form = ReviewForm(instance=review)
    instance = review
    model_type = "Review"
    related_instance = book
    related_model_type = "Book"
    return render(request, "instance-form.html",
                  {"form": form, "instance": instance, "model_type": model_type, "related_instance": related_instance,
                   "related_model_type": related_model_type})


@login_required
def book_media(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    is_file_upload = True
    if request.method == "POST":
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(False)
            if form.cleaned_data.get("cover"):
                image = Image.open(form.cleaned_data['cover'])
                image.thumbnail((300, 300))
            book.save()
            messages.success(request, 'Book "{}" was successfully updated.'.format(book))
        return redirect("book_detail", book_pk)
    else:
        form = BookMediaForm(instance=book)
    return render(request, "instance-form.html", {"form": form, "instance": book, "model_type": "Book", "is_file_upload": is_file_upload})