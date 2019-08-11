import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# guoxiaonao error + 4
from message.models import Message
from tools.loging_decorator import loging_check, get_user_by_request
from topic.models import Topic
from user.models import UserProfile


@loging_check("POST", "DELETE")
def topics(request, author_id=None):
    # /v1/topcis/<author_id>
    if request.method == "POST":
        #发表博客 注：发表博客必须为登录状态
        #当前token中认证通过的用户 即为 作者
        author = request.user

        #拿数据
        json_str = request.body
        if not json_str:
            #判断字符串是否为空
            result = {'code':302, 'error': 'Please give me json '}
            return JsonResponse(result)

        #把json串反序列化成python对象
        json_obj = json.loads(json_str)
        title = json_obj.get('title')
        #带全部样式的文章内容 - content，如加粗，颜色等
        content = json_obj.get('content')
        #纯文本的文章内容 - content_text 用来做introduce的截取
        content_text = json_obj.get('content_text')
        #根据content_text的内容 生成 文章简介
        introduce = content_text[:30]
        #文章权限 public or private
        limit = json_obj.get('limit')
        if limit not in ['public', 'private']:
            #判断权限是否合法
            result = {'code': 303, 'error': 'Please give me right limit !'}
            return JsonResponse(result)
        #文章种类  tec - 技术类   no-tec - 非技术类
        category = json_obj.get('category')
        if category not in ['tec', 'no-tec']:
            result = {'code': 304, 'error': 'Please give me right category !'}
            return JsonResponse(result)
        #设置创建时间/修改时间
        now = datetime.datetime.now()

        #存储topic
        Topic.objects.create(title=title, content=content,limit=limit, category=category,author=author,created_time=now,modified_time=now,introduce=introduce)

        result = {'code':200, 'username':author.username}
        return JsonResponse(result)

    elif request.method == 'DELETE':
        #删除博主的博客文章
        author = request.user
        if author.username != author_id:
            result = {'code':306, 'error':'You can not do it !'}
            return JsonResponse(result)
        #当token中用户名和 url中的author_id严格一致时；方可执行删除

        topic_id = request.GET.get('topic_id')
        if not topic_id:
            result = {'code':307, 'error': 'You can not do it !! '}
            return JsonResponse(result)
        #查询欲删除的topic
        try:
            topic = Topic.objects.get(id=topic_id)
        except Exception as e:
            #如果当前topic不存在，则返回异常
            print('topic delete error is %s'%(e))
            result = {'code':308, 'error': 'Your topic is not existed'}
            return JsonResponse(result)

        topic.delete()

        return JsonResponse({'code':200})

    elif request.method == 'GET':
        #/v1/topics/guoxiaonao
        #获取用户博客列表 or 具体博客内容【带?t_id=xx】
        #1,访问当前博客的 访问者 - visitor
        #2,当前博客的博主 - author
        authors = UserProfile.objects.filter(username=author_id)

        if not authors:
            result = {'code':305, 'error': 'The current author is not existed !'}
            return JsonResponse(result)
        #当前访问的博客的博主
        author = authors[0]

        visitor = get_user_by_request(request)
        visitor_username = None
        if visitor:
            visitor_username = visitor.username
        #对比两者的username是否一致，从而判断当前是否要取 private的博客

        #尝试获取t_id,如果有t_id则证明 当前请求是获取用户指定ID的博客内容
        #/v1/topics/guoxiaonao?t_id=1
        t_id = request.GET.get('t_id')
        if t_id:
            #取指定t_id的博客
            t_id = int(t_id)

            #博主访问自己博客的标记/True 则表明当前为 博主访问自己的博客 / False 陌生人访问当前博客
            is_self = False

            if visitor_username == author_id:
                #改变标记
                is_self = True

                #博主访问自己的博客
                try:
                    author_topic = Topic.objects.get(id=t_id)
                except Exception as e:
                    result = {'code': 309, 'error': 'No topic'}
                    return JsonResponse(result)
            else:
                try:
                    author_topic = Topic.objects.get(id=t_id, limit='public')
                except Exception as e:
                    result = {'code': 309, 'error': 'No topic'}
                    return JsonResponse(result)

            #生成具体返回
            res = make_topic_res(author, author_topic, is_self)
            return JsonResponse(res)

        else:
            #/v1/topics/guoxiaonao 用户全量的数据
            #/v1/topics/guoxiaonao?category=tec|no-tec
            category = request.GET.get('category')

            if category in ['tec', 'no-tec']:
                #判断category取值范围
                if visitor_username == author_id:
                    #博主在访问自己的博客, 此时获取用户全部权限的博客
                    author_topics = Topic.objects.filter(author_id=author_id,category=category)
                else:
                    #其他访问者在访问当前博客
                    author_topics = Topic.objects.filter(author_id=author_id, limit='public',category=category)
            else:
                #获取博主全部博客【判断权限】
                if visitor_username == author_id:
                    #博主在访问自己的博客, 此时获取用户全部权限的博客
                    author_topics = Topic.objects.filter(author_id=author_id)
                else:
                    #其他访问者在访问当前博客
                    author_topics = Topic.objects.filter(author_id=author_id, limit='public')

            res = make_topics_res(author, author_topics)
            return JsonResponse(res)


def make_topics_res(author, author_topics):

    res = {'code':200 , 'data': {}}
    topics_res = []
    for topic in  author_topics:
        d = {}
        d['id'] = topic.id
        d['title'] = topic.title
        d['category'] = topic.category
        d['created_time'] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
        d['introduce'] = topic.introduce
        d['author'] = author.nickname
        topics_res.append(d)
    res['data']['topics'] = topics_res
    res['data']['nickname'] = author.nickname
    return res


def make_topic_res(author, author_topic, is_self):
    '''
    生成具体博客内容的返回值
    :param author:
    :param author_topic:
    :return:
    '''
    if is_self:
        #博主访问自己的
        #next
        #取出ID大于当前博客ID的数据的第一个
        next_topic = Topic.objects.filter(id__gt=author_topic.id,author=author).first()
        #last
        #取出ID小于当前博客ID的数据的最后一个
        last_topic = Topic.objects.filter(id__lt=author_topic.id,author=author).last()
    else:
        #当前访问者不是当前访问博客的博主
        next_topic = Topic.objects.filter(id__gt=author_topic.id,limit='public',author=author).first()
        #取出ID小于当前博客ID的数据的最后一个
        last_topic = Topic.objects.filter(id__lt=author_topic.id,limit='public',author=author).last()

     # 判断下一个是否存在
    if next_topic:
        # 下一个博客内容的id
        next_id = next_topic.id
        # 下一个博客内容的title
        next_title = next_topic.title
    else:
        next_id = None
        next_title = None
    #原理同next
    if last_topic:
        last_id = last_topic.id
        last_title =last_topic.title
    else:
        last_id = None
        last_title = None


    #生成message返回结构
    #拿出所有该topic的message 并 按时间倒叙排序
    all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')
    # leve1_msg = {1:[m1,m2,m3], 3,:[m4,m5,m6]}
    # messages = [ma_1, mb_3, mc_5 ]
    msg_list = []
    #key：是留言id, value是[回复对象,回复对象]
    level1_msg = {} # 'aaa': []
    #全部留言及回复的数量
    m_count = 0
    for msg in all_messages:
        m_count += 1
        if msg.parent_message:
            #回复
            level1_msg.setdefault(msg.parent_message, [])
            level1_msg[msg.parent_message].append({'msg_id':msg.id,'publisher':msg.publisher.nickname,'publisher_avatar':str(msg.publisher.avatar), 'content':msg.content,'created_time':msg.created_time.strftime('%Y-%m-%d')})
        else:
            #留言
            msg_list.append({'id':msg.id, 'content':msg.content,'publisher':msg.publisher.nickname,'publisher_avatar': str(msg.publisher.avatar), 'created_time':msg.created_time.strftime('%Y-%m-%d'), 'reply':[]})

    #关联，将 留言和回复进行合并
    for m in msg_list:
        if m['id'] in level1_msg:
            m['reply'] = level1_msg[m['id']]

    result = {'code':200, 'data':{}}
    result['data']['nickname'] = author.nickname
    result['data']['title'] = author_topic.title
    result['data']['category'] = author_topic.category
    result['data']['created_time'] = author_topic.created_time.strftime('%Y-%m-%d')
    result['data']['content'] = author_topic.content
    result['data']['introduce'] = author_topic.introduce
    result['data']['author'] = author.nickname
    result['data']['next_id'] = next_id
    result['data']['next_title'] = next_title
    result['data']['last_id'] = last_id
    result['data']['last_title'] = last_title
    #暂时为假数据
    result['data']['messages'] = msg_list
    result['data']['messages_count'] = m_count
    return result
























    return JsonResponse({'code':200, 'data':'this is test'})

