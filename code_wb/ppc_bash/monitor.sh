#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

type crudini >/dev/null 2>&1
if [ $? -ne 0 ];then
    sudo yum -y install crudini >/dev/null 2>&1
fi

height_threshold=20

alert_reciver=[#ALERT_RECIVER]
system_id=[#SYSTEM_ID]
chain_name=[#CHAIN_NAME]
sit="0"

alarm() {
        echo "$1"
        alert_ip=$(/sbin/ifconfig eth0 | grep inet | grep -v inet6 | awk '{print $2}')
        time=$(date "+%Y-%m-%d %H:%M:%S")
        if [ -z ${chain_name} ]; then
                chain_name="chain:${system_id}"
        fi
        
        ims_ip="172.16.40.51"
        ims_port="10812"
        if [[ "1" == ${sit} ]];then
                ims_ip="172.21.0.130"
        fi
        
        # cagent_tools alarm "$1"
        curl -H "Content-Type: application/json" -X POST --data "{alertList:[{'alert_title':'$alert_ip','sub_system_id':'$system_id','alert_level':3,'alert_info':'$time:[$chain_name]$1','alert_ip':'$alert_ip','alert_way':3,'alert_reciver':'$alert_reciver'}]}" http://${ims_ip}:${ims_port}/ims_data_access/send_alarm_by_json.do
}

# restart the node
restart() {
        local nodedir=$1
        # bash $nodedir/stop.sh
        # sleep 5
        bash $nodedir/start.sh
}

# echo message with time
info() {
        time=$(date "+%Y-%m-%d %H:%M:%S")
        echo "[$time] $1"
}

error() {
        echo -e "\033[31m $1 \033[0m"
}

# check if nodeX is work well
function check_node_work_properly() {
        # node dir
        nodedir=$1
        # node name
        node=$(basename $nodedir)
        # fisco-bcos path
        fiscopath=${nodedir}/../fisco-bcos
        # config.ini for this node
        config=${nodedir}/config.ini

        ok="true"

        # listen ip
        config_ip=$(egrep 'listen_ip' ${configfile} | awk 'NR==2' | awk -F"=" '{print $2}')
        # listen port
        config_port=$(egrep 'listen_port' ${configfile} | awk 'NR==2' | awk -F"=" '{print $2}')

        # check if process id exist
        pid=$(ps aux | grep "$fiscopath" | egrep "fisco-bcos" | grep -v "grep" | awk -F " " '{print $2}')
        [ -z "${pid}" ] && {
                alarm " ERROR! $config_ip:$config_port $node does not exist"
                restart $nodedir
                return 1
        }

        # get group_id 
        group=$(egrep 'group_id' ${configfile} | awk -F"=" '{print $2}')

        # getBlockNumber
        blocknumberresult=$(curl -s "http://$config_ip:$config_port" -X POST --data "{\"jsonrpc\":\"2.0\",\"method\":\"getBlockNumber\",\"params\":[\"${group}\", \"\"],\"id\":67}")

        # echo $blocknumberresult
        height=$(echo $blocknumberresult | grep -o "result.*" | egrep -o "[0-9]+")
        [[ -z "$height" ]] && {
                alarm " ERROR! Cannot connect to $config_ip:$config_port ${group}:${node}, method: getBlockNumber"
                return 1
        }

        height_file="$nodedir/$node_$group.height"
        echo $height >$height_file

        # getConsensusStatus
        consresult=$(curl -s "http://$config_ip:$config_port" -X POST --data "{\"jsonrpc\":\"2.0\",\"method\":\"getConsensusStatus\",\"params\":[\"${group}\", \"\"],\"id\":67}")
        [[ -z "$consresult" ]] && {
                alarm " ERROR! Cannot connect to $config_ip:$config_port ${group}:${node}, method: getConsensusStatus"
                return 1
        }
        # echo ${consresult}
        timeout=$(echo ${consresult} | egrep -o "timeout.*" | awk -F ","  '{ print $1 }' | awk -F ":" '{ print $2 }')
        [[ "${timeout}" == "true" ]] && {
                alarm " ERROR! Consensus timeout $config_ip:$config_port ${group}:${node}"
                return 1
        }

        # getSealerList
        nodeids=$(curl -s "http://$config_ip:$config_port" -X POST --data "{\"jsonrpc\":\"2.0\",\"method\":\"getSealerList\",\"params\":[\"${group}\", \"\"],\"id\":67}" | egrep "nodeID" | awk -F "\"" '{ print $4}' | tr -s "\n" " ")
        [[ -z "$nodeids" ]] && {
                alarm " ERROR! Cannot connect to $config_ip:$config_port ${group}:${node}, method: getSealerList"
                return 1
        }
        # echo ${sealerresult}
        nodeids_array=(${nodeids})

        # getSyncStatus
        syncstatusresult=$(curl -s "http://$config_ip:$config_port" -X POST --data "{\"jsonrpc\":\"2.0\",\"method\":\"getSyncStatus\",\"params\":[\"${group}\", \"\"],\"id\":67}")
        [[ -z "$syncstatusresult" ]] && {
                alarm " ERROR! Cannot connect to $config_ip:$config_port ${group}:${node}, method: getSyncStatus"
                return 1
        }

        # check if any node disconnected
        for nodeid in ${nodeids_array[@]}
        do
                nodeid_exist=$(echo "${syncstatusresult}" | grep -o ${nodeid})
                if [[ -z "${nodeid_exist}" ]]; then
                       alarm " ERROR! The node info is missing in the sync status info, the node may be disconnected, nodeid: ${nodeid} " 
                       ok="false"
                       continue
                fi
        done 

        # check if any block number is too far behind
        blocknumbers=$(echo "${syncstatusresult}" | tr -s '\\\"' '"' | egrep -o "blockNumber\":[0-9]+" | awk -F ":" '{ print $2 }' | tr -s "\n" " ")
        blocknumber_array=(${blocknumbers})

        sync_nodeids=$(echo "${syncstatusresult}" | tr -s '\\\"' '"' | tr -s "}" "\n" | tr -s "{" "\n" | egrep -o "nodeID.*" | awk -F '"' '{ print $3}' | tr -s "\n" " ")
        sync_nodeids_array=(${sync_nodeids})

        max_blocknumber=0
        max_node=""
        min_blocknumber=2147483647
        min_node=""
        for((i=0;i<${#blocknumber_array[@]};i++)) do
                blocknumber=${blocknumber_array[i]}
                nodeid=${sync_nodeids_array[i]}
                if [[ ${blocknumber} -ge ${max_blocknumber} ]];then
                        max_blocknumber=${blocknumber}
                        max_node=${nodeid}
                fi

                if [[ ${min_blocknumber} -ge ${blocknumber} ]];then
                        min_blocknumber=${blocknumber}
                        min_node=${nodeid}
                fi
        done;

        ((diff_blocknumber=max_blocknumber-min_blocknumber))

        # 
        if [[ ${diff_blocknumber} -ge "${height_threshold}" ]];then
                ok="false"
                echo "max node: ${max_node}"
                echo "min node: ${min_node}"
                error_msg="[highest block number: ${max_blocknumber}, nodeid: ${max_node}, lowest block number: ${min_blocknumber}, nodeid: ${min_node}]"
                alarm " ERROR! The lowest blocknumber is too far behind the highest block number queried by getSyncStatus, ${error_msg}, content: ${syncstatusresult}"     
        fi

        if [[ "${ok}" == "true" ]];then
             info " OK! $config_ip:$config_port $node:$group is working properly: height $height"
        fi
   
        return 0
}

# check all node of this server, if all node work well.
function check_all_node_work_properly() {
        local work_dir=$1
        for configfile in $(ls ${work_dir}/config.ini); do
                check_node_work_properly $(dirname $(readlink -f $configfile))
        done
}

dir=${dirpath}

function help() {
        echo "Usage:"
        echo "Optional:"
        echo "    -d  <path>          work dir(default: \$dirpath/../). "
        echo "    -r                  alert_reciver. "
        echo "    -c                  chain name"
        echo "    -s                  system id"
        echo "    -S                  sit enviroment test"
        echo "    -t                  block number far behind threshold"
        echo "    -h                  Help."
        echo "Example:"
        echo "    bash monitor.sh -d /data/app/baas-cncbc "
        echo "    bash monitor.sh -d /data/app/baas-cncbc -r octopuswang "
        echo "    bash monitor.sh -d /data/app/baas-cncbc -r octopuswang -s 5379"
        echo "    bash monitor.sh -d /data/app/baas-cncbc -r octopuswang -s 5379 -c test"
        exit 0
}

work_dir=${dirpath}/

while getopts "d:r:c:s:St:h" option; do
        case $option in
        d) work_dir=$OPTARG ;;
        r) alert_reciver=$OPTARG ;;
        c) chain_name=$OPTARG ;;
        s) system_id=$OPTARG ;;
        S) sit="1" ;;
        t) height_threshold=$OPTARG ;;
        h) help ;;
        esac
done

[ ! -d ${work_dir} ] && {
        echo " work_dir($work_dir) not exist "
        exit 0
}

#
check_all_node_work_properly ${work_dir}
