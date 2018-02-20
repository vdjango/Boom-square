#!/bin/bash

function version(){
	return $(lsb_release -a| grep Release: | awk '{print $2}' | awk -F. '{print $1}')
}

function debug(){
	echo "lsb_release -a:"
	lsb_release -a
	echo ""
	echo "uname:"
	uname -a}

function init(){
	
	pya=""

	get=$(rpm -qa | grep "^python3.-3\."| wc -l)
	if [[ "$get" == "1" ]]; then

		if [[ "$(rpm -qa | grep "^python3.-3\.4")" == "" ]]; then
			pya="36"
		else 
			pya="34"
		fi

	fi
	if [[ "$get" == "2" ]]; then
		pya="36"
	fi

	return pya

}

function install7(){
	yum install wget -y
	wget -O ./epel-release-7.noarch.rpm https://mirrors.ustc.edu.cn/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
	rpm -ivh ./epel-release-7.noarch.rpm
	yum makecache
	yum install python36 -y
}
function system_7(){
	if [[ "$(init)" == "36" ]]; then
		ph="python3.6"
		pi="pip3.6"
	elif [[ "$(init)" =="34" ]]; then
		ph="python3.4"
		pi="pip3.4"
	else
		install7
	fi
	wget -O ./get-pip.py https://bootstrap.pypa.io/get-pip.py
	$ph ./get-pip.py
	$pi install Django==1.9.2
	$pi install uwsgi
	yum install -y nginx

}
function system_6(){

}

function main(){
	data=$(date +'%y%m%d%H%M%s')
	file="debug_$(data).logs"
	echo "时间： $(date +'%y-%m-%d %H:%M:%s') " >> ./$file
	echo "" >> ./$file

	if [[ "$(version)" == "7" ]]; then
		echo -e "\e[5;34m 系统版本号为： $(version) \e[0m"
		sleep 1
		system_7 >> ./$file
	fi
	if [[ "$(version)" == "6" ]]; then
		echo -e "\e[5;34m 系统版本号为： $(version) \e[0m"
		sleep 1
		system_6 >> ./$file
	fi
	echo -e "\e[0;31m 不支持您的系统版本：  $(version)\e[0m"
	echo "作者希望您把以下信息发送到作者邮箱"
	echo 
	echo
	echo "==============================================="
	debug  >> ./$file
	echo "==============================================="



}

main

