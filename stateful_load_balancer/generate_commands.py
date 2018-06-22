########################################################
# 1. generate commands.txt based on threshold
########################################################

import sys
from topo_to_json import get_topo_data

if len(sys.argv) < 3:
    print("Format: %s <TYPE> <SERVER_THRESHOLD>" % sys.argv[0])
    sys.exit()

THRESHOLD = int(sys.argv[2])

def generate(num_servers_left, l):
    if num_servers_left == 1:
        s = ""
        for j in range(THRESHOLD):
            new_l = l + [j]
            min_val = min(new_l)
            min_ind = new_l.index(min_val)
            s += "table_add set_server_dest_port_table set_server_dest_port " + \
                ' '.join([str(i) for i in new_l]) + " => %d %d\n" % (min_val, min_ind + 2)
        return s
    else:
        s = ""
        for j in range(THRESHOLD):
            s += generate(num_servers_left - 1, l + [j])
        return s

def generate_commands(topo_stats):
    keylist = topo_stats.keys()

    for key in keylist:
        template = open("commands_template_%s_%s.txt" % (sys.argv[1], key), 'r')
        s = template.read()
        stat = topo_stats[key]
        # Assuming only 1 host
        num_servers = stat['SERVERS'] - 1
        s += generate(num_servers, [])

        commands = open('commands_%s.txt' % key, 'w')
        commands.write(s)
        commands.close()
        template.close()

if __name__ == '__main__':
    topo_stats = get_topo_data()["topo_stats"]
    # print(topo_stats)
    generate_commands(topo_stats)