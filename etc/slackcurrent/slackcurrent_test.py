from sys import path
path.append("/usr/sbin")

import unittest
import slackcurrent

class PackagesTests(unittest.TestCase):
	def testDoc(self):
		print "Doc test"
		p1 = slackcurrent.SlackPack("xyz-lib-1.23.45brc6-i386-1.tgz")
		p2 = slackcurrent.SlackPack("xyz-lib-1.23.45crc6-i386-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testBuild(self):
		print "Build test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23-i486-2.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testRc(self):
		print "RC test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23rc1-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23rc2-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testTwoTokens(self):
		print "2 tokens test"
		p1 = slackcurrent.SlackPack("libidn-1.5-i486-1.tgz")
		p2 = slackcurrent.SlackPack("libidn-1.6-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testThreeTokens(self):
		print "3 tokens test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.24-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testFourTokens(self):
		print "4 tokens test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23.12-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23.16-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testThreeTokensChar(self):
		print "3 tokens with char test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23a-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23b-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testFourTokensChar(self):
		print "4 tokens char test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23.12a-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23.12b-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testThreeTokensCharBuild(self):
		print "3 tokens with char and build test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23b-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23b-i486-2.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testFourTokensCharBuild(self):
		print "4 tokens char and build test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23.12b-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23.12b-i486-2.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testThreeTokensCharBuildRc(self):
		print "3 tokens with char, build and rc test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23brc1-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23brc2-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testFourTokensCharBuild(self):
		print "4 tokens char and build test"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23.12brc1-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23.12brc2-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

	def testTrevor(self):
		print "Testing the packages that Trevor warned me"
		p1 = slackcurrent.SlackPack("kernel-generic-2.6.23.12-i486-1.tgz")
		p2 = slackcurrent.SlackPack("kernel-generic-2.6.23.16-i486-1.tgz")
		print "testing "+p1.file+" ("+str(p1.cversion)+") and "+p2.file+" ("+str(p2.cversion)+")"
		assert p1<p2, "\n"+str(p1.cversion)+" greater than\n"+str(p2.cversion)

		p3 = slackcurrent.SlackPack("kernel-generic-smp-2.6.23.12_smp-i686-1.tgz")
		p4 = slackcurrent.SlackPack("kernel-generic-smp-2.6.23.16_smp-i686-1.tgz")
		print "testing "+p3.file+" ("+str(p3.cversion)+") and "+p4.file+" ("+str(p4.cversion)+")"
		assert p3<p4, "\n"+str(p3.cversion)+" greater than\n"+str(p4.cversion)

		p5 = slackcurrent.SlackPack("kernel-headers-2.6.23.12_smp-i386-1.tgz")
		p6 = slackcurrent.SlackPack("kernel-headers-2.6.23.16_smp-i386-1.tgz")
		print "testing "+p5.file+" ("+str(p5.cversion)+") and "+p6.file+" ("+str(p6.cversion)+")"
		assert p5<p6, "\n"+str(p5.cversion)+" greater than\n"+str(p6.cversion)

		p7 = slackcurrent.SlackPack("kernel-huge-2.6.23.12-i486-1.tgz")
		p8 = slackcurrent.SlackPack("kernel-huge-2.6.23.16-i486-1.tgz")
		print "testing "+p7.file+" ("+str(p7.cversion)+") and "+p8.file+" ("+str(p8.cversion)+")"
		assert p7<p8, "\n"+str(p7.cversion)+" greater than\n"+str(p8.cversion)

		p9 = slackcurrent.SlackPack("kernel-huge-smp-2.6.23.12_smp-i686-1.tgz")
		p10 = slackcurrent.SlackPack("kernel-huge-smp-2.6.23.16_smp-i686-1.tgz")
		print "testing "+p9.file+" ("+str(p9.cversion)+") and "+p10.file+" ("+str(p10.cversion)+")"
		assert p9<p10, "\n"+str(p9.cversion)+" greater than\n"+str(p10.cversion)

		p11 = slackcurrent.SlackPack("kernel-modules-2.6.23.12-i486-1.tgz")
		p12 = slackcurrent.SlackPack("kernel-modules-2.6.23.16-i486-1.tgz")
		print "testing "+p11.file+" ("+str(p11.cversion)+") and "+p12.file+" ("+str(p12.cversion)+")"
		assert p11<p12, "\n"+str(p11.cversion)+" greater than\n"+str(p12.cversion)

		p13 = slackcurrent.SlackPack("kernel-modules-smp-2.6.23.12_smp-i686-1.tgz")
		p14 = slackcurrent.SlackPack("kernel-modules-smp-2.6.23.16_smp-i686-1.tgz")
		print "testing "+p13.file+" ("+str(p13.cversion)+") and "+p14.file+" ("+str(p14.cversion)+")"
		assert p13<p14, "\n"+str(p13.cversion)+" greater than\n"+str(p14.cversion)

		p15 = slackcurrent.SlackPack("kernel-source-2.6.23.12_smp-noarch-1.tgz")
		p16 = slackcurrent.SlackPack("kernel-source-2.6.23.16_smp-noarch-1.tgz")
		print "testing "+p15.file+" ("+str(p15.cversion)+") and "+p16.file+" ("+str(p16.cversion)+")"
		assert p15<p16, "\n"+str(p15.cversion)+" greater than\n"+str(p16.cversion)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
