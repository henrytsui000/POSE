import json
joint_list = ["nose","L_eye_in","L_eye ","L_eye_out","R_eye_in",
        "R_eye","R_eye_out","L_ear","R_ear","L_mouth","R_mouth",
        "L_sho","R_sho","L_elb","R_elb","L_wri","R_wri",
        "L_pin","R_pin","L_index","R_index","L_thu","R_thu","L_hip",
        "R_hip","L_knee","R_knee","L_ank","R_ank","L_heel","R_heel",
        "L_foot_ind","R_foot_ind"]
dic = {
        "Joint_List" : joint_list,
        "Joint_Vec" : {# Head
                "MOUTH":("L_mouth","R_mouth","L_mouth","R_mouth"),
                # Hands
                "LH" : ("L_sho", "L_wri", "R_sho", "L_sho"),
                "RH" : ("R_sho", "R_wri", "L_sho", "R_sho"),
                "LH_U" : ("L_sho", "L_elb", "R_sho", "L_sho"),
                "LH_D" : ("L_elb", "L_wri", "L_sho", "L_elb"),
                "RH_U" : ("R_sho", "R_elb","L_sho", "R_sho"),
                "RH_D" : ("R_elb", "R_wri","R_sho", "R_elb"),
                # Hip
                "HIP":("L_hip","R_hip","L_hip","R_hip"),
                # Feet
                "LF" : ("L_hip", "L_ank", "R_hip", "L_hip"),
                "RF" : ("R_hip", "R_ank", "L_hip", "R_hip"),
                "LF_U" : ("L_hip", "L_knee", "R_hip", "L_hip"),
                "LF_D" : ("L_knee", "L_ank", "L_hip", "L_knee"),
                "RF_U" : ("R_hip", "R_knee","L_hip", "R_hip"),
                "RF_D" : ("R_hip", "R_ank","R_hip", "R_knee"),  }     

             
}

with open("media_config.json", "w") as outfile:
    json.dump(dic, outfile, indent=4)