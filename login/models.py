from django.db import models
from django.contrib.auth.models import User
import datetime
import Levenshtein as L
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/")


class Session(models.Model): #date, browser_family, browser_version, ip, device, system_family, system_version
    date = models.DateTimeField() #mobile, tablet, touch_capable, pc, bot
    browser_family = models.TextField() # request.user_agent.browser.family
    browser_version = models.TextField() # request.user_agent.browser.version_string
    ip = models.GenericIPAddressField() #request.REMOTE_ADDR #for comparison check only theese last ip's numbers
    ##Below fields can't change from machine to machine
    device = models.TextField() # request.user_agent.device.family
    system_family = models.TextField() # request.user_agent.os.family
    system_version = models.TextField() # request.user_agent.os.version_string
    mobile = models.BooleanField() #request.user_agent.is_mobile
    tablet = models.BooleanField() #request.user_agent.is_tablet
    touch_capable = models.BooleanField() #request.user_agent.is_touch_capable
    pc = models.BooleanField() #request.user_agent.is_pc
    bot = models.BooleanField() #request.user_agent.is_bot
    #META['APPDATA']
    #META['COMPUTERNAME']
    #META['DRIVERDATA']
    ##other meta
    meta = models.TextField()




##RETURNS AVATAR URL
def getAvatar(usr):
    return UserProfile.objects.get(user=usr).avatar.url

##FINDS SESSION FROM COOKIES



def CreateSession(request):
    date = datetime.datetime.today()
    browser_family = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    ip = request.META['REMOTE_ADDR']
    device = request.user_agent.device.family
    os_family = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    mobile = request.user_agent.is_mobile
    tablet = request.user_agent.is_tablet
    touch = request.user_agent.is_touch_capable
    pc = request.user_agent.is_pc
    bot = request.user_agent.is_bot
    meta = ''
    try:
        meta = request.META['CSRF_COOKIE']
    except:
        pass
    sess = Session.objects.get_or_create(
        date=date, browser_family=browser_family, browser_version=browser_version, ip=ip, device=device, system_family=os_family,
        system_version=os_version, mobile=mobile, tablet=tablet, touch_capable=touch, pc=pc, bot=bot, meta=meta
    )
    return sess



def sessRatio(s1, s2):
    ratio = L.seqratio([s1.browser_family, s1.device, s1.os_family, s1.os_version, s1.ip, s1.browser_version],
                      [s2.browser_family, s2.device, s2.os_family, s2.os_version, s2.ip, s2.browser_version])
    ratio += boolRatio(s1.mobile==s2.mobile, s1.tablet==s2.tablet, s1.touch==s2.touch, s1.pc==s2.pc, s1.bot==s2.bot)
    if(len(s1.meta)>0 and len(s2.meta)>0):
        ratio += L.ratio(s1.meta, s2.meta)
        ratio /= 3
    else:
        ratio /= 2
    return ratio


def boolRatio(b1, b2, b3, b4, b5):
    dist = 0
    if(b1):
        dist+=1
    if(b2):
        dist+=1
    if(b3):
        dist+=1
    if(b4):
        dist+=1
    if(b5):
        dist+=1
    return dist/5
