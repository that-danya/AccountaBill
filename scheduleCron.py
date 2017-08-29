from crontab import CronTab

# identify user
my_cron = CronTab(user='vagrant')

# where is that script located that needs to run?
job = my_cron.new(command='python /home/vagrant/src/AccountaBill/getNumbers.py')

# schedule this
# job.minute.every(1)
job.hour.every(24)

my_cron.write()
