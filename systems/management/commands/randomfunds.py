import csv
import simplejson as json
from datetime import datetime
from datetime import date, timedelta as td
from django.db                   import transaction
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from systems                     import models as systemmodels
from funds                        import models    as fundmodels
from collections                 import defaultdict,Counter
from decimal import Decimal as D
from decimal import getcontext
from systems.fundaccounts import FundAccount,CashOutAccount, FundRunner, getstakespenalty
import pickle
import random

import sys
from django.db.utils import IntegrityError

# def create_dict_from_json(cls, data):

#     exc = ['id', '_state']
#     #7
#     obj = cls()
#     obj_dict = obj.__dict__

#     for field in exc:
#         del obj_dict[field]
#     for key in obj_dict:
#         obj_dict[key] = data.get(key)
#     return obj_dict

def place_winningbet(stakes, bfsp,stakespenalty,BETFAIRDEDUCTION):
    returns = stakes*bfsp
    # print("winning bfsp", bfsp)
    # print("returns", returns)
    # stakespenalty = getstakespenalty(bfsp, stakes)
    returns = returns*stakespenalty
    # print("stakespen", stakespenalty)
    # print("returns post stakes", returns)
    returns = returns*BETFAIRDEDUCTION
    return returns


def write_report(r, filename):
    with open(filename, "a") as input_file:
        print("---------------------", file=input_file)
        for k, v in r.items():
            line = '{}, {}'.format(k, v)
            print(line, file=input_file)

enco = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime)
    or isinstance(obj, date)
    else None
)



class Command( BaseCommand ):
    help = 'Import data'

    #get fund information

    # f1 = models.Fund.objects.first()
    # code = f1.code
    # description = f1.description
    # bettingratio  = f1.bettingratio
    # openingbank = f1.openingbank
    # managementfee = f1.managementfee
    # performancefee = f1.performancefee
    # performancethreshold = f1.performancethreshold
    explorative = False
    firstn = True
    
    fundname = 'TOP10 ACTIVE'
    description = "TOP 10 ACTIVE 2015 Full season 1000 No Stakes"
    bettingratio  = 0.05
    openingbank = D('1000.00')
    managementfee = D('0.05')
    bailoutfee = D('0.2')
    performancefee = D('0.10')
    performancethreshold = D('1.5')
    horses = Counter()
    winninghorses = Counter()
    stakescap = D('999.00')
   
    season = '2015'
    preselected = False
    SRATIO = 0.3
    TRATIO= 0.4
    JRATIO = 0.2
    MIRATIO = 0.1
    LRATIO = 0.0
    BETFAIRDEDUCTION = D('0.95')
    BASEFILE = description
    # fundname = 'A1'
    # description = "A1 2015 Full season 1000"
    # bettingratio  = 0.05
    # openingbank = D('1000.00')
    # managementfee = D('0.05')
    # bailoutfee = D('0.2')
    # performancefee = D('0.10')
    # performancethreshold = D('1.5')
    # horses = Counter()
    # winninghorses = Counter()
    # stakescap = D('50.00')
    # firstn = False
    # season = '2015'
    # preselected = True

    # 20130330 to 20131109
    # 20140329 to 20141108
    # 20150328 to 20151127
    #specific to test

    ##SEAONS 2013
    if season == '2013':
        STARTDATE = datetime.strptime('20130330',"%Y%m%d")
        seasonstart = STARTDATE.date()
        ENDDATE = datetime.strptime('20131109',"%Y%m%d")
    if season == '2014':
        STARTDATE = datetime.strptime('20140329',"%Y%m%d")
        seasonstart = STARTDATE.date()
        ENDDATE = datetime.strptime('20141108',"%Y%m%d")
    if season == '2015':
        STARTDATE = datetime.strptime('20150328',"%Y%m%d")
        seasonstart = STARTDATE.date()
        ENDDATE = datetime.strptime('20151127',"%Y%m%d")


    # BASEFILE = "A_" + str(NOSYSTEMS) + '_'+ 'firstn_' + 'sr_'+ str(SRATIO)+ 'tr_'+ str(TRATIO)+ 'MIr_'+ str(MIRATIO)+ 'jr_'+ str(JRATIO)+ '_'+ str(seasonstart)
    #SYSTEMS

    TOP_10ACTIVE = [
    '2016-S-04A',
    '2016-S-05A',
    '2016-S-06A',
    '2016-MI-S-02A',
    '2016-J-01A',
    '2016-J-04A',
    '2016-J-08A',
    '2016-S-08A',
    '2016-T-02A',
    '2016-J-05A'
     ]



    a1_sires = ["2016-S-02A","2016-S-03T","2016-S-06A", "2016-S-09T","2016-S-10A", "2016-S-11A", "2016-S-12T", "2016-S-13A","2016-S-14T", ]
    a1_jockeys = ["2016-J-03T","2016-J-04A", "2016-J-06T","2016-J-07A", "2016-J-09A"]
    a1_metainvest = ["2016-MI-S-01A","2016-MI-S-02A","2016-MI-O-01T","2016-MI-O-02A" ]
    a1_trainers = ["2016-T-17A","2016-T-20T","2016-T-02A"]

    sires = [
    '2016-S-01T','2016-S-02A', '2016-S-03T', '2016-S-04A', '2016-S-05A', '2016-S-06A',
    '2016-S-07T', '2016-S-08A', '2016-S-09T', '2016-S-10A', '2016-S-11A', '2016-S-12T',
    '2016-S-13A', '2016-S-14T']

    jockeys = ['2016-J-01T','2016-J-02T','2016-J-03T','2016-J-04A','2016-J-05A','2016-J-06T',
    '2016-J-07A','2016-J-08A','2016-J-09A','2016-J-10T']

    metainvest= ['2016-MI-S-01A','2016-MI-S-02A','2016-AW-01A','2016-AW-02A','2016-MI-AW-03A','2016-MI-O-01T','2016-MI-T-01T',
    '2016-MI-O-02A','2016-MI-O-03A']

    trainers = ['2016-T-01A','2016-T-02A','2016-T-03T','2016-T-04A','2016-T-05T','2016-T-06T','2016-T-07T','2016-T-08T',
    '2016-T-09A','2016-T-10A','2016-T-11A','2016-T-12T',
    '2016-T-13A', '2016-T-14T', '2016-T-15A','2016-T-16T', '2016-T-17A', '2016-T-18T', '2016-T-19T',
    '2016-T-20T','2016-T-21T']
    row_num = 0

    @transaction.atomic
    def handle( self, *args, **options ):
        # print("Trying out system combinations for: ")
        # print(self.code, self.description)
        # print(self.bettingratio, self.openingbank)
        if self.explorative:
            _s = int(self.SRATIO*self.NOSYSTEMS)+1
            _t = int(self.TRATIO*self.NOSYSTEMS)+1
            _j = int(self.JRATIO*self.NOSYSTEMS)+1
            _mi = int(self.MIRATIO*self.NOSYSTEMS)+1
            CANDIDATESYSTEMS = list() #members, winsr, etc..
            if self.preselected and self.fundname == 'A1':
                CANDIDATESYSTEMS.extend(self.a1_sires)
                CANDIDATESYSTEMS.extend(self.a1_jockeys)
                CANDIDATESYSTEMS.extend(self.a1_metainvest)
                CANDIDATESYSTEMS.extend(self.a1_trainers)
            else:
                if self.firstn:
                    CANDIDATESYSTEMS.extend(self.sires[:_s])
                    CANDIDATESYSTEMS.extend(self.trainers[:_t])
                    CANDIDATESYSTEMS.extend(self.jockeys[:_j])
                    CANDIDATESYSTEMS.extend(self.metainvest[:_mi])
                else:
                    CANDIDATESYSTEMS.extend(random.sample(self.sires, _s))
                    CANDIDATESYSTEMS.extend(random.sample(self.trainers, _t))
                    CANDIDATESYSTEMS.extend(random.sample(self.jockeys, _j))
                    CANDIDATESYSTEMS.extend(random.sample(self.metainvest, _mi))
        else:
            CANDIDATESYSTEMS = self.TOP_10ACTIVE
        # print(CANDIDATESYSTEMS)
        # BIGRUNNERS = list()
        rundict = defaultdict(list) #date as key dictionary as value
        systems = systemmodels.System.objects.filter(systemname__in=CANDIDATESYSTEMS)

        notdy_winners = notdy_losers = norunners = totalwinningprices = totalwinningbfprices = 0


        ##decimal precision
        getcontext().prec = 5
        ##DO FOR 2013, 2014
        mintime = datetime.min.time()
        for s in systems:
            #get runners for these systems
            snap= s.systemsnapshot.filter(snapshottype='HISTORICAL')[0]
            runners = snap.runners.get_queryset().values() #list of runners
            # print(runners)
            '''
            [{'horsename': 'Stormy Antarctic', 'newraceclass': '', 'fsrating': 92.4, 'trainername': 'Ed Walker', 'fsratingrank': 1, 'racecourseid': 0, 'racecoursename': 'Sandown',
            'norunners': 10, 'sirename': 'Stormy Atlantic(USA)', 'winsp': 1.75, 'runtype': 'HISTORICAL', 'id': 5411, 'isbfplaced': True,
            'racename': 'Invest AD/British Stallion Studs EBF Maiden Stakes Div 2', 'racetime': '16:05', 'oldraceclass': 'E', 'finalpos': '1',
            'racedate': datetime.date(2015, 8, 21), 'horseid': 0, 'fsraceno': '2015TH2104', 'bfsp': Decimal('2.96'), 'jockeyid': 0, 'racetypeconditions': '',
            'lbw': -2.25, 'winsppos': 1, 'sireid': 0, 'damname': 'Bea Remembered', 'ownerid': 0, 'racetypehorse': 'Mdn', 'distance': 7.0, 'isplaced': True,
            'going': 'GdSf', 'totalruns': 2, 'damsireid': 0, 'stats': {}, 'trainerid': 0, 'ages': '2yo', 'damid': 0, 'damsirename':
             'Doyen(IRE)', 'draw': 3, 'racetypehs': 'Stk', 'allowance': 0, 'jockeyname': 'Antonio Fresu', 'bfpsp': Decimal('1.41')},.....]
            '''
            #add to big list and sort
            for r in runners:
                # print(r)
                # _d = dict()

                _rd = r['racedate']
                _rdt = datetime.combine(_rd, mintime)
                _fsraceno = r['fsraceno'] #str
                _bfsp  = r['bfsp']
                hname = r['horsename']

                _winsp = r['winsp'] #float
                _finalpos = r["finalpos"]

                runner = FundRunner(racedatetime=_rdt, fsraceno=_fsraceno, bfsp=_bfsp, winsp=_winsp, finalpos=_finalpos, systemname=s.systemname, horsename=hname)
                # _d = {'racedatetime': _rdt, 'fsraceno': _fsraceno, 'bfsp': _bfsp, 'winsp': _winsp, 'finalpos': _finalpos, 'systemname': s.systemname }
                # rundict[_rdt].append(_d)
                rundict[_rd].append(runner)
        # print(rundict)
        #print in normal text file.
        # RS = sorted(rundict, key = lambda x: x["racedatetime"])
        # RS = sorted(rundict.items())
        # print(RS)
        # d = sorted(rundict.items(), key=lambda p: p[1], reverse=True)
        # with csv.writer(open('dict.csv', 'wb')) as csvfile:
        #     for key, value in RS.items():
        #         writer.writerow([key, value])


        # d = {k: sorted(v, key=k['racedatetime']) for k,v in rundict.items()}
        # writer = csv.writer(open('dict.csv', 'w'))
        # for key, value in RS:
        #     writer.writerow([key, value])
        #sort on racedatetime
        # sortedrundict = sorted(rundict, key=lambda p: p['racedatetime'])


        thesystems = [s.systemname for s in systems]
        # print(thesystems)
        startdate = self.STARTDATE
        enddate = self.ENDDATE
        delta = enddate- startdate
        #######################################

        fundaccount = FundAccount(
            stakescap = self.stakescap, description=self.description,
            currency='GBP', nosystems=len(systems), 
            jratio= self.JRATIO, tratio=self.TRATIO, miratio=self.MIRATIO, sratio=self.SRATIO, 
            fundname=self.fundname, initialbalance=self.openingbank, year=self.season


            )
        fundaccount.startdate = startdate
        fundaccount.enddate = enddate
        fundaccount.systems = thesystems

        #test
        cashoutaccount = CashOutAccount('A')

        # winpattern, individualrunners, uniquetdy_winners
        for i in range(delta.days + 1):
            # if i == 28:
            #     break

            _d = (startdate + td(days=i)).date()

            tdy_returns = D('0.00')
            tdy_cashedout = D('0.00')
            tdy_invested = D('0.00')
            tdy_netgains = D('0.00')
            tdy_winners = tdy_losers = tdy_bets = 0
            tdy_returns_list = list()
            tdy_invested_list = list()
            tdy_prices_list = list()
            tdy_places = ""
            tdy_sequences = ""
            tdy_pos = ""

            tdy_bfbalance_start = fundaccount.getbfbalance()
            fundaccount.bfstartdaybalances.append(tdy_bfbalance_start)
            #GET TODAYS RACES
            todaysraces = rundict[_d] #default dict list of runnerobjects
            print("the race", todaysraces)
            # assert(1==2)

            notdy_bets = len(todaysraces)
            print("notdy_bets", notdy_bets)
            print("bfbalance", tdy_bfbalance_start)
            if notdy_bets ==0:
                continue
            if tdy_bfbalance_start <= D('0'):
                break
            fundaccount.racedates.append(_d)

            ### BetControl class
            # betamounts = dict()
            # for b in todaysraces:
            #     betamounts.append(b.bfsp)
            # betamountssorted = sorted(betamounts, reverse=True)

            #sort todaysraces by bfsp


            todaysstakestobfsp = dict()
            todaysruns_sbfp = sorted(todaysraces, key=lambda p: p.bfsp)
            print([x.bfsp for x in todaysruns_sbfp])

            # assert(1==2)
            for r in todaysruns_sbfp:
                stakes = D('0.0')
                tdy_bets+=1
                fundaccount.nobets+=1
                stakes= fundaccount.getbfbalance()*D('0.05')
                print(fundaccount.getbfbalance())
                print("stakes", stakes)
                print("stakescap",self.stakescap)

                if stakes > self.stakescap:
                    diff = stakes - self.stakescap
                    fundaccount.add('bf',diff)
                    stakes = self.stakescap
                ##MAKE Investment
                fundaccount.subtract('bf',stakes)
                tdy_invested += stakes
                tdy_invested_list.append(stakes)
                print(fundaccount.getbfbalance())

                bfsp = r.bfsp
                winsp = r.winsp
                fpos = r.finalpos
                tdy_places += fpos + ','
                fundaccount.subtract('bf',stakes)
                tdy_prices_list.append(bfsp)
                todaysstakestobfsp[stakes] = bfsp
                winsp = r.winsp
                self.horses[r.horsename]+=1


                if fpos == '1':
                    print(r.horsename)
                    tdy_winners+=1
                    tdy_sequences += '1'
                    fundaccount.nowinners +=1
                    fundaccount.winpattern += '1'
                    self.winninghorses[r.horsename]+=1

                    #do returns after loop:
                    returns = place_winningbet(stakes, bfsp, getstakespenalty(bfsp, stakes),D(self.BETFAIRDEDUCTION))
                    tdy_returns_list.append(returns)
                    tdy_returns += returns
                    ##do not add to balance yet
                    print("returns post BF", returns)
                    # winningslessbf=returns
                    # winningslessbfstakes = returns
                    # fundaccount.winningreturns.append(returns)
                    #update balance
                    # fundaccount.add('bf',returns)
                    print("balancecheck", fundaccount.getbfbalance())
                else:
                    tdy_losers+=1
                    fundaccount.nolosers +=1
                    tdy_returns_list.append(D('0.00'))
                    fundaccount.winpattern +='0'
                    tdy_sequences += '0'

                    print("balancecheck", fundaccount.getbfbalance())

            print("todayinvested", tdy_invested)
            print("todaysinvested_list", tdy_invested_list)
            print("balancecheck", fundaccount.getbfbalance())
            # assert(2==1)
            #NOW ADD returns
            fundaccount.add('bf',tdy_returns)
            #tdy_bets DONE WHERE ARE WE?
            fundaccount.investments.append(tdy_invested_list)
            fundaccount.bfprices.append(tdy_prices_list)
            fundaccount.returns.append(tdy_returns)
            # tdy_places += tdy_places
            fundaccount.placepattern += tdy_places + '>'
            fundaccount.sequences+= tdy_sequences + '>'
            fundaccount.totalinvested += tdy_invested
            bfbalanceendofday = fundaccount.getbfbalance()
            print("tdy returns", tdy_returns)
            tdy_netgains = tdy_returns - tdy_invested
            print("net gains", tdy_netgains)
            ## TRACK BALANCES
            if bfbalanceendofday > fundaccount.maxbfbalance:
                maxbfbalance = bfbalanceendofday
            if bfbalanceendofday < fundaccount.minbfbalance:
                minbfbalance = bfbalanceendofday
            fundaccount.dailybfbalances.append(bfbalanceendofday)

            #####CASHOUT
            if bfbalanceendofday >= fundaccount.cashoutthreshold:
                tdy_cashedout = bfbalanceendofday - fundaccount.cashoutthreshold
                fundaccount.subtract('bf', tdy_cashedout)
                fundaccount.cashedoutbalance += tdy_cashedout
                cashoutaccount.add(tdy_cashedout)


            fundaccount.dailycashoutbalances.append(tdy_cashedout)
            bfbalanceendofday = fundaccount.getbfbalance()
            print("fundaccount.cashoutthreshold", fundaccount.cashoutthreshold)
            print("balancecheck", fundaccount.getbfbalance())
            fundaccount.bfenddaybalances.append(bfbalanceendofday)

            cashedoutbalance = cashoutaccount.getbalance()
            print("balancecheck-cashedout", cashedoutbalance)
            print("balancecheck-cashedout2", fundaccount.cashedoutbalance)
            #cashedout plus bfbalanceendofday
            fundaccount.bfcumtotalbalances.append(cashedoutbalance+bfbalanceendofday)
            # assert(1==2)
            _today = {
            'date': _d,
            'tdy_bfbalance_start': tdy_bfbalance_start,
            'tdy_betstoday': tdy_bets,
            'tdy_winnerstoday': tdy_winners,
            'tdy_loserstoday': tdy_losers,
            'investedtoday': tdy_invested,
            'tdy_invested_list': tdy_invested_list,
            'tdy_returns': tdy_returns,
            'tdy_returns_list': tdy_returns_list,
            'tdy_netgains': tdy_netgains,
            'bfbalanceendofday': bfbalanceendofday,
            'cashedouttoday': tdy_cashedout,
            'cashedoutbalance': cashedoutbalance,
            'totalbalanceinclcashout': bfbalanceendofday+cashedoutbalance
            }
            #print one record per line
            fieldnames = ['date', 'tdy_bfbalance_start', 'tdy_betstoday', 'tdy_winnerstoday', 'tdy_loserstoday', 'investedtoday', 'tdy_invested_list', 'tdy_returns', 'tdy_returns_list', 'tdy_netgains',\
            'bfbalanceendofday', 'cashedouttoday', 'cashedoutbalance','totalbalanceinclcashout']
            outfile = self.BASEFILE +'.txt'
            write_report(_today, outfile)

        #at end of period
        ### UPDATE FUNDACCOUNT AND CASHACCOUNT to DB
        # SYSTEMS?

        fundres = {
    
            'fundname': fundaccount.fundname,
            'slug': slugify((fundaccount.fundname+fundaccount.description)),
            'description': fundaccount.description,
            'bettingratio': fundaccount.bettingratio,
            'managementfee': fundaccount.managementfee,
            'performancefee': fundaccount.performancefee,
            'bailoutfee': fundaccount.bailoutfee,
            'currency': fundaccount.currency,
            'stakecap': fundaccount.stakescap,
            'performancethreshold': fundaccount.performancethreshold,
            'systemslist': [s.systemname for s in systems], #needs to be a list of system objects
            'paysDividends': fundaccount.paysDividends,
            'bfbalance': fundaccount.getbfbalance(),
            'winspbalance': fundaccount.winspbalance,
            'openingbank': fundaccount.openingbank,
            'nosystems': len(systems),
            'jratio': fundaccount.jratio,
            'lratio': 0.0,
            'sratio': fundaccount.sratio,
            'tratio': fundaccount.tratio,
            'oratio': 0.0,
            'miratio': fundaccount.miratio,
            'racedates': fundaccount.racedates,
            'investments': fundaccount.investments,
            'sequences': fundaccount.sequences,
            'returns': fundaccount.returns,
            'bfprices': fundaccount.bfprices,
            'winpattern': fundaccount.winpattern,
            'placepattern': fundaccount.placepattern,
            'cashoutthreshold': fundaccount.cashoutthreshold,
            'totalinvested': fundaccount.gettotalinvested(),
            'startdate' :self.seasonstart,
            'enddate': self.ENDDATE.date(),
            'nobets': fundaccount.nobets,
            'nowinners': fundaccount.nowinners,
            'nolosers': fundaccount.nolosers,
            'uniquewinners': len(list(self.winninghorses)),
            'maxlosingsequence': fundaccount.getmaxlosingstreak(),
            'avglosingsequence': fundaccount.getavglosingstreak3(),
            'minbalance': fundaccount.getmindailybfbalance(),
            'maxbalance': fundaccount.getmaxdailybfbalance(),
            'isLive': True,
            'a_e': fundaccount.geta_e(),
            'year': self.STARTDATE.date().year,
            'maxstake': fundaccount.getmaxbetamount(),
            'avgstake': fundaccount.getavgbetamount(),
            'individualrunners': len(list(self.horses)),
            'livesince': fundaccount.LiveSince(),
            'bfwinsr': fundaccount.getbfwinsr(),
            'cashoutbalance': cashoutaccount.getbalance(),
            'totalwinnings': (cashoutaccount.getbalance()+ fundaccount.getbfbalance()),
            "totalroi": ((cashoutaccount.getbalance()+ fundaccount.getbfbalance()) /fundaccount.openingbank )*D('100.0'),
            'dailybfbalances': fundaccount.dailybfbalances,
            'dailycashoutbalances': fundaccount.dailycashoutbalances,
            'bfcumtotalbalances': fundaccount.bfcumtotalbalances,
            'bfstartdaybalances': fundaccount.bfstartdaybalances,
            'bfenddaybalances': fundaccount.bfenddaybalances,
            'places': fundaccount.places,
            'systems': systems
            # 'Runsdata': RUNSDATA
        }


        try:
            fundaccount = fundmodels.FundAccount.objects.create(
                fundname= fundaccount.fundname,
                description= fundaccount.description,
                slug=slugify((fundaccount.fundname+fundaccount.description)),
                bettingratio= fundaccount.bettingratio,
                managementfee= fundaccount.managementfee,
                performancefee= fundaccount.performancefee,
                bailoutfee= fundaccount.bailoutfee,
                currency= fundaccount.currency,
                stakescap= fundaccount.stakescap,
                performancethreshold= fundaccount.performancethreshold,
                systemslist= [s.systemname for s in systems], #needs to be a list of system objects
                paysDividends= fundaccount.paysDividends,
                bfbalance= fundaccount.getbfbalance(),
                winspbalance= fundaccount.winspbalance,
                openingbank= fundaccount.openingbank,
                nosystems= len(systems),
                oratio= 0.0,
                lratio= 0.0,
                sratio= fundaccount.sratio,
                tratio= fundaccount.tratio,
                miratio= fundaccount.miratio,
                jratio= fundaccount.jratio,
                racedates= [ d.strftime("%Y%m%d") for d in fundaccount.racedates] ,
                investments= json.dumps(fundaccount.investments,default=enco  ),
                sequences= fundaccount.sequences,
                returns= json.dumps(fundaccount.returns,default=enco),
                bfprices= json.dumps(fundaccount.bfprices,default=enco),
                winpattern= fundaccount.winpattern,
                placepattern= fundaccount.placepattern,
                cashoutthreshold= fundaccount.cashoutthreshold,
                totalinvested= fundaccount.gettotalinvested(),
                startdate=self.seasonstart,
                enddate= self.ENDDATE.date(),
                nobets= fundaccount.nobets,
                nowinners= fundaccount.nowinners,
                nolosers= fundaccount.nolosers,
                uniquewinners= len(list(self.winninghorses)),
                maxlosingsequence= fundaccount.getmaxlosingstreak(),
                avglosingsequence= fundaccount.getavglosingstreak3(),
                minbalance= fundaccount.getmindailybfbalance(),
                maxbalance= fundaccount.getmaxdailybfbalance(),
                isLive= True,
                a_e= fundaccount.geta_e(),
                year= self.STARTDATE.date().year,
                maxstake= fundaccount.getmaxbetamount(),
                avgstake= fundaccount.getavgbetamount(),
                individualrunners= len(list(self.horses)),
                liveSince= fundaccount.LiveSince(),
                bfwinsr= fundaccount.getbfwinsr(),
                cashoutbalance= cashoutaccount.getbalance(),
                totalwinnings= (cashoutaccount.getbalance()+ fundaccount.getbfbalance()),
                totalroi= ((cashoutaccount.getbalance()+ fundaccount.getbfbalance()) /fundaccount.openingbank )*D('100.0'),
                dailybfbalances= json.dumps(fundaccount.dailybfbalances,default=enco),
                dailycashoutbalances= json.dumps(fundaccount.dailybfbalances,default=enco),
                bfcumtotalbalances= json.dumps(fundaccount.bfcumtotalbalances,default=enco),
                bfstartdaybalances= json.dumps(fundaccount.bfstartdaybalances,default=enco),
                bfenddaybalances= json.dumps(fundaccount.bfenddaybalances,default=enco),
                places= fundaccount.places
            )
        except IntegrityError as e:
            print("error %s" % e)
            pass

        # print(fundres)
        # fa = create_dict_from_json(fundmodels.FundAccount, fundres)
        # print(fa)
        # for key in fa:
        #     if fa[key]:
        #         fa[key] = json.dumps(fa[key],default=enco)
        #     elif key in ['wentLive'] and not fa[key]:
        #         fa[key] = datetime.now()
        # try:
        #     fund_obj = fundmodels.FundAccount.objects.create(**fa)
        # except IntegrityError as e:
        #     print("error %s" % e)
        # self.stdout.write("Json is successfully updated to DB")
        # # bigres.append(res)
        # d = json.dumps(fundres,default=enco)
        # print(d)
        # print(jsontemplate.expand(htmltemplate,d))
        # file_name2 = self.BASEFILE + '.json'
        # with open( file_name2, 'a+' ) as outfile:
        #     json.dump( fundres, outfile, indent = 2,default=enco )
        # print(res)
