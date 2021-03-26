#! /usr/bin/env python
#
#Script para obtener un resumen de la plataforma
#Elaborado por W.A. - 31/05/2010

#Los imports necesarios
import os
import time
import sys
import subprocess

#Diccionario con direcciones de correo
dirs={}
dirs["sysadmin"]="wasuaje@eluniversal.com"
dirs["sysadmin2"]="wasuaje@hotmail.com"

#Diccionario con los servidores
servers={}
servers["A-manduca5"]="204.228.236.5"
servers["A-Web01"]="204.228.236.6"
servers["A-manduca7"]="204.228.236.7"
servers["A-manduca8"]="204.228.236.8"
servers["A-manduca10"]="204.228.236.10"
servers["A-Web02"]="204.228.236.13"
servers["A-Web03"]="204.228.236.17"
servers["A-App01"]="204.228.236.19"
servers["A-manduca33"]="204.228.236.33"
#Servidores de la plataforma local
servers["B-twingo"]="10.3.0.2"
servers["B-239"]="10.3.0.239"
servers["B-233"]="10.3.33.233"
servers["B-130"]="10.3.0.130"


#Diccionario con comandos
cmds={}
cmds={}
cmds["df"]=["Espacio en disco disponible","df -ah"]
cmds["df2"]=["Espacio en disco disponible","df -ak"]
cmds["log1"]=["Estado de los logs Static","ls -lah /usr/local/apacheTest-statics/logs"]
cmds["log2"]=["Estado de los logs EU","ls -lah /usr/local/eu-dyn/logs"]
cmds["log3"]=["Estado de los logs Estampas","ls -lah /usr/local/apacheD2-es/logs"]
cmds["log4"]=["Estado de los logs CEU","ls -lah /usr/local/apache-ceu/logs"]
cmds["log5"]=["Estado de los logs Widgets","ls -lah /usr/local/apache-widgets/logs"]
cmds["log6"]=["Estado de los logs OpenAdstream","du -sh  /home/manduca/apache/htdocs/RealMedia/ads/OpenAd/Logs/*"]
cmds["log7"]=["Estado de la cola de correo","mailq | grep Total"]
cmds["log8"]=["Estado de los logs de Apache OAS","ls -lah /home/manduca/apache/logs/"]
cmds["log9"]=["Estado de la Tmp","find /tmp -name *.jpg"]
cmds["log10"]=["Estado de logs de jboss","ls -lah /usr/local/jboss/server/default/log"]
cmds["warn"]=["Warns del sistema operativo","cat /var/log/messages | grep warning"]
cmds["error"]=["Errors del sistema operativo","cat /var/log/messages | grep error"]
cmds["panic"]=["Panics del sistema operativo","cat /var/log/messages | grep panic"]
cmds["secure"]=["Alertas de seguridad de acceso","tail -300  /var/log/secure | grep failure"]
cmds["crons"]=["Estado de las ultimas ejecuciones de los crons","tail -30 /var/log/cron"]
cmds["crons1"]=["Listado de los cronjobs","\"find /var/spool/cron/ -type f -exec cat {} \; \""]
cmds["crons2"]=["Listado de los cronjobs - Solaris","\"find /var/spool/cron/crontabs/ -type f -exec cat {} \; \""]
cmds["crons3"]=["Listado de los cronjobs - Solaris - Manduca5","tail -30/var/cron/log"]
cmds["crons4"]=["Estado de las ultimas ejecuciones de los crons","tail -30 /var/log/cron/info"]
#para maquina solaris
cmds["warn1"]=["Warns del sistema operativo - Solaris","cat /var/log/syslog | grep warning"]
cmds["error1"]=["Errors del sistema operativo - Solaris","cat /var/log/syslog | grep error"]
cmds["panic1"]=["Panics del sistema operativo - Solaris","cat /var/log/syslog | grep panic"]
cmds["secure1"]=["Alertas de seguridad de acceso - Solaris","tail -300  /var/log/authlog | grep Failed"]

#Diccionario de comandos por servidor para evitar que servidores ejcuten comandos que no les correnponde
cmd_srv={}
cmd_srv["A-manduca5"]=[cmds["df2"],cmds["warn1"],cmds["error1"],cmds["panic1"],cmds["secure1"],cmds["crons3"],cmds["crons2"]]
cmd_srv["A-Web01"]=[cmds["df"],cmds["log1"],cmds["log2"],cmds["log4"],cmds["log5"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons"],cmds["crons1"]]
cmd_srv["A-manduca7"]=[cmds["df"],cmds["log3"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons"],cmds["crons1"]]
cmd_srv["A-manduca8"]=[cmds["df2"],cmds["warn1"],cmds["error1"],cmds["panic1"],cmds["secure1"],cmds["crons2"]]
cmd_srv["A-manduca10"]=[cmds["df"],cmds["log8"],cmds["log6"],cmds["log7"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons"],cmds["crons1"]]
cmd_srv["A-Web02"]=[cmds["df"],cmds["log1"],cmds["log2"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons"],cmds["crons1"]]
cmd_srv["A-Web03"]=[cmds["df"],cmds["log1"],cmds["log2"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons"],cmds["crons1"]]
cmd_srv["A-App01"]=[cmds["df"],cmds["log9"],cmds["log10"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons"],cmds["crons1"]]
cmd_srv["A-manduca33"]=[cmds["df2"],cmds["warn1"],cmds["error1"],cmds["panic1"],cmds["secure1"],cmds["crons2"]]
cmd_srv["B-twingo"]=[cmds["df"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons4"],cmds["crons1"]]
cmd_srv["B-239"]=[cmds["df2"],cmds["warn1"],cmds["error1"],cmds["panic1"],cmds["secure1"],cmds["crons2"]]
cmd_srv["B-233"]=[cmds["df"],cmds["warn"],cmds["error"],cmds["panic"],cmds["crons1"]]
cmd_srv["B-130"]=[cmds["df"],cmds["warn"],cmds["error"],cmds["panic"],cmds["secure"],cmds["crons"],cmds["crons1"]]

#devuelve una lista ordenada de las claves del diccionario
def sortedDictValues2(adict):
    keys = adict.keys()
    keys.sort()
    return keys

#funcion que abre archivo de texto donde se va a reunir la informacion
def write_file(newLine):
	file = open("resumen.txt", "w")
	file.write(newLine)
	file.close()

def run_cmd(comando):
	p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read().strip()
	return out  #This is the stdout from the shell command

def send_mail():
	import smtplib
	# Import the email modules we'll need
	from email.mime.text import MIMEText
	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open("resumen.txt", 'rb')
	# Create a text/plain message
	msg = MIMEText(fp.read())
	fp.close()

	for mail in dirs.keys():
		msg['Subject'] = "Resumen diario de la plataforma"
		msg['From'] = "Sysadmin"
		msg['To'] = dirs[mail]
		prueba = dirs[mail]
		# Send the message via our own SMTP server, but don't include the envelope header.
		s = smtplib.SMTP('localhost')		
		s.sendmail(msg['Subject'], prueba, msg.as_string())
		s.quit()

def begin_ser(srv):
	linea="\n********************* Servidor:"+srv+" *******************************************\n"
	return linea

def end_serv(srv):
	linea="\n********************* Fin Servidor:"+srv+" ***************************************\n"
	return linea

def gather_info(srv,cmd):
	comando = cmd
	from time import strftime
	ip=servers[srv]
	fecha=strftime("%Y-%m-%d %H:%M:%S")
	linea="----------------------------------------------------------------------------\n"
	linea=linea+fecha+ " -- Ejecutando:  "+comando[0] + "  --\n"
	linea=linea+"----------------------------------------------------------------------------\n"
	linea=linea+run_cmd("ssh root@"+ip+" "+comando[1])
	linea=linea+"\n"
	return linea

def main(server = "", comando = ""):
	linea=""
	if server == "" and comando == "":		#toda la corrida
		a=sortedDictValues2(servers)		#solicito la lista ordenada de claves
		for srv in a:
			linea=linea+begin_ser(srv)
			for cmd in cmd_srv[srv]:
				linea=linea+gather_info(srv,cmd)
			linea=linea+end_serv(srv)
	elif server != "" and comando != "":		#un servidor un comando
		try:
			if servers[server] and cmds[comando]:
				srv=server				
				linea=linea+begin_ser(srv)
				linea=linea+gather_info(srv,cmds[comando])
				linea=linea+end_serv(srv)
		except KeyError:                     
			linea= "El servidor especificado o el comando no existe,los servidores y comandos validos son\n"
			for srv in servers.keys():
				linea=linea+srv+"\n"				
			for cmd in cmds.keys():
				linea=linea+cmd+"\n"
				
	elif server != "" and comando == "":		#un servidor todos sus comandos
		srv=server	
		linea=linea+begin_ser(srv)
		for cmd in cmd_srv[srv]:
			linea=linea+gather_info(srv,cmd)
		linea=linea+end_serv(srv)
			
	#print linea
	write_file(linea+"\n")
	return linea

if len(sys.argv) == 2:
	parametro=sys.argv[1]		
	parametro2=""
elif len(sys.argv) == 3:
	parametro=sys.argv[1]		
	parametro2=sys.argv[2]		
else:
	parametro=""
	parametro2=""
#main(parametro,parametro2)

#send_mail()






