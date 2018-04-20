import xml.etree.cElementTree as ET
from xml.dom import minidom


prefix = \
"<?xml version=\"1.0\" encoding=\"utf-8\"?> \
<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>"


root = ET.Element('nta')
#can do all declarations here I guess

declaration = ET.SubElement(root, 'declaration')
declaration.text = "chan ready0, ready1;"
# for x in declarations whatever this will be
template = ET.SubElement(root, 'template')
template_name = ET.SubElement(template, 'name')
template_declaration = ET.SubElement(template, 'declaration')
template_location = ET.SubElement(template, 'location')
template_init = ET.SubElement(template, 'init')
template_transition = ET.SubElement(template, 'transition')
system = ET.SubElement(root, 'system')
queries = ET.SubElement(root, 'queries')



xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
with open("UPPAAL_model.xml", "w") as f:
    f.write(xmlstr)




# Former assignment as reference XML

"""
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>
<nta>
	<declaration>// Place global declarations here.
chan ready0, ready1;
urgent chan red1;
clock wait0, wait1;</declaration>
	<template>
		<name x="5" y="5">Sig0</name>
		<declaration>// Place local declarations here.
clock t0, testTRed;</declaration>
		<location id="id0" x="0" y="-357">
			<name x="-10" y="-391">start0</name>
		</location>
		<location id="id1" x="8" y="85">
			<name x="-25" y="77">R</name>
			<label kind="invariant" x="-2" y="102">t0&lt;=2</label>
		</location>
		<location id="id2" x="0" y="-68">
			<name x="-33" y="-76">Y</name>
			<label kind="invariant" x="17" y="-76">t0&lt;=10</label>
		</location>
		<location id="id3" x="0" y="-204">
			<name x="-33" y="-221">G</name>
			<label kind="invariant" x="26" y="-238">wait1&lt;=1</label>
		</location>
		<init ref="id0"/>
		<transition>
			<source ref="id1"/>
			<target ref="id3"/>
			<label kind="synchronisation" x="229" y="-34">ready1?</label>
			<label kind="assignment" x="221" y="-17">t0:=0</label>
			<nail x="306" y="-85"/>
		</transition>
		<transition>
			<source ref="id0"/>
			<target ref="id3"/>
			<label kind="synchronisation" x="4" y="-280">red1?</label>
			<label kind="assignment" x="8" y="-314">t0:=0, testTRed:=2</label>
		</transition>
		<transition>
			<source ref="id2"/>
			<target ref="id1"/>
			<label kind="guard" x="-187" y="-33">t0&gt;=1</label>
			<label kind="synchronisation" x="-187" y="-8">ready0!</label>
			<label kind="assignment" x="-178" y="17">t0:=0, wait0:=0, testTRed:=0</label>
		</transition>
		<transition>
			<source ref="id3"/>
			<target ref="id2"/>
			<label kind="guard" x="17" y="-170">t0&gt;=1</label>
			<label kind="assignment" x="17" y="-153">t0:=0</label>
		</transition>
	</template>
	<template>
		<name>Sig1</name>
		<declaration>clock t1, testTRed;</declaration>
		<location id="id4" x="8" y="144">
			<name x="17" y="110">start1</name>
		</location>
		<location id="id5" x="8" y="8">
			<name x="-17" y="-17">R</name>
			<label kind="invariant" x="-42" y="17">t1&lt;=2</label>
		</location>
		<location id="id6" x="8" y="-340">
			<name x="-25" y="-357">G</name>
			<label kind="invariant" x="42" y="-365">wait0&lt;=1</label>
		</location>
		<location id="id7" x="8" y="-144">
			<name x="-25" y="-152">Y</name>
			<label kind="invariant" x="25" y="-152">t1&lt;=10</label>
		</location>
		<init ref="id4"/>
		<transition>
			<source ref="id5"/>
			<target ref="id6"/>
			<label kind="synchronisation" x="26" y="-98">ready0?</label>
			<label kind="assignment" x="26" y="-81">t1:=0</label>
			<nail x="289" y="-170"/>
		</transition>
		<transition>
			<source ref="id4"/>
			<target ref="id5"/>
			<label kind="synchronisation" x="-178" y="59">red1!</label>
			<label kind="assignment" x="-178" y="76">t1:=0, wait1:=0, testTRed:=0</label>
		</transition>
		<transition>
			<source ref="id7"/>
			<target ref="id5"/>
			<label kind="guard" x="-179" y="-102">t1&gt;=1</label>
			<label kind="synchronisation" x="-187" y="-76">ready1!</label>
			<label kind="assignment" x="-179" y="-51">t1:=0, wait1:=0, testTRed:=0</label>
		</transition>
		<transition>
			<source ref="id6"/>
			<target ref="id7"/>
			<label kind="guard" x="-34" y="-280">t1&gt;=1</label>
			<label kind="assignment" x="-34" y="-246">t1:=0</label>
		</transition>
	</template>
	<system>// Place template instantiations here.
P0 = Sig0();
P1 = Sig1();
// List one or more processes to be composed into a system.
system P0, P1;
    </system>
	<queries>
		<query>
			<formula>A[] ((P0.G imply (P0.testTRed&gt;=2)) and (P1.G imply (P1.testTRed&gt;=2)))
			</formula>
			<comment>
			</comment>
		</query>
		<query>
			<formula>A[] ((P0.G imply (P0.testTRed&lt;=14)) and (P1.G imply (P1.testTRed&lt;=14)))
			</formula>
			<comment>
			</comment>
		</query>
		<query>
			<formula>A[] not deadlock
			</formula>
			<comment>
			</comment>
		</query>
		<query>
			<formula>E&lt;&gt;  not ((P0.G or P0.Y) and (P1.G or P1.Y))
			</formula>
			<comment>
			</comment>
		</query>
		<query>
			<formula>A[] (P0.R or (P1.R or P1.start1))
			</formula>
			<comment>
			</comment>
		</query>
		<query>
			<formula>A[] (((P0.G or P0.Y) imply P1.R) and ((P1.G or P1.Y) imply P0.R))
			</formula>
			<comment>
			</comment>
		</query>
	</queries>
</nta>
"""
