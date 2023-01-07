import json
joint_list = ["nose","L_eye_in","L_eye ","L_eye_out","R_eye_in",
        "R_eye","R_eye_out","L_ear","R_ear","L_mouth","R_mouth",
        "L_sho","R_sho","L_elb","R_elb","L_wri","R_wri",
        "L_pin","R_pin","L_index","R_index","L_thu","R_thu","L_hip",
        "R_hip","L_knee","R_knee","L_ank","R_ank","L_heel","R_heel",
        "L_foot_ind","R_foot_ind"]
dic = {
        "target_list" : ["LH_U", "LH_D", "RH_U", "RH_D", "LF_D", "RF_D", "LF_U", "RF_U"],
        "base_dict" : {
            "LH_U" : ("upperarm_l", "upperarm_r", "upperarm_l", 1.5),
            "LH_D" : ("lowerarm_l", "upperarm_l", "upperarm_l", 1),
            "RH_U" : ("upperarm_r", "upperarm_l", "upperarm_r", 1.5),
            "RH_D" : ("lowerarm_r", "upperarm_r", "upperarm_r", 1),
            
            "LF_U" : ("thigh_l", "thigh_r", "thigh_l", 1),
            "LF_D" : ( "calf_l", "thigh_l", "thigh_l", 1),
            "RF_U" : ("thigh_r", "thigh_l", "thigh_r", 1),
            "RF_D" : ( "calf_r", "thigh_r", "thigh_r", 1),
        },
        "chain_list_dict" : {
            "LH_U" : ["upperarm_l", "lowerarm_l"],
            "LH_D" : ["lowerarm_l", "hand_l"],
            "RH_U" : ["upperarm_r", "lowerarm_r"],
            "RH_D" : ["lowerarm_r", "hand_r"],
            
            "LF_U" : ["thigh_l", "calf_l"],
            "LF_D" : ["calf_l", "foot_l"],
            "RF_U" : ["thigh_r", "calf_r"],
            "RF_D" : ["calf_r", "foot_r"],
        },
        "joint_constrain": {
            "upperarm_l" : ("ball",  ("A" , (-1, 1))),
            "lowerarm_l" : ("ball", ("y" , (-1, 1))),
            "upperarm_r" : ("ball",  ("A" , (-1, 1))),
            "lowerarm_r" : ("ball", ("y" , (-1, 1))),
            
            "thigh_l" : ("ball",  ("A" , (-1, 1))),
            "calf_l" : ("hinge", ("y" , (-1, 1))),
            "thigh_r" : ("ball",  ("A" , (-1, 1))),
            "calf_r" : ("hinge", ("y" , (-1, 1))),
        }
}

with open("./Venv/Panda_config.json", "w") as outfile:
    json.dump(dic, outfile, indent=4)