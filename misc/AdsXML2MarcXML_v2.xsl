<?xml version="1.0" encoding="UTF-8"?>
<!-- 
Copyright (C) 2011, The SAO/NASA Astrophysics Data System

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<!-- xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" omit-xml-declaration="yes"/-->
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
	<xsl:variable name="smallcase" select="'abcdefghijklmnopqrstuvwxyz'"/>
	<xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
	<xsl:variable name="adsmetadata" select="'ADS metadata'"/>
	<xsl:template match="/">
		<collections>
			<xsl:for-each select="/records/record">
				<xsl:variable name="canonical_bibcode" select="@bibcode" />
				<collection>
					<xsl:for-each select="metadata">
						<xsl:variable name="origin_metadata" select="@origin" />
						<record>
							<!-- ISBN -->
							<xsl:if test="isbns">
								<xsl:for-each select="isbns/isbn">
					            	<datafield tag="020" ind1="" ind2="">
					                    <subfield code="a"><xsl:value-of select="."/></subfield>
					                    <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
					                </datafield>
					            </xsl:for-each>
				            </xsl:if>
				            <!-- ISSN -->
							<xsl:if test="issns">
								<xsl:for-each select="issns/issn">
					            	<datafield tag="022" ind1="" ind2="">
					                    <subfield code="a"><xsl:value-of select="."/></subfield>
					                    <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
					                </datafield>
					            </xsl:for-each>
				            </xsl:if>
							<!-- DOI -->
							<xsl:if test="DOI">
				            	<datafield tag="024" ind1="7" ind2="">
				                    <subfield code="a"><xsl:value-of select="DOI"/></subfield>
				                    <subfield code="2">DOI</subfield>
				                    <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				                </datafield>
				            </xsl:if>
							<!-- Bibcode -->
							<datafield tag="970" ind1="" ind2="">
			                    <subfield code="a"><xsl:value-of select="$canonical_bibcode"/></subfield>
			                    <subfield code="8"><xsl:value-of select="$adsmetadata"/></subfield>
			                </datafield>
			                <datafield tag="035" ind1="" ind2="">
			                    <subfield code="a"><xsl:value-of select="$canonical_bibcode"/></subfield>
			                    <subfield code="2">ADS bibcode</subfield>
			                    <subfield code="8"><xsl:value-of select="$adsmetadata"/></subfield>
			                </datafield>
				            <!-- Alternate bibcodes -->
				            <xsl:if test="alternates">
				            	<xsl:for-each select="alternates/alternate">
				            		<xsl:if test=". != $canonical_bibcode">
					                	<xsl:if test="@type = 'deleted'">
						            		<datafield tag="035" ind1="" ind2="">
							                    <subfield code="z"><xsl:value-of select="."/></subfield>
							                    <subfield code="2"><xsl:value-of select="@type"/></subfield>
							                    <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
						                	</datafield>
					                	</xsl:if>
					                	<xsl:if test="@type = 'eprint'">
						            		<datafield tag="035" ind1="" ind2="">
							                    <subfield code="y"><xsl:value-of select="."/></subfield>
							                    <subfield code="2">eprint bibcode</subfield>
							                    <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
						                	</datafield>
					                	</xsl:if>
					                	<xsl:if test="(@type != 'deleted') and (@type != 'eprint')">
						            		<datafield tag="035" ind1="" ind2="">
							                    <subfield code="y"><xsl:value-of select="."/></subfield>
							                    <subfield code="2"><xsl:value-of select="@type"/></subfield>
							                    <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
						                	</datafield>
					                	</xsl:if>
					                </xsl:if>
				            	</xsl:for-each>
				            </xsl:if>
			                <!-- other codes: arXiv -->
			                <xsl:if test="preprintid">
				            	<datafield tag="035" ind1="" ind2="">
				                    <subfield code="a"><xsl:value-of select="preprintid"/></subfield>
				                    <subfield code="2">arXiv</subfield>
				                    <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				                </datafield>
				            </xsl:if>
			                <!-- Language code In ADS: this field contains the value of the tag language if exists, otherwise 
			                a copy of the field 245__y (language of the main title)-->
			                <xsl:if test="title">
		            			<xsl:choose>
		            				<xsl:when test="language">
            							<datafield tag="041" ind1="" ind2="">
			                    			<subfield code="a"><xsl:value-of select="language"/></subfield>
			                    			<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                    		</datafield>
				            		</xsl:when>
		            				<xsl:when test="count(title) = 1">
	            						<xsl:if test="title/@lang">
	            							<datafield tag="041" ind1="" ind2="">
				                    			<subfield code="a"><xsl:value-of select="title/@lang"/></subfield>
				                    			<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				                    		</datafield>
				                    	</xsl:if>
				            		</xsl:when>
				            		<xsl:when test="count(title) > 1">
		            					<xsl:choose>
		            						<xsl:when test="title[(@lang != '') and (@lang != 'en')]">
				            					<xsl:for-each select="title[(@lang != '') and (@lang != 'en')]">
					            					<xsl:choose>
					            						<xsl:when test="position() = 1">
					            							<xsl:if test="@lang">
						            							<datafield tag="041" ind1="" ind2="">
									                    			<subfield code="a"><xsl:value-of select="@lang"/></subfield>
									                    			<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
									                    		</datafield>
									                    	</xsl:if>
					            						</xsl:when>
					            					</xsl:choose>
					            				</xsl:for-each>
					            			</xsl:when>
					            			<xsl:otherwise>
				            					<xsl:for-each select="title">
					            					<xsl:choose>
					            						<xsl:when test="position() = 1">
					            							<xsl:if test="@lang">
						            							<datafield tag="041" ind1="" ind2="">
									                    			<subfield code="a"><xsl:value-of select="@lang"/></subfield>
									                    			<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
									                    		</datafield>
									                    	</xsl:if>
					            						</xsl:when>
					            					</xsl:choose>
					            				</xsl:for-each>
					            			</xsl:otherwise>
		            					</xsl:choose>
		            				</xsl:when>
		            			</xsl:choose>
		            		</xsl:if>
			                <!--Authors-->
				            <xsl:if test="author">
				                <xsl:for-each select="author">
				                	<!-- <xsl:variable name="position" select="position()" />-->
				                    <xsl:choose>
				                        <xsl:when test="@nr = 1">
				                            <datafield tag="100" ind1="" ind2="">
				                            	<!-- normal name -->
				                                <subfield code="a"><xsl:value-of select="name/western"/></subfield>
				                                <!-- normalized name -->
				                                <xsl:if test="name/normalized">
				                                	<subfield code="b"><xsl:value-of select="name/normalized"/></subfield>
				                                </xsl:if>
				                                <xsl:if test="name/native">
				                                	<subfield code="q"><xsl:value-of select="name/native"/></subfield>
				                                </xsl:if>
				                                <!-- type of author -->
				                                <xsl:if test="type">
				                                	<subfield code="e"><xsl:value-of select="type"/></subfield>
				                                </xsl:if>
				                                <!-- Affiliations -->
				                                <xsl:if test="affiliations">
				                                	<xsl:for-each select="affiliations/affiliation">
				                                		<subfield code="u"><xsl:value-of select="."/></subfield>
				                                	</xsl:for-each>
				                                </xsl:if>
				                                <!-- email -->
				                                <xsl:if test="emails">
				                                	<xsl:for-each select="emails/email">
				                                		<subfield code="m"><xsl:value-of select="."/></subfield>
				                                	</xsl:for-each>
				                                </xsl:if>
				                                <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				                            </datafield>
				                        </xsl:when>
				                        <xsl:otherwise>
				                            <datafield tag="700" ind1="" ind2="">
				                                <!-- normal name -->
				                                <subfield code="a"><xsl:value-of select="name/western"/></subfield>
				                                <!-- normalized name -->
				                                <xsl:if test="name/normalized">
				                                	<subfield code="b"><xsl:value-of select="name/normalized"/></subfield>
				                                </xsl:if>
				                                <xsl:if test="name/native">
				                                	<subfield code="q"><xsl:value-of select="name/native"/></subfield>
				                                </xsl:if>
				                                <!-- type of author -->
				                                <xsl:if test="type">
				                                	<subfield code="e"><xsl:value-of select="type"/></subfield>
				                                </xsl:if>
				                                <!-- Affiliations -->
				                                <xsl:if test="affiliations">
				                                	<xsl:for-each select="affiliations/affiliation">
				                                		<subfield code="u"><xsl:value-of select="."/></subfield>
				                                	</xsl:for-each>
				                                </xsl:if>
				                                <!-- email -->
				                                <xsl:if test="emails">
				                                	<xsl:for-each select="emails/email">
				                                		<subfield code="m"><xsl:value-of select="."/></subfield>
				                                	</xsl:for-each>
				                                </xsl:if>
				                                <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				                            </datafield>
				                        </xsl:otherwise>
				                    </xsl:choose>
				                </xsl:for-each>
							</xsl:if>
							<!-- title -->
				            <xsl:if test="title">
				            	<xsl:choose>
				            		<xsl:when test="count(title) = 1">
					            		<datafield tag="245" ind1="" ind2="">
					                    	<subfield code="a"><xsl:value-of select="title"/></subfield>
					                    	<xsl:if test="@lang">
					                    		<subfield code="y"><xsl:value-of select="@lang"/></subfield>
					                    	</xsl:if>
					                    	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
					                	</datafield>
				            		</xsl:when>
				            		<!-- In case I have more then one title -->
				            		<xsl:when test="count(title) > 1">
				            			<xsl:choose>
					            			<!-- If there is one or more title with a specific language not English I split the nodes between the (not English) and the 
					            			(English + unknown + title without lang attribute)
					            			-->
				            				<xsl:when test="title[(@lang != '') and (@lang != 'en')]">
				            					<xsl:for-each select="title[(@lang != '') and (@lang != 'en')]">
					            					<!-- If there are more then one not English title, only the first is 245 -->
					            					<xsl:choose>
					            						<xsl:when test="position() = 1">
					            							<datafield tag="245" ind1="" ind2="">
									                    		<subfield code="a"><xsl:value-of select="."/></subfield>
									                    		<subfield code="y"><xsl:value-of select="@lang"/></subfield>
									                    		<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
							                				</datafield>
					            						</xsl:when>
					            						<xsl:otherwise>
					            							<datafield tag="242" ind1="" ind2="">
									                    		<subfield code="a"><xsl:value-of select="."/></subfield>
									                    		<subfield code="y"><xsl:value-of select="@lang"/></subfield>
									                    		<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
							                				</datafield>
					            						</xsl:otherwise>
					            					</xsl:choose>
					            				</xsl:for-each>
					            				<xsl:for-each select="title[(@lang = '') or (@lang = 'en') or not(@lang)]">
					            					<datafield tag="242" ind1="" ind2="">
							                    		<subfield code="a"><xsl:value-of select="."/></subfield>
							                    		<xsl:if test="(@lang) and (@lang != '')">
						                    				<subfield code="y"><xsl:value-of select="@lang"/></subfield>
						                    			</xsl:if>
						                    			<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
							                		</datafield>
					            				</xsl:for-each>
				            				</xsl:when>
				            				<!-- Otherwise I set as 245 the first one and all the others as 242 -->
				            				<xsl:otherwise>
				            					<xsl:for-each select="title">
					            					<xsl:choose>
					            						<xsl:when test="position() = 1">
					            							<datafield tag="245" ind1="" ind2="">
									                    		<subfield code="a"><xsl:value-of select="."/></subfield>
									                    		<xsl:if test="@lang">
						                    						<subfield code="y"><xsl:value-of select="@lang"/></subfield>
						                    					</xsl:if>
						                    					<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
							                				</datafield>
					            						</xsl:when>
					            						<xsl:otherwise>
					            							<datafield tag="242" ind1="" ind2="">
									                    		<subfield code="a"><xsl:value-of select="."/></subfield>
									                    		<xsl:if test="@lang">
						                    						<subfield code="y"><xsl:value-of select="@lang"/></subfield>
						                    					</xsl:if>
						                    					<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
							                				</datafield>
					            						</xsl:otherwise>
					            					</xsl:choose>
				            					</xsl:for-each>
				            				</xsl:otherwise>
				            			</xsl:choose>
				            		</xsl:when>
				            	</xsl:choose>
				            </xsl:if>
				            <!-- Publication date -->
							<xsl:if test="dates">
								<xsl:for-each select="dates/date">
				                    <datafield tag="260" ind1="" ind2="">
				                       <subfield code="c"><xsl:value-of select="."/></subfield>
				                       <subfield code="t"><xsl:value-of select="@type"/></subfield>
				                       <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				                    </datafield>
			                    </xsl:for-each>
							</xsl:if>
							
							<!-- Number of pages -->
							<xsl:if test="pagenumber">
								<datafield tag="300" ind1="" ind2="">
									<subfield code="a"><xsl:value-of select="pagenumber"/></subfield>
									<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
								</datafield>
							</xsl:if>
							
							<!-- Comments -->
							<xsl:if test="comment">
								<datafield tag="500" ind1="" ind2="">
									<subfield code="a"><xsl:value-of select="comment"/></subfield>
									<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
									<subfield code="9"><xsl:value-of select="comment/@origin"/></subfield>
								</datafield>
							</xsl:if>
							
							<!-- Theses -->
							
							<!-- Abstract -->
			                <xsl:if test="abstract">
			                	<xsl:for-each select="abstract">
				                	<xsl:if test=". != 'Not Available'">
					                    <datafield tag="520" ind1="" ind2="">
					                        <subfield code="a"><xsl:value-of select="."/></subfield>
					                        <xsl:if test="(@lang) and (@lang != '')">
		                  						<subfield code="y"><xsl:value-of select="@lang"/></subfield>
		                  					</xsl:if>
		                  					<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
					                    </datafield>
				                    </xsl:if>
			                    </xsl:for-each>
			                </xsl:if>
			                
			                <!-- Copyright -->
			                <xsl:if test="copyright">
			                    <datafield tag="542" ind1="" ind2="">
			                        <subfield code="a"><xsl:value-of select="copyright"/></subfield>
			                        <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                    </datafield>
			                </xsl:if>
							<!-- Associate papers -->
			                <xsl:if test="associates">
			                	<xsl:for-each select="associates/associate">
			                		<datafield tag="591" ind1="" ind2="">
			                            <subfield code="a"><xsl:value-of select="."/></subfield>
			                            <subfield code="c"><xsl:value-of select="@comment"/></subfield>
			                            <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                        </datafield>
			                	</xsl:for-each>
			                </xsl:if>
			                
			                <!-- Special collection for eprints -->
				            <xsl:if test="arxivcategories">
				            	<xsl:for-each select="arxivcategories/arxivcategory">
				            		<xsl:if test="@type = 'main'">
				            			<datafield tag="650" ind1="1" ind2="7">
				            				<subfield code="a"><xsl:value-of select="."/></subfield>
				            				<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				            			</datafield>
				            		</xsl:if>
				            		<xsl:if test="@type = ''">
				            			<datafield tag="650" ind1="2" ind2="7">
				            				<subfield code="a"><xsl:value-of select="."/></subfield>
				            				<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				            			</datafield>
				            		</xsl:if>
				            	</xsl:for-each>
				            </xsl:if>
			                <!-- Keywords -->
			                <xsl:if test="keywords">
			                   <xsl:for-each select="keywords">
			                       <xsl:variable name="institute" select="@type" />
			                       <!-- If the length of the institution is zero, it's a free keyword -->
			                       <xsl:if test="string-length($institute) = 0">
				                       <xsl:for-each select="keyword">
				                           <xsl:if test="string-length(original) != 0">
					                           <datafield tag="653" ind1="1" ind2="">
					                               <subfield code="a"><xsl:value-of select="original"/></subfield>
					                               <subfield code="b"><xsl:value-of select="normalized"/></subfield>
					                               <xsl:if test="$institute != ''">
					                                   <subfield code="9"><xsl:value-of select="$institute"/></subfield>
					                               </xsl:if>
					                               <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
					                           </datafield>
				                           </xsl:if>
				                       </xsl:for-each>
			                       </xsl:if>
			                       <!-- If the length of the institution is non zero, it's a controlled keyword-->
			                       <xsl:if test="string-length($institute) != 0">
				                       <xsl:for-each select="keyword">
				                           <xsl:if test="string-length(original) != 0">
					                           <datafield tag="695" ind1="" ind2="">
					                               <subfield code="a"><xsl:value-of select="original"/></subfield>
					                               <subfield code="b"><xsl:value-of select="normalized"/></subfield>
					                               <xsl:if test="$institute != ''">
					                                   <subfield code="9"><xsl:value-of select="$institute"/></subfield>
					                               </xsl:if>
					                               <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
					                           </datafield>
				                           </xsl:if>
				                       </xsl:for-each>
			                       </xsl:if>
			                   </xsl:for-each>
			                </xsl:if>
			                <!-- The category is mapped to a keyword with type sti -->
			                <xsl:if test="category">
			                	<xsl:for-each select="category">
			                		<datafield tag="695" ind1="" ind2="">
		                            	<subfield code="a"><xsl:value-of select="original"/></subfield>
		                            	<subfield code="b"/>
		                                <subfield code="9">STI</subfield>
		                            	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
									</datafield>
			                	</xsl:for-each>
			                </xsl:if>
			                <!-- Facility/telescope -->
			                <!-- Collaboration -->
			                
			                <!-- 
		                    Journal
		                        I consider the name of the journal only before the 1st ",". To extract it correctly we have to split the value into more subfields
				            -->
			               	<xsl:if test="journal">
			                	<datafield tag="773" ind1="" ind2="">
			                		<!-- Journal name will come from another tag -->
			                       <subfield code="p"><xsl:value-of select="substring-before(journal,',')"/></subfield>
			                       <xsl:if test="volume">
			                           <subfield code="v"><xsl:value-of select="volume"/></subfield>
			                       </xsl:if>
			                       <xsl:if test="issue">
			                           <subfield code="n"><xsl:value-of select="issue"/></subfield>
			                       </xsl:if>
			                       <xsl:if test="page">
			                           <subfield code="c"><xsl:value-of select="page"/><xsl:if test="lastpage"><xsl:text>-</xsl:text><xsl:value-of select="lastpage"/></xsl:if></subfield>
			                       </xsl:if>
			                       <subfield code="y"><xsl:value-of select="substring($canonical_bibcode, 1, 4)"/></subfield>
			                       <!-- Full string of the journal -->
			                       <subfield code="z"><xsl:value-of select="journal"/></subfield>
			                       <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                	</datafield>
							</xsl:if>
							<!-- Links -->
							<xsl:if test="links">
				                <xsl:for-each select="links/link">
				                    <datafield tag="856" ind1="4" ind2="">
			                            <subfield code="u"><xsl:value-of select="@url"/></subfield>
			                            <subfield code="y"><xsl:value-of select="@title"/></subfield>
			                            <subfield code="3"><xsl:value-of select="@type"/></subfield>
			                            <xsl:if test="@count">
			                            	<subfield code="7"><xsl:value-of select="@count"/></subfield>
			                            </xsl:if>
			                            <subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                        </datafield> 
				                </xsl:for-each>
			                </xsl:if>
			                <!-- Origin -->
			                <xsl:if test="origin">
			                	<xsl:for-each select="origin">
			                		<datafield tag="907" ind1="" ind2="">
			                        	<subfield code="a"><xsl:value-of select="."/></subfield>
			                        	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                    	</datafield>
			                	</xsl:for-each>
			                </xsl:if>
			                <!-- Instruments -->
			                <xsl:if test="instruments">
			                	<xsl:for-each select="instruments">
			                		<datafield tag="908" ind1="" ind2="">
			                        	<subfield code="a"><xsl:value-of select="."/></subfield>
			                        	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                    	</datafield>
			                	</xsl:for-each>
			                </xsl:if>
			                <!-- Instruments -->
			                <xsl:if test="objects">
			                	<xsl:for-each select="objects/object">
			                		<datafield tag="909" ind1="" ind2="">
			                        	<subfield code="a"><xsl:value-of select="."/></subfield>
			                        	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                        	<xsl:if test="@origin">
			                        		<subfield code="9"><xsl:value-of select="@origin"/></subfield>
			                        	</xsl:if>
			                    	</datafield>
			                	</xsl:for-each>
			                </xsl:if>
			                <!-- Creation and modification dates -->
							<xsl:if test="creation_time">
								<xsl:if test="modification_time">
									<datafield tag="961" ind1="" ind2="">
										<subfield code="c"><xsl:value-of select="modification_time"/></subfield>
										<subfield code="x"><xsl:value-of select="creation_time"/></subfield>
										<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
									</datafield>
								</xsl:if>
							</xsl:if>
							
							<!-- COLLECTIONS -->
							<!-- main collections: databases -->
							<xsl:if test="databases">
								<xsl:for-each select="databases/database">
									<datafield tag="980" ind1="" ind2="">
										<xsl:choose>
											<xsl:when test=". = 'AST'">
												<subfield code="a">ASTRONOMY</subfield>
											</xsl:when>
											<xsl:when test=". = 'PHY'">
												<subfield code="a">PHYSICS</subfield>
											</xsl:when>
											<xsl:when test=". = 'GEN'">
												<subfield code="a">GENERAL</subfield>
											</xsl:when>
											<xsl:when test=". = 'PRE'">
												<subfield code="a">EPRINT</subfield>
											</xsl:when>
											<xsl:otherwise>
												<subfield code="a"><xsl:value-of select="." /></subfield>
											</xsl:otherwise>
										</xsl:choose>
										<subfield code="m">database</subfield>
										<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
									</datafield>
								</xsl:for-each>
							</xsl:if>
							<!-- other collections (SOMETHING MISSING?????)-->
				            <xsl:if test="collection = '1'">
				             <datafield tag="980" ind1="" ind2="">
				             	<subfield code="a">COLLECTION</subfield>
				             	<subfield code="m">attribute</subfield>
				             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				             </datafield>
				            </xsl:if>
				            <xsl:if test="nonarticle = '1'">
				             <datafield tag="980" ind1="" ind2="">
				             	<subfield code="a">NONARTICLE</subfield>
				             	<subfield code="m">attribute</subfield>
				             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				             </datafield>
				            </xsl:if>
				            <xsl:if test="ocrabstract = '1'">
				             <datafield tag="980" ind1="" ind2="">
				             	<subfield code="a">OCRABSTRACT</subfield>
				             	<subfield code="m">attribute</subfield>
				             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				             </datafield>
				            </xsl:if>
				            <xsl:if test="openaccess = '1'">
				             <datafield tag="980" ind1="" ind2="">
				             	<subfield code="a">OPENACCESS</subfield>
				             	<subfield code="m">attribute</subfield>
				             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				             </datafield>
				            </xsl:if>
				            <xsl:if test="private = '1'">
				             <datafield tag="980" ind1="" ind2="">
				             	<subfield code="a">PRIVATE</subfield>
				             	<subfield code="m">attribute</subfield>
				             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				             </datafield>
				            </xsl:if>
				            <xsl:if test="refereed = '1'">
				             <datafield tag="980" ind1="" ind2="">
				             	<subfield code="a">REFEREED</subfield>
				             	<subfield code="m">attribute</subfield>
				             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
				             </datafield>
				            </xsl:if>
				            <!-- Special collection "pubtype" -->
				            <xsl:if test="pubtype">
					            <xsl:if test="translate(pubtype, $smallcase, $uppercase) != 'EPRINT'">
						             <datafield tag="980" ind1="" ind2="">
						             	<subfield code="a"><xsl:value-of select="translate(pubtype, $smallcase, $uppercase)" /></subfield>
						             	<subfield code="m">attribute</subfield>
						             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
						             </datafield>
					            </xsl:if>
					        </xsl:if>
					        <!-- Bibliographig groups -->
					        <xsl:if test="bibgroups">
								<xsl:for-each select="bibgroups/bibgroup">
									<datafield tag="980" ind1="" ind2="">
						             	<subfield code="a"><xsl:value-of select="." /></subfield>
						             	<subfield code="m">bibgroup</subfield>
						             	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
						             </datafield>
								</xsl:for-each>
							</xsl:if>
							<!-- Timestamp signature -->
							<xsl:if test="JSON_timestamp">
								<datafield tag="995" ind1="" ind2="">
									<subfield code="a"><xsl:value-of select="JSON_timestamp"/></subfield>
									<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
								</datafield>
							</xsl:if>
							<!-- References -->
			                <xsl:if test="reference">
			               		<xsl:for-each select="reference">
			               			<datafield tag="999" ind1="C" ind2="5">
			                        	<!-- The position is deprecated for the merger, since we cannot rely on thus field to order the references -->
			                        	<!-- subfield code="o"><xsl:text>[</xsl:text><xsl:value-of select="position()"/><xsl:text>]</xsl:text></subfield-->
			                        	<xsl:if test="@bibcode != ''">
			                        		<subfield code="i"><xsl:value-of select="@bibcode"/></subfield>
			                        	</xsl:if>
			                        	<xsl:if test="@arxid != ''">
			                        		<subfield code="r">arxiv: <xsl:value-of select="@arxid"/></subfield>
			                        	</xsl:if>
			                        	<xsl:if test="@doi != ''">
			                        		<subfield code="a">doi: <xsl:value-of select="@doi"/></subfield>
			                        	</xsl:if>
			                        	<xsl:if test="@score != ''">
			                        		<subfield code="e"><xsl:value-of select="@score"/></subfield>
			                        	</xsl:if>
			                        	<xsl:if test="@source != ''">
			                        		<subfield code="f"><xsl:value-of select="@source"/></subfield>
			                        	</xsl:if>
			                        	<xsl:if test="not(string-length(.) = 0)">
			                        		<subfield code="b"><xsl:value-of select="."/></subfield>
			                        	</xsl:if>
			                        	<subfield code="8"><xsl:value-of select="$origin_metadata"/></subfield>
			                        </datafield>
			               		</xsl:for-each>
			                </xsl:if>
							
						</record>
					</xsl:for-each>
				</collection>
			</xsl:for-each>
		</collections>
	</xsl:template>
</xsl:stylesheet>
 