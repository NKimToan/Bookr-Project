from django.db import models
from django.contrib import auth


# Create your models here.
# Nhà xuất bản
class Publisher(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="The name of the Publisher."
    )
    website = models.URLField(
        help_text="The Publisher's website."
    )
    email = models.EmailField(
        help_text="The Publisher's email address."
    )

    def __str__(self):
        return self.name

# Người đóng góp
class Contributor(models.Model):
    first_names = models.CharField(
        max_length=50,
        help_text="The contributor's last name or names."
    )
    last_names = models.CharField(
        max_length=50,
        help_text="The contributor's last name or names."
    )
    email = models.EmailField(
        help_text="The contact email for the contributor."
    )

    def initialled_name(self):
        first_name = ""
        for name in self.first_names.split(" "):
            first_name += name[0]
        return f"{self.last_names}, {first_name}"
    # Hàm str gọi lại phương thức initialled_name
    def __str__(self):
        return self.initialled_name()

    # def __str__(self):
    #     return self.first_names

# Sách
class Book(models.Model):
    title = models.CharField(
        max_length=70,
        help_text="The title of the book."
    )
    publication_date = models.DateField(
        verbose_name="Date the book was published."
    )
    isbn = models.CharField(
        max_length=20,
        verbose_name="ISBN number of the book."
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE
    )
    contributors = models.ManyToManyField(
        'Contributor',
        through="BookContributor"
    )
    cover = models.ImageField(
        null=True,
        upload_to="book_covers/"
    )
    sample = models.FileField(
        null=True,
        upload_to='book_samples/'
    )

    def __str__(self):
        return "{} ({})".format(self.title, self.isbn)
        # return f'{self.title},{self.isbn}'

# Người tham gia viết sách
class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co_Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE
    )
    # contributor = models.ForeignKey(
    #     Contributor,
    #     on_delete=models.PROTECT
    # )
    role = models.CharField(
        verbose_name="The role this contributor had in the book.",
        choices=ContributionRole.choices, max_length=20
    )

# Review
class Review(models.Model):
    content = models.TextField(
        help_text="The Review text."
    )
    rating = models.IntegerField(
        help_text="The rating the reviewer has given."
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the review was created."
    )
    date_edited = models.DateTimeField(
        null=True,
        help_text="The date and time the review was last edited."
    )
    creator = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        help_text="The Book that this review is for."
    )

    # def __str__(self):
    #     return self.content
