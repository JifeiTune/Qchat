from django.db import models

#帖子
class Post(models.Model):
    #帖子ID
    postId=models.AutoField(primary_key=True)
    #发送者ID，外键
    userId=models.ForeignKey(to="User.User",to_field="userId",on_delete=models.CASCADE)
    #发送时间
    crTime=models.IntegerField()
    #标题
    head=models.CharField(max_length=20)
    #内容
    content=models.CharField(max_length=2000)
    #回复数
    repNum=models.IntegerField(default=0)
    #赞数
    prNum=models.IntegerField(default=0)
    #踩数
    ctrNum=models.IntegerField(default=0)
    #浏览数
    readNum=models.IntegerField(default=0)
    def __str__(self):
        return 'User: '+self.head[0:10]+"……"

#帖子的赞与踩
class JudgeOfPost(models.Model):
    #帖子ID号，外键
    postId = models.ForeignKey(to="Post", to_field="postId", on_delete=models.CASCADE)
    #用户ID，外键
    userId = models.ForeignKey(to="User.User", to_field="userId", on_delete=models.CASCADE)
    #是否是赞（否则是踩）
    isPr=models.BooleanField(default=True)

#回复
class Reply(models.Model):
    #回复ID
    replyId=models.AutoField(primary_key=True)
    #发送者ID，外键
    userId = models.ForeignKey(to="User.User", to_field="userId", on_delete=models.DO_NOTHING,related_name="Mfrom")
    #接收者ID，外键
    revId = models.ForeignKey(to="User.User", to_field="userId", on_delete=models.DO_NOTHING,related_name="Mto")
    #发送时间
    crTime = models.IntegerField()
    #内容
    content = models.CharField(max_length=2000)
    #赞数
    prNum = models.IntegerField(default=0)
    #踩数
    ctrNum = models.IntegerField(default=0)
    #浏览数
    readNum = models.IntegerField(default=0)

    def __str__(self):
        return 'User: '+self.content[0:10]+"……"

#回复的赞与踩
class JudgeOfReply(models.Model):
    #回复ID，外键
    ReplyId = models.ForeignKey(to="Reply", to_field="replyId", on_delete=models.CASCADE)
    #用户ID，外键
    userId = models.ForeignKey(to="User.User", to_field="userId", on_delete=models.CASCADE)
    #是否是赞（否则是踩）
    isPr=models.BooleanField(default=True)

#帖子与回复的关联
class ReplyOfPost(models.Model):
    postId=models.ForeignKey(to="Post",to_field="postId",on_delete=models.CASCADE,related_name="post")
    replyId=models.ForeignKey(to="Reply",to_field="replyId",on_delete=models.CASCADE,related_name="reply")

    def __str__(self):
        return 'Post: '+str(self.postId)+", Reply: "+str(self.replyId)

