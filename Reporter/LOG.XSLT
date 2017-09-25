<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
 <html>
 <Head>
        <style type="text/css">

          body {
          background:#fff;
          margin:0;
          padding:40px 20px;
          font-family: "Arial", Arial, Sans-serif;
          font-size: 16px;
          color:#000;
          }

          table {
          margin:5px 5px 0;
          border:0px solid #222;
          font-size: 0.8em;
          }

          td {
          margin:5px 5px 0;
          padding:10px 10px 10px 10px;
          vertical-align:text-top;
          border:1px solid #222;
          border-width:1px 1px 1px 1px;
          }

          td.light {
          border:0px solid #222;
          }

          td.number {
          text-align:right;
          }

          td.status {
          text-align:right;
          vertical-align:text-bottom;
          }

        </style>


 </Head>
 <body>
   <!--OVER RESULT -->
   <xsl:variable name="OVER_STATUS" select="REPORT/OVER_STATUS"/>
   <xsl:variable name="STATUS" select="REPORT/LOG_ENTRY/STATUS"/>



   <h2>自动化测试执行报告</h2>
   <!--table -->
   <table border="1">
     <!--all result value-->
     <tr bgcolor="white" height = "35">
        <td>Overall Test Result</td>
        <td><xsl:value-of select="$OVER_STATUS"/></td>
        <td colspan="8"> </td>
     </tr>

     <tr bgcolor="#D8BFD9" height = "35">
       <th>Step</th>
       <th>Execute Time</th>
       <th>Step Result</th>
       <th>Description</th>
       <th>Step Description</th>
       <th>Action</th>
       <th>Index</th>
       <th>Element</th>
       <th>Value</th>
       <th>Expected Results </th>
     </tr>

       <!--select font color -->
       <xsl:variable name="fontColor">
           <xsl:choose>
               <xsl:when test="$STATUS = FAILED or $STATUS = PASSED">
                   <xsl:text>white</xsl:text>
               </xsl:when>
               <xsl:otherwise>black</xsl:otherwise>
           </xsl:choose>
       </xsl:variable>


          <!-- Compute the background color according to the overall test result -->
       <xsl:variable name="StatusBackgroundColor">
            <xsl:choose>
              <xsl:when test="$STATUS = 'FAILED'">
                <!--<xsl:text>rgb(158, 48, 57)</xsl:text> -->
                <xsl:text>rgb(255, 40, 38)</xsl:text>
              </xsl:when>
              <xsl:when test="$STATUS = 'WARNING'">
                <xsl:text>rgb(132, 76, 84)</xsl:text>
              </xsl:when>
              <xsl:when test="$STATUS = 'PASSED'">
                <xsl:text>rgb(121, 180, 112)</xsl:text>
              </xsl:when>
              <xsl:when test="$STATUS = 'DONE'">
                <xsl:text>white</xsl:text>
              </xsl:when>
              <xsl:when test="$STATUS = 'INFO'">
                <xsl:text>white</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:text>white</xsl:text>
              </xsl:otherwise>
            </xsl:choose>
       </xsl:variable>


       <!--log entry-->
       <xsl:for-each select = "REPORT/LOG_ENTRY">

           <tr>
               <td><xsl:value-of select="STEP"/></td>
               <td><xsl:value-of select="EXECUTION_TIME"/></td>
               <td bgcolor="{$StatusBackgroundColor}"><xsl:value-of select="STEP_RESULT"/></td>
               <td><xsl:value-of select="DESCRIPTION"/></td>
               <td><xsl:value-of select="STEP_DESCRIPTION"/></td>
               <td><xsl:value-of select="ACTION"/></td>
               <td><xsl:value-of select="INDEX"/></td>
               <td><xsl:value-of select="ELEMENT"/></td>
               <td><xsl:value-of select="VALUE"/></td>
               <td><xsl:value-of select="EXPECTED_RESULTS"/></td>
           </tr>
           <!--    Store image path    -->
           <xsl:variable name="Image">
                <xsl:value-of select="IMAGE_PATH"/>
           </xsl:variable>
           <!--  If XML contains an image path then display it according to the following -->
           <xsl:choose>
               <xsl:when test="normalize-space($Image)!=''">
                  <!-- Comment the Next line to Stop showing embedded image in log  and change the width number to make image size change-->
                  <tr>
                     <td colspan="10">
                       <a href="{$Image}" target="_blank" >
                         <img src="{$Image}" width="300"></img>
                       </a>
                     </td>
                  </tr>
               </xsl:when>
           </xsl:choose>
       </xsl:for-each>

       <tr bgcolor="white">
           <font color="{$fontColor}">
               <td colspan="10">Overall Test Result:  <xsl:value-of select="$OVER_STATUS"/></td>
           </font>
       </tr>
   </table>
 </body>
 </html>
</xsl:template>
</xsl:stylesheet>