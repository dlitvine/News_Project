
from news.models import Author, Category, Post, Comment, PostCategory
from django.contrib.auth.models import User

user1 = User.objects.create_user(username='user1')
user2 = User.objects.create_user(username='user2')
user3 = User.objects.create_user(username='user3')

auth1 = Author.objects.create(name='author1', user=user1)
auth2 = Author.objects.create(name='author2', user=user2)
auth3 = Author.objects.create(name='author3', user=user3)
auth4 = Author.objects.create(name='author4', user=user3)


Category.objects.create(category_name='events')
Category.objects.create(category_name='sport')
Category.objects.create(category_name='politics')
Category.objects.create(category_name='economics')

post1 = Post.objects.create(author=auth1, type='AR', title='Article1', text='Here is Article 1 content')
post2 = Post.objects.create(author=auth1, type='AR', title='Article2', text='Here is Article 2 content')
post3 = Post.objects.create(author=auth2, type='NW', title='News3', text='Here is News 3 content')

cat_events = Category.objects.get(category_name='events')
cat_sport = Category.objects.get(category_name='sport')
cat_politics = Category.objects.get(category_name='politics')
cat_economics = Category.objects.get(category_name='economics')

post1.category.add(cat_events)
post2.category.add(cat_sport)
post3.category.add(cat_politics)
post3.category.add(cat_economics)

comment1 = Comment.objects.create(user=user1, post=post1, title='comment1', text='super post 1')
comment2 = Comment.objects.create(user=user1, post=post1, title='comment2', text='super post 2')
comment3 = Comment.objects.create(user=user2, post=post2, title='comment3', text='super post 3')
comment4 = Comment.objects.create(user=user2, post=post2, title='comment4', text='super post 4')
comment5 = Comment.objects.create(user=user2, post=post3, title='comment5', text='super post 5')

post1.like()
post2.like()
post2.like()
post3.like()
post3.like()
auth1.update_rating()
auth2.update_rating()

# intermediate check

Author.objects.get(name='author1').rating

post1.like()
post2.like()
post1.like()
post1.dislike()
post3.dislike()

# intermediate check


Author.objects.get(name='author1').rating

auth1.update_rating()
auth2.update_rating()

# intermediate check


Author.objects.get(name='author1').rating

comment1.like()
comment2.like()
comment3.like()
comment4.like()
comment5.like()

auth1.update_rating()
auth2.update_rating()

best_author = Author.objects.all().order_by('-rating')[0]
best_post = Post.objects.all().order_by('-rating')[0]

print(f'Best author name is: {best_author.name}, his current rating is: {best_author.rating}')
print(f'Best post currently is {best_post.title}, its rating is {best_post.rating}, posted at {best_post.time}')
print (f'Here is the preview: {best_post.preview()}')

for comment in Comment.objects.filter(post=best_post):
    print(f'Comment posted {comment.time}, by {comment.user}, rated {comment.rating}')
    print(f'Comment content{comment.text}')