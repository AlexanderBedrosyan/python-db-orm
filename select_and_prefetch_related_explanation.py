# Разликата между select_related и prefetch_related в Django е в начина, по който те зареждат свързаните данни от базата
# данни, и в ефективността на техните реализации.
#
# select_related
# select_related използва SQL JOIN за да зареди свързаните данни в една-единствена SQL заявка. Това е ефективно за
# ForeignKey и OneToOneField релации, тъй като обединява данните в едно запитване, което намалява броя на заявките към
# базата данни.
#
# Пример
# Имате модели Book и Author, където всяка книга има един автор:
#
# python
# Copy code
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
# Ако искате да вземете всички книги и техните автори, можете да използвате select_related:
#
# python
# Copy code
books = Book.objects.select_related('author').all()

for book in books:
    print(book.title, book.author.name)
# Това ще направи една SQL заявка, която ще включва JOIN за таблицата с авторите, и ще върне всички книги заедно с
# техните автори.
#
# prefetch_related
# prefetch_related прави отделни SQL заявки за основните и свързаните данни и след това "предзарежда" свързаните данни
# в паметта на Python. Това е полезно за ManyToManyField и reverse ForeignKey релации (т.е. свързани обекти,
# които не са директно свързани с текущия модел).
#
# Пример
# Имате модели Book и Tag, където всяка книга може да има множество тагове:
#
# python
# Copy code
class Tag(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
# Ако искате да вземете всички книги и техните тагове, можете да използвате prefetch_related:
#
# python
# Copy code
books = Book.objects.prefetch_related('tags').all()

for book in books:
    print(book.title)
    for tag in book.tags.all():
        print(tag.name)

# Това ще направи две SQL заявки: една за книгите и една за таговете, и след това ще свърже таговете с книгите в
# паметта.
#
# Сравнение
# select_related: Използва JOIN и прави една SQL заявка. Подходящ за ForeignKey и OneToOneField релации. Пример: Заявка
# за книги и техните автори.
# prefetch_related: Прави отделни SQL заявки и "предзарежда" данните в паметта. Подходящ за ManyToManyField и обратни
# ForeignKey релации. Пример: Заявка за книги и техните тагове.
# Заключение
# Използвайте select_related когато имате ForeignKey или OneToOneField релации и искате да намалите броя на заявките към
# базата данни чрез JOIN.
# Използвайте prefetch_related когато имате ManyToManyField или обратни ForeignKey релации и искате да "предзаредите"
# свързаните данни в отделни заявки.
# И двата метода могат значително да оптимизират производителността на вашето приложение, когато се използват правилно.