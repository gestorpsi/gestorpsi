from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime, timedelta
from celery.task import Task
from celery.registry import tasks




# this will run everyday at 3:00 am, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
@periodic_task(run_every=crontab(hour="1", minute="0", day_of_week="*"))
#@periodic_task(run_every=crontab(hour="*", minute="*", second=5, day_of_week="*"))
#@periodic_task(run_every=timedelta(minutes=0, seconds=10))
def check_and_charge():
    from gestorpsi.organization.models import Activitie
    d = str(datetime.now())
    a = Activitie(description=d)
    a.save()


'''class CheckAndCharge(Task):
    def run(self, some_arg, **kwargs):
        from gestorpsi.organization.models import Activitie
        d = str(datetime.now())
        a = Activitie(description= d )
        a.save()
        print d
        logger = self.get_logger(**kwargs)
        logger.info("Did something: %s" % some_arg)
        return d
tasks.register(CheckAndCharge)'''