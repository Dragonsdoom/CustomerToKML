import unittest as ut
import dao_test
import kml_test
import geocode_test

daosuite = ut.TestLoader().loadTestsFromTestCase(dao_test.TestDAO)
kmlsuite = ut.TestLoader().loadTestsFromTestCase(kml_test.TestKML)
geocodesuite = ut.TestLoader().loadTestsFromTestCase(geocode_test.TestGeocoder)
alltestsuite = ut.TestSuite([daosuite, kmlsuite, geocodesuite])
ut.TextTestRunner(verbosity=2).run(alltestsuite)