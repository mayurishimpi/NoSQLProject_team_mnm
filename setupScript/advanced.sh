#!/bin/bash




function spinWait(){
    val=$1
    echo "Waiting for $1 seconds"
    while [ $val -gt 0 ]
    do
        sleep 1
        val=$((val-1))
    done
    echo "Time's up!"
}


# Function: non_mongos_instance
#
# Description: 
#   Perform intialization and setup for the config and shard instances.
#   This involves setting up MongoDB, the ports, and stitching them together in MONGOSH.
#
# Usage: non_mongos_instance ipv4_address public_ipv4_dns instance_name
#
# Arguments:
#   instance: Name of the instance we are setting up (either config or shards 1-3)
#   ipv4_address: Elastic IPv4 address of the EC2 instance 
#   public_ipv4_dns: Public IPv4 DNS of the EC2 instance
#
# Example usage: 
#   non_mongos_instance $instance $ipv4_address $public_ipv4_dns
#
function non_mongos_instance(){

    # echo "Enter a fruit:"
    # read fruit
    dir1="shard/"$3"rep1"
    dir2="shard/"$3"rep2"
    dir3="shard/"$3"rep3"
    name=""$3"_repl"
    port1=""
    port2=""
    port3=""
    svr_type="shardsvr"

    case $3 in
    "config") 
        port1="28041"
        port2="28042"
        port3="28043"
        svr_type="configsvr"
        ;;
    "shard1") 
        port1="28081"
        port2="28082"
        port3="28083"
        ;;
    "shard2") 
        port1="29081"
        port2="29082"
        port3="29083"
        ;;
    "shard3") 
        port1="29085"
        port2="29086"
        port3="29087"
        ;;
    *) echo "Sorry, that is not a valid instance.";;
    esac


    chmod 600 Downloads/mickey-das.pem 
    ssh -i Downloads/mickey-das.pem ubuntu@$1 << REMOTE_COMMANDS

        
        wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
        sudo apt-get install gnupg
        wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
        echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
        sudo apt-get update
        sudo apt-get install -y mongodb-org

        echo -e "\n\nMongoD installation successful!\nProceeding to port setup!\n\n "
        sudo service mongod start
        sudo service mongod status
        mkdir -p $dir1 $dir2 $dir3

        echo -e "\n\nThe following new directories have been made!\nProceeding to nohup commands!"
        cd shard
        ls
        cd ..

        echo "nohup mongod --$svr_type  --port $port1 --bind_ip localhost,$2 --replSet $name --dbpath $dir1 &"
        nohup mongod --$svr_type  --port $port1 --bind_ip localhost,$2 --replSet $name --dbpath $dir1 &
        echo -ne '\n' | command
        wait
        sleep 60

        echo "nohup mongod --$svr_type  --port $port2 --bind_ip localhost,$2 --replSet $name --dbpath $dir2 &"
        nohup mongod --$svr_type  --port $port2 --bind_ip localhost,$2 --replSet $name --dbpath $dir2 &
        echo -ne '\n' | command
        wait
        sleep 60

        echo "nohup mongod --$svr_type  --port $port3 --bind_ip localhost,$2 --replSet $name --dbpath $dir3 &"
        nohup mongod --$svr_type  --port $port3 --bind_ip localhost,$2 --replSet $name --dbpath $dir3 &
        echo -ne '\n' | command
        wait
        sleep 60
        
        wait
        
        echo -e "\nnohup commands executed successfuly!\nProceeding to Mongo Shell after a short break!"

        sleep 60

        mongosh --host $1  --port $port1
        # rsconf = { _id: "$name", members: [{_id: 0, host: "$1:$port1"}, {_id: 1, host: "$1:$port2"}, {_id: 2, host: "$1:$port3"}]}
        rsconf = { _id: "$name", members: [{_id: 0, host: \"$1:$port1\"}, {_id: 1, host:\"$1:$port2\"}, {_id: 2, host: \"$1:$port3\"}]}
        rs.initiate(rsconf)

        quit


REMOTE_COMMANDS
    return

    val=30
    while [ $val -gt 0 ]
    do
        echo "Time: $val"
        sleep 1
        val=$((val-1))
    done
    echo "Time's up!"


    ssh -i Downloads/mickey-das.pem ubuntu@$1 << REMOTE_COMMANDS
        echo "Proceeding to Mongo Shell!"
        mongosh --host $1  --port $port1 
        rs.status()
        quit
REMOTE_COMMANDS

}


function mongo_setup(){
    chmod 600 Downloads/mickey-das.pem 
    ssh -i Downloads/mickey-das.pem ubuntu@$1 << REMOTE_COMMANDS

        
        wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
        sudo apt-get install gnupg
        wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
        echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
        sudo apt-get update
        sudo apt-get install -y mongodb-org

        echo -e "\n\nMongoD installation successful!\nProceeding to port setup!\n\n "
REMOTE_COMMANDS
}


function non_mongos_instance_dump(){

    dir1="shard/"$3"rep1"
    dir2="shard/"$3"rep2"
    dir3="shard/"$3"rep3"
    name=""$3"_repl"
    port1=""
    port2=""
    port3=""
    svr_type="shardsvr"

    case $3 in
    "config") 
        port1="28041"
        port2="28042"
        port3="28043"
        svr_type="configsvr"
        ;;
    "shard1") 
        port1="28081"
        port2="28082"
        port3="28083"
        ;;
    "shard2") 
        port1="29081"
        port2="29082"
        port3="29083"
        ;;
    "shard3") 
        port1="29085"
        port2="29086"
        port3="29087"
        ;;
    *) echo "Sorry, that is not a valid instance.";;
    esac
    
    echo "
        $3 

        chmod 600 Downloads/mickey-das.pem
        ssh -i Downloads/mickey-das.pem ubuntu@$1

        sudo service mongod start
        sudo service mongod status

        mkdir -p $dir1 $dir2 $dir3

        NOHUP COMMANDS
        nohup mongod --$svr_type  --port $port1 --bind_ip localhost,$2 --replSet $name --dbpath $dir1 &
        nohup mongod --$svr_type  --port $port2 --bind_ip localhost,$2 --replSet $name --dbpath $dir2 &
        nohup mongod --$svr_type  --port $port3 --bind_ip localhost,$2 --replSet $name --dbpath $dir3 &
  
        MONGOSH
        mongosh --host $1  --port $port1
        rsconf = { _id: \"$name\", members: [{_id: 0, host: \"$1:$port1\"}, {_id: 1, host:\"$1:$port2\"}, {_id: 2, host: \"$1:$port3\"}]}
        rs.initiate(rsconf)
        Wait for 30s before proceeding to rs.status()
        rs.status()
        " >> output1.txt
}

# Function: non_mongos_instance
#
# Description: 
#   Perform intialization and setup for the config and shard instances.
#   This involves setting up MongoDB, the ports, and stitching them together in MONGOSH.
#
# Usage: non_mongos_instance ipv4_address public_ipv4_dns instance_name
#
# Arguments:
#   config_dns:
#   mongos_dns: 
#   shard1_ip
#   shard2_ip
#   shard3_ip :
#   mongos_ip
#
# Example usage: 
#   non_mongos_instance $instance $ipv4_address $public_ipv4_dns
#
function mongos_instance_dump(){
    echo "
        mongos 

        chmod 600 Downloads/mickey-das.pem
        ssh -i Downloads/mickey-das.pem ubuntu@$6

        nohup mongos --configdb config_repl/$1:28041,$1:28042,$1:28043 --bind_ip localhost,$2 &

        mongosh --host $2 --port 27017

        sh.addShard( "shard1_repl/$3:28081,$3:28082,$3:28083")
        sh.addShard( "shard2_repl/$4:29081,$4:29082,$4:29083")
        sh.addShard( "shard3_repl/$5:29085,$5:29086,$5:29087")

        sh.status()
        
        " >> output1.txt


}


######################SCRIPT STARTS HERE###########################

#Working memory
file=$1
inst_arr=() 


#Read the input data from the file
while read -r line1 && read -r line2 && read -r line3; do
    inst_arr+=("$line1" "$line2" "$line3")
done < $file

#Verify input data from file
echo -e "\nPlease verity the input data from the file!\n"
idx=0
while [ $idx -lt 5 ]
do
    # echo "$[idx*3]"
    echo "${inst_arr[idx*3]}"
    # echo "$[idx*3+1]"
    echo "${inst_arr[idx*3+1]}"
    # echo "$[idx*3+2]"
    echo -e "${inst_arr[idx*3+2]}\n"
    let idx+=1
done

#Wait for inbound rules verification!
echo -e "Warning: Have you configured your inbound rules for all the instances?(y/n)"
inbound_rules_complete=false

while ! $inbound_rules_complete
do
    read -t 10 -p "" -n1 -s commandKey
    if [ ! -z "$commandKey" ] && [ $commandKey = "y" ]; then
        inbound_rules_complete=true
        echo -e "\nOkay! Let's proceed!"
    elif [ ! -z "$commandKey" ] && [ $commandKey = "n" ]; then
        echo -e "\nGee, sucks to be you \nExiting..."
        exit
    fi
done


# Perform Mongod setup (without starting Mongod) on all the instances 
idx=0
while [ $idx -lt 5 ]
do
    # echo "${inst_arr[idx*3]}"
    # echo "${inst_arr[idx*3+1]}"
    # echo -e "${inst_arr[idx*3+2]}\n"
    echo -e "\nExecuting Mongod Setup for "${inst_arr[idx*3]}" instance. Shall we proceed?\n"
    
    read -t 100 -p "" -n1 -s commandKey
    if [ ! -z "$commandKey" ] && [ $commandKey = "y" ]; then
        echo -e "\nOkay! Let's go!"
        mongo_setup "${inst_arr[idx*3+1]}"
        echo -e "Setup Complete! Performing Dump!"
        # mongos_instance_dump "${inst_arr[2]}" "${inst_arr[14]}" "${inst_arr[4]}" "${inst_arr[7]}" "${inst_arr[10]}" "${inst_arr[13]}"
        non_mongos_instance_dump "${inst_arr[idx*3+1]}" "${inst_arr[idx*3+2]}" "${inst_arr[idx*3]}" 
        echo -e "\nDump Complete"
    elif [ ! -z "$commandKey" ] && [ $commandKey = "n" ]; then
        echo -e "\n\nExiting..."
        exit
    fi


    let idx+=1
done

# # Dump ready-to-enter instructions into the output.txt file
# idx=0
# while [ $idx -lt 4 ]
# do
#     non_mongos_instance_dump "${inst_arr[idx*3+1]}" "${inst_arr[idx*3+2]}" "${inst_arr[idx*3]}" 
#     let idx+=1
# done

mongos_instance_dump "${inst_arr[2]}" "${inst_arr[14]}" "${inst_arr[4]}" "${inst_arr[7]}" "${inst_arr[10]}" "${inst_arr[13]}"

echo "Thank you for using Mickey's Advanced Script! Exiting....."
exit
    