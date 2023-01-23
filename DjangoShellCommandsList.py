from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

# 1.  Создать двух пользователей (с помощью метода User.objects.create_user('username')).
User.objects.create_user(username='Foma_KINIAEV', password='b7#iHSQ%Fv')
User.objects.create_user(username='Yekaterina_ZUBKOVA', password='WklR6cb|Q{')

# 2.  Создать два объекта модели Author, связанные с пользователями.
Author.objects.create(user=User.objects.get(pk=1))
Author.objects.create(user=User.objects.get(username='Yekaterina_ZUBKOVA'))

# 3.  Добавить 4 категории в модель Category.
Category.objects.create(theme='Экономика')
Category.objects.create(theme='Политика')
Category.objects.create(theme='Технологии')
Category.objects.create(theme='Спорт')

# 4.  Добавить 2 статьи и 1 новость.
Post.objects.create(author=Author.objects.get(pk=1),
                    type='P',
                    title='Похудел на 50 кг.',
                    text='Началось все в 2018, фоток ДО практически нет, потому что когда ты выглядишь как свинота, '
                         'не очень хочется фоткаться. Есть пара шакальных фото ДО, уж извините,но там все видно. '
                         'Изначально мой вес колебался между 95 и 110 при росте 174(!!!). '
                         'На момент когда я все таки решился на этот отчаянный шаг, на весах светилась цифра - 98 кг. '
                         'Как худеть я понятия не имел, поэтому посерфив ютубы и интернеты, понял одно - '
                         'нужно меньше жраь и пить сладкого. С чего я и начал. Одним днем перестал есть все сладкое, '
                         'мучное, пить кофе и газировки с энергетиками(моя слабость). Первое время было трудно, '
                         'особенно с напитками, ибо пью я много, воду в себя заливал с большим трудом. '
                         'Пил только зеленый чай и воду/кефир.'
                    )
Post.objects.create(author=Author.objects.get(pk=2),
                    type='P',
                    title='Обзор ASUS ROG Flow X13: невозможный ноутбук?',
                    text='Без лукавства в предыдущем абзаце не обошлось: да, ROG Flow X13 действительно укомплектован '
                         'ноутбучной RTX 3080, только она во внешнем корпусе. Но и в самом лэптопе графика некислая: '
                         'встройка AMD Radeon Vega 8 и мобильная GTX 1650 Max-Q с 4 ГБ собственной памяти. '
                         'Получается уникальная штука: лёгкий и расторопный лэптоп для поездок, который без труда '
                         'превращается в мощную рабочую станцию для дома и офиса. И если вы подумали, что речь '
                         'про док-станцию, подключаемую через разъём Thunderbolt со всеми вытекающими ограничениями '
                         'и проблемами, то снова не угадали. Но обо всём по порядку.'
                    )
Post.objects.create(author=Author.objects.get(pk=2),
                    type='N',
                    title='Цена нефти Brent на бирже ICE превысила $89 за баррель впервые с 1 декабря 2022 года',
                    text='Стоимость фьючерса на нефть марки Brent с поставкой в марте 2023 года '
                         'на лондонской бирже ICE превысила $89 за баррель впервые с 1 декабря 2022 года, '
                         'свидетельствуют данные торгов. По данным на 19:12 мск, стоимость фьючерса Brent '
                         'росла на 1,67% - до $89,09 за баррель. К 19:40 мск цена Brent замедлила рост и находилась '
                         'на уровне $88,79 за баррель (+1,32%). В то же время фьючерс на нефть марки WTI с поставкой '
                         'в марте 2023 года рос на 0,98% - до $82,44 за баррель.'
                    )

# 5.  Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(post=Post.objects.get(pk=1), category=Category.objects.get(pk=4))
PostCategory.objects.create(post=Post.objects.get(pk=2), category=Category.objects.get(pk=3))
PostCategory.objects.create(post=Post.objects.get(pk=3), category=Category.objects.get(pk=1))
PostCategory.objects.create(post=Post.objects.get(pk=3), category=Category.objects.get(pk=2))

# 6.  Создать как минимум 4 комментария к разным объектам модели Post
#     (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(post=Post.objects.get(pk=1),
                       author=User.objects.get(pk=1),
                       text='Как вам моя трансформация?')
Comment.objects.create(post=Post.objects.get(pk=1),
                       author=User.objects.get(pk=2),
                       text='Не могу в это поверить!')
Comment.objects.create(post=Post.objects.get(pk=2),
                       author=User.objects.get(pk=1),
                       text='Проплаченный пост. Отписка!')
Comment.objects.create(post=Post.objects.get(pk=3),
                       author=User.objects.get(pk=1),
                       text='Никогда такого не было и вот опять...')
Comment.objects.create(post=Post.objects.get(pk=3),
                       author=User.objects.get(pk=2),
                       text='Тонко...')

# 7.  Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Post.objects.get(pk=1).like()
Post.objects.get(pk=1).like()
Post.objects.get(pk=1).dislike()
Post.objects.get(pk=1).like()
Post.objects.get(pk=2).like()
Post.objects.get(pk=3).dislike()
Post.objects.get(pk=3).dislike()
Post.objects.get(pk=3).dislike()
Post.objects.get(pk=3).dislike()
Comment.objects.get(pk=1).like()
Comment.objects.get(pk=1).dislike()
Comment.objects.get(pk=1).like()
Comment.objects.get(pk=2).like()
Comment.objects.get(pk=2).dislike()
Comment.objects.get(pk=3).like()
Comment.objects.get(pk=3).like()
Comment.objects.get(pk=3).like()
Comment.objects.get(pk=4).like()
Comment.objects.get(pk=4).like()

# 8.  Обновить рейтинги пользователей.
Author.objects.get(pk=1).update_rating()
Author.objects.get(pk=2).update_rating()

# 9.  Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
top_author = Author.objects.all().order_by('-_rating').values('user', '_rating')[0]
top_user = User.objects.get(pk=top_author["user"])
print(f'{top_user} is the most popular author with rating: {top_author["_rating"]}.')

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
#     основываясь на лайках/дислайках к этой статье.
Post.objects.order_by('-_rating').values('creation_date', 'author__user__username', '_rating', 'title')[0]
best_post = Post.objects.all().order_by('-_rating')[0]
best_post.preview()

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(post=best_post).values('creation_date', 'author__username', '_rating', 'text')
