#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

sit="1"

alert_reciver=""
system_id="5379"

function alarm() {
        local alert_info=$1
        local alert_title="【Test Chain Status Report: $(date "+%Y-%m-%d %H:%M:%S")】"

        echo "$alert_info"
        alert_ip=$(/sbin/ifconfig eth0 | grep inet | grep -v inet6 | awk '{print $2}')
        
        ims_ip="172.16.40.51"
        ims_port="10812"
        if [[ "1" == ${sit} ]];then
                ims_ip="172.21.0.130"
        fi
        
        # cagent_tools alarm "$1"
        curl -H "Content-Type: application/json" -X POST --data "{alertList:[{'alert_title':'$alert_title','sub_system_id':'$system_id','alert_level':5,'alert_info':'$alert_info','alert_ip':'$alert_ip','alert_way':3,'alert_reciver':'$alert_reciver'}]}" http://${ims_ip}:${ims_port}/ims_data_access/send_alarm_by_json.do ||  alarm "$1"
}

function query_air_nodes_info() {
    local uip=${1} # app@127.0.0.1
    local pswd=${2}
    local prefix=${3}
    local nodesPath=${4}

    #ps -aux|grep ${nodesPath} |grep node |grep -v grep|awk -v prefix=${prefix} '{print prefix"\tmemory\t"$11"\t"$6}'
    #du node*/log -sh |awk -v prefix=${prefix} '{print prefix"\tstorage\t"$2"\t"$1}'
    #for node in $(ls|grep node); do  for log in $(ls $(pwd)/${node}/log/* -t); do report=$(cat ${log}|grep -ia report |tail -n 1); if [ "${report}" ]; then echo ${report}|awk -F',' '{print $4}'|awk -v prefix=${prefix} -v node=${node} -F'=' '{print prefix"\tnumber\t"node"\t"$2}' ; break; fi; done; done;
 
    sshpass -p  ${pswd} ssh ${uip} " 
    cd ${nodesPath}
    ps -aux|grep ${nodesPath} |grep node |grep -v grep|awk -v prefix=${prefix} '{print prefix\"\\t\"\$11\"\\tmemory\\t\"\$6}'
    du *node*/data -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\"\\tstorage\t\"\$1}'
    du *node*/log -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\"\\tstorage\t\"\$1}'
    for node in \$(ls | grep node); do  for log in \$(ls \$(pwd)/\${node}/log/* -t); do report=\$(cat \${log}|grep -ia Report|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F',' '{for(i=1;i<=NF;i++)if(\$i ~ \"committedIndex.*\") print \$i }'|awk -v prefix=${prefix} -v node=\${node} -F'=' '{print prefix\"\\t\"node\"\\tnumber\\t\"\$2}'; break; fi; done; done;
    for node in \$(ls | grep node); do  for log in \$(ls \$(pwd)/\${node}/log/* -t); do report=\$(cat \${log}|grep -iaE 'Report.*committedIndex'|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F '.' '{print \$1}'| awk -v prefix=${prefix} -v node=\${node} '{print prefix\"\\t\"node\"\\ttimestamp\\t\"\$2}'; break; fi; done; done;
    "

}


function query_pro_nodes_info() {
    local uip=${1} # app@127.0.0.1
    local pswd=${2}
    local prefix=${3}
    local nodesPath=${4}
    local usesudo=${5}

    
    sshpass -p  ${pswd} ssh ${uip} "
    cd ${nodesPath} && for name in \$(${usesudo} ls|grep -iaE \"group|gateway\"|grep -v grep|awk -v dir=${nodesPath##*\/} '{print \$1}'); do ${usesudo} ps -aux|grep \${name}|grep -vaE \"grep|awk\"|awk -v prefix=${prefix} -v name=\${name} '{print prefix\"\\t\"name\"\\tmemory\\t\"\$6}' ; done; 
    ${usesudo} du ${nodesPath}/group*/group* -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\"\\tstorage\t\"\$1}'
    ${usesudo} du ${nodesPath}/group*/log -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\"\\tstorage\t\"\$1}'
    cd  ${nodesPath} && for node in \$(${usesudo} ls ${nodesPath} | grep -ia group); do for log in \$(${usesudo} find \${node}/log -type f |sort -r); do report=\$(${usesudo} cat \${log}|grep -a Report|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F',' '{for(i=1;i<=NF;i++)if(\$i ~ \"committedIndex.*\") print \$i }'|awk -v prefix=${prefix} -v node=\${node##*\/} -F'=' '{print prefix\"\\t\"node\"\\tnumber\\t\"\$2}' ; break; fi; done; done;
    for node in \$(${usesudo} ls ${nodesPath} | grep -ia group); do for log in \$(${usesudo} find \${node}/log -type f |sort -r); do report=\$(${usesudo} cat \${log}|grep -iaE 'Report.*committedIndex'|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F '.' '{print \$1}'| awk -v prefix=${prefix} -v node=\${node} '{print prefix\"\\t\"node\"\\ttimestamp\\t\"\$2}'; break; fi; done; done;
    "
}

function query_pro_tars_nodes_info() {
    local uip=${1} # app@127.0.0.1
    local pswd=${2}
    local prefix=${3}
    local nodesLogBasePath=${4}
    local nodesDataBasePath=${5}
    local usesudo=${6}

    sshpass -p  ${pswd} ssh ${uip} "
    for name in \$(${usesudo} ls ${nodesLogBasePath}|grep -iaE \"group|gateway\"|grep -v grep|awk -v dir=${nodesLogBasePath##*\/} '{print dir\".\"\$1}'); do ${usesudo} ps -aux|grep \${name}|grep -vaE \"grep|awk\"|awk -v prefix=${prefix} -v name=\${name} '{print prefix\"\\t\"name\"\\tmemory\\t\"\$6}' ; done; 
    ${usesudo} du ${nodesLogBasePath}/* -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\"/log\\tstorage\t\"\$1}'
    ${usesudo} du ${nodesDataBasePath}.*/group* -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\"\\tstorage\t\"\$1}'
    for node in \$(${usesudo} ls ${nodesLogBasePath} | grep -ia group); do for log in \$(${usesudo} find ${nodesLogBasePath}/\${node} -type f |sort -r|grep -E 'log.*'); do report=\$(${usesudo} cat \${log}|grep -a Report|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F',' '{for(i=1;i<=NF;i++)if(\$i ~ \"committedIndex.*\") print \$i }'|awk -v prefix=${prefix} -v node=\${node##*\/} -F'=' '{print prefix\"\\t\"node\"\\tnumber\\t\"\$2}' ; break; fi; done; done;
    for node in \$(${usesudo} ls ${nodesLogBasePath} | grep -ia group); do for log in \$(${usesudo} find ${nodesLogBasePath}/\${node} -type f |sort -r|grep -E 'log.*'); do report=\$(${usesudo} cat \${log}|grep -iaE 'Report.*committedIndex'|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F '.' '{print \$1}'| awk -v prefix=${prefix} -v node=\${node} '{print prefix\"\\t\"node\"\\ttimestamp\\t\"\$2}'; break; fi; done; done;
    "
}

function query_max_nodes_info() {
    local uip=${1} # app@127.0.0.1
    local pswd=${2}
    local prefix=${3}
    local nodesPath=${4}
    local usesudo=${5}

    #for name in $(find 310*/* -maxdepth 1 -type d|sed "s/\//\./g"); do ps -aux|grep ${name}|grep -vaE "grep|awk"|awk -v prefix=${prefix} -v name=${name} '{print prefix"\tmemory\t"name"\t"$6}' ; done;


    sshpass -p  ${pswd} ssh ${uip} " 
    ${usesudo} du /root/.tiup/data/tikv.2379 -sh | awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\"\\tstorage\t\"\$1}' 
    for name in \$(${usesudo} ls ${nodesPath}|grep -iavE \"sdk|console\"|grep -v grep|awk -v dir=${nodesPath##*\/} '{print dir\".\"\$1}'); do ${usesudo} ps -aux|grep \${name}|grep -vaE \"grep|awk\"|awk -v prefix=${prefix} -v name=\${name} '{print prefix\"\\t\"name\"\\tmemory\\t\"\$6}' ; done; 
    ${usesudo} du ${nodesPath}/* -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\".log\\tstorage\t\"\$1}'
    for node in \$(${usesudo} ls ${nodesPath} | grep -ia maxnode); do  for log in \$(${usesudo} ls ${nodesPath}/\${node}/ -t|grep -vi node); do report=\$(${usesudo} cat ${nodesPath}/\${node}/\${log}|grep -a Report |grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report} |awk -F',' '{for(i=1;i<=NF;i++)if(\$i ~ \"committedIndex.*\") print \$i }'|awk -v prefix=${prefix} -v node=\${node##*\/} -F'=' '{print prefix\"\\t\"node\"\\tnumber\\t\"\$2}' ; break; fi; done; done;
    for node in \$(${usesudo} ls ${nodesPath} | grep -ia maxnode); do  for log in \$(${usesudo} ls ${nodesPath}/\${node}/ -t|grep -vi node); do report=\$(${usesudo} cat ${nodesPath}/\${node}/\${log}|grep -iaE 'Report.*committedIndex'|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F '.' '{print \$1}'| awk -v prefix=${prefix} -v node=\${node} '{print prefix\"\\t\"node\"\\ttimestamp\\t\"\$2}'; break; fi; done; done;
    "
}

function query_max_nodes_info_without_storage() {
    local uip=${1} # app@127.0.0.1
    local pswd=${2}
    local prefix=${3}
    local nodesPath=${4}
    local usesudo=${5}

    #for name in $(find 310*/* -maxdepth 1 -type d|sed "s/\//\./g"); do ps -aux|grep ${name}|grep -vaE "grep|awk"|awk -v prefix=${prefix} -v name=${name} '{print prefix"\tmemory\t"name"\t"$6}' ; done;


    sshpass -p  ${pswd} ssh ${uip} "
    sudo du ${nodesPath}/* -sh 
    ${usesudo} du ${nodesPath}/* -sh |awk -v prefix=${prefix} '{print prefix\"\\t\"\$2\".log\\tstorage\t\"\$1}'
    for name in \$(${usesudo} ls ${nodesPath}|grep -iavE \"sdk|console\"|grep -v grep|awk -v dir=${nodesPath##*\/} '{print dir\".\"\$1}'); do ${usesudo} ps -aux|grep \${name}|grep -vaE \"grep|awk\"|awk -v prefix=${prefix} -v name=\${name} '{print prefix\"\\t\"name\"\\tmemory\\t\"\$6}' ; done;
    for node in \$(${usesudo} ls ${nodesPath} | grep -ia maxnode); do  for log in \$(${usesudo} ls ${nodesPath}/\${node}/ -t|grep -vi node); do report=\$(${usesudo} cat ${nodesPath}/\${node}/\${log}|grep -a Report|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F',' '{for(i=1;i<=NF;i++)if(\$i ~ \"committedIndex.*\") print \$i }' |awk -v prefix=${prefix} -v node=\${node##*\/} -F'=' '{print prefix\"\\t\"node\"\\tnumber\\t\"\$2}' ; break; fi; done; done;
    for node in \$(${usesudo} ls ${nodesPath} | grep -ia maxnode); do  for log in \$(${usesudo} ls ${nodesPath}/\${node}/ -t|grep -vi node); do report=\$(${usesudo} cat ${nodesPath}/\${node}/\${log}|grep -iaE 'Report.*committedIndex'|grep -v statReporterInterval |tail -n 1); if [ \"\${report}\" ]; then echo \${report}|awk -F '.' '{print \$1}'| awk -v prefix=${prefix} -v node=\${node} '{print prefix\"\\t\"node\"\\ttimestamp\\t\"\$2}'; break; fi; done; done;
    "
}


function query_chain1_info() {
    query_air_nodes_info hulk@172.21.0.89 Apps@123 air-89 /data/hulk/chain1/172.21.0.89
    query_air_nodes_info hulk@172.21.0.133 Apps@123 air-133 /data/hulk/chain1/172.21.0.133

    query_pro_nodes_info hulk@172.16.144.69 Apps@123 pro-69 /data/hulk/chain1/pro_nodes/172.16.144.69  
    query_air_nodes_info hulk@172.16.144.69 Apps@123 air-69 /data1/hulk/chain1/172.16.144.69

    query_max_nodes_info gavinouyang@172.16.144.109 Aa12345! max-109 /root/app/tars/app_log/310chain1 "sudo "
}

function query_chain2_info() {
    query_air_nodes_info hulk@10.107.120.225 Apps@123 air-org1 /data/hulk/chain2Air/nodes/10.107.120.225
    query_air_nodes_info hulk@172.16.144.106 Apps@123 air-org2  /data1/hulk/chain2Air/nodes/172.16.144.106

    query_pro_tars_nodes_info hulk@172.16.144.106 Apps@123 pro-106 /data1/hulk/tars/app/tars/app_log/310chain2 /data1/hulk/tars/app/tars/tarsnode-data/310chain2
    #query_pro_tars_nodes_info gavinouyang@172.16.144.106 Aa12345! pro /data1/hulk/tars/app/tars/app_log/310chain2 "sudo " 

    query_max_nodes_info_without_storage gavinouyang@172.16.144.109 Aa12345! max-109 /root/app/tars/app_log/310chain2 "sudo "
    #query_max_nodes_info_without_storage hulk@172.16.144.109 Apps@123 max-109 /data1/hulk/tars/app_log/310chain2 
    query_max_nodes_info hulk@172.16.144.131 Apps@123 max-131 /data1/hulk/tars/app/tars/app_log/310chain2
    query_max_nodes_info_without_storage hulk@172.16.144.145 Apps@123 max-145 /data1/hulk/tars/app/tars/app_log/310chain2
}

function query_chain3_info() {
    query_air_nodes_info hulk@172.21.193.5 Apps@123 air  /data1/hulk/chain3/172.21.193.5
}

function query_chain4_info() {
    query_air_nodes_info hulk@10.107.120.226 Apps@123 air-226 /data/hulk/3.0-hybird/10.107.120.226
    query_air_nodes_info hulk@10.107.120.227 Apps@123 air-227 /data/hulk/3.0-hybird/10.107.120.227

    query_pro_tars_nodes_info hulk@10.107.120.233 Apps@123 pro-233  /data/hulk/app/tars/framework/app_log/chain0 /data/hulk/app/tars/framework/tarsnode-data/chain0

    query_max_nodes_info_without_storage hulk@10.107.120.228 Apps@123 max-228 /data/hulk/app/tars/app_log/chain0
}

function info_filter() {
    echo -e "name\tprocess/dir\ttype\tinfo\n${1}" |
	sed "s/\/data.*node/node/g" |
	sed "s/\/data.*chain/chain/g" |
	sort -k3r -k1   |
	awk '{print $1"\t"$3:$2"\t"$4}'|
	sed "s/storage/[f]]/g" |
	sed "s/memory/[m]]/g" |
	sed "s/number/[n]/g" |
	column -t
}

function to_tree() {
    local treename="${1}"
    local name="${2}"
    local procdir="${3}"
    local type="${4}"
    local info="${5}"
    if [[ $name == air* ]];then
        if [ "${type}" == "number"  ]; then
            mkdir -p ${treename}/${name}"-"${procdir}":"${info}
        elif [ "${type}" == "timestamp"  ]; then
	    local dir=$(find .|grep "${treename}/${name}-${procdir}:*")
            mv ${dir} ${dir}:$(echo "${info}"|sed "s/:/\./g")
        elif [ "${type}" == "memory"  ]; then
            mkdir -p ${treename}/${name}"-"${procdir}":"$((${info}/1024))M
        elif [ "${type}" == "storage"  ]; then
            mkdir -p ${treename}/${name}"-"${procdir}":"${info}
        fi
    elif [[ $name == pro* ]];then
        if [ "${type}" == "number"  ]; then
            mkdir -p ${treename}/pro-${procdir}/${name}:${info}
        elif [ "${type}" == "timestamp"  ]; then
            local dir=$(find .|grep "${treename}/pro-${procdir}/${name}:*")
            mv ${dir} ${dir}:$(echo "${info}"|sed "s/:/\./g")
        elif [ "${type}" == "memory"  ]; then
            mkdir -p ${treename}/pro-${procdir}/${name}:$((${info}/1024))M
        elif [ "${type}" == "storage"  ]; then
            mkdir -p ${treename}/${name}/pro-${procdir}:${info}
        fi
    else
        if [ "${type}" == "number"  ]; then
            mkdir -p ${treename}/max-${procdir}/${name}:${info}
        elif [ "${type}" == "timestamp"  ]; then
            local dir=$(find .|grep "${treename}/max-${procdir}/${name}:*")
            mv ${dir} ${dir}:$(echo "${info}"|sed "s/:/\./g")
        elif [ "${type}" == "memory"  ]; then
            mkdir -p ${treename}/max-${procdir}/${name}:$((${info}/1024))M
        elif [ "${type}" == "storage"  ]; then
            mkdir -p ${treename}/${name}/max-${procdir}:${info}
        fi
    fi
}

function info_filter2() {
    echo -e ${@} |
	sed "s/\/data.*node/node/g" | 
	sed "s/\/data.*chain/chain/g" | 
	sed "s/\/data.*group/group/g" |
	sed "s/\/\.\.\/fisco-bcos//g" |
	sed "s/ .*\.agency/ agency/g"  | 
	sed "s/ .*\.tiup\/data\// tikv-/g" |
	sed "s/agency/org/g"|
	sed "s/group/g/g" |
	sed "s/BcosNodeService/Node/g" |
	sed "s/BcosMaxNodeService/MaxNode/g" |
	sed "s/BcosExecutorService/Exe/g" | 
	sed "s/BcosRpcService/Rpc/g" | 
	sed "s/BcosGatewayService/Gateway/g" 
}


function info_tree_builder() {
    local content=${1}
    echo "${content}" > chainReport.log
    rm -rf blockNumber
    echo "${content}" |grep -iaE 'number|timestamp' |
    while IFS= read -r line
    do
        #info_filter2 ${line}
        to_tree blockNumber $(info_filter2 ${line})
    done
    echo -n "★ "
    tree blockNumber |grep -v directories | column -t -s ':'|sed "s/\./:/g"
    #tree blockNumber |grep -v directories  |sed "s/:/ /g"
    echo ""
    rm -rf memory
    echo "${content}" |grep memory |
    while IFS= read -r line
    do
        #info_filter2 ${line}
        to_tree memory $(info_filter2 ${line})
    done
    echo -n "★ "
    tree memory |grep -v directories  | column -t -s ':'
    #tree memory |grep -v directories  |sed "s/:/ /g"
    echo ""
    rm -rf storage
    echo "${content}" | grep storage|
    while IFS= read -r line
    do
        #info_filter2 ${line}
        to_tree storage $(info_filter2 ${line})
    done
    echo -n "★ "
    tree storage |grep -v directories | column -t -s ':'
    #tree storage |grep -v directories |sed "s/:/ /g"

#    echo "${content}" > chainInfo.log
#    for line in $(cat chainInfo.log); do
#        info_filter2 ${line}
#        to_tree  $(info_filter2 ${line})
#    done
#    tree info_tree
}

function query_chain1_info_with_filter() {
    echo -e "[chain1]"
    info_tree_builder "$(query_chain1_info)"
}

function query_chain2_info_with_filter() {
    echo -e "[chain2]"
    info_tree_builder "$(query_chain2_info)"
}

function query_chain3_info_with_filter() {
    echo -e "[chain3]"
    info_tree_builder "$(query_chain3_info)"
}

function query_chain4_info_with_filter() {
    echo -e  "[chain4]"
    info_tree_builder "$(query_chain4_info)"
}

function query_all_chain_info() {
    query_chain1_info_with_filter
    query_chain2_info_with_filter
    query_chain3_info_with_filter
#    query_chain4_info_with_filter
}

function report_all_chain_info() {
    alarm "$(query_chain1_info_with_filter)" 
   #alarm "$(query_chain2_info_with_filter)"
    alarm "$(query_chain3_info_with_filter)"
#    alarm "$(query_chain4_info_with_filter)"
}


function help() {
        echo "Usage:"
        echo "Optional:"
        echo "    -r                  [Optional] alert_reciver. "
        echo "    -s                  [Optional] system id"
        echo "    -h                  Help."
        echo "Example:"
        echo "    bash $0 -r octopuswang,jimmyshi -s 5379"
        exit 0
}


while getopts "r:s:h" option; do
        case $option in
        r) alert_reciver=$OPTARG ;;
        s) system_id=$OPTARG ;;
        h) help ;;
        esac
done

report_all_chain_info

#query_all_chain_info

test(){
rm -rf info_tree

cat chainReport.log | grep storage|
while IFS= read -r line
do
        #storage_info_filter ${line}
        #to_tree info_tree $(storage_info_filter ${line})
        info_filter2 ${line}
        to_tree info_tree $(info_filter2 ${line})
done

tree info_tree | column -t -s ':'
}

#test




