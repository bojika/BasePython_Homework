import textfsm


def get_lsdb(raw_lsdb):
    # let's check what we have. IS-IS or OSPF
    if "ATT/P/OL" in raw_lsdb:
        # IS-IS
        template = open('topology/templates/tfsm/sh_isis_database_iosxr_1.tfsm')
        fsm = textfsm.TextFSM(template)
        result_1 = fsm.ParseText(raw_lsdb)

        lsdb = [[str(i), x[0][:-3] if x[0][-3:] == '.00' else x[0], x[1][:-3] if x[1][-3:] == '.00' else x[1], x[2],
                 x[0] + "->" + x[1]] for i, x in enumerate(result_1, 1)]

        template = open('topology/templates/tfsm/sh_isis_database_iosxr_2.tfsm')
        fsm = textfsm.TextFSM(template)
        result_2 = fsm.ParseText(raw_lsdb)

    else:
        # OSPF
        template = 'topology/templates/tfsm/sh_ip_ospf_database_router.tfsm'

        f = open(template)
        re_table = textfsm.TextFSM(f)
        header = re_table.header
        result = re_table.ParseText(raw_lsdb)

        # T - transit, P - p2p, S - stub
        for i, s in enumerate(result):
            result[i][3] = str(result[i][3][0:1]).upper()

        # remove stub links
        result = [a for a in result if a[3] != "S"]

        # process "R" router LSA
        lsdb = list(
            [str(a), result[a][0], "DR_" + result[a][5] if result[a][3] == "T" else result[a][4], result[a][8],
             result[a][6]] for a in range(len(result)) if result[a][9] == "R")
        # process "N" network LSA
        lsdb += list([str(a), "DR_" + result[a][0], result[a][10], "0", result[a][0]] for a in range(len(result)) if
                     result[a][9] == "N")

    return (lsdb)