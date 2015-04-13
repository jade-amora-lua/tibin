#1/bin/bash
set -x

# This script should be linked to from
# /etc/NetworkManager/dispatcher.d/vpn-up/strongvpn-tinyproxy-up.sh
# and
# /etc/NetworkManager/dispatcher.d/vpn-up/strongvpn-tinyproxy-down.sh
#
# It will automagically configure your machine to get tinyproxy
# forwarding every connection to the vpn connection and every other
# request to be served by the regular connection.

IP_TABLE=3
FW_MARK=2
TINYPROXY_UID=125

UP_DIR=/etc/NetworkManager/dispatcher.d/vpn-up
DOWN_DIR=/etc/NetworkManager/dispatcher.d/vpn-down

touch /tmp/init

makelinks() {
    echo $0
    fqn=$(readlink -f $0)
    mkdir -p $UP_DIR
    ln -s \
       "$fqn" \
       $UP_DIR/strongvpn-tinyproxy-up.sh
    mkdir -p $DOWN_DIR
    ln -s \
       "$fqn" \
        $DOWN_DIR/strongvpn-tinyproxy-down.sh
}

run() {
    touch /tmp/ran
    if [ x"$CONNECTION_ID" != x"strongvpn-tinyproxy" ]; then
        exit
    fi
    touch /tmp/ran
    ip rule $IP_COMMAND \
       fwmark $FW_MARK table $IP_TABLE
    ip route $IP_COMMAND \
       default dev ppp0 via proto static scope link  metric 1024 table $IP_TABLE
    iptables -t mangle $IPTABLES_COMMAND OUTPUT \
             -m owner --uid-owner $TINYPROXY_UID -j MARK --set-mark $FW_MARK
    iptables -t nat $IPTABLES_COMMAND POSTROUTING \
             -o ppp0 -j MASQUERADE
}

case x"$(basename $0)" in
    x"strongvpn-tinyproxy-up.sh")
        IP_COMMAND="add"
        IPTABLES_COMMAND="-A"
        run
        ;;
    x"strongvpn-tinyproxy-down.sh")
        IP_COMMAND="del"
        IPTABLES_COMMAND="-D"
        run
        ;;
    x"strongvpn-tinyproxy-configure.sh")
        makelinks
        ;;
    *)
        touch /tmp/getout
        echo x"$(basename $0)"
        exit
        ;;
esac
