<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:interface="http://zero-install.sourceforge.net/2004/injector/interface"
    xmlns:catalog="http://0install.de/schema/injector/catalog"
    version="1.0">
  <xsl:output method="xml" encoding="utf-8"
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
        doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>
  <xsl:template match="/catalog:catalog">
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta http-equiv="Content-Language" content="en" />
        <title>Zero Install - Software catalogue</title>
        <link rel="stylesheet" href="https://apps.0install.net/resources/catalog.css" type="text/css" />
        <script src="https://apps.0install.net/resources/list.min.js"></script>
        <script>
          window.addEventListener("keydown", function (e) {
            if (e.keyCode === 114 || (e.ctrlKey &amp;&amp; e.keyCode === 70)) { 
              document.getElementById("search").focus();
              e.preventDefault();
            }
          });
        </script>
        <base target="_parent" />
      </head>

      <body>
        <div id="main">
          <div class="searchBar">
            <input class="search" placeholder="Search" />
          </div>
          <div class="list">
            <xsl:for-each select="interface:interface">
              <div class="app">
                <a href="{@uri}">
                  <xsl:variable name="icon" select="interface:icon[@type='image/png']/@href"/>
                  <xsl:if test="$icon">
                    <img class="icon" src="{$icon}" referrerpolicy="no-referrer"/>
                  </xsl:if>
                  <xsl:if test="not($icon)">
                    <img class="icon" src="https://0install.net/tango/applications-system.png" referrerpolicy="no-referrer"/>
                  </xsl:if>
                </a>
                <div class="info">
                  <h2 class="name">
                    <a href="{@uri}">
                      <xsl:value-of select="interface:name"/>
                    </a>
                  </h2>
                  <p class="categories" hidden="true">
                    <xsl:for-each select="interface:category">
                      <xsl:value-of select="text()"/>
                    </xsl:for-each>
                  </p> 
                  <p class="summary">
                    <xsl:if test="interface:summary[@lang='en']">
                      <xsl:value-of select="interface:summary[@lang='en']"/>
                    </xsl:if>
                    <xsl:if test="not(interface:summary[@lang='en'])">
                      <xsl:value-of select="interface:summary"/>
                    </xsl:if>
                  </p>
                </div>
                <div class="actions">
                  <form action="https://get.0install.net/bootstrap/" method="get">
                    <input type="hidden" name="name" value="{interface:name}"/>
                    <input type="hidden" name="uri" value="{@uri}"/>
                    <input type="hidden" name="mode" value="run"/>
                    <input type="submit" value="Run"/>
                  </form>
                  <form action="https://get.0install.net/bootstrap/" method="get">
                    <input type="hidden" name="name" value="{interface:name}"/>
                    <input type="hidden" name="uri" value="{@uri}"/>
                    <input type="hidden" name="mode" value="integrate"/>
                    <input type="submit" value="Integrate"/>
                  </form>
                </div>
              </div>
            </xsl:for-each>
          </div>
        </div>
        <script>new List('main', {valueNames: ['name', 'categories', 'summary']});</script>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
