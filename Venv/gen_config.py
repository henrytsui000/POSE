import json
dic = {
    "CR" : {"real_joint" : "clavicle_r",
            "init_degree" : (180, 0, 90)},
    "UAR" : {"real_joint" : "upperarm_r",
            "init_degree" : ( 0, 0, 0)},
    "LAR" : {"real_joint" : "lowerarm_r",
            "init_degree" : ( 0, 0, 0)},

    "CL"  : {"real_joint" : "clavicle_l",
            "init_degree" : ( 0, 0, 90)},
    "UAL" : {"real_joint" : "upperarm_l",
            "init_degree" : ( 0, 0, 0)},
    "LAL" : {"real_joint" : "lowerarm_l",
            "init_degree" : ( 0, 0, 0)},
}

with open("config.json", "w") as outfile:
    json.dump(dic, outfile, indent=4)