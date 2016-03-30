from django.db import models
from django.utils.translation  import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse



class Runner(models.Model):
    # objects = models.Manager()
    # live = LiveManager()

    RUNTYPE = (
    ('LIVE', 'LIVE'),
    ('HISTORICAL', 'HISTORICAL'),
    )
    #unique identifiers
    runtype = models.CharField(help_text=_('live_or_historical'), choices=RUNTYPE, max_length=15, default='HISTORICAL')
    racedate = models.DateField(help_text=_('race date'),)
    racecoursename = models.CharField(help_text=_('racecourse'), max_length=35)
    racecourseid = models.IntegerField(help_text=_('racecourseid'),blank=True)
    racename = models.CharField(help_text=_('race name'), max_length=250)
    racetypehorse = models.CharField(help_text=_('entry type horse'),max_length=35)
    racetypeconditions = models.CharField(help_text=_('entry conditions'),max_length=35)
    racetypehs= models.CharField(help_text=_('handicap or stakes'),max_length=35)
    ages = models.CharField(help_text=_('entry type ages'),max_length=35)
    oldraceclass = models.CharField(help_text=_('old raceclass'),max_length=35)
    newraceclass = models.CharField(help_text=_('new raceclass'),max_length=35, blank=True)
    distance = models.FloatField(help_text=_('distance furlongs')) ##convert
    going = models.CharField(help_text=_('going'),max_length=35) #convert?
    norunners = models.SmallIntegerField(help_text=_('number of runners'),)
    horsename = models.CharField(help_text=_('horse name'),max_length=250)
    horseid = models.IntegerField(help_text=_('Horse id'),blank=True,default=None)
    sirename = models.CharField(help_text=_('sire name'),max_length=250)
    sireid = models.IntegerField(help_text=_('Sire id'),blank=True,default=None)
    trainername = models.CharField(help_text=_('trainer'),max_length=250)
    trainerid = models.IntegerField(help_text=_('Trainerid'),blank=True,default=None)
    jockeyname = models.CharField(help_text=_('jockey'),max_length=250)
    jockeyid = models.IntegerField(help_text=_('Jockey id'),blank=True,default=None)
    allowance = models.SmallIntegerField(help_text=_('jockey allowance'))
    finalpos = models.CharField(help_text=_('Final position'),max_length=5)
    lbw = models.FloatField(help_text=_('Beaten by L'),)
    winsp = models.FloatField(help_text=_('final starting price win'),) #may need to be converted
    winsppos = models.SmallIntegerField(help_text=_('rank final starting price'),)
    bfsp = models.DecimalField(help_text=_('Betfair SP win'),max_digits=6, decimal_places=2)
    bfpsp = models.DecimalField(help_text=_('Betfair SP place'),max_digits=6, decimal_places=2)
    fsratingrank = models.SmallIntegerField(help_text=_('FS Rating rank'),)
    fsrating = models.FloatField(help_text=_('FS Rating'),)
    fsraceno = models.CharField(help_text=_('distance'),max_length=250, unique=True)
    draw = models.SmallIntegerField(help_text=_('barrier'),)
    damname = models.CharField(help_text=_('Dam\'s name'),max_length=250, null=True)
    damid = models.IntegerField(help_text=_('Dam id'),blank=True,default=None)
    damsirename  = models.CharField(help_text=_('Dam\'s sire name'),max_length=250,null=True)
    damsireid = models.IntegerField(help_text=_('Dam sire id'),blank=True, default=None)
    ownerid = models.IntegerField(help_text=_('Owner id'),blank=True,default=None)
    racetime  = models.CharField(help_text=_('Race off time'),max_length=250,null=True)
    totalruns =  models.SmallIntegerField(help_text=_('total runs horse'))
    isplaced = models.NullBooleanField(help_text=_('Placed?'))
    isbfplaced= models.BooleanField(help_text=_('is Placed on Betfair?'))
    stats = JSONField(default={}) #aggregate trainerstats etc

    #snapshotid runnerid--> system_runner table
    class Meta:
        unique_together = ('racedate', 'horsename',)
        ordering = ('-racedate',)

class System(models.Model):

    def get_absolute_url(self):
        return reverse('system_detail', args=[str(self.id)])
    ##_systemtype = fs, custom, id
    SYSTEMTYPES = (
    ('tg', 'Trainglot'),
    ('mi', 'Metainvest'),
    ('custom', 'Custom'),
    ('other', 'Other'),
    )
    systemtype = models.CharField(help_text=_('type: '),choices=SYSTEMTYPES, default='tg',max_length=50)
    systemname =  models.CharField(help_text=_('system name'),max_length=50,unique=True) #2016-T-21T unique=true?
    snapshotid  = models.IntegerField()
    description= models.TextField(help_text=_('rationale'),null=True)
    isActive = models.BooleanField(help_text=_('is the system an active system?'))
    isTurf = models.BooleanField(help_text=_('turf only?'))
    exposure = ArrayField(models.CharField(max_length=500), help_text=_('exposure'),default ='{}')
    query = JSONField(default ='{}')
    rpquery = JSONField(default ='{}') #for alerts
    isLay = models.BooleanField(help_text=_('lay?'), default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    def __str__(self):
        return self.systemname

    class Meta:
        ordering = ('snapshotid',)


class SystemSnapshot(models.Model):
    SNAPSHOTTYPES = (
    ('LIVE', 'LIVE'),
    ('HISTORICAL', 'HISTORICAL'),
    )
    snapshottype = models.CharField(help_text=_('initial(historical/live) '),choices=SNAPSHOTTYPES, default='HISTORICAL',max_length=15)
    system = models.ForeignKey(System, related_name='systemsnapshot')
    runners = models.ManyToManyField(Runner)
    bluerows = JSONField(default ='{}')
    greenrows = JSONField(default ='{}')
    redrows = JSONField(default ='{}')
    yearcolorcounts = JSONField(default ='{}')
    yearstats = JSONField(default ='{}')
    stats = JSONField(default ='{}')
    bfwins = models.SmallIntegerField(default=None)
    bfruns = models.SmallIntegerField(default=None)
    winsr = models.FloatField(default=None)
    expectedwins= models.FloatField(default=None)
    a_e = models.FloatField(default=None)
    levelbspprofit= models.DecimalField(max_digits=10, decimal_places=2,default=None)
    levelbsprofitpc= models.FloatField(default=None)
    a_e_last50 = models.FloatField(default=None)
    archie_allruns= models.FloatField(default=None)
    expected_last50= models.FloatField(default=None)
    archie_last50= models.FloatField(default=None)
    last50wins= models.SmallIntegerField(default=None)
    last50pc= models.FloatField(default=None)
    last50str= models.CharField(max_length=250,default=None)
    last28daysruns=  models.SmallIntegerField(default=None)
    profit_last50= models.DecimalField(max_digits=10, decimal_places=2,default=None)
    longest_losing_streak=models.SmallIntegerField(default=None)
    average_losing_streak=models.FloatField(default=None)
    average_winning_streak=models.FloatField(default=None)
    red_rows_ct = models.SmallIntegerField(default=None)
    blue_rows_ct  = models.SmallIntegerField(default=None)
    green_rows_ct = models.SmallIntegerField(default=None)
    total_rows_ct = models.SmallIntegerField(default=None)
    red_rows_pc= models.FloatField(default=None)
    blue_rows_pc= models.FloatField(default=None)
    green_rows_pc= models.FloatField(default=None)
    individualrunners=  models.FloatField(default=None)
    uniquewinners=  models.FloatField(default=None)
    uniquewinnerstorunnerspc= models.FloatField(default=None)
    yearstats= JSONField(default ='{}')
    yearcolorcounts= JSONField(default ='{}')
    totalbackyears = models.SmallIntegerField(default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    
    class Meta:
        ordering = ('-levelbsprofitpc',)
        get_latest_by = 'created'
