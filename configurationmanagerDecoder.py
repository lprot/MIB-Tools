#-------------------------------------------------------------------
#--- Decoder of configurationmanager.res for MIB2
#
# Purpose:     Remapping of SETUP/TRAFFIC/INFO to APP button and/or
#              change of the HMI events the buttons do
# Author:      jojothemojo, lprot
# Revision:    2.0
# Changelog:   1.0: Initial version
#              2.0: Cleanup, automatisation, description
#-------------------------------------------------------------------
'''
How to use:
1. Get /tsd/hmi/HMI/res/configurationmanager.res via mibstd2_toolbox>customization>advanced>Copy configurationmanager.res
2. Convert res to log like: py -3 configurationmanagerDecoder.py configurationmanager.res
3. Find the offset of the keyID in configurationmanager.log
Note: Some buttons are mapped only to certain keyboardIds (for example to MFW (Multifunction Steering Wheel or to
Central Console)

You can change functions of the buttons like follows:
a) Swap the keyIDs of two buttons (for example SOUND and APP, to make SOUND button to function like APP button) 
b) Swap the eventID of one button to the eventID of another button (for example to make long press of MUTE to act like
short press of SOUND)

4. Open configurationmanager.res in your favorite hexeditor and patch(swap) bytes at the offset you found in the logfile.
5. Save patched res file
6. Copy patched configurationmanager.res to /custom/buttons folder on Toolbox SD
7. Run mibstd2_toolbox>customization>advanced>copy configurationmanager.res
8. Rebooot the unit

Note: Some buttons like VOICE or PTT have a special handling. VOICE Menu will still appear
after the execution of the remapped button function or the changed event
'''
import os, sys
if sys.version_info[0] < 3:
    raw_input("You need to run this with Python 3!\nPress Enter to exit...")
    sys.exit(1)
f=None

filename="configurationmanager.res"
if (sys.argv[1]=='/d'):
    dbg=1
    filename=sys.argv[2]
else:
    dbg=0
    filename=sys.argv[1]
sys.stdout = open(os.path.splitext(filename)[0] + '.log', 'w', encoding='utf-8')

#from de\vw\mib\asl\internal\system\util\SystemKeyUtil.java notifyKeyListener
stateDescription={
    1: "Pressed",       #"onPressed",
    0: "Released",      #"onReleased",
    3: "Long pressed",  #"onLongPressed",
    4: "UltraLongPr.",  #"onUltraLongPressed",
  100: "Long pr.rel.",  #"onLongReleased",
  101: "Double click",  #"onMultiPressed", VOICE/PTT double tap to exit from Voice Menu
  102: "RotateLeft",    #"onRotationLeft",
  103: "RotateRight"    #"onRotationRight"
}

#eventnames collected by try and error or derived from list by mrfixpl "infos for hidden functions" from mibwiki
eventDescription={
        259:"TP pressed",
        260:"TP released",

        263:"TRAFFIC pressed",
        264:"TRAFFIC released",
        261:"TRAFFIC long pressed",
        265:"TRAFFIC ulng pressed (GUI Debug Overlay)",
        262:"TRAFFIC long press released",

        266:"EJECT pressed",
        335:"EJECT released",
        268:"EJECT long pressed",
        334:"EJECT ultralong pressed",
        267:"EJECT long press released",

        272:"SOUND pressed",
        271:"SOUND released",
        274:"SOUND long pressed",
        270:"SOUND ultralong pressed",
        273:"SOUND long press released",

        277:"SETUP pressed",
        276:"SETUP released",
        279:"SETUP long pressed (Service Mode)",
        275:"SETUP ultralong pressed (Testmode)",
        278:"SETUP long press released",

        282:"RADIO/BAND pressed",
        281:"RADIO/BAND released",
        355:"RADIO/BAND long pressed",
        280:"RADIO/BAND ultralong pressed",
        356:"RADIO/BAND long press released",

        286:"RIGHT KNOB pressed",
        287:"RIGHT KNOB released",
        284:"RIGHT KNOB long pressed",
        289:"RIGHT KNOB ultralong pressed",
        285:"RIGHT KNOB long press released",

        298:"VOL(headunit) ultralong press (Reboot)",
        293:"VOL(headunit) long press release",

        303:"CAR pressed",
        304:"CAR released",
        299:"CAR long pressed",
        305:"CAR u.long pr. (Rendering Debug Overlay)",
        302:"CAR long press released",

        309:"MUTE pressed",
        308:"MUTE released",
        
        306:"CLIMATE pressed",
        269:"CLIMATE released",

        314:"HANDSET(MFW) pressed",
        313:"HANDSET(MFW) released",
        316:"HANDSET(MFW) long pressed",
        310:"HANDSET(MFW) ultralong pressed",
        315:"HANDSET(MFW) long press released",

        320:"MENU pressed",
        319:"MENU released",
        322:"MENU long pressed (Service Menu)",
        318:"MENU ultralong pressed (Testmode)",
        321:"MENU long press released",

        326:"MEDIA(headunit) pressed",
        325:"MEDIA(headunit) released",
        328:"MEDIA(headunit) long pressed(Screenshot)",
        324:"MEDIA(headunit) ultralong pressed",
        327:"MEDIA(headunit) long press released",

        331:"MAP pressed",
        330:"MAP released",
        333:"MAP long pressed",
        329:"MAP ultralong pressed",
        332:"MAP long press released",

        336:"NEXT/FORWARD pressed",
        337:"NEXT/FORWARD released",
        358:"NEXT/FORWARD long pressed",
        338:"NEXT/FORWARD ultralong pressed",
        357:"NEXT/FORWARD long press released",

        341:"PHONE(headunit) pressed",
        342:"PHONE(headunit) released",
        339:"PHONE(headunit) long pressed",
        343:"PHONE(headunit) ultralong pressed",
        340:"PHONE(headunit) long press released",

        346:"PREV/BACK pressed",
        347:"PREV/BACK released",
        344:"PREV/BACK long pressed",
        348:"PREV/BACK ultralong pressed",
        345:"PREV/BACK long press released",

        352:"VOICE pressed",
        353:"VOICE released",
        349:"VOICE long pressed (Google Assistant/Siri)",
        354:"VOICE ultralong pressed",
        350:"VOICE long press released",
        351:"VOICE double clicked (cancel Voice Menu)",

        361:"NAV pressed",
        360:"NAV released",
        307:"NAV long pressed",
        359:"NAV ultralong pressed",
        362:"NAV long press released",

        470:"DMB pressed", #DAB in EU
        471:"DMB released",
        472:"DMB ultralong pressed",
        469:"DMB long press released",

        474:"TPEG pressed", #DAB Traffic TPEG
        475:"TPEG released",
        476:"TPEG ultralong pressed",
        473:"TPEG long press released",

        593:"INFO pressed",
        592:"INFO released",
    2110004:"INFO long pressed",
    2110005:"INFO ultralong pressed",
    2110003:"INFO long press released",

    2110020:"NEXT(console) pressed",
    2110021:"NEXT(console) released",
    2110018:"NEXT(console) long pressed",
    2110022:"NEXT(console) ultralong pressed",
    2110019:"NEXT(console) long press released",

    2110030:"PREV(console) pressed",
    2110031:"PREV(console) released",
    2110028:"PREV(console) long pressed",
    2110032:"PREV(console) ultralong pressed",
    2110039:"PREV(console) long press released",

    2110015:"MEDIA(console) pressed",
    2110016:"MEDIA(console) released",
    2110013:"MEDIA(console) long pressed",
    2110017:"MEDIA(console) ultralong pressed",
    2110014:"MEDIA(console) long press released",

    2110058:"RADIO/BAND(console) pressed",
    2110059:"RADIO/BAND(console) released",
    2110056:"RADIO/BAND(console) long pressed",
    2110060:"RADIO/BAND(console) ultralong pressed",
    2110057:"RADIO/BAND(console) long press released",

    2110012:"VOL ultralong pressed (Reboot)",
    2110007:"VOL long press released",

    2110035:"SELECT(console) pressed",
    2110036:"SELECT(console) released",
    2110033:"SELECT(console) long pressed",
    2110037:"SELECT(console) ultralong pressed",
    2110034:"SELECT(console) released",

    #APP/SMARTPHONE button handling is not available in FWs 01xx and 02xx
    2110065:"APP pressed",
    2110066:"APP released",
    2110063:"APP long pressed",
    2110067:"APP ultralong pressed",
    2110064:"APP long press released",

    2110070:"HOME pressed",
    2110071:"HOME released",
    2110068:"HOME long pressed",
    2110072:"HOME ultralong pressed",
    2110069:"HOME long press released",
}

keyboardIdNames={
    0x1:"Console buttons",
    0x4:"Steer. wheel/MFW buttons",
    0xD:"Head unit buttons"
}


#Unused definitions from \org\dsi\ifc\keypanel\Constants.java
'''
keynames=[ 
"KEY_INVALID",                   #00
"KEY_MED",                       #01
"KEY_MAIL",                      #02
"KEY_TEL",                       #03
"KEY_NAV",                       #04
"KEY_TRAFFIC",                   #05
"KEY_CAR",                       #06
"KEY_SET",                       #07
"KEY_SK_NW",                     #08
"KEY_SK_SW",                     #09
"KEY_PREV",                      #10
"KEY_SK_NE",                     #11
"KEY_SK_SE",                     #12
"KEY_BACK",                      #13
"KEY_NEXT",                      #14
"KEY_TUN",                       #15
"KEY_DDS",                       #16
"KEY_VOL",                       #17
"KEY_JOYSTICK_M",                #18
"KEY_JOYSTICK_N",                #19
"KEY_JOYSTICK_NE",               #20
"KEY_JOYSTICK_E",                #21
"KEY_JOYSTICK_SE",               #22
"KEY_JOYSTICK_S",                #23
"KEY_JOYSTICK_SW",               #24
"KEY_JOYSTICK_W",                #25
"KEY_JOYSTICK_NW",               #26
"KEY_EJECT",                     #27
"KEY_DISPLAY_KEY",               #28
"KEY_MFW_NO_KEY",                #29
"KEY_MFW_MENU",                  #30
"KEY_MFW_ARROW_RIGHT",           #31
"KEY_MFW_ARROW_LEFT",            #32
"KEY_MFW_UP",                    #33
"KEY_MFW_DOWN",                  #34
"KEY_MFW_ROLLER_LEFT",           #35
"KEY_MFW_CANCEL",                #36
"KEY_MFW_VOLUME_UP",             #37
"KEY_MFW_VOLUME_DOWN",           #38
"KEY_MFW_ROLLER_RIGHT",          #39
"KEY_MFW_AUDIOSOURCE",           #40
"KEY_MFW_ARROW_A_UP",            #41
"KEY_MFW_ARROW_A_DOWN",          #42
"KEY_MFW_ARROW_B_UP",            #43
"KEY_MFW_ARROW_B_DOWN",          #44
"KEY_MFW_PTT_ON",                #45
"KEY_MFW_PTT_CANCEL",            #46
"KEY_MFW_INFO",                  #47
"KEY_MFW_HOOK",                  #48
"KEY_MFW_HANGUP",                #49
"KEY_MFW_OFFHOOK",               #50
"KEY_MFW_LIGHT",                 #51
"KEY_MFW_MUTE",                  #52
"KEY_MFW_JOKER1",                #53
"KEY_MFW_JOKER2",                #54
"KEY_MFW_INIT",                  #55
"KEY_NUM_1",                     #56
"KEY_NUM_2",                     #57
"KEY_NUM_3",                     #58
"KEY_NUM_4",                     #59
"KEY_NUM_5",                     #60
"KEY_NUM_6",                     #61
"KEY_DISPLAY_2_KEY",             #62
"KEY_DRIVE_SELECT",              #63
"KEY_EMERGENCY_CALL_1",          #64
"KEY_EMERGENCY_CALL_2",          #65
"KEY_TP_ILLU_PRESET_KEYS",       #66
"KEY_TP_ILLU_MAP_SCROLL_BUTTON", #67
"KEY_TP_ILLU_MAP_RETURN_BUTTON", #68
"KEY_TP_ILLU_BORDERS",           #69
"KEY_TP_ILLU_HANDWRITING_SYMBOL",#70
"KEY_TP_ENCODER_X",              #71
"KEY_TP_ENCODER_Y",              #72
"KEY_MENU",                      #73
"KEY_CLIMATE",                   #74
"KEY_THREE_BA_1",                #75
"KEY_THREE_BA_2",                #76
"KEY_THREE_BA_3",                #77
"KEY_TOUCHPANEL_GENERAL",        #78
"KEY_TIPDSIPLAYACTIVE",          #79
"KEY_NAME",                      #80
"KEY_TONE",                      #81
"KEY_TP",                        #82
"KEY_MUTE",                      #83
"KEY_TPEG",                      #84
"KEY_SAT",                       #85
"KEY_TI",                        #86
"KEY_SYSTEM",                    #87
"KEY_DMB",                       #88
"KEY_ROOF_1",                    #89
"KEY_ROOF_2",                    #90
"KEY_ROOF_3",                    #91
"KEY_EAST",                      #92
"KEY_WEST",                      #93
"KEY_MFW_SIDEMENULEFT",          #94
"KEY_MFW_SIDEMENURIGHT",         #95
"KEY_NUM_7",                     #96
"KEY_NUM_8",                     #97
"KEY_SOURCE",                    #98
"KEY_MAP",                       #99
"KEY_HOR",                       #100
"KEY_OPTION",                    #101
"KEY_INFO",                      #102
"KEY_PLAYPAUSE",                 #103
"KEY_SEAT",                      #104
"KEY_HYBRID",                    #105
"KEY_OFFROAD",                   #106
"KEY_JOKER",                     #107
"KEY_ASSIST",                    #108
"KEY_SMARTPHONE",                #109
"KEY_ONLINESERVICES",            #110
"KEY_HOME",                      #111
"KEY_SPOILER_DEP",               #112
"KEY_SPOILER_RET",               #113
"KBD_INVALID",                   #114
"KBD_FCC",                       #115
"KBD_FLC",                       #116
"KBD_FRC",                       #117
"KBD_MFW",                       #118
"KBD_JOY_STICK",                 #119
"KBD_JOY_STICK_LC",              #120
"KBD_JOY_STICK_RC",              #121
"KBD_MFW_3GP",                   #122
"KBD_TOUCHPAD",                  #123
"KBD_REMOTE_FRONT",              #124
"KBD_REMOTE_LEFT",               #125
"KBD_REMOTE_RIGHT",              #126
"KBD_TOUCHSCREEN_FRONT",         #127
"KBD_TOUCHSCREEN_REAR_LEFT",     #128
"KBD_TOUCHSCREEN_REAR_RIGHT",    #129
"KBD_TOUCHSCREEN_FRONT_BOTTOM",  #130
"KBD_VOLUME_CONTROL",            #131
"KST_RELEASED",                  #132
"KST_PRESSED",                   #133
"KST_DOUBLEPRESSED",             #134
"KST_LONGPRESSED",               #135
"KST_LONGPRESSED2",              #136
"KST_LONGPRESSED3",              #137
"KST_APPROACHED",                #138
"KST_ABANDONED",                 #139
]

#de.vw.mib.asl.internal.system.ASLSystemHKEventConstants 
keynames2=[
"DDS_EVENT_LEFT",                   #00
"DDS_EVENT_LONGPRESSED",            #01
"DDS_EVENT_LONGRELEASED",           #02
"DDS_EVENT_PRESSED",                #03
"DDS_EVENT_RELEASED",               #04
"DDS_EVENT_RIGHT",                  #05
"DDS_EVENT_ULTRALONGPRESSED",       #06
"DDS_EVENT_WIDGET_TRIGGER_RELEASED",#07
"DDS_VOLUME_LEFT",                  #08
"DDS_VOLUME_LEFT_MFL",              #09
"DDS_VOLUME_LONGPRESSED",           #10
"DDS_VOLUME_LONGRELEASED",          #11
"DDS_VOLUME_PRESSED",               #12
"DDS_VOLUME_RELEASED",              #13
"DDS_VOLUME_RIGHT",                 #14
"DDS_VOLUME_RIGHT_MFL",             #15
"DDS_VOLUME_ULTRALONGPRESSED",      #16
"HK_CAR_LONGPRESSED",               #17 299
"HK_CAR_LONGRELEASED",              #18 302
"HK_CAR_PRESSED",                   #19 303
"HK_CAR_RELEASED",                  #20 304
"HK_CAR_ULTRALONGPRESSED",          #21 305
"HK_CLIMATE_PRESSED",               #22
"HK_CLIMATE_RELEASED",              #23
"HK_DMB_LONGRELEASED",              #24
"HK_DMB_PRESSED",                   #25
"HK_DMB_RELEASED",                  #26
"HK_DMB_ULTRALONGPRESSED",          #27
"HK_EJECT_LONGPRESSED",             #28
"HK_EJECT_LONGRELEASED",            #29
"HK_EJECT_PRESSED",                 #30
"HK_EJECT_RELEASED",                #31
"HK_EJECT_ULTRALONGPRESSED",        #32
"HK_INFO_PRESSED",                  #33
"HK_INFO_RELEASED",                 #34
"HK_INFO_LONGRELEASED",             #35
"HK_INFO_LONGPRESSED",              #36
"HK_INFO_ULTRALONGPRESSED",         #37
"HK_MAP_LONGPRESSED",               #38
"HK_MAP_LONGRELEASED",              #39
"HK_MAP_PRESSED",                   #40
"HK_MAP_RELEASED",                  #41
"HK_MAP_ULTRALONGPRESSED",          #42
"HK_MEDIA_LONGPRESSED",             #43
"HK_MEDIA_LONGRELEASED",            #44
"HK_MEDIA_PRESSED",                 #45
"HK_MEDIA_RELEASED",                #46
"HK_MEDIA_ULTRALONGPRESSED",        #47
"HK_MENU_EXTRALONGPRESSED",         #48
"HK_MENU_LONGPRESSED",              #49
"HK_MENU_LONGRELEASED",             #50
"HK_MENU_PRESSED",                  #51
"HK_MENU_RELEASED",                 #52
"HK_MENU_ULTRALONGPRESSED",         #53
"HK_MFL_AUDIOSOURCE_PRESSED",       #54
"HK_MFL_AUDIOSOURCE_RELEASED",      #55
"HK_MFL_OK",                        #56
"HK_MFL_PHONE_LONGPRESSED",         #57
"HK_MFL_PHONE_LONGRELEASED",        #58
"HK_MFL_PHONE_PRESSED",             #59
"HK_MFL_PHONE_RELEASED",            #60
"HK_MFL_PHONE_ULTRALONGPRESSED",    #61
"HK_MUTE_PRESSED",                  #62
"HK_MUTE_RELEASED",                 #63
"HK_NAV_LONGPRESSED",               #64 307
"HK_NAV_LONGRELEASED",              #65 362
"HK_NAV_PRESSED",                   #66 361
"HK_NAV_RELEASED",                  #67 360
"HK_NAV_ULTRALONGPRESSED",          #68 359
"HK_NEXT_LONGPRESSED",              #69
"HK_NEXT_LONGRELEASED",             #70
"HK_NEXT_PRESSED",                  #71
"HK_NEXT_RELEASED",                 #72
"HK_NEXT_ULTRALONGPRESSED",         #73
"HK_PHONE_LONGPRESSED",             #74
"HK_PHONE_LONGRELEASED",            #75
"HK_PHONE_PRESSED",                 #76
"HK_PHONE_RELEASED",                #77
"HK_PHONE_ULTRALONGPRESSED",        #78
"HK_PREV_LONGPRESSED",              #79
"HK_PREV_LONGRELEASED",             #80
"HK_PREV_PRESSED",                  #81
"HK_PREV_RELEASED",                 #82
"HK_PREV_ULTRALONGPRESSED",         #83
"HK_PTT_LONGPRESSED",               #84
"HK_PTT_LONGRELEASED",              #85
"HK_PTT_MULTIPRESSED",              #86
"HK_PTT_PRESSED",                   #87
"HK_PTT_RELEASED",                  #88
"HK_PTT_ULTRALONGPRESSED",          #89
"HK_RADIO_LONGPRESSED",             #90
"HK_RADIO_LONGRELEASED",            #91
"HK_RADIO_PRESSED",                 #92
"HK_RADIO_RELEASED",                #93
"HK_RADIO_ULTRALONGPRESSED",        #94
"HK_SETUP_LONGPRESSED",             #95
"HK_SETUP_LONGRELEASED",            #96
"HK_SETUP_PRESSED",                 #97
"HK_SETUP_RELEASED",                #98
"HK_SETUP_ULTRALONGPRESSED",        #99
"HK_SOUND_LONGPRESSED",             #100
"HK_SOUND_LONGRELEASED",            #101
"HK_SOUND_PRESSED",                 #102
"HK_SOUND_RELEASED",                #103
"HK_SOUND_ULTRALONGPRESSED",        #104
"HK_TONE_LONGPRESSED",              #105
"HK_TONE_LONGRELEASED",             #106
"HK_TONE_PRESSED",                  #107
"HK_TONE_RELEASED",                 #108
"HK_TONE_ULTRALONGPRESSED",         #109
"HK_TP_PRESSED",                    #110
"HK_TP_RELEASED",                   #111
"HK_TPEG_LONGRELEASED",             #112
"HK_TPEG_PRESSED",                  #113
"HK_TPEG_RELEASED",                 #114
"HK_TPEG_ULTRALONGPRESSED",         #115
"HK_TRAFFIC_LONGPRESSED",           #116
"HK_TRAFFIC_LONGRELEASED",          #117
"HK_TRAFFIC_PRESSED",               #118
"HK_TRAFFIC_RELEASED",              #119
"HK_TRAFFIC_ULTRALONGPRESSED",      #110
"SYS_NOPROXIMITY",                  #111
"SYS_PROXIMITY",                    #112
]

#de.vw.mib.asl.api.system.KeyListener
keynames3=[
"KEY_UNKNOWN",             #00  
"KEY_MEDIA",               #01 
"KEY_TELEPHONE",           #02
"KEY_NAVIGATION",          #03
"KEY_TRAFFIC",             #04
"KEY_CAR",                 #05
"KEY_SETTINGS",            #06
"KEY_PREVIOUS",            #07
"KEY_MFW_ARROW_A_DOWN",    #08
"KEY_MFW_ARROW_A_UP",      #09
"KEY_NEXT",                #10
"KEY_TUNER",               #11
"KEY_DDS",                 #12
"KEY_VOLUME",              #13
"KEY_EJECT",               #14
"KEY_MFW_PTT_ON",          #15
"KEY_MENU",                #16
"KEY_CLIMATE",             #17
"KEY_TONE",                #18
"KEY_TP",                  #19
"KEY_MUTE",                #20
"KEY_MFW_MUTE",            #21
"KEY_MFW_ROLLER_RIGHT",    #22
"KEY_TPEG",                #23
"KEY_DMB",                 #24
"KEY_MAP",                 #25
"KEY_INFO",                #26
"KEY_MFW_AUDIOSOURCE",     #27
"KEY_MFW_VOLUME_UP",       #28
"KEY_MFW_VOLUME_DOWN",     #29
"KEY_MFW_ARROW_B_UP",      #30
"KEY_MFW_ARROW_B_DOWN",    #31
"KEY_MFW_HOOK",            #32
"KEY_HOME",                #33
"KEY_SMARTPHONE",          #34
"KEY_ALL",                 #35
"KBD_ALL",                 #36
"KBD_TOUCHSCREEN_FRONT",   #37
"KBD_MFW",                 #38
"KBD_FCC",                 #39
]
'''

#keymapping by mrfixpl #https://github.com/olli991/mib-std2-pq-zr-toolbox/issues/7#issuecomment-1366846144
keynames={
   1:"MEDIA",
   3:"PHONE/TEL",
   4:"NAV",
   5:"TMC/TRAFFIC",
   6:"CAR",
   7:"SETUP/SETTING",
  10:"PREV",
  14:"NEXT",
  15:"RADIO/BAND/TUNER",
  16:"RIGHT KNOB/DDS",
  17:"VOL",
  32:"EJECT",
  42:"MFW_VOL_UP",
  43:"MFW_VOL_DOWN",
  44:"MFW_ROLLER_RIGHT",
  45:"MFW_SOURCE",
  46:"MFW_A_UP",
  47:"MFW_A_DOWN",
  48:"MFW_B_UP",
  49:"MFW_B_DOWN",
  50:"VOICE/MFW_PTT",
  52:"INFO2",
  53:"HANDSET/MFW_HOOK",
  57:"MFW_MUTE",
  78:"MENU",
  79:"CLIMATE",
  86:"SOUND",
  87:"TP",
  88:"MUTE",
  89:"TPEG", #DAB traffic?
  93:"DMB", #DAB TV (abandoned)
 104:"MAP",
 107:"INFO",
 108:"SELECT",
 114:"APP/SMARTPHONE", #VW App-Connect/Skoda Smartlink/Seat Full Link (Android Auto/Carplay)
 116:"HOME",
  }

def readnumber(size,name=""):
    a=int.from_bytes(f.read(size),"little")
    if dbg: print("%10s 0x%08X %10d %d bytes"%(name,a,a,size))
    return a

def readstring(nr=0,name=""):
    strcounter=nr
    magic =int.from_bytes(f.read(4),"little") #magic or initial null byte
    if (magic!=0):
        if dbg: print("string magic %x"%magic)
    strlen=int.from_bytes(f.read(4),"little")
    ss=f.read(strlen*2).decode('utf-16')
    if dbg: print("[%s]%3d;%3d;%3d;'%s'"%(name,magic,strcounter,strlen, ss));
    return ss

def readStringblock(ab=None,name=""):
    if dbg: print("\n------------------------------------------------------")
    expectedMagic=1
    expectedType="String"
    if (ab!=None):
        f.seek(ab,0) 
    if dbg: print("[%s] Stringblock Start filepos 0x%0X "%(name,f.tell()))
    magic=readnumber(4,"[%s] expectedmagic %d "%(name,expectedMagic))
    if (magic != expectedMagic):
        if dbg: print("Error this is not a %s block got %d expected %d"%(expectedType,magic,expectedMagic))
        if (magic != 0):
          exit()
    elementcnt=readnumber(4,"[%s]    Elementcount "%name)
    
    if dbg: print("[%s]%s;%s;%s;'%s'"%(name,"mag","cnt","len", "string"));
    arr=[]
    for i in range(0,elementcnt):
        arr.append(readstring(i,name=name))
    if dbg: print("[%s] End filepos 0x%0X"%(name,f.tell()))
    return arr

def readIntblock(startpos=None,name="",expectedType="INT"):
    arr=[]
    
    if (expectedType == "LONG"):
        expectedMagic=6
        expectedSize=8 # 8 Bytes per Element long
        
    if (expectedType == "INT"):
        expectedMagic=5
        expectedSize=4 # 8 Bytes per Element integer
        
    
    #go to filepos if given or continue at currrent filepos
    if (startpos!=None):
        f.seek(startpos,0) 
    if dbg: print("\n------------------------------------------------------")
    if dbg: print("[%s] %s Block Start filepos 0x%0X "%(name,expectedType,f.tell()))
    magic=readnumber(4,"[%s] expected magic {%d}"%(name,expectedMagic))
    if (magic != expectedMagic):
        if dbg: print("Error this is not a %s block got %d expected %d"%(expectedType,magic,expectedMagic))
        if (magic != 0):
            exit()
    totalElements=readnumber(4,"[%s] Elementcounter    "%name)
    for i in range(0,totalElements):
      nr=readnumber(expectedSize,"[%s] %s%04d "%(name,expectedType, i))
      arr.append(nr)

    if dbg: print("[%s] %s Block End filepos 0x%0X "%(name,expectedType,f.tell()))
    return arr
    
def getFilepos(start,i):
    filepos=int(start)+i*4+8
    return filepos
    
def interpretKeyTimesAndMappingsData(arr,start,filename=""):
    if dbg: print("------------------ interpretKeyTimesAndMappingsData --------------------------------------------")
    if dbg: print("IMPORTANT! Bytes in the configurationmanager.res are in reversed byte order, also known as")
    if dbg: print("Little Endian. E.g. value 0x12345678 from here will look like '78 56 34 12' in a Hex Editor\n")
    if dbg: print("\nFilename: %s"%filename)
    i=0
    versionnumber=0xFFFFFFFF-arr[i]
    if abs(versionnumber) not in [2]:
        if dbg: print("MappingVersion %d "%1)
        interpretKeyTimesAndMappingsDataOldFormat(arr,start)
        return
    i+=1
    if dbg: print("MappingVersion %d "%versionnumber)
    totalMappingEntrys=arr[i]
    if dbg: print("MappingEntryCount %d "%totalMappingEntrys)
    
    for p in range(0,totalMappingEntrys):
        i+=1
        id=arr[i]
        
        if dbg: print("\n---------------MappingEntry#%02d ------------------------------------------ Filepos"%(p))
        if dbg: print("KeyID:0x%02X %-41s                      0x%X"%(id,keynames.get(id,"???"),getFilepos(start,i)))
        i+=1
        keyboardid=[]
        keyboardidlen=arr[i]
        stKeyIds=""
        for l in range(0,keyboardidlen):
            i+=1
            kId=arr[i]
            keyboardid.append(kId)
            stKeyIds+="0x%02X:%s,"%(kId,keyboardIdNames.get(kId,"???"))
        if dbg: print("Attached keyboards:%d %-52s 0x%X"%(keyboardidlen,stKeyIds.rstrip(","),getFilepos(start,i)))
        i+=1
        HKEventslen=arr[i]
        if dbg: print("Attached events:%d                                                         0x%X"%(HKEventslen,getFilepos(start,i)))
        keyStateID=[]
        hkEventID=[]
        #if (HKEventslen>0):
        #   if dbg: print("%-19s | %-31s"%("State","Event"))
        for n in range(0,HKEventslen):
            i+=1
            fpos=i
            state=arr[i]
            keyStateID.append(state)
            i+=1
            ev=arr[i]
            hkEventID.append(ev)
            if dbg: print("0x%02x %-12s   > %8s %-40s 0x%X"%(state,stateDescription[state],str("0x%08X"%ev),eventDescription.get(ev,"?"),getFilepos(start,fpos)))
        i+=1
        longpresstiming=arr[i]
        if dbg: print("Long press timing: %4d ms                                                0x%X"%(longpresstiming,getFilepos(start,i)))
        i+=1
        ultralongpresstiming=arr[i]
        if dbg: print("Ultra long press timing: %4d ms                                          0x%X"%(ultralongpresstiming,getFilepos(start,i)))

def interpretKeyTimesAndMappingsDataOldFormat(arr,start=0):
    if dbg: print("------------------ interpretKeyTimesAndMappingsDataOldFormat --------------------------------")
    i=0
    ##timingData
    totalTimingEntrys=arr[i]
    if dbg: print("TimingEntries: %d "%totalTimingEntrys)
    
    for p in range(0,totalTimingEntrys):
        i+=1
        id=arr[i]
        if dbg: print("---------------TimingEntry  #%02d Filepos0x%04X -----------------------------------------------"%(p,getFilepos(start,i)))
        if dbg: print("              KeyId: %4d 0x%02X %-20s      0x%04X "%(id,id,keynames.get(id,"???"),getFilepos(start,i)))
        
        i+=1
        longpresstiming=arr[i]
        if dbg: print("    longpresstiming: %4d ms "%longpresstiming)
        i+=1
        ultralongpresstiming=arr[i]
        if dbg: print("ultalongpresstiming: %4d ms "%ultralongpresstiming)

    ###mappingData
    i+=1
    totalMappings=arr[i]
    if dbg: print("\n\nMappingEntries %d "%totalMappings)
    for p in range(0,totalMappings):
        i+=1
        id=arr[i]
        if dbg: print("\n---------------MappingEntry #%02d  --------------------------------------------------- Filepos"%(p))
        if dbg: print("KeyID:%3d 0x%02X %-66s    0x%X"%(id,id,keynames.get(id,"???"),getFilepos(start,i)))
        i+=1
        totalEvents=arr[i]
        n5=0
        states=[]
        events=[]
        if dbg: print("Attached Events:%d                                                                    0x%X"%(totalEvents,getFilepos(start,i)))
        #if (totalEvents>0):
        #    if dbg: print("%-19s | %-20s"%("State","Event"))
        for l in range(0,totalEvents):
            i+=1
            statepos=i
            state=arr[i]
            states.append(state)
            i+=1
            ev=arr[i]
            events.append(ev)
            if dbg: print("0x%02x %-12s > %10s %10d %-40s   0x%X"%(state,stateDescription[state],str("0x%X"%ev),ev,eventDescription.get(ev,"?"),getFilepos(start,statepos)))
    if dbg: print("---------------Mapping END --------------------------------------------------------- 0x%04X"%(int(start)+i*4+12))

strcounter=0
if dbg: print("Opening %s..."%filename)
f = open(filename, "rb")

#for file structure of your /tsd/hmi/HMI/res/configurationmanager.res see
#de\vw\mib\configuration\internal\generated\ConfigurationManagerImplGenerated.java 
#and seach for this.objectSwapperData Ids (order of the blocks) and datatypes 
'''
Tested with
MST2_EU_SK_PQ_P0253T (mapping format old)
MST2_EU_SK_ZR_P0478T (mapping format new)

getWorkUnitName(int n)                           (String[])  objectSwapperData[1]
getServiceName(int n)                            (String[])  objectSwapperData[2]
getAslTargetQualifiedName(int n)                 (String[])  objectSwapperData[3]
getStartupWorkUnitData()                         (int[])     objectSwapperData[4]
getLumMappings()                                 (int[])     objectSwapperData[5]
getLamMappings()                                 (int[])     objectSwapperData[6]
setFeatureFlagValues                             (int[])     objectSwapperData[7]
setConstantValues                                (int[])     objectSwapperData[8]
setConstantValues                                (int[])     objectSwapperData[9]
setConstantValues                                (String[])  objectSwapperData[10]
getUsedDisplayContextData()                      (int[])     objectSwapperData[11]
getContextGroupForContext(int n)                 (int[])     objectSwapperData[12]
getDisplayContextName(int n)                     (int[])     objectSwapperData[12]
getDisplayContextName(int n)                     (String[])  objectSwapperData[13]
getHmiSoftwareCgRunVersion()                     (String[])  objectSwapperData[14]
getLscDependencyType(int n, int n2)              (int[])     objectSwapperData[15]
getLanguageReplacement(String string)            (String[])  objectSwapperData[16]
getHapticLanguages()                             (String[])  objectSwapperData[17]
getSpeechLanguages()                             (String[])  objectSwapperData[18]
getSpellerLanguages()                            (String[])  objectSwapperData[19]
getUsedLscListenerTypes()                        (int[])     objectSwapperData[20]
getExcludedAslTargets()                          (long[])    objectSwapperData[21]
setFeatureFlagValue(String string, boolean bl)   (String[])  objectSwapperData[22]
setFeatureFlagValue(String string, boolean bl)   (int[])     objectSwapperData[23]
getKeyTimesAndMappingsData()                     (int[])     objectSwapperData[24]
getAppAssemblyStringData()                       (String[])  objectSwapperData[25]
getAppAssemblyIntData()                          (int[])     objectSwapperData[26]
getParticleParameterSetName(String string,int n) (String[])  objectSwapperData[27]
getAslStartupString(int n)                       (String[])  objectSwapperData[28]
'''
readnumber(4,"Count of Blocks in this file")
readStringblock(None,"fileinfo")                        #01
readStringblock(None,"getWorkUnitName")                 #01
readStringblock(None,"getServiceName")                  #02
readStringblock(None,"getAslTargetQualifiedName")       #03
readIntblock   (None,"getStartupWorkUnitData")          #04
readIntblock   (None,"getLumMappings")                  #05
readIntblock   (None,"getLamMappings")                  #06
readIntblock   (None,"setFeatureFlagValues")            #07
readIntblock   (None,"setConstantValues")               #08
readIntblock   (None,"setConstantValues")               #09
readStringblock(None,"setConstantValues")               #10
readIntblock   (None,"getUsedDisplayContextData")       #11
readIntblock   (None,"getContextGroupForContext")       #12
readStringblock(None,"getDisplayContextName")           #13
readStringblock(None,"getHmiSoftwareCgRunVersion")      #14
readIntblock   (None,"getLscDependencyType")            #15
readStringblock(None,"getLanguageReplacement")          #16
readStringblock(None,"getHapticLanguages")              #17
readStringblock(None,"getSpeechLanguages")              #18
readStringblock(None,"getSpellerLanguages")             #19
readIntblock   (None,"getUsedLscListenerTypes")         #20
readIntblock   (None,"getExcludedAslTargets","LONG")    #21
readStringblock(None,"setFeatureFlagValue")             #22
readIntblock   (None,"setFeatureFlagValue")             #23
startMappingData=int(f.tell())
arrayMappingData=readIntblock(None,"getKeyTimesAndMappingsData")     #24
readStringblock(None,"getAppAssemblyStringData")        #25
readIntblock   (None,"getAppAssemblyIntData")           #26
readStringblock(None,"getParticleParameterSetName")     #27
readStringblock(None,"getAslStartupString")             #28
dbg = 1
interpretKeyTimesAndMappingsData(arrayMappingData,startMappingData,filename)
if dbg: print("--- END ---")