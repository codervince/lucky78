import csv
import json
import datetime

from django.db                   import transaction
from django.core.management.base import BaseCommand
from systems                     import models


class Command( BaseCommand ):
    help = 'Import data'

    @transaction.atomic
    def handle( self, *args, **options ):

        with open( 'systems/import/race.csv' ) as csvfile:

            result = {}

            reader = csv.reader( csvfile )
            row_num = 0
            for row in reader:

                row_num += 1
                if row_num == 1:
                    continue

                fsraceno   = row[24]
                snapshotid = row[32]

                # Skip if record with 'fsraceno' already exists
                if models.Runner.objects.filter( fsraceno = fsraceno ).count() > 0:
                    if fsraceno not in result:
                        result[ fsraceno ] = []
                    result[ fsraceno ].append( snapshotid )
                    continue

                date = row[0].split( '/' )
                date = datetime.date( 2000 + int( date[2] ), int( date[0] ), int( date[1] ) )
                models.Runner.objects.create(
                   #runtype            =                    # not presentm has default 
                    racedate           = date,
                    racecoursename     = row[1],
                    racecourseid       = 0,                 # not presentm, set 0
                    racename           = row[2],
                    racetypehorse      = row[3],
                    racetypeconditions = row[4],
                    racetypehs         = row[5],
                    ages               = row[6],
                    oldraceclass       = row[7],
                    newraceclass       = '',                # not presen, set ''
                    distance           = float( row[8] ),
                    going              = row[9],
                    norunners          = int( row[10] ),
                    horsename          = row[11],
                    horseid            = 0,                 # not present, default = Null
                    sirename           = row[12], 
                    sireid             = 0,                 # not present, default = Null
                    trainername        = row[13],
                    trainerid          = 0,                 # not present, default = Null
                    jockeyname         = row[14],
                    jockeyid           = 0,                 # not present, default = Null
                    allowance          = int( row[15] ),
                    finalpos           = row[16],
                    lbw                = float( row[17] ),
                    winsp              = float( row[18] ),
                    winsppos           = int( row[19] ),
                    bfsp               = float( row[20] ),
                    bfpsp              = float( row[21] ),
                    fsratingrank       = int( row[22] ),
                    fsrating           = float( row[23] ),
                    fsraceno           = row[24],
                    draw               = int( row[25] ),
                    damname            = row[26],
                    damid              = 0,                 # not present, default = Null
                    damsirename        = row[27],
                    damsireid          = 0,                 # not present, default = Null
                    ownerid            = 0,                 # not present, default = Null
                    racetime           = row[28],
                    totalruns          = int( row[29] ),
                    isplaced           = True if int( row[30] ) == 1 else False,
                    isbfplaced         = True if int( row[31] ) == 1 else False
                )

        with open( 'result.txt', 'w' ) as outfile:
            json.dump( result, outfile, indent = 2 )

        self.stdout.write( 'Successfully imported data into database' )

