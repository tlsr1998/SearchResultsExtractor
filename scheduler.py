from crontab import CronTab

my_cron = CronTab(user = 'root')

for job in my_cron:
	print job
job = my_cron.new(command=r'scrapy runspider C:\Users\ABHISH~1\Desktop\SCRAPY~1\spider\Project2.py')
job.minute.every(3)
 
my_cron.write()