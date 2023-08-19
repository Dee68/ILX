from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin
                                        )
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
import datetime


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise ValueError('User should have a username!')
        if email is None:
            raise ValueError('User should have an Email')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        if password is None:
            raise TypeError('Superuser should have a password!')
        user = self.create_user(username, email, password, **extra_fields)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=60,
        db_index=True
        )
    # is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    """User profile to extend the account profile
    """
    COUNTY_CHOICES = [
        ('CORK', 'CORK'),
        ('GALWAY', 'GALWAY'),
        ('DONEGAL', 'DONEGAL'),
        ('MAYO', 'MAYO'),
        ('KERRY', 'KERRY'),
        ('TIPPERARY', 'TIPPERARY'),
        ('CLARE', 'CLARE'),
        ('TYRONE', 'TYRONE'),
        ('ANTRIM', 'ANTRIM'),
        ('LIMERICK', 'LIMERICK'),
        ('ROSCOMMON', 'ROSCOMMON'),
        ('DOWN', 'DOWN'),
        ('WEXFORD', 'WEXFORD'),
        ('MEATH', 'MEATH'),
        ('LONDONDERRY', 'LONDONDERRY'),
        ('KILKENNY', 'KILKENNY'),
        ('WICKLOW', 'WICKLOW'),
        ('OFFALY', 'OFFALY'),
        ('CAVAN', 'CAVAN'),
        ('WATERFORD', 'WATERFORD'),
        ('WESTMEATH', 'WESTMEATH'),
        ('SLIGO', 'SLIGO'),
        ('LAOIS', 'LAOIS'),
        ('KILDARE', 'KILDARE'),
        ('FERMANAGH', 'FERMANAGH'),
        ('LEITRIM', 'LEITRIM'),
        ('ARMAGH', 'ARMAGH'),
        ('MONOGHAN', 'MONOGHAN'),
        ('LONGFORD', 'LONGFORD'),
        ('DUBLIN', 'DUBLIN'),
        ('CARLOW', 'CARLOW'),
        ('LOUTH', 'LOUTH'),
    ]

    CITIES_CHOICES = [
        ('Dublin','Dublin'),
        ('Finglas','Finglas'),
        ('Cork','Cork'),
        ('Tallaght', 'Tallaght'),
        ('Galway','Galway'),
        ('Limerick','Limerick'),
        ('Lucan','Lucan'),
        ('Waterford','Waterford'),
        ('Clondalkin','Clondalkin'),
        ('Drogheda','Drogheda'),
        ('Dún Dealgan','Dún Dealgan'),
        ('Swords','Swords'),
        ('Navan','Navan'),
        ('Blackrock','Blackrock'),
        ('Douglas','Douglas'),
        ('Ennis','Ennis'),
        ('Carlow','Carlow'),
        ('Dunleary','Dunleary'),
        ('Tralee','Tralee'),
        ('Ashtown','Ashtown'),
        ('Kilkenny','Kilkenny'),
        ('Port Laoise','Port Laoise'),
        ('Naas','Naas'),
        ('Baile Átha Luain','Baile Átha Luain'),
        ('Mullingar','Mullinger'),
        ('Celbridge','Celbridge'),
        ('Wexford','Wexford'),
        ('Letterkenny','Letterkenny'),
        ('Sligo','Sligo'),
        ('Ballincollig','Ballincollig'),
        ('Greystones','Greystones'),
        ('Rathfarnham','Rathfarnham'),
        ('Clonmel','Clonmel'),
        ('Carrigaline','Carrigaline'),
        ('Leixlip','Leixlip'),
        ('Tullamore','Tullamore'),
        ('Maigh Nuad','Maigh Nuad'),
        ('Killarney','Killarney'),
        ('Arklow','Arklow'),
        ('Glencullen','Glencullen'),
        ('Midleton','Midleton'),
        ('Cobh','Cobh'),
        ('Castlebar','Castlebar'),
        ('Enniscorthy','Enniscorthy'),
        ('Palmerston','Palmerston'),
        ('An Cabhán','An Cabhán'),
        ('Wicklow','Wicklow'),
        ('Tramore','Tramore'),
        ('Na Sceirí','Na Sceirí'),
        ('Longford','Longford'),
        ('Gorey','Gorey'),
        ('Athy','Athy'),
        ('Ráth Tó','Ráth Tó'),
        ('Rush','Rush'),
        ('Shannon','Shannon'),
        ('Nenagh','Nenagh'),
        ('Glanmire','Glanmire'),
        ('Tuam','Tuam'),
        ('New Ross','New Ross'),
        ('Dungarvan','Dungarvan'),
        ('Youghal','Youghal'),
        ('Thurles','Thurles'),
        ('Lusca','Lusca'),
        ('Monaghan','Monaghan'),
        ('Kildare','Kildare'),
        ('Donabate','Donabate'),
        ('Edenderry','Edenderry'),
        ('Clane','Clane'),
        ('Buncrana','Buncrana'),
        ('Carrigtohill','Carrigtohill'),
        ('Ballinasloe','Ballinasloe'),
        ('Fermoy','Fermoy'),
        ('Westport','Westport'),
        ('Kilcock','Kilcock'),
        ('Carrickmines','Carrickmines'),
        ('Ros Comáin','Ros Comáin'),
        ('Sallins','Sallins'),
        ('Passage West','Passage West'),
        ('Carrick-on-Suir','Carrick-on-Suir'),
        ('Dunboyne','Dunboyne'),
        ('Loughrea','Loughrea'),
        ('Blessington','Blessington'),
        ('Roscrea','Roscrea'),
        ('Carraig Mhachaire Rois','Carraig Mhachaire Rois'),
        ('Oranmore','Oranmore'),
        ('Tipperary','Tipperary'),
        ('Baile Átha Fhirdhia','Baile Átha Fhirdhia'),
        ('Kinsale','Kinsale'),
        ('Ballybofey','Ballybofey'),
        ('Listowel','Listowel'),
        ('Mountmellick','Mountmellick'),
        ('Tullow','Tullow'),
        ('Athenry','Athenry'),
        ('Rathcoole','Rathcoole'),
        ('Monasterevin','Monasterevin'),
        ('Kilcoole','Kilcoole'),
        ('Damhliag','Damhliag'),
        ('Gweedore','Gweedore'),
        ('Carrick on Shannon','Carrick on Shannon'),
        ('Dunshaughlin','Dunshaughlin'),
        ('Bandon','Bandon'),
        ('Mulhurddart','Mulhurddart'),
        ('Macroom','Macroom'),
        ('Mitchelstown','Mitchelstown'),
        ('Kilcullen','Kilcullen'),
        ('Claremorris','Claremorris'),
        ('Riverchapel','Riverchapel'),
        ('Castleblayney','Castleblayney'),
        ('Caher','Caher'),
        ('Courtown','Courtown'),
        ('Rathnew','Rathnew'),
        ('Stamullin','Stamullin'),
        ('Saggart','Saggart'),
        ('Delgany','Delgany'),
        ('Gort','Gort'),
        ('Cashel','Cashel'),
        ('Newtown Mount Kennedy','Newtown Mount Kennedy'),
        ('Ballinrobe','Ballinrobe'),
        ('Skibbereen','Skibbereen'),
        ('Togher','Togher'),
        ('An Móta','An Móta'),
        ('Kinnegad','Kinnegad'),
        ('Bantry','Bantry'),
        ('Kilrush','Kilrush'),
        ('Coill an Chollaigh','Coill an Chollaigh'),
        ('Ballyjamesduff','Ballyjamesduff'),
        ('Sixmilebridge','Sixmilebridge'),
        ('Donegal','Donegal'),
        ('Crosshaven','Crosshaven'),
        ('Blarney','Blarney'),
        ('Dún An Ri','Dún An Ri'),
        ('Castleisland','Castleisland'),
        ('Carndonagh','Carndonagh'),
        ('Thomastown','Thomastown'),
        ('Athboy','Athboy'),
        ('Ballyhaunis','Ballyhaunis'),
        ('Ballyshannon','Ballyshannon'),
        ('Killorglin','Killorglin'),
        ('Kenmare','Kenmare'),
        ('Clogherhead','Clogherhead'),
        ('Baltinglass','Baltinglass'),
        ('Castleconnell','Castleconnell'),
        ('Meathas Troim','Meathas Troim'),
        ('Leopardstown','Leopardstown'),
        ('Dingle','Dingle'),
        ('Abbeyfeale','Abbeyfeale'),
        ('Barna','Barna'),
        ('Castlerea','Castlerea'),
        ('Tobercurry','Tobercurry'),
        ('Bunclody','Bunclody'),
        ('Bundoran','Bundoran'),
        ('Templemore','Templemore'),
        ('Enniskerry','Enniskerry'),
        ('Baile Uí Mhatháin','Baile Uí Mhatháin'),
        ('Ballybunnion','Ballybunnion'),
        ('Cootehill','Cootehill'),
        ('Castlebridge','Castlebridge'),
        ('Ballivor','Ballivor'),
        ('Ballaghaderreen','Ballaghaderreen'),
        ('Dunmore East','Dunmore East'),
        ('Cloyne','Cloyne'),
        ('Newmarket on Fergus','Newmarket on Fergus'),
        ('Mountrath','Mountrath'),
        ('Abbeyleix','Abbeyleix'),
        ('Rathcormack','Rathcormack'),
        ('Banagher','Banagher'),
        ('Strandhill','Strandhill'),
        ('Portlaw','Portlaw'),
        ('Moycullen','Moycullen'),
        ('Kilmallock','Kilmallock'),
        ('Dunmanway','Dunmanway'),
        ('Lifford','Lifford'),
        ('Collooney','Collooney'),
        ('Derrinturn','Derrinturn'),
        ('Castlemartyr','Castlemartyr'),
        ('Tearmann Feichín','Tearmann Feichín'),
        ('Ballymote','Ballymote'),
        ('Portraine','Portraine'),
        ('Clifden','Clifden'),
        ('Caherconlish','Caherconlish'),
        ('Castledermot','Castledermot'),
        ('Graiguenamanagh','Graiguenamanagh'),
        ('Droichead Chaisleán Loiste','Droichead Chaisleán Loiste'),
        ('Manorhamilton','Manorhamilton'),
        ('Portumna','Portumna'),
        ('Rathkeale','Rathkeale'),
        ('Ardnacrusha','Ardnacrusha'),
        ('Belturbet','Belturbet'),
        ('Swinford','Swinford'),
        ('Moroe','Moroe'),
        ('Slane','Slane'),
        ('Ballysadare','Ballysadare'),
        ('Stradbally','Stradbally'),
        ('Watergrasshill','Watergrasshill'),
        ('Béal Átha Ghártha','Béal Átha Ghártha'),
        ('Foxford','Foxford'),
        ('Cill Bheagáin','Cill Bheagáin'),
        ('Killybegs','Killybegs'),
        ('Rathdowney','Rathdowney'),
        ('Kilpedder','Kilpedder'),
        ('Claregalway','Claregalway'),
        ('Ballybay','Ballybay'),
        ('Piltown','Piltown'),
        ('Dromiskin','Dromiskin'),
        ('Ferbane','Ferbane'),
        ('Athgarvan','Athgarvan'),
        ('Mooncoin','Mooncoin'),
        ('Dunglow','Dunglow'),
        ('Inishcrone','Inishcrone'),
        ('Askeaton','Askeaton'),
        ('Adare','Adare'),
        ('Baile an Ghearlánaigh','Baile an Ghearlánaigh'),
        ('Ballylynan','Ballylynan'),
        ('Raphoe','Raphoe'),
        ('Ballyragget','Ballyragget'),
        ('Newtown Cunningham','Newtown Cunningham'),
        ('Daingean','Daingean'),
        ('Kiltamagh','Kiltamagh'),
        ('Kilworth','Kilworth'),
        ('Crossmolina','Crossmolina'),
        ('Kilmacanoge','Kilmacanoge'),
        ('Cahersiveen','Cahersiveen'),
        ('Urlingford','Urlingford'),
        ('Kinlough','Kinlough'),
        ('Aghada','Aghada'),
        ('Kilmeage','Kilmeage'),
        ('Coolaney','Coolaney'),
        ('Headford','Headford'),
        ('Kilkee','Kilkee'),
        ('Buttevant','Buttevant'),
        ('Drommahane','Drommahane'),
        ('Roundwood','Roundwood'),
        ('Rathvilly','Rathvilly'),
        ('Borrisokane','Borrisokane'),
        ('Tinahely','Tinahely'),
        ('Kilcormac','Kilcormac'),
        ('Droim Lis','Droim Lis'),
        ('Béal an Átha Móir','Béal an Átha Móir'),
        ('Inishannon','Inishannon'),
        ('Killeagh','Killeagh'),
        ('Collann','Collann'),
        ('Ballymore Eustace','Ballymore Eustace'),
        ('Mohill','Mohill'),
        ('Patrickswell','Patrickswell'),
        ('Dunlavin','Dunlavin'),
        ('Milltown Malbay','Milltown Malbay'),
        ('Lisdoonvarna','Lisdoonvarna'),
        ('Passage East','Passage East'),
        ('Belgooly','Belgooly'),
        ('Clonee','Clonee'),
        ('Glenties','Glenties'),
        ('Gowran','Gowran'),
        ('Bruff','Bruff'),
        ('An Lios Breac','An Lios Breac'),
        ('Mount Bellew Bridge','Mount Bellew Bridge'),
        ('Craughwell','Craughwell'),
        ('Kilmacrenan','Kilmacrenan'),
        ('Ardfert','Ardfert'),
        ('Ballyconnell','Ballyconnell'),
        ('Bennettsbridge','Bennettsbridge'),
        ('Kinvarra','Kinvarra'),
        ('Avoca','Avoca'),
        ('Holycross','Holycross'),
        ('Cloonlara','Cloonlara'),
        ('Kildalkey','Kildalkey'),
        ('Emyvale','Emyvale'),
        ('Skull','Skull'),
        ('Calverstown','Calverstown'),
        ('Cappoquin','Cappoquin'),
        ('Johnstown Bridge','Johnstown Bridge'),
        ('Crinkill','Crinkill'),
        ('Borrisoleigh','Borrisoleigh'),
        ('Manorcunningham','Manorcunningham'),
        ('Tallanstown','Tallanstown'),
        ('Knockbridge','Knockbridge'),
        ('Carlanstown','Carlanstown'),
        ('Clonmellon','Clonmellon'),
        ('Tulla','Tulla'),
        ('Ladysbridge','Ladysbridge'),
        ('Kilmessan','Kilmessan'),
        ('Killenaule','Killenaule'),
        ('Pallaskenry','Pallaskenry'),
        ('Kilrane','Kilrane'),
        ('Shinrone','Shinrone'),
        ('Rosbercon','Rosbercon'),
        ('Cappamore','Cappamore'),
        ('Cloghjordan','Cloghjordan'),
        ('Glanworth','Glanworth'),
        ('Omeath','Omeath'),
        ('Pettigoe','Pettigoe'),
        ('Fahan','Fahan'),
        ('Bruree','Bruree'),
        ('Aherla','Aherla'),
        ('Naul','Naul'),
        ('Clonaslee','Clonaslee'),
        ('Kilkishen','Kilkishen'),
        ('Fieries','Fieries'),
        ('Crusheen','Crusheen'),
        ('Ballymurn','Ballymurn'),
        ('Ballycanew','Ballycanew'),
        ('Dromahair','Dromahair'),
        ('Mullinahone','Mullinahone'),
        ('Ballycotton','Ballycotton'),
        ('Rathmullan','Rathmullan'),
        ('Mountcharles','Mountcharles'),
        ('Ballinderreen','Ballinderreen'),
        ('Slieveroe','Slieveroe'),
        ('Bellanode','Bellanode'),
        ('Oldtown','Oldtown'),
        ('Drimoleague','Drimoleague'),
        ('Campile','Campile'),
        ('Ballinakill','Ballinakill'),
        ('Kilmihil','Kilmihil'),
        ('Garristown','Garristown'),
        ('Ballincar','Ballincar'),
        ('Ventry','Ventry'),
        ('Clondulane','Clondulane'),
        ('Rockcorry','Rockcorry'),
        ('Ármhach','Ármhach'),
        ('Ballybrittas','Ballybrittas'),
        ('Coolgreany','Coolgreany'),
        ('Fiddown','Fiddown'),
        ('Goresbridge','Goresbridge'),
        ('Kildorrery','Kildorrery'),
        ('Nobber','Nobber'),
        ('Cappagh White','Cappagh White'),
        ('Farran','Farran'),
        ('Riverstown','Riverstown'),
        ('Aglish','Aglish'),
        ('Ballintogher','Ballintogher'),
        ('Fedamore','Fedamore'),
        ('Newbliss','Newbliss'),
        ('Ballyporeen','Ballyporeen'),
        ('Ballylanders','Ballylanders'),
        ('Durrus','Durrus'),
        ('Emly','Emly'),
        ('Dunfanaghy','Dunfanaghy'),
        ('Kilronan','Kilronan'),
        ('Knockvicar Bridge','Knockvicar Bridge'),
        ('Myshall','Myshall'),
        ('Castlemagner','Castlemagner'),
        ('Inis Caoin','Inis Caoin'),
        ('Killavullen','Killavullen'),
        ('Tullaghan','Tullaghan'),
        ('Trim','Trim')
   ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default='firstname')
    last_name = models.CharField(max_length=20, default='lastname')
    street_address1 = models.CharField(blank=True, max_length=100, null=True)
    phone_number = models.CharField(blank=True, max_length=12)
    city = models.CharField(blank=True, max_length=30, null=True, choices=CITIES_CHOICES)
    county = models.CharField(
        blank=True,
        max_length=30,
        null=True,
        choices=COUNTY_CHOICES
        )
    postcode = models.CharField(blank=True, max_length=30)
    avatar = models.ImageField(blank=True, upload_to='profile_pics/', null=True)

    def image_tag(self):
        if self.avatar:
            return mark_safe(
                '<img src="%s" height="50" width="50">' % self.avatar.url
                )
        return "No image found"
    
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return f'Profile of {self.user.username}'
