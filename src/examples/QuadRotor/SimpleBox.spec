# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
flyLow, 0
flyHigh, 0
turn0, 0
turnPi, 0

CompileOptions:
convexify: True
fastslow: False

CurrentConfigName:
QuadRevamped

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
SimpleBox.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)
highButton, 0
lowButton, 0
PiButton, 0
zeroButton, 0


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
bottomLeft = p2
r1 = p1
others = 
1 = p9
3 = p7
2 = p8
5 = p5
4 = p6
7 = p3
6 = p4

Spec: # Specification in structured English
visit 5
visit 1

