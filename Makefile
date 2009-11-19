# ---------------------------------------------------------
# Qpackage config
QPDOMAIN=cloud.aserver.com
QPNAME=cloud_ras_server
QPVERSION=0.1
#QPDEPENDENCY=['pexpect','pylabs.org',None,'','','generic']

# ---------------------------------------------------------
# Qpackage rules
QR=/opt/qbase3/var/qpackages/${QPDOMAIN}/${QPNAME}/${QPVERSION}/upload_trunk/
QT=${QR}tasklets/generic/
QF=${QR}files/generic/
true:
	true
create:
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.create('${QPNAME}','${QPVERSION}','${QPDOMAIN}','trunk','generic')"
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='NEW').addDependency(*${QPDEPENDENCY})"
	sudo rsync -rtv qpackage/ ${QT}
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='NEW').source.export()"
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='NEW').package()"
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='NEW').install()"
createpub:
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='NEW').publish()"
update:
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='LOCAL').prepare()"
	sudo rsync -rtv qpackage/ ${QT}
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='MOD').source.export()"
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='MOD').package()"
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='MOD').install()"
updatepub:
	sudo /opt/qbase3/qshell -c "q.qshellconfig.interactive=True;i.qpackages.findFirst('${QPNAME}','${QPVERSION}',state='MOD').publish()"

# ---------------------------------------------------------
commit:
	echo hg commit -m "`hg tip --template={desc}`";
	echo hg push
	echo make update
	echo make updatepub

db:
	psql -h localhost -U qbase osis

test:
	cd code;sudo zip /opt/qbase3/lib/python/site-packages/osis-0.1-py2.5.egg osis/store/OsisConnection.py; cd ..
	cd code;sudo zip -r /opt/qbase3/lib/python/site-packages/osis-0.1-py2.5.egg osis/store/pg8000 ; cd ..
	sudo /opt/qbase3/qshell -c "q.manage.applicationserver.restart()"
	sudo /opt/qbase3/qshell -d -c "u=q.drp.clouduser.get('fcd76bb5-0fcb-4abe-9ba4-b4b818e35cf2');print u"
	#sudo tail -f /opt/qbase3/var/log/twistd_rasserver.log

