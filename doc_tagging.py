#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob



##############
#Main Function
##############

def doc_tagging():
	mypath = "./txt/*.txt"
	allfiles = glob.glob(mypath)
	for singleFile in allfiles:
		currentText = open(singleFile, 'r')
		varTmp = singleFile.split(".txt")
		newNameFile = varTmp[0] + "with_tags.txt"
		newText = open(newNameFile, 'w')
		
		#control variables
		documentBegins = 0
		currentSection = ''
		previousSection = '</_tag_JunOS>'
		
		#sectionACX = 0
		#sectionCSRX = 0
		#sectionEX = 0
		#sectionMX = 0
		#sectionQFX = 0
		#sectionPTX = 0
		#sectionSRX = 0

		for line in currentText:
			#print("line es: ", line)
			newText.write(line)
			if (line.startswith("Junos OS Release ") and ("Notes" not in line) and ("," not in line)):
				print("inserta tag de numero release")
				newText.write("<_tag_" + line.strip() + ">\n")
				continue
			if (line.startswith("Revision History")):
				documentBegins = 1
				continue
			if (line.startswith("Junos OS Release Notes for ACX") and documentBegins):
				print("inserta tag de seccion ACX")
				previousSection=currentSection
				currentSection="ACX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for cRPD") and documentBegins):
				print("inserta tag de seccion CRPD")
				previousSection=currentSection
				currentSection="CRPD"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for cSRX") and documentBegins):
				print("inserta tag de seccion cSRX")
				previousSection=currentSection
				currentSection="CSRX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for EX") and documentBegins):
				print("inserta tag de seccion EX")
				previousSection=currentSection
				currentSection="EX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for JRR") and documentBegins):
				print("inserta tag de seccion JRR")
				previousSection=currentSection
				currentSection="JRR"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for Juniper Secure") and documentBegins):
				print("inserta tag de seccion SecureConnect")
				previousSection=currentSection
				currentSection="SecureConnect"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for Junos Fusion for Enterprise") and documentBegins):
				print("inserta tag de seccion FusionEnterprise")
				previousSection=currentSection
				currentSection="SecureConnect"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for Junos Fusion for Provider") and documentBegins):
				print("inserta tag de seccion FusionProvider")
				previousSection=currentSection
				currentSection="SecureConnect"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for MX") and documentBegins):
				print("inserta tag de seccion MX")
				previousSection=currentSection
				currentSection="MX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for NFX") and documentBegins):
				print("inserta tag de seccion NFX")
				previousSection=currentSection
				currentSection="NFX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for PTX") and documentBegins):
				print("inserta tag de seccion PTX")
				previousSection=currentSection
				currentSection="PTX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue				
			if (line.startswith("Junos OS Release Notes for QFX") and documentBegins):
				print("inserta tag de seccion QFX")
				previousSection=currentSection
				currentSection="QFX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for SRX") and documentBegins):
				print("inserta tag de seccion SRX")
				previousSection=currentSection
				currentSection="SRX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for vMX") and documentBegins):
				print("inserta tag de seccion VMX")
				previousSection=currentSection
				currentSection="VMX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for vRR") and documentBegins):
				print("inserta tag de seccion VRR")
				previousSection=currentSection
				currentSection="VRR"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue
			if (line.startswith("Junos OS Release Notes for vSRX") and documentBegins):
				print("inserta tag de seccion VSRX")
				previousSection=currentSection
				currentSection="VSRX"
				newText.write("</_tag_" + previousSection.strip() + "_section>\n")
				newText.write("<_tag_" + currentSection.strip() + "_section>")
				continue				
			if (line.startswith("What's New") and (documentBegins) and ("|" not in line)):
				newText.write("<_tag_" + currentSection.strip() + "_newfeatures>\n")
				continue
			if (line.startswith("What’s Changed") and (documentBegins) and ("|" not in line)):
				newText.write("<_tag_" + currentSection.strip() + "_changes>\n")
				continue
			if (line.startswith("Known Limitations") and (documentBegins) and ("|" not in line)):
				newText.write("<_tag_" + currentSection.strip() + "_limitations>\n")
				continue
			if (line.startswith("Open Issues") and (documentBegins) and ("|" not in line)):
				newText.write("<_tag_" + currentSection.strip() + "_openissues>\n")
				continue
			if (line.startswith("Resolved Issues") and (documentBegins) and ("|" not in line)):
				newText.write("<_tag_" + currentSection.strip() + "_solvedissues>\n")
				continue
			if (line.startswith("Migration, Upgrade, and Downgrade Instructions") and (documentBegins) and ("|" not in line)):
				newText.write("<_tag_" + currentSection.strip() + "_instructions>\n")
				continue
		currentText.close()
		newText.close()


##############
#Main Program
##############

if __name__ == "__main__":
   print ("Script starts")
   doc_tagging()
   print("Script finished")