from datetime import datetime
from PIL import Image
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.contrib.auth.models import User
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
datetime.strptime('2014-12-04', '%Y-%m-%d').date()


class Home_contents(models.Model):
    # company info
    title = models.CharField(
        'Title', max_length=200, default='', blank=True, null=False)
    image = models.ImageField(default='default.png',
                              upload_to='home_contents_pics')
    content = models.TextField(
        'Content', default='', blank=True, null=False)
    created_at = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, blank=True, null=True)

    # def __str__(self):
    #     return f'{self.title}'


class Home_slides(models.Model):
    image = models.ImageField(default='default.png',
                              upload_to='home_slides_pics')
    slogan1 = models.CharField(
        'Slogan 1', max_length=200, default='', blank=True, null=False)
    slogan2 = models.CharField(
        'Slogan 2', max_length=200, default='', blank=True, null=False)
    data_index = models.CharField(
        'Data index', max_length=255, default='', blank=True, null=False)
    created_at = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.slogan1}'


class Partners(models.Model):
    name = models.CharField(
        'Name', max_length=200, default='', blank=True, null=False)
    image = models.ImageField(default='default.png',
                              upload_to='partners_pics')
    description = models.TextField(
        'Description', max_length=1000, default='', blank=True, null=False)
    link = models.CharField(
        'Link', max_length=255, default='', blank=True, null=False)
    created_at = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    # def save(self):
    #     super().save()
    #     img = Image.open(self.image.path)
    #     if img.height > 120 or img.width > 120:
    #         output_size = (120, 120)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Services(models.Model):
    name = models.CharField(
        'Name', max_length=200, default='', blank=True, null=False)
    image = models.ImageField(default='default.png',
                              upload_to='Services_pics')
    description = models.TextField(
        'Description', max_length=1000, default='', blank=True, null=False)
    created_at = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    # def save(self):
    #     super().save()
    #     img = Image.open(self.image.path)
    #     if img.height > 370 or img.width > 231:
    #         output_size = (370,231)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Teams(models.Model):
    name = models.CharField(
        'Name', max_length=200, default='', blank=True, null=False)
    occupation = models.CharField(
        'Occupation', max_length=200, default='', blank=True, null=False)
    image = models.ImageField(default='default.png',
                              upload_to='Team_pics')
    facebook = models.CharField(
        'Facebook', max_length=1000, default='', blank=True, null=False)
    twitter = models.CharField(
        'Twitter', max_length=1000, default='', blank=True, null=False)
    instagram = models.CharField(
        'Instagram', max_length=1000, default='', blank=True, null=False)
    created_at = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 182 or img.width > 182:
            output_size = (182, 182)
            img.thumbnail(output_size)
        else:
            output_size = (182, 182)
            img.thumbnail(output_size)
        img.save(self.image.path)


class Careers(models.Model):
    title = models.CharField(
        'Title', max_length=200, default='', blank=True, null=False)
    summary = models.TextField(
        'Job Summary', max_length=1000, default='', blank=True, null=False)
    generalConditions = models.TextField(
        'General Conditions', max_length=10000, default='', blank=True, null=False)
    location = models.CharField(
        'Location', max_length=100, default='', blank=True, null=False)
    salary = models.CharField(
        'Salary', max_length=50, default='', blank=True, null=False)
    deadline = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    remark = models.CharField(
        'Remark', max_length=100, default='', blank=True, null=False)
    status = models.IntegerField(
        'Status', default='', blank=True, null=False)
    created_at = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class CareerExperience(models.Model):
    career = models.ForeignKey(Careers, on_delete=models.CASCADE)
    experience = models.TextField(
        'Experience', max_length=1000, default='', blank=True, null=False)

    def __str__(self):
        return f'{self.career}'


class CareerDuties(models.Model):
    career = models.ForeignKey(Careers, on_delete=models.CASCADE)
    dutiesResposibilities = models.TextField(
        'Experience', max_length=1000, default='', blank=True, null=False)

    def __str__(self):
        return f'{self.career}'

class Events(models.Model):
    # company info
    title = models.CharField(
        'Title', max_length=500, default='', blank=True, null=False)
    image1 = models.ImageField(upload_to='Events_pics')
    image2 = models.ImageField(upload_to='Events_pics')
    image3 = models.ImageField(upload_to='Events_pics')
    image4 = models.ImageField(upload_to='Events_pics')
    created_at = models.DateField(
        auto_now_add=False, auto_now=True, blank=True, null=True)
    def __str__(self):
        return f'{self.title}'
    
class JobApplications(models.Model):
    career_title = models.CharField(
        'Career title', max_length=250, default='', blank=True, null=False)
    fullname = models.CharField(
        'Full Name', max_length=150, default='', blank=True, null=False)
    email = models.CharField(
        'Email', max_length=150, default='', blank=True, null=False)
    phone_number = models.CharField(
        'Phone Number', max_length=30, default='', blank=True, null=False)
    personal_info = models.TextField(
        'Personal Information', max_length=5000, default='', blank=True, null=False)
    education = models.TextField(
        'Your Education', max_length=5000, default='', blank=True, null=False)
    experience = models.TextField(
        'Work Experience', max_length=500, default='', blank=True, null=False)
    resume = models.FileField('Upload Resume/CV',
                              upload_to='Application_cv')
    letter = models.FileField('Upload Cover Letter',
                              upload_to='Application_letters')
    applied_on = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)


class Kikundi(models.Model):
    namba_yakikundi = models.CharField(
        'Namba ya usajili wa kikundi', max_length=50, default='', blank=True, null=False)
    jina_laKikundi = models.CharField(
        'Jina la kikundi', max_length=150, default='', blank=True, null=False)

    def __str__(self):
        return f'{self.namba_yakikundi}'


class Farmers(models.Model):
    namba_yakikundi = models.ForeignKey(Kikundi, on_delete=models.CASCADE)
    jina = models.CharField(
        'Jina kamili', max_length=150, default='', blank=True, null=False)
    namba_yasimu = models.CharField(
        'Namba ya simu', max_length=15, default='', blank=True, null=False)
    mkoa = models.CharField(
        'Mkoa', max_length=150, default='', blank=True, null=False)
    wilaya = models.CharField(
        'Wilaya', max_length=100, default='', blank=True, null=False)
    kata = models.CharField(
        'Kata', max_length=150, default='', blank=True, null=False)
    kijiji = models.CharField(
        'Kijiji', max_length=100, default='', blank=True, null=False)
    kitongoji = models.CharField(
        'Kitongoji', max_length=80, default='', blank=True, null=False)
    zao = models.CharField(
        'Zao', max_length=80, default='', blank=True, null=True)
    aina_yaKilimo = models.CharField(
        'Aina ya kilimo', max_length=80, default='', blank=True, null=True)
    ukubwa_washamba = models.CharField(
        'Ukubwa wa shamba', max_length=50, default='', blank=True, null=True)
    kiasi_chambegu = models.CharField(
        'Kiasi cha mbegu kinachohitajika', max_length=50, default='', blank=True, null=True)
    aina_yaudongo = models.CharField(
        'Aina ya udongo', max_length=100, default='', blank=True, null=True)
    
    location = models.CharField(max_length=200, null=True),
    tarehe = models.DateField(
        auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'{self.jina}'

class TaarifaZaShamba(models.Model):
    tarehe = models.DateField(auto_now_add=False, auto_now=True)
    mkulima = models.CharField(max_length=50, default='', blank=True, null=True)
    kuandaa_shamba = models.DateField('Kuandaa Shamba (Tarehe)',auto_now_add=False, auto_now=False, null=True)
    kupanda = models.DateField('Kupanda (Tarehe)',auto_now_add=False, auto_now=False, null=True)
    hari_ya_shamba = models.CharField('Hari Ya Shamba (Maelezo)',max_length=200, null=True)
    hari_ya_hewa = models.CharField('Hari Ya Hewa (Maelezo)',max_length=200, null=True)
    mabadiriko = models.CharField('Mabadiriko (Maelezo)',max_length=200, null=True)
    mavuno = models.CharField('Mavuno', max_length=50, default='', blank=True, null=True)
    maoni =   models.CharField(
        'Maoni', max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return f'{self.tarehe}'


class ViongoziWaKikundi(models.Model):
    namba_yakikundi = models.ForeignKey(Kikundi, on_delete=models.CASCADE)
    jina = models.CharField(
        'Jina la kiongozi wa 1', max_length=150, default='', blank=True, null=False)
    namba_yaNida = models.CharField(
        'Namba ya NIDA', max_length=20, default='', blank=True, null=False)
    cheo = models.CharField(
        'Cheo', max_length=100, default='', blank=True, null=False)
    simu = models.CharField(
        'Namba ya simu', max_length=100, default='', blank=True, null=False)

    jina2 = models.CharField(
        'Jina la kiongozi wa 2', max_length=150, default='', blank=True, null=False)
    namba_yaNida2 = models.CharField(
        'Namba ya NIDA', max_length=20, default='', blank=True, null=False)
    cheo2 = models.CharField(
        'Cheo', max_length=100, default='', blank=True, null=False)
    simu2 = models.CharField(
        'Namba ya simu', max_length=100, default='', blank=True, null=False)

    jina3 = models.CharField(
        'Jina la kiongozi wa 3', max_length=150, default='', blank=True, null=False)
    namba_yaNida3 = models.CharField(
        'Namba ya NIDA', max_length=20, default='', blank=True, null=False)
    cheo3 = models.CharField(
        'Cheo', max_length=100, default='', blank=True, null=False)
    simu3 = models.CharField(
        'Namba ya simu', max_length=100, default='', blank=True, null=False)

    jina4 = models.CharField(
        'Jina la kiongozi wa 4', max_length=150, default='', blank=True, null=False)
    namba_yaNida4 = models.CharField(
        'Namba ya NIDA', max_length=20, default='', blank=True, null=False)
    cheo4 = models.CharField(
        'Cheo', max_length=100, default='', blank=True, null=False)
    simu4 = models.CharField(
        'Namba ya simu', max_length=100, default='', blank=True, null=False)

    def __str__(self):
        return f'{self.namba_yakikundi}'


class AboutUs(models.Model):
    image = models.ImageField(default='default.png',
                              upload_to='About_pics')
    overview = models.TextField(
        'Overview', max_length=1000, default='', blank=True, null=False)
    vision = models.TextField(
        'Vision', max_length=1000, default='', blank=True, null=False)
    mission = models.TextField(
        'Mission', max_length=1000, default='', blank=True, null=False)
    created_at = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, blank=True, null=True)

