from django.contrib import admin
from systems        import models


class RunnerAdmin( admin.ModelAdmin ):
    pass

class SystemAdmin( admin.ModelAdmin ):
    pass

class SystemSnapshotAdmin( admin.ModelAdmin ):
    pass


admin.site.register( models.Runner,         RunnerAdmin         )
admin.site.register( models.System,         SystemAdmin         )
admin.site.register( models.SystemSnapshot, SystemSnapshotAdmin )
