from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager



class TrixUserManager(BaseUserManager):
 
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=TrixUserManager.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    The Trix user model.
    """
    is_active = models.BooleanField(default=True,
            verbose_name=_('Is active?'),
            help_text=_('User is active? Inactive users can not log in.'))

    is_admin = models.BooleanField(default=False,
            verbose_name=_('Is admin?'),
            help_text=_('User is admin? Admins have full access to the admin UI.'))

    email = models.EmailField(max_length=250, blank=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = TrixUserManager()


    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


    def __unicode__(self):
        return self.displayname

    def get_short_name(self):
        return self.displayname

    @property
    def displayname(self):
        """
        Get a name for the user. Use this whenever you show the user in the UI.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?

        We do not use the permission system, so we answer YES.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?

        We do not use the permission system, so we answer YES.
        """
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        return self.is_admin

    @property
    def is_superuser(self):
        """
        Is the user a superuser?
        """
        return self.is_admin



class Tag(models.Model):
    """
    A tag for an assignment.
    """

    # NOTE: Help and field size in UI must make users use short tags
    tag = models.CharField(
        unique=True,
        max_length=30)

    category = models.CharField(
        max_length=1,
        blank=True, null=False,
        default='',
        choices=[
            ('', _('No category')),
            ('c', _('Course')),
            ('p', _('Period')),
        ]
    )


class Course(models.Model):
    """
    A course is simply a tag with an optional active period tag, and a list of admins.
    """
    admins = models.ManyToManyField(User)

    #: TODO: Limit choices to ``c``-tags
    course_tag = models.ForeignKey(Tag, related_name='course_set')

    #: TODO: Limit choices to ``p``-tags
    active_period = models.ForeignKey(Tag, related_name='active_period_set',
        null=True, blank=True)



class Assignment(models.Model):
    unique_string = models.CharField(max_length=255,
        unique=True, blank=False, null=False)

    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    text = models.TextField()
    solution = models.TextField()



class Permalink(models.Model):
    unique_string = models.CharField(max_length=255,
        unique=True, blank=False, null=False)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=255,
        blank=True, null=False, default='')
    description = models.TextField(
        blank=True, null=False, default='')