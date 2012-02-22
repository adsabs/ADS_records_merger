# coding=UTF-8
# Copyright (C) 2011, The SAO/NASA Astrophysics Data System
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
@author: Giovanni Di Milia and Benoit Thiell
File containing an example of the steps that should be taken (and better coded) before using the merger
'''

try:
    from invenio.bibrecord import create_records
except ImportError:
    import sys
    sys.path.append('/proj/adsx/invenio/lib/python/')
    from invenio.bibrecord import create_records

#XML string from ADSExports
#MarcXML after transormation with new xslt
marcxml = """
<?xml version="1.0" encoding="UTF-8"?>
<collections>
  <collection>
    <record>
      <datafield tag="024" ind1="7" ind2="">
        <subfield code="a">10.1086/175729</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="970" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="035" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">STI</subfield>
        <subfield code="9">ADS bibcode</subfield>
      </datafield>
      <datafield tag="100" ind1="" ind2="">
        <subfield code="a">Armus, L.</subfield>
        <subfield code="b">Armus, L</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="u">Palomar Observatory, California Institute of Technology, Pasadena, CA, US</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Heckman, T. M.</subfield>
        <subfield code="b">Heckman, T</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="u">Palomar Observatory, California Institute of Technology, Pasadena, CA, US</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Weaver, K. A.</subfield>
        <subfield code="b">Weaver, K</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="u">Pennsylvania State University, University Park, PA, US</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Lehnert, M. D.</subfield>
        <subfield code="b">Lehnert, M</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="u">Pennsylvania State University, University Park, PA, US</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="245" ind1="" ind2="">
        <subfield code="a">ROSAT observations of NGC 2146: Evidence for a starburst-driven superwind</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="260" ind1="" ind2="">
        <subfield code="c">1995-06-00</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="520" ind1="" ind2="">
        <subfield code="a">We have imaged the edge-on starburst galaxy NGC 2146 with the Position Sensitive Proportional Counter (PSPC) and the High Resolution Imager (HRI) on board ROSAT and have compared these data to optical images and long-slit spectra. NGC 2146 possesses a very large X-ray nebula with a half-light radius of 1 min (4 kpc) and a maximum diameter of approximately 4 min, or 17 kpc. The X-ray emission is resolved by the PSPC and preferentially oriented along the minor axis, with a total flux of 1.1 x 10&lt;SUP&gt;-12&lt;/SUP&gt; ergs/sq cm/s over 0.2 - 2.4 keV and a luminosity of approximately 3 x 10&lt;SUP&gt;40&lt;/SUP&gt; ergs/s. The inner X-ray nebula is resolved by the HRI into at least four bright knots together with strong diffuse emission responsible for at least 50% of the flux within a radius of 0.5 min (approximately 2 kpc). The brightest knot has a luminosity of (2 - 3) x 10&lt;SUP&gt;39&lt;/SUP&gt; ergs/s. The X-ray nebula has a spatial extent much larger than the starburst ridge seen at centimeter wavelengths by Kronberg &amp; Biermann (1981) and is oriented in a `X-like' pattern along the galaxy minor axis at a position angle of approximately 30 degrees. This minor-axis X-ray emission is associated with a region of H alpha and dust filaments seen in optical images. Optical spectra show that the emission-line gas along the minor axis is characterized by relatively broad lines (approximately 250 km/s full width half-maximum (FWHM)) and by `shocklike' emission-line flux ratios. Together with the blue-asymmetric nuclear emission-line and NaD interstellar absorption-line profiles, these optical data strongly suggest the presence of a starburst-driven superwind. The X-ray spectrum extracted from the central 5 min contains a strong Fe L emission-line complex at 0.6 - 1.0 keV and a hard excess above 1.0 keV. The spectrum is best described with a two-component model, containing a soft (kT approximately 400 - 500 eV) Raymond-Smith thermal plasma together with either a Gamma = 1.7 power-law or a kT greater than 2.2 keV bremsstrahlung component. The soft thermal component provides approximately 30% of the total luminosity over 0.2 - 2.4 keV, or approximately 10&lt;SUP&gt;40&lt;/SUP&gt; ergs/s. The pressure derived from the soft component of the X-ray spectrum is consistent with that predicted from a starburst-driven superwind if the filling factor of the warm gas is approximately 1% - 10 %. If the hard X-ray component is thermal gas associated with the galactic outflow, the filling factor must be close to unity. Predictions of the luminosity, temperature, and size of an adiabatic starburst-generated windblown bubble are consistent with those measured for the soft thermal X-ray emission in NGC 2146. The hard X-ray component, however, has a luminosity much larger than predicted by the superwind model if this component is thermal emission from gas heated by an internal shock in the expanding bubble. We briefly review various possibilities as to the nature of the hard X-ray component in NGC 2146.</subfield>
        <subfield code="y">en</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="773" ind1="" ind2="">
        <subfield code="p">Astrophysical Journal</subfield>
        <subfield code="v">445</subfield>
        <subfield code="n">2</subfield>
        <subfield code="c">666-679</subfield>
        <subfield code="y">1995</subfield>
        <subfield code="d">1995-06-00</subfield>
        <subfield code="z">Astrophysical Journal, Part 1 (ISSN 0004-637X), vol. 445, no. 2, p. 666-679</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
      <datafield tag="961" ind1="" ind2="">
        <subfield code="c">2011-07-22T14:00:01</subfield>
        <subfield code="x">2011-07-22T14:00:01</subfield>
        <subfield code="8">STI</subfield>
      </datafield>
    </record>
    <record>
      <datafield tag="970" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="035" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
        <subfield code="9">ADS bibcode</subfield>
      </datafield>
      <datafield tag="100" ind1="" ind2="">
        <subfield code="a">Armus, L.</subfield>
        <subfield code="b">Armus, L</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Heckman, T. M.</subfield>
        <subfield code="b">Heckman, T</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Weaver, K. A.</subfield>
        <subfield code="b">Weaver, K</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Lehnert, M. D.</subfield>
        <subfield code="b">Lehnert, M</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="245" ind1="" ind2="">
        <subfield code="a">ROSAT Observations of NGC 2146: Evidence for a Starburst-driven Superwind</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="260" ind1="" ind2="">
        <subfield code="c">1995-06-00</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="520" ind1="" ind2="">
        <subfield code="a">We have imaged the edge-on starburst galaxy NGC 2146 with the Position Sensitive Proportional Counter (PSPC) and the High Resolution Imager (HRI) on board ROSAT and have compared these data to optical images and long-slit spectra. NGC 2146 possesses a very large X-ray nebula with a half-light radius of 1' (4 kpc) and a maximum diameter of ~4', or 17 kpc. The X-ray emission is resolved by the PSPC and preferentially oriented along the minor axis, with a total flux of 1.1 x 10^-12^ ergs cm^-2^ s^- 1^ over 0.2-2.4 keV and a luminosity of ~3 x 10^40^ ergs s^-1^. The inner X-ray nebula is resolved by the HRI into at least four bright knots together with strong diffuse emission responsible for at least 50% of the flux within a radius of 0.5' (~2 kpc). The brightest knot has a luminosity of (2-3) x 10^39^ ergs s^-1^. The X-ray nebula has a spatial extent much larger than the starburst ridge seen at centimeter wavelengths by Kronberg &amp; Biermann (1981) and is oriented in a "X-like" pattern along the galaxy minor axis at a position angle of ~30^deg^. This minor-axis X-ray emission is associated with a region of Hα and dust filaments seen in optical images. Optical spectra show that the emission-line gas along the minor axis is characterized by relatively broad lines (~250 km s^-1^ FWHM) and by "shocklike" emission-line flux ratios. Together with the blue-asymmetric nuclear emission-line and NaD interstellar absorption-line profiles, these optical data strongly suggest the presence of a starburst-driven superwind. The X-ray spectrum extracted from the central 5' contains a strong Fe L emission-line complex at 0.6-1.0 keV and a hard excess above 1.0 keV. The spectrum is best described with a two-component model, containing a soft (kT~400-500 eV) Raymond-Smith thermal plasma together with either a {GAMMA} = 1.7 power-law or a kT 〉 2.2 keV bremsstrahlung component. The soft thermal component provides 30% of the total luminosity over 0.2-2.4 keV, or ~10^40^ ergs s^-1^. The pressure derived from the soft component of the X-ray spectrum is consistent with that predicted from a starburst-driven superwind if the filling factor of the warm gas is ~1%-10%. If the hard X-ray component is thermal gas associated with the galactic outflow, the filling factor must be close to unity. Predictions of the luminosity, temperature, and size of an adiabatic starburst-generated windblown bubble are consistent with those measured for the soft thermal X-ray emission in NGC 2146. The hard X-ray component, however, has a luminosity much larger than predicted by the superwind model if this component is thermal emission from gas heated by an internal shock in the expanding bubble. We briefly review various possibilities as to the nature of the hard X-ray component in NGC 2146.</subfield>
        <subfield code="y">en</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="773" ind1="" ind2="">
        <subfield code="p">Astrophysical Journal v.445</subfield>
        <subfield code="v">445</subfield>
        <subfield code="c">666</subfield>
        <subfield code="y">1995</subfield>
        <subfield code="d">1995-06-00</subfield>
        <subfield code="z">Astrophysical Journal v.445, p.666</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
      <datafield tag="961" ind1="" ind2="">
        <subfield code="c">2011-10-06T18:11:12</subfield>
        <subfield code="x">2011-10-06T18:11:12</subfield>
        <subfield code="8">APJ; KNUDSEN; NED</subfield>
      </datafield>
    </record>
    <record>
      <datafield tag="970" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="035" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">SIMBAD</subfield>
        <subfield code="9">ADS bibcode</subfield>
      </datafield>
      <datafield tag="100" ind1="" ind2="">
        <subfield code="a">Armus, L.</subfield>
        <subfield code="b">Armus, L</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Heckman, T. M.</subfield>
        <subfield code="b">Heckman, T</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Weaver, K. A.</subfield>
        <subfield code="b">Weaver, K</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="700" ind1="" ind2="">
        <subfield code="a">Lehnert, M. D.</subfield>
        <subfield code="b">Lehnert, M</subfield>
        <subfield code="e">regular</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="245" ind1="" ind2="">
        <subfield code="a">ROSAT observations of NGC 2146 : evidence for a starburst-driven superwind.</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="260" ind1="" ind2="">
        <subfield code="c">1995-06-00</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="773" ind1="" ind2="">
        <subfield code="p">Astrophysical Journal</subfield>
        <subfield code="v">445</subfield>
        <subfield code="c">666</subfield>
        <subfield code="y">1995</subfield>
        <subfield code="d">1995-06-00</subfield>
        <subfield code="z">Astrophysical Journal, 445, 666-679 (1995)</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
      <datafield tag="961" ind1="" ind2="">
        <subfield code="c">2011-11-16T00:56:30</subfield>
        <subfield code="x">2011-11-16T00:56:30</subfield>
        <subfield code="8">SIMBAD</subfield>
      </datafield>
    </record>
    <record>
      <datafield tag="970" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="035" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8"/>
        <subfield code="9">ADS bibcode</subfield>
      </datafield>
      <datafield tag="980" ind1="" ind2="">
        <subfield code="a">ASTRONOMY</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="980" ind1="" ind2="">
        <subfield code="a">OPENACCESS</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="980" ind1="" ind2="">
        <subfield code="a">REFEREED</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="980" ind1="" ind2="">
        <subfield code="a">ARTICLE</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="995" ind1="" ind2="">
        <subfield code="a">{'refs': [{'p': '/proj/ads/references/resolved/ApJ/0445/1995ApJ...445..666A.ref.ocr.txt.result', 't': 1316020829}, {'p': '/proj/ads/references/resolved/ISI/ApJ/ApJ0445.isi.pairs.result', 't': 1302279890}], 'abs': [{'p': '/proj/ads/abstracts/ast/text/A95/A95-93282.abs', 't': '1311357601'}, {'p': '/proj/ads/abstracts/ast/text/J95/J95-93282.abs', 't': '1317939072'}, {'p': '/proj/ads/abstracts/ast/text/S95/S95-93282.abs', 't': '1298489706'}], 'links': {'simbad': [{'c': '4', 'u': 'http://$SIMBAD$/simbo.pl?bibcode=1995ApJ...445..666A'}], 'ned': [{'c': '1', 'u': 'http://$NED$/cgi-bin/nph-objsearch?search_type=Search&amp;refcode=1995ApJ...445..666A'}], 'data': [{'u': 'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=1995ApJ...445..666A'}]}, 'full': {'p': '/proj/ads/fulltext/extracted/19/95/Ap/J,/,,/44/5,/,6/66/A//body.txt', 't': 1313691075}, 'prop': ['article', 'bibgroup: ROSAT', 'refereed']}</subfield>
        <subfield code="8"/>
      </datafield>
    </record>
    <record>
      <datafield tag="970" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="035" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8"/>
        <subfield code="9">ADS bibcode</subfield>
      </datafield>
      <datafield tag="961" ind1="" ind2="">
        <subfield code="c">2011-09-14T13:20:29</subfield>
        <subfield code="x">2011-09-14T13:20:29</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[1]</subfield>
        <subfield code="r">1989ApJ...347..727A</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Armus, L., Heckman, T. M., &amp; Miley, 0. K. 1989, ApJ, 347,727 (AHM89)</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[2]</subfield>
        <subfield code="r">1990ApJ...364..471A</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">---.1990, ApJ, 364,471</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[3]</subfield>
        <subfield code="r">1975A&amp;amp;A....41...91B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Benvenuti, P., Capaccioli, M., &amp; D Odorico, S. 1975, A&amp;A, 41,91</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[4]</subfield>
        <subfield code="r">1993A&amp;amp;A...268...25B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Bernlohr, K. 1993a, A&amp;A, 268,25</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[5]</subfield>
        <subfield code="r">1993A&amp;amp;A...270...20B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">---1993b, A&amp;A, 270,20</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[6]</subfield>
        <subfield code="r">1969drea.book.....B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Bevington, P. R. 1969, Data Reduction and Error Analysis for the Physical Sciences (New York: McGraw-Hill)</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[7]</subfield>
        <subfield code="r">1982AJ.....87.1165B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Burstein, D., &amp; Heiles, C. 1982, AJ, 87, 1165</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[8]</subfield>
        <subfield code="r">1975ApJ...200L.107C</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Castor, J., McCray, R., &amp; Weaver, R. 1975, ApJ, 200, L107</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[9]</subfield>
        <subfield code="r">1985Natur.317...44C</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Chevalier, R. A., &amp; Clegg, A. W. 1985, Nature, 317,44</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[10]</subfield>
        <subfield code="e">0</subfield>
        <subfield code="m">Dahlem, M., Heckman, T. M., Fabbiano, 0., &amp; Gilmore, D. 1995, in preparation</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[11]</subfield>
        <subfield code="r">1988ApJ...330..672F</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Fabbiano, 0. 1988, ApJ, 330, 672</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[12]</subfield>
        <subfield code="r">1990ApJ...355..442F</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Fabbiano, 0., Heckman, T. M., &amp; Keel, W. C. 1990, ApJ, 355,442</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[13]</subfield>
        <subfield code="r">1984ApJ...286..491F</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Fabbiano, 0., &amp; Trinchieri, 0. 1984, ApJ, 286,491</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[14]</subfield>
        <subfield code="e">0</subfield>
        <subfield code="m">Hasinger, 0., Turner, T. J., George, I. M., &amp; Boese, 0. 1992, Legacy, 2,77</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[15]</subfield>
        <subfield code="r">1990ApJS...74..833H</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Heckman, T. M., Armus, L., &amp; Miley, 0. K. 1990, ApJS, 74,833</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[16]</subfield>
        <subfield code="e">0</subfield>
        <subfield code="m">Heckman, T. M., Lehnert, M. D., &amp; Armus, L. 1993, in The Evolution of Galaxies and Their Environments, ed. S. M. Shull &amp; H. Thronson (Dordrecht: Kluwer), 455 (HLA93)</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[17]</subfield>
        <subfield code="r">1990AJ....100...60H</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Hutchings, J. B., Neff, S. 0., Stanford, S. A., Lo, E., &amp; Unger, S. W. 1990, AJ, 100,60</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[18]</subfield>
        <subfield code="r">1992ApJ...393..134K</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Kim, D.-W., Fabbiano, 0., &amp; Trinchieri, 0. 1992, ApJ, 393, 134</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[19]</subfield>
        <subfield code="r">1992ApJ...388..103K</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Koo, B.-C. &amp; McKee, C. 1992, ApJ, 388, 103</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[20]</subfield>
        <subfield code="r">1981ApJ...243...89K</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Kronberg, P. P., &amp; Biermann, P. 1981, ApJ, 243,89</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[21]</subfield>
        <subfield code="r">1995ApJS...97...89L</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Lehnert, M. D., &amp; Heckman, T. M. 1995, ApJS, 97,89</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[22]</subfield>
        <subfield code="e">0</subfield>
        <subfield code="m">Lehnert, M. D., et al. 1995, in preparation</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[23]</subfield>
        <subfield code="r">1995ApJS...96....9L</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Leitherer, C., &amp; Heckman, T. M. 1995, ApJS, 96,9</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[24]</subfield>
        <subfield code="r">1989agna.book.....O</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Osterbrock, D. E. 1989, Astrophysics, ofGaseous Nebulae and Active Galactic Nuclei (Mill Valley: University Science)</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[25]</subfield>
        <subfield code="r">1992pngn.conf...67P</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Peitsch, W. 1993, in The Physics of Nearby Galaxies: Nurture or Nature? ed. T. X. Thuan, C. Balkowski, &amp; J. T. T. Van (Paris: Editions Frontieres), 67</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[26]</subfield>
        <subfield code="r">1993nag..conf..117P</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Petre, R. 1993, in The Nearest Active Galaxies, ed. J. Beckman, L. Colina, &amp; H. Netzer (Madrid: Consejo Superior de Investigaciones Cientificas), 117</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[27]</subfield>
        <subfield code="r">1993AJ....105..486P</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Phillips, A. C. 1993, AJ, 105,486</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[28]</subfield>
        <subfield code="r">1994ApJ...423L..35P</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Prada, F., Beckman, J. E., McKeith, C. D., Castles, J., &amp; Greve, A. 1994, ApJ, 423, L35</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[29]</subfield>
        <subfield code="r">1977ApJS...35..419R</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Raymond, J. C., &amp; Smith, B. 1977, ApJS, 35,419</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[30]</subfield>
        <subfield code="r">1993ApJ...412...99R</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Rieke, 0. H., Loken, K., Rieke, M. J., &amp; Tamblyn, P. 1993, ApJ, 412,99</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[31]</subfield>
        <subfield code="r">1989ApJ...336..722S</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Schaaf, R., Petisch, P., Biermann, P., Kronberg, P. P., &amp; Schmutzler, T. 1989, ApJ, 336, 732</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[32]</subfield>
        <subfield code="r">1994ApJ...424L..99S</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Schlegel, E. M. 1994, ApJ, 424, L99</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[33]</subfield>
        <subfield code="r">1991ApJ...369..320S</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Seaquist, E., &amp; Odegrad, N. 1991, ApJ, 369, 320</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[34]</subfield>
        <subfield code="e">5</subfield>
        <subfield code="m">Shafer, R. A., Haberl, F., &amp; Arnaud, K. A. 1989, in XSPEC: An X-Ray Spectral Fitting Package (ESA TM-09; Paris: ESA)</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[35]</subfield>
        <subfield code="r">1994ApJ...430..511S</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Suchkov, A., Balsara, D., Heckman, T. M., &amp; Leitherer, C. 1994, ApJ, 430,511</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[36]</subfield>
        <subfield code="r">1987ApJS...63..295V</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Veilleux, S., &amp; Osterbrock, D. E. 1987, ApJS, 63, 295</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[37]</subfield>
        <subfield code="r">1984ApJ...286..144W</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Watson, M., Stanger, V., &amp; Griffiths, R. 1984, ApJ, 286, 144</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[38]</subfield>
        <subfield code="r">1988ApJ...331L..81Y</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">Young, J. S., Claussen, M. J., Kleinmann, S. 0., Rubin, V. C., &amp; Scoville, N. 1988, ApJ, 331, L81</subfield>
        <subfield code="8"/>
      </datafield>
    </record>
    <record>
      <datafield tag="970" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="035" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8"/>
        <subfield code="9">ADS bibcode</subfield>
      </datafield>
      <datafield tag="961" ind1="" ind2="">
        <subfield code="c">2011-04-08T12:24:50</subfield>
        <subfield code="x">2011-04-08T12:24:50</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[1]</subfield>
        <subfield code="r">1981ApJ...243...89K</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1981ApJ...243...89K</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[2]</subfield>
        <subfield code="r">1982AJ.....87.1165B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1982AJ.....87.1165B</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[3]</subfield>
        <subfield code="r">1984ApJ...286..144W</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1984ApJ...286..144W</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[4]</subfield>
        <subfield code="r">1984ApJ...286..491F</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1984ApJ...286..491F</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[5]</subfield>
        <subfield code="r">1985Natur.317...44C</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1985Natur.317...44C</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[6]</subfield>
        <subfield code="r">1987ApJS...63..295V</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1987ApJS...63..295V</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[7]</subfield>
        <subfield code="r">1988ApJ...330..672F</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1988ApJ...330..672F</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[8]</subfield>
        <subfield code="r">1988ApJ...331L..81Y</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1988ApJ...331L..81Y</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[9]</subfield>
        <subfield code="r">1989ApJ...347..727A</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1989ApJ...347..727A</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[10]</subfield>
        <subfield code="r">1990AJ....100...60H</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1990AJ....100...60H</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[11]</subfield>
        <subfield code="r">1990ApJ...355..442F</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1990ApJ...355..442F</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[12]</subfield>
        <subfield code="r">1990ApJ...364..471A</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1990ApJ...364..471A</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[13]</subfield>
        <subfield code="r">1990ApJS...74..833H</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1990ApJS...74..833H</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[14]</subfield>
        <subfield code="r">1991ApJ...369..320S</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1991ApJ...369..320S</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[15]</subfield>
        <subfield code="r">1992ApJ...388..103K</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1992ApJ...388..103K</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[16]</subfield>
        <subfield code="r">1992ApJ...393..134K</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1992ApJ...393..134K</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[17]</subfield>
        <subfield code="r">1993A&amp;amp;A...268...25B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1993A&amp;A...268...25B</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[18]</subfield>
        <subfield code="r">1993A&amp;amp;A...270...20B</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1993A&amp;A...270...20B</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[19]</subfield>
        <subfield code="r">1993AJ....105..486P</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1993AJ....105..486P</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[20]</subfield>
        <subfield code="r">1993ApJ...412...99R</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1993ApJ...412...99R</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[21]</subfield>
        <subfield code="r">1994ApJ...423L..35P</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1994ApJ...423L..35P</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[22]</subfield>
        <subfield code="r">1994ApJ...424L..99S</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1994ApJ...424L..99S</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[23]</subfield>
        <subfield code="r">1994ApJ...430..511S</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1994ApJ...430..511S</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[24]</subfield>
        <subfield code="r">1995ApJS...96....9L</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1995ApJS...96....9L</subfield>
        <subfield code="8"/>
      </datafield>
      <datafield tag="999" ind1="C" ind2="5">
        <subfield code="o">[25]</subfield>
        <subfield code="r">1995ApJS...97...89L</subfield>
        <subfield code="e">1</subfield>
        <subfield code="m">1995ApJS...97...89L</subfield>
        <subfield code="8"/>
      </datafield>
    </record>
    <record>
      <datafield tag="970" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">x</subfield>
      </datafield>
      <datafield tag="035" ind1="" ind2="">
        <subfield code="a">1995ApJ...445..666A</subfield>
        <subfield code="8">x</subfield>
        <subfield code="9">ADS bibcode</subfield>
      </datafield>
      <datafield tag="856" ind1="4" ind2="">
        <subfield code="u">http://$SIMBAD$/simbo.pl?bibcode=1995ApJ...445..666A</subfield>
        <subfield code="y">simbad</subfield>
        <subfield code="8">x</subfield>
      </datafield>
      <datafield tag="856" ind1="4" ind2="">
        <subfield code="u">http://$NED$/cgi-bin/nph-objsearch?search_type=Search&amp;refcode=1995ApJ...445..666A</subfield>
        <subfield code="y">ned</subfield>
        <subfield code="8">x</subfield>
      </datafield>
      <datafield tag="856" ind1="4" ind2="">
        <subfield code="u">http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=1995ApJ...445..666A</subfield>
        <subfield code="y">data</subfield>
        <subfield code="8">x</subfield>
      </datafield>
      <datafield tag="856" ind1="4" ind2="">
        <subfield code="u">http://adsabs.harvard.edu/abs/1995ApJ...445..666A</subfield>
        <subfield code="y">ADSlink</subfield>
        <subfield code="8">x</subfield>
      </datafield>
    </record>
  </collection>
</collections>
"""

#I split the different collections inside the marcxml
collection = """
<collection>
  <record>
    <datafield tag="024" ind1="7" ind2="">
      <subfield code="a">10.1086/175729</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="970" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
      <subfield code="9">ADS bibcode</subfield>
    </datafield>
    <datafield tag="100" ind1="" ind2="">
      <subfield code="a">Armus, L.</subfield>
      <subfield code="b">Armus, L</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="u">Palomar Observatory, California Institute of Technology, Pasadena, CA, US</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Heckman, T. M.</subfield>
      <subfield code="b">Heckman, T</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="u">Palomar Observatory, California Institute of Technology, Pasadena, CA, US</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Weaver, K. A.</subfield>
      <subfield code="b">Weaver, K</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="u">Pennsylvania State University, University Park, PA, US</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Lehnert, M. D.</subfield>
      <subfield code="b">Lehnert, M</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="u">Pennsylvania State University, University Park, PA, US</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="245" ind1="" ind2="">
      <subfield code="a">ROSAT observations of NGC 2146: Evidence for a starburst-driven superwind</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="260" ind1="" ind2="">
      <subfield code="c">1995-06-00</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="520" ind1="" ind2="">
      <subfield code="a">We have imaged the edge-on starburst galaxy NGC 2146 with the Position Sensitive Proportional Counter (PSPC) and the High Resolution Imager (HRI) on board ROSAT and have compared these data to optical images and long-slit spectra. NGC 2146 possesses a very large X-ray nebula with a half-light radius of 1 min (4 kpc) and a maximum diameter of approximately 4 min, or 17 kpc. The X-ray emission is resolved by the PSPC and preferentially oriented along the minor axis, with a total flux of 1.1 x 10&lt;SUP&gt;-12&lt;/SUP&gt; ergs/sq cm/s over 0.2 - 2.4 keV and a luminosity of approximately 3 x 10&lt;SUP&gt;40&lt;/SUP&gt; ergs/s. The inner X-ray nebula is resolved by the HRI into at least four bright knots together with strong diffuse emission responsible for at least 50% of the flux within a radius of 0.5 min (approximately 2 kpc). The brightest knot has a luminosity of (2 - 3) x 10&lt;SUP&gt;39&lt;/SUP&gt; ergs/s. The X-ray nebula has a spatial extent much larger than the starburst ridge seen at centimeter wavelengths by Kronberg &amp; Biermann (1981) and is oriented in a `X-like' pattern along the galaxy minor axis at a position angle of approximately 30 degrees. This minor-axis X-ray emission is associated with a region of H alpha and dust filaments seen in optical images. Optical spectra show that the emission-line gas along the minor axis is characterized by relatively broad lines (approximately 250 km/s full width half-maximum (FWHM)) and by `shocklike' emission-line flux ratios. Together with the blue-asymmetric nuclear emission-line and NaD interstellar absorption-line profiles, these optical data strongly suggest the presence of a starburst-driven superwind. The X-ray spectrum extracted from the central 5 min contains a strong Fe L emission-line complex at 0.6 - 1.0 keV and a hard excess above 1.0 keV. The spectrum is best described with a two-component model, containing a soft (kT approximately 400 - 500 eV) Raymond-Smith thermal plasma together with either a Gamma = 1.7 power-law or a kT greater than 2.2 keV bremsstrahlung component. The soft thermal component provides approximately 30% of the total luminosity over 0.2 - 2.4 keV, or approximately 10&lt;SUP&gt;40&lt;/SUP&gt; ergs/s. The pressure derived from the soft component of the X-ray spectrum is consistent with that predicted from a starburst-driven superwind if the filling factor of the warm gas is approximately 1% - 10 %. If the hard X-ray component is thermal gas associated with the galactic outflow, the filling factor must be close to unity. Predictions of the luminosity, temperature, and size of an adiabatic starburst-generated windblown bubble are consistent with those measured for the soft thermal X-ray emission in NGC 2146. The hard X-ray component, however, has a luminosity much larger than predicted by the superwind model if this component is thermal emission from gas heated by an internal shock in the expanding bubble. We briefly review various possibilities as to the nature of the hard X-ray component in NGC 2146.</subfield>
      <subfield code="y">en</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="773" ind1="" ind2="">
      <subfield code="p">Astrophysical Journal</subfield>
      <subfield code="v">445</subfield>
      <subfield code="n">2</subfield>
      <subfield code="c">666-679</subfield>
      <subfield code="y">1995</subfield>
      <subfield code="d">1995-06-00</subfield>
      <subfield code="z">Astrophysical Journal, Part 1 (ISSN 0004-637X), vol. 445, no. 2, p. 666-679</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
    <datafield tag="961" ind1="" ind2="">
      <subfield code="c">2011-07-22T14:00:01</subfield>
      <subfield code="x">2011-07-22T14:00:01</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="970" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
      <subfield code="9">ADS bibcode</subfield>
    </datafield>
    <datafield tag="100" ind1="" ind2="">
      <subfield code="a">Armus, L.</subfield>
      <subfield code="b">Armus, L</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Heckman, T. M.</subfield>
      <subfield code="b">Heckman, T</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Weaver, K. A.</subfield>
      <subfield code="b">Weaver, K</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Lehnert, M. D.</subfield>
      <subfield code="b">Lehnert, M</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="245" ind1="" ind2="">
      <subfield code="a">ROSAT Observations of NGC 2146: Evidence for a Starburst-driven Superwind</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="260" ind1="" ind2="">
      <subfield code="c">1995-06-00</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="520" ind1="" ind2="">
      <subfield code="a">We have imaged the edge-on starburst galaxy NGC 2146 with the Position Sensitive Proportional Counter (PSPC) and the High Resolution Imager (HRI) on board ROSAT and have compared these data to optical images and long-slit spectra. NGC 2146 possesses a very large X-ray nebula with a half-light radius of 1' (4 kpc) and a maximum diameter of ~4', or 17 kpc. The X-ray emission is resolved by the PSPC and preferentially oriented along the minor axis, with a total flux of 1.1 x 10^-12^ ergs cm^-2^ s^- 1^ over 0.2-2.4 keV and a luminosity of ~3 x 10^40^ ergs s^-1^. The inner X-ray nebula is resolved by the HRI into at least four bright knots together with strong diffuse emission responsible for at least 50% of the flux within a radius of 0.5' (~2 kpc). The brightest knot has a luminosity of (2-3) x 10^39^ ergs s^-1^. The X-ray nebula has a spatial extent much larger than the starburst ridge seen at centimeter wavelengths by Kronberg &amp; Biermann (1981) and is oriented in a "X-like" pattern along the galaxy minor axis at a position angle of ~30^deg^. This minor-axis X-ray emission is associated with a region of Hα and dust filaments seen in optical images. Optical spectra show that the emission-line gas along the minor axis is characterized by relatively broad lines (~250 km s^-1^ FWHM) and by "shocklike" emission-line flux ratios. Together with the blue-asymmetric nuclear emission-line and NaD interstellar absorption-line profiles, these optical data strongly suggest the presence of a starburst-driven superwind. The X-ray spectrum extracted from the central 5' contains a strong Fe L emission-line complex at 0.6-1.0 keV and a hard excess above 1.0 keV. The spectrum is best described with a two-component model, containing a soft (kT~400-500 eV) Raymond-Smith thermal plasma together with either a {GAMMA} = 1.7 power-law or a kT 〉 2.2 keV bremsstrahlung component. The soft thermal component provides 30% of the total luminosity over 0.2-2.4 keV, or ~10^40^ ergs s^-1^. The pressure derived from the soft component of the X-ray spectrum is consistent with that predicted from a starburst-driven superwind if the filling factor of the warm gas is ~1%-10%. If the hard X-ray component is thermal gas associated with the galactic outflow, the filling factor must be close to unity. Predictions of the luminosity, temperature, and size of an adiabatic starburst-generated windblown bubble are consistent with those measured for the soft thermal X-ray emission in NGC 2146. The hard X-ray component, however, has a luminosity much larger than predicted by the superwind model if this component is thermal emission from gas heated by an internal shock in the expanding bubble. We briefly review various possibilities as to the nature of the hard X-ray component in NGC 2146.</subfield>
      <subfield code="y">en</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="773" ind1="" ind2="">
      <subfield code="p">Astrophysical Journal v.445</subfield>
      <subfield code="v">445</subfield>
      <subfield code="c">666</subfield>
      <subfield code="y">1995</subfield>
      <subfield code="d">1995-06-00</subfield>
      <subfield code="z">Astrophysical Journal v.445, p.666</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
    <datafield tag="961" ind1="" ind2="">
      <subfield code="c">2011-10-06T18:11:12</subfield>
      <subfield code="x">2011-10-06T18:11:12</subfield>
      <subfield code="8">APJ; KNUDSEN; NED</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="970" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
      <subfield code="9">ADS bibcode</subfield>
    </datafield>
    <datafield tag="100" ind1="" ind2="">
      <subfield code="a">Armus, L.</subfield>
      <subfield code="b">Armus, L</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Heckman, T. M.</subfield>
      <subfield code="b">Heckman, T</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Weaver, K. A.</subfield>
      <subfield code="b">Weaver, K</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
    <datafield tag="700" ind1="" ind2="">
      <subfield code="a">Lehnert, M. D.</subfield>
      <subfield code="b">Lehnert, M</subfield>
      <subfield code="e">regular</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
    <datafield tag="245" ind1="" ind2="">
      <subfield code="a">ROSAT observations of NGC 2146 : evidence for a starburst-driven superwind.</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
    <datafield tag="260" ind1="" ind2="">
      <subfield code="c">1995-06-00</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
    <datafield tag="773" ind1="" ind2="">
      <subfield code="p">Astrophysical Journal</subfield>
      <subfield code="v">445</subfield>
      <subfield code="c">666</subfield>
      <subfield code="y">1995</subfield>
      <subfield code="d">1995-06-00</subfield>
      <subfield code="z">Astrophysical Journal, 445, 666-679 (1995)</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
    <datafield tag="961" ind1="" ind2="">
      <subfield code="c">2011-11-16T00:56:30</subfield>
      <subfield code="x">2011-11-16T00:56:30</subfield>
      <subfield code="8">SIMBAD</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="970" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
      <subfield code="9">ADS bibcode</subfield>
    </datafield>
    <datafield tag="980" ind1="" ind2="">
      <subfield code="a">ASTRONOMY</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="980" ind1="" ind2="">
      <subfield code="a">OPENACCESS</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="980" ind1="" ind2="">
      <subfield code="a">REFEREED</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="980" ind1="" ind2="">
      <subfield code="a">ARTICLE</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="995" ind1="" ind2="">
      <subfield code="a">{'refs': [{'p': '/proj/ads/references/resolved/ApJ/0445/1995ApJ...445..666A.ref.ocr.txt.result', 't': 1316020829}, {'p': '/proj/ads/references/resolved/ISI/ApJ/ApJ0445.isi.pairs.result', 't': 1302279890}], 'abs': [{'p': '/proj/ads/abstracts/ast/text/A95/A95-93282.abs', 't': '1311357601'}, {'p': '/proj/ads/abstracts/ast/text/J95/J95-93282.abs', 't': '1317939072'}, {'p': '/proj/ads/abstracts/ast/text/S95/S95-93282.abs', 't': '1298489706'}], 'links': {'simbad': [{'c': '4', 'u': 'http://$SIMBAD$/simbo.pl?bibcode=1995ApJ...445..666A'}], 'ned': [{'c': '1', 'u': 'http://$NED$/cgi-bin/nph-objsearch?search_type=Search&amp;refcode=1995ApJ...445..666A'}], 'data': [{'u': 'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=1995ApJ...445..666A'}]}, 'full': {'p': '/proj/ads/fulltext/extracted/19/95/Ap/J,/,,/44/5,/,6/66/A//body.txt', 't': 1313691075}, 'prop': ['article', 'bibgroup: ROSAT', 'refereed']}</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="970" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
      <subfield code="9">ADS bibcode</subfield>
    </datafield>
    <datafield tag="961" ind1="" ind2="">
      <subfield code="c">2011-09-14T13:20:29</subfield>
      <subfield code="x">2011-09-14T13:20:29</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[1]</subfield>
      <subfield code="r">1989ApJ...347..727A</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Armus, L., Heckman, T. M., &amp; Miley, 0. K. 1989, ApJ, 347,727 (AHM89)</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[2]</subfield>
      <subfield code="r">1990ApJ...364..471A</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">---.1990, ApJ, 364,471</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[3]</subfield>
      <subfield code="r">1975A&amp;amp;A....41...91B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Benvenuti, P., Capaccioli, M., &amp; D Odorico, S. 1975, A&amp;A, 41,91</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[4]</subfield>
      <subfield code="r">1993A&amp;amp;A...268...25B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Bernlohr, K. 1993a, A&amp;A, 268,25</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[5]</subfield>
      <subfield code="r">1993A&amp;amp;A...270...20B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">---1993b, A&amp;A, 270,20</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[6]</subfield>
      <subfield code="r">1969drea.book.....B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Bevington, P. R. 1969, Data Reduction and Error Analysis for the Physical Sciences (New York: McGraw-Hill)</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[7]</subfield>
      <subfield code="r">1982AJ.....87.1165B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Burstein, D., &amp; Heiles, C. 1982, AJ, 87, 1165</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[8]</subfield>
      <subfield code="r">1975ApJ...200L.107C</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Castor, J., McCray, R., &amp; Weaver, R. 1975, ApJ, 200, L107</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[9]</subfield>
      <subfield code="r">1985Natur.317...44C</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Chevalier, R. A., &amp; Clegg, A. W. 1985, Nature, 317,44</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[10]</subfield>
      <subfield code="e">0</subfield>
      <subfield code="m">Dahlem, M., Heckman, T. M., Fabbiano, 0., &amp; Gilmore, D. 1995, in preparation</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[11]</subfield>
      <subfield code="r">1988ApJ...330..672F</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Fabbiano, 0. 1988, ApJ, 330, 672</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[12]</subfield>
      <subfield code="r">1990ApJ...355..442F</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Fabbiano, 0., Heckman, T. M., &amp; Keel, W. C. 1990, ApJ, 355,442</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[13]</subfield>
      <subfield code="r">1984ApJ...286..491F</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Fabbiano, 0., &amp; Trinchieri, 0. 1984, ApJ, 286,491</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[14]</subfield>
      <subfield code="e">0</subfield>
      <subfield code="m">Hasinger, 0., Turner, T. J., George, I. M., &amp; Boese, 0. 1992, Legacy, 2,77</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[15]</subfield>
      <subfield code="r">1990ApJS...74..833H</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Heckman, T. M., Armus, L., &amp; Miley, 0. K. 1990, ApJS, 74,833</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[16]</subfield>
      <subfield code="e">0</subfield>
      <subfield code="m">Heckman, T. M., Lehnert, M. D., &amp; Armus, L. 1993, in The Evolution of Galaxies and Their Environments, ed. S. M. Shull &amp; H. Thronson (Dordrecht: Kluwer), 455 (HLA93)</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[17]</subfield>
      <subfield code="r">1990AJ....100...60H</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Hutchings, J. B., Neff, S. 0., Stanford, S. A., Lo, E., &amp; Unger, S. W. 1990, AJ, 100,60</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[18]</subfield>
      <subfield code="r">1992ApJ...393..134K</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Kim, D.-W., Fabbiano, 0., &amp; Trinchieri, 0. 1992, ApJ, 393, 134</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[19]</subfield>
      <subfield code="r">1992ApJ...388..103K</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Koo, B.-C. &amp; McKee, C. 1992, ApJ, 388, 103</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[20]</subfield>
      <subfield code="r">1981ApJ...243...89K</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Kronberg, P. P., &amp; Biermann, P. 1981, ApJ, 243,89</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[21]</subfield>
      <subfield code="r">1995ApJS...97...89L</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Lehnert, M. D., &amp; Heckman, T. M. 1995, ApJS, 97,89</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[22]</subfield>
      <subfield code="e">0</subfield>
      <subfield code="m">Lehnert, M. D., et al. 1995, in preparation</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[23]</subfield>
      <subfield code="r">1995ApJS...96....9L</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Leitherer, C., &amp; Heckman, T. M. 1995, ApJS, 96,9</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[24]</subfield>
      <subfield code="r">1989agna.book.....O</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Osterbrock, D. E. 1989, Astrophysics, ofGaseous Nebulae and Active Galactic Nuclei (Mill Valley: University Science)</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[25]</subfield>
      <subfield code="r">1992pngn.conf...67P</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Peitsch, W. 1993, in The Physics of Nearby Galaxies: Nurture or Nature? ed. T. X. Thuan, C. Balkowski, &amp; J. T. T. Van (Paris: Editions Frontieres), 67</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[26]</subfield>
      <subfield code="r">1993nag..conf..117P</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Petre, R. 1993, in The Nearest Active Galaxies, ed. J. Beckman, L. Colina, &amp; H. Netzer (Madrid: Consejo Superior de Investigaciones Cientificas), 117</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[27]</subfield>
      <subfield code="r">1993AJ....105..486P</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Phillips, A. C. 1993, AJ, 105,486</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[28]</subfield>
      <subfield code="r">1994ApJ...423L..35P</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Prada, F., Beckman, J. E., McKeith, C. D., Castles, J., &amp; Greve, A. 1994, ApJ, 423, L35</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[29]</subfield>
      <subfield code="r">1977ApJS...35..419R</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Raymond, J. C., &amp; Smith, B. 1977, ApJS, 35,419</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[30]</subfield>
      <subfield code="r">1993ApJ...412...99R</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Rieke, 0. H., Loken, K., Rieke, M. J., &amp; Tamblyn, P. 1993, ApJ, 412,99</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[31]</subfield>
      <subfield code="r">1989ApJ...336..722S</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Schaaf, R., Petisch, P., Biermann, P., Kronberg, P. P., &amp; Schmutzler, T. 1989, ApJ, 336, 732</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[32]</subfield>
      <subfield code="r">1994ApJ...424L..99S</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Schlegel, E. M. 1994, ApJ, 424, L99</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[33]</subfield>
      <subfield code="r">1991ApJ...369..320S</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Seaquist, E., &amp; Odegrad, N. 1991, ApJ, 369, 320</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[34]</subfield>
      <subfield code="e">5</subfield>
      <subfield code="m">Shafer, R. A., Haberl, F., &amp; Arnaud, K. A. 1989, in XSPEC: An X-Ray Spectral Fitting Package (ESA TM-09; Paris: ESA)</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[35]</subfield>
      <subfield code="r">1994ApJ...430..511S</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Suchkov, A., Balsara, D., Heckman, T. M., &amp; Leitherer, C. 1994, ApJ, 430,511</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[36]</subfield>
      <subfield code="r">1987ApJS...63..295V</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Veilleux, S., &amp; Osterbrock, D. E. 1987, ApJS, 63, 295</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[37]</subfield>
      <subfield code="r">1984ApJ...286..144W</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Watson, M., Stanger, V., &amp; Griffiths, R. 1984, ApJ, 286, 144</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[38]</subfield>
      <subfield code="r">1988ApJ...331L..81Y</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">Young, J. S., Claussen, M. J., Kleinmann, S. 0., Rubin, V. C., &amp; Scoville, N. 1988, ApJ, 331, L81</subfield>
      <subfield code="8"/>
    </datafield>
  </record>
  <record>
    <datafield tag="970" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
      <subfield code="9">ADS bibcode</subfield>
    </datafield>
    <datafield tag="961" ind1="" ind2="">
      <subfield code="c">2011-04-08T12:24:50</subfield>
      <subfield code="x">2011-04-08T12:24:50</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[1]</subfield>
      <subfield code="r">1981ApJ...243...89K</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1981ApJ...243...89K</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[2]</subfield>
      <subfield code="r">1982AJ.....87.1165B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1982AJ.....87.1165B</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[3]</subfield>
      <subfield code="r">1984ApJ...286..144W</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1984ApJ...286..144W</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[4]</subfield>
      <subfield code="r">1984ApJ...286..491F</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1984ApJ...286..491F</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[5]</subfield>
      <subfield code="r">1985Natur.317...44C</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1985Natur.317...44C</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[6]</subfield>
      <subfield code="r">1987ApJS...63..295V</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1987ApJS...63..295V</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[7]</subfield>
      <subfield code="r">1988ApJ...330..672F</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1988ApJ...330..672F</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[8]</subfield>
      <subfield code="r">1988ApJ...331L..81Y</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1988ApJ...331L..81Y</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[9]</subfield>
      <subfield code="r">1989ApJ...347..727A</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1989ApJ...347..727A</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[10]</subfield>
      <subfield code="r">1990AJ....100...60H</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1990AJ....100...60H</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[11]</subfield>
      <subfield code="r">1990ApJ...355..442F</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1990ApJ...355..442F</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[12]</subfield>
      <subfield code="r">1990ApJ...364..471A</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1990ApJ...364..471A</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[13]</subfield>
      <subfield code="r">1990ApJS...74..833H</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1990ApJS...74..833H</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[14]</subfield>
      <subfield code="r">1991ApJ...369..320S</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1991ApJ...369..320S</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[15]</subfield>
      <subfield code="r">1992ApJ...388..103K</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1992ApJ...388..103K</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[16]</subfield>
      <subfield code="r">1992ApJ...393..134K</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1992ApJ...393..134K</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[17]</subfield>
      <subfield code="r">1993A&amp;amp;A...268...25B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1993A&amp;A...268...25B</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[18]</subfield>
      <subfield code="r">1993A&amp;amp;A...270...20B</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1993A&amp;A...270...20B</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[19]</subfield>
      <subfield code="r">1993AJ....105..486P</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1993AJ....105..486P</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[20]</subfield>
      <subfield code="r">1993ApJ...412...99R</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1993ApJ...412...99R</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[21]</subfield>
      <subfield code="r">1994ApJ...423L..35P</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1994ApJ...423L..35P</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[22]</subfield>
      <subfield code="r">1994ApJ...424L..99S</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1994ApJ...424L..99S</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[23]</subfield>
      <subfield code="r">1994ApJ...430..511S</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1994ApJ...430..511S</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[24]</subfield>
      <subfield code="r">1995ApJS...96....9L</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1995ApJS...96....9L</subfield>
      <subfield code="8"/>
    </datafield>
    <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">[25]</subfield>
      <subfield code="r">1995ApJS...97...89L</subfield>
      <subfield code="e">1</subfield>
      <subfield code="m">1995ApJS...97...89L</subfield>
      <subfield code="8"/>
    </datafield>
  </record>
  <record>
    <datafield tag="970" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">1995ApJ...445..666A</subfield>
      <subfield code="8">ADS metadata</subfield>
      <subfield code="9">ADS bibcode</subfield>
    </datafield>
    <datafield tag="856" ind1="4" ind2="">
      <subfield code="u">http://$SIMBAD$/simbo.pl?bibcode=1995ApJ...445..666A</subfield>
      <subfield code="y">simbad</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="856" ind1="4" ind2="">
      <subfield code="u">http://$NED$/cgi-bin/nph-objsearch?search_type=Search&amp;refcode=1995ApJ...445..666A</subfield>
      <subfield code="y">ned</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="856" ind1="4" ind2="">
      <subfield code="u">http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=1995ApJ...445..666A</subfield>
      <subfield code="y">data</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="856" ind1="4" ind2="">
      <subfield code="u">http://adsabs.harvard.edu/abs/1995ApJ...445..666A</subfield>
      <subfield code="y">ADSlink</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
  </record>
</collection>
"""

if __name__ == '__main__':
    # Pass one single collection to the invenio bibrecord funtion
    pass
#   bibrecords = create_records(collection)
#   import merger
#   print merger.merge(bibrecords)
