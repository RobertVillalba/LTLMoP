# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)

CompileOptions:
convexify: True
fastslow: False

CurrentConfigName:
Untitled configuration

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
RichardSimple.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)
Left, 0
Right, 0
Above, 0
Below, 0
TrackRed, 1


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
r4 = p5, p7
r5 = p4
end = p8
r2 = p6, p7
start = p1
others = 

Spec: # Specification in structured English
if you are sensing TrackRed then visit start
if you are not sensing TrackRed then visit end

