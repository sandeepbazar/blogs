<?xml version="1.0" encoding="UTF-8"?>
<!-- SPDX-FileCopyrightText: 2026 Sandeep Bazar -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
<!--
  Makes feed.xml readable when a person opens it in a browser. Feed readers
  ignore this entirely and parse the RSS underneath, so the feed is unchanged
  by its presence. If a browser drops XSLT support the page degrades to the
  raw XML it already showed, which is why this is safe to ship.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/rss/channel">
    <html lang="en">
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title><xsl:value-of select="title"/> &#183; RSS feed</title>
        <link rel="stylesheet" href="/blogs/static/site.css"/>
      </head>
      <body>
        <main id="main" class="wrap post">
          <header class="post__head">
            <span class="tag tag--kubernetes">RSS feed</span>
            <h1 class="post__title"><xsl:value-of select="title"/></h1>
            <p class="post__dek"><xsl:value-of select="description"/></p>
          </header>

          <div class="post__layout">
          <article class="post__body prose">
            <p class="callout">
              This is a <strong>feed</strong>, meant for a feed reader rather
              than a browser. Copy this page's address into
              NetNewsWire, Feedly, Inoreader, Thunderbird or any other reader
              and new posts arrive there automatically, with no account and no
              tracking. Prefer to just read? Go to
              <a href="/blogs/">all writing</a>.
            </p>

            <h2>In this feed</h2>
            <xsl:for-each select="item">
              <p>
                <a>
                  <xsl:attribute name="href"><xsl:value-of select="link"/></xsl:attribute>
                  <strong><xsl:value-of select="title"/></strong>
                </a>
                <br/>
                <small><xsl:value-of select="category"/> &#183; <xsl:value-of select="pubDate"/></small>
                <br/>
                <xsl:value-of select="description"/>
              </p>
            </xsl:for-each>
          </article>
          </div>

          <footer class="post__foot">
            <p><a href="/blogs/">&#8592; All writing</a></p>
          </footer>
        </main>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
